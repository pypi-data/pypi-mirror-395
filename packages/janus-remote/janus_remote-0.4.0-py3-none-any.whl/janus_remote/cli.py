#!/usr/bin/env python3
"""
CLI entry point for janus-remote

Usage:
    claude-janus              # Start new Claude session with voice paste
    claude-janus --resume     # Resume previous session
    claude-janus -r           # Short form resume
"""

import sys
import os
import shutil


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
        if arg in ('--resume', '-r', 'resume'):
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
