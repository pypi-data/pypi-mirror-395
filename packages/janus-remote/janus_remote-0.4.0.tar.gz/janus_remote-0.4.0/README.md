# janus-remote

Voice-to-text paste bridge for Claude CLI on remote SSH sessions.

Use your voice to interact with Claude CLI running on remote servers, with transcriptions pasted directly into the terminal - no window switching needed!

## Installation

```bash
pip install janus-remote
```

## Requirements

1. **Local Mac**: Janus Electron app running (provides voice recognition + WebSocket server)
2. **SSH Config**: Port forwarding enabled (one-time setup)

## SSH Setup (One-Time)

Add this to your `~/.ssh/config` on your **local Mac**:

```
Host *
    RemoteForward 9473 localhost:9473
```

Or for specific hosts:

```
Host myserver
    HostName myserver.example.com
    RemoteForward 9473 localhost:9473
```

This forwards the Janus WebSocket bridge (port 9473) to the remote server.

## Usage

On your remote server via SSH:

```bash
# Start a new Claude session with voice paste support
claude-janus

# Resume a previous session
claude-janus --resume
claude-janus -r
```

## How It Works

```
LOCAL MAC                           REMOTE SERVER (via SSH)
┌─────────────────────┐             ┌─────────────────────┐
│ Janus Electron      │             │ claude-janus        │
│ (Voice Recognition) │             │ (This package)      │
│         │           │             │         │           │
│         ▼           │             │         │           │
│ WebSocket :9473 ────┼─────────────┼───────► │           │
│                     │  SSH Tunnel │         ▼           │
│                     │             │ Inject into PTY     │
└─────────────────────┘             └─────────────────────┘
```

1. Speak into your Mac's microphone
2. Janus transcribes and sends via WebSocket
3. SSH tunnel forwards to remote server
4. `claude-janus` receives and injects text directly into Claude CLI

## Features

- **Sexy Terminal Banner**: Claude + Janus ASCII art on startup 🔮
- **Voice Paste**: Speak on your Mac → text appears in remote terminal
- **Approval Overlay**: Claude permission requests show on your local Mac overlay
- **Zero latency feel**: WebSocket connection, no polling
- **Background paste**: No window switching - text appears directly in terminal
- **Multi-session support**: Run multiple `claude-janus` sessions on different servers
- **Auto-reconnect**: Handles connection drops gracefully

## Troubleshooting

### "Bridge connection failed"
- Ensure Janus Electron is running on your local Mac
- Verify SSH port forwarding is configured
- Check that port 9473 isn't blocked

### "Could not find 'claude' binary"
- Install Claude CLI: `npm install -g @anthropic-ai/claude-cli`
- Or ensure it's in your PATH

## License

MIT

## Author

He Who Seeks
