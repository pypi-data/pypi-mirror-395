# talkops

TalkOps Client which connects to various TalkOps A2A Servers.

## Installation

Install via pip:
```bash
pip install talkops-client
```

Or via uv:
```bash
uv pip install talkops-client
```

**Note:** The package name is `talkops-client`, but the CLI command is still `talkops`.

## Usage

### Basic Usage

Connect to an A2A server:

```bash
talkops --host localhost --port 10102
```

### With Agent Card File

If you have an agent card file (JSON):

```bash
talkops --host localhost --port 10102 --agent-card /path/to/agent-card.json
```

### With Agent Card URL

You can also provide an agent card URL:

```bash
talkops --host localhost --port 10102 --agent-card http://example.com/agent-card.json
```

### Options

- `--host`: A2A server host (default: `localhost`)
- `--port`: A2A server port (default: `10102`)
- `--agent-card`: Path to agent card file (JSON) or URL. If not provided, will fetch from server
- `--session`: Session ID (0 = generate new, default: `0`)
- `--history`: Show task history after completion (flag)
- `--timeout`: HTTP request timeout in seconds (0 = no timeout for async streaming, default: `0`)

### Examples

```bash
# Connect to remote server
talkops --host example.com --port 8080

# Use a specific session ID
talkops --host localhost --port 10102 --session 12345

# Show history after task completion
talkops --host localhost --port 10102 --history

# Use custom timeout
talkops --host localhost --port 10102 --timeout 30
```

## Development

To install in development mode:

```bash
pip install -e .
```

Or with uv:

```bash
uv pip install -e .
```
