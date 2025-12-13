#!/usr/bin/env python3
"""
CLI entry point for janus-remote

Usage:
    claude-janus              # Start new Claude session with voice paste
    claude-janus --resume     # Resume previous session
    claude-janus -r           # Short form resume
    claude-janus --setup      # Configure VSCode settings for tab title
"""

import sys
import os
import shutil
import json


def print_banner(is_resume=False):
    """Print the sexy Janus terminal banner"""
    print()
    print("  \033[1;38;5;141m█▀▀ █   ▄▀█ █ █ █▀▄ █▀▀\033[0m  \033[38;5;208m+\033[0m  \033[1;38;5;208m▀█ ▄▀█ █▄ █ █ █ █▀▀\033[0m  🔮")
    print("  \033[1;38;5;141m█▄▄ █▄▄ █▀█ █▄█ █▄▀ ██▄\033[0m     \033[1;38;5;208m█▄ █▀█ █ ▀█ █▄█ ▄██\033[0m")

    if is_resume:
        print("  \033[38;5;245m────────────────────────────────────────────\033[0m")
        print("  \033[38;5;141m⏪ Resume Session\033[0m")

    print()


def get_session_title():
    """Ask user for optional session title"""
    print("  \033[38;5;245mSession title (Enter to skip): \033[0m", end='', flush=True)
    try:
        title = input().strip()
        return title if title else None
    except (EOFError, KeyboardInterrupt):
        return None


def find_claude():
    """Find the claude binary location"""
    # Check PATH first
    claude_path = shutil.which('claude')
    if claude_path:
        return claude_path

    # Common locations
    common_paths = [
        '/usr/local/bin/claude',
        '/opt/homebrew/bin/claude',
        os.path.expanduser('~/.local/bin/claude'),
        os.path.expanduser('~/bin/claude'),
        '/usr/bin/claude',
        os.path.expanduser('~/.npm-global/bin/claude'),
    ]

    for path in common_paths:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

    return None


def get_vscode_settings_paths():
    """Get possible VSCode settings.json paths for different platforms"""
    home = os.path.expanduser('~')
    paths = []

    # macOS
    paths.append(os.path.join(home, 'Library/Application Support/Code/User/settings.json'))
    paths.append(os.path.join(home, 'Library/Application Support/Code - Insiders/User/settings.json'))
    paths.append(os.path.join(home, 'Library/Application Support/Cursor/User/settings.json'))

    # Linux
    paths.append(os.path.join(home, '.config/Code/User/settings.json'))
    paths.append(os.path.join(home, '.config/Code - Insiders/User/settings.json'))
    paths.append(os.path.join(home, '.config/Cursor/User/settings.json'))

    # WSL / Windows (if running in WSL)
    paths.append(os.path.join(home, '.vscode-server/data/Machine/settings.json'))

    return paths


def setup_vscode_settings(silent=False):
    """Configure VSCode terminal tab settings for Janus title display"""
    required_settings = {
        'terminal.integrated.tabs.title': '${sequence}',
        'terminal.integrated.tabs.description': '${process}'
    }

    paths = get_vscode_settings_paths()
    configured = False

    for settings_path in paths:
        if not os.path.exists(settings_path):
            continue

        try:
            # Read existing settings
            with open(settings_path, 'r') as f:
                content = f.read()
                # Handle empty file
                settings = json.loads(content) if content.strip() else {}

            # Check if already configured
            needs_update = False
            for key, value in required_settings.items():
                if settings.get(key) != value:
                    needs_update = True
                    break

            if not needs_update:
                if not silent:
                    print(f"  \033[38;5;82m✓\033[0m VSCode already configured: {settings_path}")
                configured = True
                continue

            # Update settings
            settings.update(required_settings)

            # Write back
            with open(settings_path, 'w') as f:
                json.dump(settings, f, indent=4)

            if not silent:
                print(f"  \033[38;5;82m✓\033[0m VSCode configured: {settings_path}")
                print(f"    \033[38;5;245mAdded: terminal.integrated.tabs.title = ${{sequence}}\033[0m")
            configured = True

        except (json.JSONDecodeError, PermissionError, OSError) as e:
            if not silent:
                print(f"  \033[38;5;208m⚠\033[0m Could not update {settings_path}: {e}")

    return configured


def check_first_run():
    """Check if this is the first run and offer to setup VSCode"""
    marker_file = os.path.expanduser('~/.janus-remote-configured')

    if os.path.exists(marker_file):
        return  # Already configured

    # First run - try to auto-configure VSCode
    print("  \033[38;5;141m🔧 First run detected - configuring VSCode...\033[0m")
    configured = setup_vscode_settings(silent=False)

    if configured:
        # Create marker file
        try:
            with open(marker_file, 'w') as f:
                f.write('configured')
            print("  \033[38;5;245mReload VSCode window to apply settings\033[0m")
        except:
            pass
    else:
        print("  \033[38;5;245mNo VSCode settings found - manual setup may be needed\033[0m")
        print("  \033[38;5;245mRun: claude-janus --setup\033[0m")

    print()


def main():
    """Main entry point"""
    # Parse arguments
    args = sys.argv[1:]
    is_resume = False
    ssh_host_alias = None
    claude_args = []

    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ('--setup', '--configure'):
            # Just setup VSCode and exit
            print()
            print("  \033[38;5;141m🔧 Configuring VSCode for Janus...\033[0m")
            print()
            setup_vscode_settings(silent=False)
            print()
            print("  \033[38;5;245mReload VSCode window to apply settings (Cmd+Shift+P → Reload Window)\033[0m")
            print()
            sys.exit(0)
        elif arg in ('--resume', '-r', 'resume'):
            is_resume = True
            claude_args.append('--resume')
        elif arg == '--host':
            if i + 1 < len(args):
                ssh_host_alias = args[i + 1]
                i += 1
            else:
                print("\033[31mError: --host requires a value\033[0m", file=sys.stderr)
                sys.exit(1)
        elif arg.startswith('--host='):
            ssh_host_alias = arg[7:]
        else:
            claude_args.append(arg)
        i += 1

    # Print sexy banner
    print_banner(is_resume)

    # Check first run and auto-configure VSCode
    check_first_run()

    # Set SSH host alias for bridge matching
    # This should match VSCode's [SSH: xxx] in window title
    if ssh_host_alias:
        os.environ['JANUS_SSH_HOST'] = ssh_host_alias
        print(f"  \033[38;5;245mSSH host alias: \033[38;5;208m{ssh_host_alias}\033[0m")

    # Get optional session title
    title = get_session_title()
    if title:
        os.environ['JANUS_TITLE'] = title
        # Set terminal title
        print(f"\033]0;{title}\007", end='', flush=True)
        print(f"  \033[38;5;245mSession: \033[38;5;141m{title}\033[0m")

    print()

    args = claude_args

    # Find claude
    claude_path = find_claude()

    if not claude_path:
        print("\033[31mError: Could not find 'claude' binary.\033[0m", file=sys.stderr)
        print("Please ensure Claude CLI is installed and in your PATH.", file=sys.stderr)
        print("Install: npm install -g @anthropic-ai/claude-cli", file=sys.stderr)
        sys.exit(1)

    # Import and run the PTY capture
    from .pty_capture import run_claude_session

    try:
        run_claude_session(claude_path, args)
    except KeyboardInterrupt:
        print("\n\033[38;5;245mSession interrupted.\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\033[31mError: {e}\033[0m", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
