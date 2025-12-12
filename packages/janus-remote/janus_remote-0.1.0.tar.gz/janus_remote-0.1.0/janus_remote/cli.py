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
    ]

    for path in common_paths:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

    return None


def main():
    """Main entry point"""
    # Find claude
    claude_path = find_claude()

    if not claude_path:
        print("Error: Could not find 'claude' binary.", file=sys.stderr)
        print("Please ensure Claude CLI is installed and in your PATH.", file=sys.stderr)
        print("Install: npm install -g @anthropic-ai/claude-cli", file=sys.stderr)
        sys.exit(1)

    # Check for resume flag
    args = sys.argv[1:]
    if args and args[0] in ('--resume', '-r', 'resume'):
        args[0] = '--resume'

    # Import and run the PTY capture
    from .pty_capture import run_claude_session

    try:
        run_claude_session(claude_path, args)
    except KeyboardInterrupt:
        print("\nSession interrupted.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
