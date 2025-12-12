#!/usr/bin/env python3
"""
PTY Capture for Janus Remote

Wraps Claude CLI in a PTY and connects to local Janus via WebSocket
for voice-to-text paste support over SSH.
"""

import sys
import os
import pty
import select
import termios
import tty
import subprocess
from datetime import datetime
import signal
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


def get_janus_title():
    """Get session title from environment"""
    return os.environ.get('JANUS_TITLE', '')


class RemotePasteClient:
    """WebSocket client for receiving pastes from local Janus via SSH port forwarding"""

    def __init__(self, master_fd, port=JANUS_BRIDGE_PORT):
        self.master_fd = master_fd
        self.port = port
        self.ws = None
        self.running = True
        self.connected = False
        self.client_thread = None
        self.session_id = f"pty-{os.getpid()}-{int(time.time())}"

    def start(self):
        """Start the WebSocket client in a background thread"""
        self.client_thread = threading.Thread(target=self._run_client, daemon=True)
        self.client_thread.start()

    def _run_client(self):
        """Main client loop - connect and listen for pastes"""
        try:
            import websocket
        except ImportError:
            print("[janus-remote] websocket-client not installed. Run: pip install websocket-client", file=sys.stderr)
            return

        while self.running:
            try:
                ws_url = f"ws://localhost:{self.port}"
                print(f"[janus-remote] Connecting to Janus bridge at {ws_url}...", file=sys.stderr)

                self.ws = websocket.create_connection(ws_url, timeout=5)
                self.connected = True
                print("[janus-remote] Connected to Janus bridge!", file=sys.stderr)

                # Register this session
                my_title = get_janus_title()
                hostname = socket.gethostname()
                register_msg = json.dumps({
                    'type': 'register',
                    'sessionId': self.session_id,
                    'title': my_title,
                    'hostname': hostname
                })
                self.ws.send(register_msg)

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
                        break
                    except Exception:
                        break

            except Exception as e:
                if self.running:
                    print(f"[janus-remote] Bridge connection failed: {e}", file=sys.stderr)
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
                    self._inject_text(text)
            elif msg_type == 'registered':
                print(f"[janus-remote] {msg.get('message', 'Registered')}", file=sys.stderr)

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
            print(f"[janus-remote] Paste error: {e}", file=sys.stderr)

    def stop(self):
        """Stop the client"""
        self.running = False
        self.connected = False
        if self.ws:
            try:
                self.ws.close()
            except:
                pass


def run_claude_session(claude_path, args):
    """Run Claude CLI wrapped in PTY with Janus voice paste support"""

    # Save original terminal settings
    old_tty = termios.tcgetattr(sys.stdin)

    try:
        # Create a pseudo-terminal
        master_fd, slave_fd = pty.openpty()

        # Fork and run Claude in the child process
        pid = os.fork()

        if pid == 0:  # Child process
            os.close(master_fd)
            os.setsid()
            os.dup2(slave_fd, 0)  # stdin
            os.dup2(slave_fd, 1)  # stdout
            os.dup2(slave_fd, 2)  # stderr

            # Run Claude
            os.execv(claude_path, [claude_path] + args)

        else:  # Parent process
            os.close(slave_fd)

            # Set stdin to raw mode
            tty.setraw(sys.stdin.fileno())

            # Make master_fd non-blocking
            flags = fcntl.fcntl(master_fd, fcntl.F_GETFL)
            fcntl.fcntl(master_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

            # Initialize Remote Paste Client
            remote_client = RemotePasteClient(master_fd)
            remote_client.start()

            while True:
                rfds, _, _ = select.select([sys.stdin, master_fd], [], [], 0.01)

                # Check if child has exited
                pid_status = os.waitpid(pid, os.WNOHANG)
                if pid_status[0] != 0:
                    break

                if sys.stdin in rfds:
                    try:
                        data = os.read(sys.stdin.fileno(), 1024)
                        if data:
                            os.write(master_fd, data)
                    except OSError:
                        pass

                if master_fd in rfds:
                    try:
                        data = os.read(master_fd, 4096)
                        if data:
                            # Strip title escape sequences
                            data = TITLE_ESCAPE_PATTERN.sub(b'', data)
                            os.write(sys.stdout.fileno(), data)
                    except OSError:
                        pass

            # Stop remote client
            remote_client.stop()

            # Get exit status
            _, exit_status = os.waitpid(pid, 0)
            exit_code = os.WEXITSTATUS(exit_status) if os.WIFEXITED(exit_status) else 1

    finally:
        # Restore terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)

    sys.exit(exit_code if 'exit_code' in locals() else 0)


def main():
    """Standalone entry point"""
    from .cli import main as cli_main
    cli_main()


if __name__ == '__main__':
    main()
