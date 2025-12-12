#!/usr/bin/env python3
"""
PTY Capture for Janus Remote

Wraps Claude CLI in a PTY and connects to local Janus via WebSocket
for voice-to-text paste and approval overlay support over SSH.
"""

import sys
import os
import pty
import select
import termios
import tty
from datetime import datetime
import fcntl
import time
import json
import re
import threading
import socket

# WebSocket bridge port (must match Janus Electron)
JANUS_BRIDGE_PORT = 9473

# Regex to strip title escape sequences
TITLE_ESCAPE_PATTERN = re.compile(rb'\x1b\][012];[^\x07\x1b]*(?:\x07|\x1b\\)')

# Approval detection patterns - when Claude asks for permission
APPROVAL_PATTERNS = [
    r'❯\s*1\.\s*Yes',
    r'1\.\s*Yes\s*$',
    r'2\.\s*Yes,?\s*allow all',
    r'3\.\s*No,?\s*and tell',
    r'allow all.*during this session',
    r'tell Claude what to do differently',
    r'Allow\s+(this\s+)?(tool|action|command|operation)',
    r'Do you want to (allow|run|execute|proceed)',
    r'Press Enter to (allow|approve|continue|proceed)',
    r'\[y/n\]',
    r'\[Y/n\]',
    r'\[yes/no\]',
    r'Allow\?',
    r'Approve\?',
    r'Run\s+(this\s+)?(command|bash|script)',
    r'Execute\s+(this\s+)?(command|bash|script)',
    r'(Write|Create|Delete|Modify)\s+(to\s+)?file',
    r'Allow (writing|reading|creating|deleting)',
    r'(y/n/a)',
    r'\(y\)es.*\(n\)o',
]

COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in APPROVAL_PATTERNS]


def get_janus_title():
    """Get session title from environment"""
    return os.environ.get('JANUS_TITLE', '')


def remove_ansi(text):
    """Remove ANSI escape codes from text"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


class RemotePasteClient:
    """WebSocket client for bidirectional communication with local Janus"""

    def __init__(self, master_fd, port=JANUS_BRIDGE_PORT):
        self.master_fd = master_fd
        self.port = port
        self.ws = None
        self.running = True
        self.connected = False
        self.client_thread = None
        self.session_id = f"pty-{os.getpid()}-{int(time.time())}"
        self.pending_approval = None
        self.approval_id = 0

    def start(self):
        """Start the WebSocket client in a background thread"""
        self.client_thread = threading.Thread(target=self._run_client, daemon=True)
        self.client_thread.start()

    def _get_public_ip(self):
        """Get the server's public IP address for SSH config matching"""
        try:
            import urllib.request
            # Try multiple services in case one is down
            services = [
                'https://api.ipify.org',
                'https://ifconfig.me/ip',
                'https://icanhazip.com',
            ]
            for url in services:
                try:
                    with urllib.request.urlopen(url, timeout=3) as response:
                        ip = response.read().decode('utf-8').strip()
                        if ip:
                            return ip
                except:
                    continue
        except:
            pass
        return ''

    def _run_client(self):
        """Main client loop - connect and listen for messages"""
        try:
            import websocket
        except ImportError:
            print("\033[38;5;208m[janus-remote]\033[0m websocket-client not installed. Run: pip install websocket-client", file=sys.stderr)
            return

        while self.running:
            try:
                ws_url = f"ws://localhost:{self.port}"
                print(f"\033[38;5;208m[janus-remote]\033[0m Connecting to Janus bridge...", file=sys.stderr)

                self.ws = websocket.create_connection(ws_url, timeout=5)
                self.connected = True
                print(f"\033[38;5;82m[janus-remote]\033[0m \033[1mConnected to Janus bridge!\033[0m 🔮", file=sys.stderr)

                # Register this session
                my_title = get_janus_title()
                system_hostname = socket.gethostname()

                # Get public IP for automatic SSH config matching
                public_ip = self._get_public_ip()

                register_msg = json.dumps({
                    'type': 'register',
                    'sessionId': self.session_id,
                    'title': my_title,
                    'hostname': system_hostname,
                    'publicIP': public_ip,
                    'capabilities': ['paste', 'approval']
                })
                self.ws.send(register_msg)
                if public_ip:
                    print(f"\033[38;5;245m[janus-remote]\033[0m Public IP: {public_ip}", file=sys.stderr)

                # Listen for messages
                while self.running and self.connected:
                    try:
                        self.ws.settimeout(1.0)
                        message = self.ws.recv()
                        if message:
                            self._handle_message(message)
                    except websocket.WebSocketTimeoutException:
                        try:
                            self.ws.send(json.dumps({'type': 'ping'}))
                        except:
                            break
                    except websocket.WebSocketConnectionClosedException:
                        print(f"\033[38;5;208m[janus-remote]\033[0m Connection closed", file=sys.stderr)
                        break
                    except Exception:
                        break

            except Exception as e:
                if self.running:
                    pass  # Silently retry
                self.connected = False

            if self.running:
                time.sleep(5)

    def _handle_message(self, message):
        """Handle incoming WebSocket message"""
        try:
            msg = json.loads(message)
            msg_type = msg.get('type')

            if msg_type == 'paste':
                text = msg.get('text', '')
                if text:
                    print(f"\033[38;5;82m[janus-remote]\033[0m Voice paste received", file=sys.stderr)
                    self._inject_text(text)

            elif msg_type == 'registered':
                pass  # Already printed connection message

            elif msg_type == 'approval_response':
                # Response from local Janus approval overlay
                action = msg.get('action', 'deny')
                self._inject_approval_response(action)

        except json.JSONDecodeError:
            pass

    def _inject_text(self, text):
        """Inject text directly into the PTY"""
        try:
            encoded = text.encode('utf-8')
            chunk_size = 256
            for i in range(0, len(encoded), chunk_size):
                chunk = encoded[i:i + chunk_size]
                os.write(self.master_fd, chunk)
                if len(encoded) > chunk_size:
                    time.sleep(0.02)

            time.sleep(0.15)
            os.write(self.master_fd, b'\r')
        except OSError as e:
            print(f"\033[31m[janus-remote]\033[0m Paste error: {e}", file=sys.stderr)

    def _inject_approval_response(self, action):
        """Inject approval response keystroke to Claude"""
        try:
            if action == 'approve':
                os.write(self.master_fd, b'1')
                time.sleep(0.05)
                os.write(self.master_fd, b'\r')
                print(f"\033[38;5;82m[janus-remote]\033[0m ✓ Approved", file=sys.stderr)
            elif action == 'approve_all':
                os.write(self.master_fd, b'2')
                time.sleep(0.05)
                os.write(self.master_fd, b'\r')
                print(f"\033[38;5;82m[janus-remote]\033[0m ✓ Approved all", file=sys.stderr)
            elif action == 'deny':
                os.write(self.master_fd, b'\x1b')  # Escape to cancel
                print(f"\033[38;5;208m[janus-remote]\033[0m ✗ Denied", file=sys.stderr)
            elif action.startswith('deny:'):
                feedback = action[5:]
                os.write(self.master_fd, b'3')
                time.sleep(0.1)
                os.write(self.master_fd, b'\r')
                time.sleep(0.2)
                os.write(self.master_fd, feedback.encode('utf-8'))
                time.sleep(0.05)
                os.write(self.master_fd, b'\r')
                print(f"\033[38;5;208m[janus-remote]\033[0m ✗ Denied with feedback", file=sys.stderr)
            else:
                os.write(self.master_fd, b'\x1b')

            self.pending_approval = None

        except OSError as e:
            print(f"\033[31m[janus-remote]\033[0m Approval inject error: {e}", file=sys.stderr)

    def send_approval_request(self, tool_name, context):
        """Send approval request to local Janus for overlay display"""
        if not self.connected or not self.ws:
            return

        self.approval_id += 1
        self.pending_approval = {
            'id': self.approval_id,
            'timestamp': datetime.now().isoformat(),
            'tool': tool_name,
            'context': context
        }

        try:
            self.ws.send(json.dumps({
                'type': 'approval_request',
                'sessionId': self.session_id,
                'approvalId': self.approval_id,
                'tool': tool_name,
                'context': context,
                'hostname': socket.gethostname()
            }))
            print(f"\033[38;5;141m[janus-remote]\033[0m 🔔 Approval request sent → {tool_name}", file=sys.stderr)
        except Exception:
            pass

    def clear_pending_approval(self):
        """Clear pending approval (user handled it manually)"""
        self.pending_approval = None

    def stop(self):
        """Stop the client"""
        self.running = False
        self.connected = False
        if self.ws:
            try:
                self.ws.close()
            except:
                pass


class ApprovalDetector:
    """Detects approval requests in Claude output"""

    def __init__(self, remote_client):
        self.remote_client = remote_client
        self.recent_lines = []
        self.last_detection_time = 0
        self.detection_cooldown = 0.5

    def add_line(self, line):
        """Add a line and check for approval patterns"""
        cleaned = remove_ansi(line).strip()
        if not cleaned:
            return

        self.recent_lines.append(cleaned)
        if len(self.recent_lines) > 50:
            self.recent_lines = self.recent_lines[-30:]

        # Check for completion markers - clear pending
        if self.remote_client.pending_approval:
            if '✓' in cleaned or '✗' in cleaned:
                self.remote_client.clear_pending_approval()
                return

        # Check for approval request
        if self._is_approval_request(cleaned):
            current_time = time.time()
            if (current_time - self.last_detection_time) >= self.detection_cooldown:
                if not self.remote_client.pending_approval:
                    self.last_detection_time = current_time
                    tool_name, context = self._extract_tool_info()
                    self.remote_client.send_approval_request(tool_name, context)

    def _is_approval_request(self, line):
        """Check if line matches approval patterns"""
        for pattern in COMPILED_PATTERNS:
            if pattern.search(line):
                return True
        return False

    def _extract_tool_info(self):
        """Extract tool name and context from recent lines"""
        tool_name = 'Unknown'
        context = self.recent_lines[-5:] if len(self.recent_lines) >= 5 else self.recent_lines

        for line in reversed(self.recent_lines):
            if '⏺' in line:
                if 'Bash' in line:
                    tool_name = 'Bash'
                elif 'Edit' in line:
                    tool_name = 'Edit'
                elif 'Write' in line:
                    tool_name = 'Write'
                elif 'Read' in line:
                    tool_name = 'Read'
                elif 'Glob' in line:
                    tool_name = 'Glob'
                elif 'Grep' in line:
                    tool_name = 'Grep'
                elif 'Task' in line:
                    tool_name = 'Task'
                break

        return tool_name, context


def run_claude_session(claude_path, args):
    """Run Claude CLI wrapped in PTY with Janus voice paste support"""

    old_tty = termios.tcgetattr(sys.stdin)

    try:
        master_fd, slave_fd = pty.openpty()
        pid = os.fork()

        if pid == 0:  # Child process
            os.close(master_fd)
            os.setsid()
            os.dup2(slave_fd, 0)
            os.dup2(slave_fd, 1)
            os.dup2(slave_fd, 2)
            os.execv(claude_path, [claude_path] + args)

        else:  # Parent process
            os.close(slave_fd)
            tty.setraw(sys.stdin.fileno())

            flags = fcntl.fcntl(master_fd, fcntl.F_GETFL)
            fcntl.fcntl(master_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

            # Initialize Remote Client and Approval Detector
            remote_client = RemotePasteClient(master_fd)
            remote_client.start()

            approval_detector = ApprovalDetector(remote_client)

            line_buffer = b''

            while True:
                rfds, _, _ = select.select([sys.stdin, master_fd], [], [], 0.01)

                pid_status = os.waitpid(pid, os.WNOHANG)
                if pid_status[0] != 0:
                    break

                if sys.stdin in rfds:
                    try:
                        data = os.read(sys.stdin.fileno(), 1024)
                        if data:
                            # If user manually handles approval, clear pending
                            if remote_client.pending_approval:
                                if data in (b'1', b'2', b'3', b'\r', b'\n', b'\x1b'):
                                    remote_client.clear_pending_approval()
                            os.write(master_fd, data)
                    except OSError:
                        pass

                if master_fd in rfds:
                    try:
                        data = os.read(master_fd, 4096)
                        if data:
                            data = TITLE_ESCAPE_PATTERN.sub(b'', data)
                            os.write(sys.stdout.fileno(), data)

                            # Process lines for approval detection
                            line_buffer += data
                            while b'\n' in line_buffer or b'\r' in line_buffer:
                                nl_pos = line_buffer.find(b'\n')
                                cr_pos = line_buffer.find(b'\r')

                                if nl_pos == -1:
                                    pos = cr_pos
                                elif cr_pos == -1:
                                    pos = nl_pos
                                else:
                                    pos = min(nl_pos, cr_pos)

                                if pos == -1:
                                    break

                                line = line_buffer[:pos]
                                line_buffer = line_buffer[pos+1:]

                                text = line.decode('utf-8', errors='ignore')
                                approval_detector.add_line(text)

                    except OSError:
                        pass

            remote_client.stop()
            _, exit_status = os.waitpid(pid, 0)
            exit_code = os.WEXITSTATUS(exit_status) if os.WIFEXITED(exit_status) else 1

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)

    print()
    print("\033[38;5;245mSession ended.\033[0m")
    sys.exit(exit_code if 'exit_code' in locals() else 0)


def main():
    """Standalone entry point"""
    from .cli import main as cli_main
    cli_main()


if __name__ == '__main__':
    main()
