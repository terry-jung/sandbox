# iMessage MCP Server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that connects to Apple iMessage on macOS. It lets AI assistants read your message history and send iMessages.

## Requirements

- **macOS** (iMessage is Apple-only)
- **Python 3.10+**
- **Full Disk Access** granted to the terminal app running the server (System Settings → Privacy & Security → Full Disk Access)
- **Messages.app** must have been used at least once (so `chat.db` exists)

## Install

```bash
cd imessage-mcp-server
pip install -r requirements.txt
```

## Run

```bash
python server.py
```

The server communicates over stdio using the MCP protocol.

## Configure with Claude Code

Add this to your Claude Code MCP settings (`.claude/settings.json` or via the `/mcp` command):

```json
{
  "mcpServers": {
    "imessage": {
      "command": "python",
      "args": ["/absolute/path/to/imessage-mcp-server/server.py"]
    }
  }
}
```

## Tools

| Tool | Description |
|------|-------------|
| `list_conversations` | List recent iMessage conversations with participant info |
| `read_messages` | Read messages from a specific conversation by chat ID |
| `search_messages` | Search all message history by text query |
| `get_contact_info` | Get participant details for a conversation |
| `send_message` | Send an iMessage or SMS to a phone number or email |
| `count_messages` | Get message count statistics for a conversation |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `IMESSAGE_DB_PATH` | `~/Library/Messages/chat.db` | Path to the iMessage SQLite database |

## Security Notes

- The database is opened in **read-only** mode — the server never modifies `chat.db`.
- `send_message` uses AppleScript to send via Messages.app, which may trigger a macOS permission prompt on first use.
- Grant Full Disk Access only to the specific terminal you use for this server.
