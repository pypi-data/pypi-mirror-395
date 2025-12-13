"""
Janus Remote - Voice-to-text paste bridge for Claude CLI on remote SSH sessions

Usage:
    pip install janus-remote
    claude-janus  # Start Claude with voice paste support

Requires:
    - Janus Electron app running on your local Mac
    - SSH port forwarding: RemoteForward 9473 localhost:9473
"""

__version__ = "0.2.0"
__author__ = "He Who Seeks"

from .pty_capture import main as run_pty_capture

__all__ = ["run_pty_capture", "__version__"]
