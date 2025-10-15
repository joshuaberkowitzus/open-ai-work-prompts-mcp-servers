# Workplace Prompts MCP Server

A Model Context Protocol (MCP) server that exposes workplace productivity prompts as resources, prompts, and tools. Available in both HTTP and stdio implementations.
Prompts : https://academy.openai.com/public/clubs/work-users-ynjqu/resources/chatgpt-for-any-role

## Features

- **20 workplace prompts** organized into 4 categories:
  - Communication & Writing
  - Meetings & Collaboration
  - Problem Solving & Decision Making
  - Organization & Productivity

- **Three MCP primitives:**
  - **Resources**: Access prompts as readable resources
  - **Prompts**: Use prompts with parameter substitution
  - **Tools**: Execute prompts with user input

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### HTTP Server

Start the HTTP server:

```bash
python mcp_http_server.py
```

The server will run on `http://localhost:3000`

**Available endpoints:**

- `POST /mcp/v1/initialize` - Initialize connection
- `POST /mcp/v1/resources/list` - List all prompt resources
- `POST /mcp/v1/resources/read` - Read a specific prompt
- `POST /mcp/v1/prompts/list` - List all available prompts
- `POST /mcp/v1/prompts/get` - Get a prompt with arguments
- `POST /mcp/v1/tools/list` - List all available tools
- `POST /mcp/v1/tools/call` - Execute a tool

**Example request:**

```bash
curl -X POST http://localhost:3000/mcp/v1/resources/list \
  -H "Content-Type: application/json" \
  -d '{}'
```

### stdio Server

Run the stdio server:

```bash
python mcp_stdio_server.py
```

The server reads JSON-RPC requests from stdin and writes responses to stdout.

**Example request (via stdin):**

```json
{"jsonrpc": "2.0", "id": 1, "method": "resources/list", "params": {}}
```

## MCP Methods

### Resources

**List resources:**
```json
{"method": "resources/list", "params": {}}
```

**Read resource:**
```json
{
  "method": "resources/read",
  "params": {
    "uri": "prompt://communication-writing/write-professional-email"
  }
}
```

### Prompts

**List prompts:**
```json
{"method": "prompts/list", "params": {}}
```

**Get prompt with arguments:**
```json
{
  "method": "prompts/get",
  "params": {
    "name": "communication-writing/write-professional-email",
    "arguments": {
      "recipient": "Sarah Johnson",
      "topic": "Q4 budget review"
    }
  }
}
```

### Tools

**List tools:**
```json
{"method": "tools/list", "params": {}}
```

**Call tool:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "meetings-collaboration/create-meeting-agenda",
    "arguments": {
      "input": "Sprint planning meeting for next week"
    }
  }
}
```

## Prompt Categories

### Communication & Writing
- `write-professional-email` - Draft professional emails
- `rewrite-for-clarity` - Improve text clarity
- `adapt-message-for-audience` - Adjust tone for different audiences
- `draft-meeting-invite` - Create meeting invitations
- `summarize-long-email` - Summarize email threads

### Meetings & Collaboration
- `create-meeting-agenda` - Structure meeting agendas
- `summarize-meeting-notes` - Organize meeting notes
- `create-action-items-list` - Extract tasks from notes
- `prep-questions-for-meeting` - Generate thoughtful questions
- `draft-follow-up-email` - Write meeting follow-ups

### Problem Solving & Decision Making
- `identify-root-cause` - Analyze workplace issues
- `compare-options` - Evaluate multiple solutions
- `decision-criteria` - Define decision frameworks
- `risk-assessment` - Assess plan risks
- `recommend-best-option` - Provide recommendations

### Organization & Productivity
- `document-daily-priorities` - Prioritize daily tasks
- `create-weekly-plan` - Build weekly schedules
- `summarize-long-document` - Create document summaries
- `brainstorm-solutions` - Generate solution ideas
- `write-project-update` - Draft status updates

## Configuration

### Claude Desktop

To use with Claude Desktop, add to your config file:

**For stdio version** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "workplace-prompts": {
      "command": "python",
      "args": ["/path/to/mcp_stdio_server.py"]
    }
  }
}
```

**Config file locations:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**For HTTP version:**
Start the HTTP server separately, then configure Claude Desktop to connect to `http://localhost:3000`

### VS Code with GitHub Copilot

GitHub Copilot in VS Code supports MCP servers through the Copilot Extensions API.

**Setup with stdio version:**

1. Create or edit `.vscode/settings.json` in your workspace:

```json
{
  "github.copilot.advanced": {
    "mcp.servers": {
      "workplace-prompts": {
        "command": "python",
        "args": ["-u", "/absolute/path/to/mcp_stdio_server.py"],
        "env": {}
      }
    }
  }
}
```

2. Reload VS Code window (Cmd/Ctrl + Shift + P → "Developer: Reload Window")

3. Access prompts through Copilot Chat using `@workplace-prompts`

**Setup with HTTP version:**

1. Start the HTTP server:
```bash
python mcp_http_server.py
```

2. Configure in `.vscode/settings.json`:
```json
{
  "github.copilot.advanced": {
    "mcp.servers": {
      "workplace-prompts": {
        "url": "http://localhost:3000/mcp/v1"
      }
    }
  }
}
```

**Usage in VS Code:**
```
@workplace-prompts /communication-writing/write-professional-email
```

### Gemini CLI

Google's Gemini CLI (experimental) supports MCP through configuration files.

**Setup with stdio version:**

1. Create or edit `~/.gemini/config.json`:

```json
{
  "mcpServers": {
    "workplace-prompts": {
      "command": "python3",
      "args": ["/absolute/path/to/mcp_stdio_server.py"],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

2. Verify the server is registered:
```bash
gemini mcp list
```

**Usage with Gemini CLI:**
```bash
# List available prompts
gemini mcp resources list workplace-prompts

# Use a prompt
gemini chat --mcp workplace-prompts \
  "Use the write-professional-email prompt for a budget update to my manager"

# Call a tool directly
gemini mcp tools call workplace-prompts \
  communication-writing/write-professional-email \
  --input "Recipient: John Smith, Topic: Q4 Budget Review"
```

**Setup with HTTP version:**

1. Start the HTTP server first:
```bash
python mcp_http_server.py
```

2. Configure in `~/.gemini/config.json`:
```json
{
  "mcpServers": {
    "workplace-prompts": {
      "transport": "http",
      "url": "http://localhost:3000"
    }
  }
}
```

**Environment Variables for Gemini:**
```bash
export GEMINI_MCP_WORKPLACE_PROMPTS_ENABLED=true
export GEMINI_MCP_LOG_LEVEL=debug  # For troubleshooting
```

## Architecture

Both implementations follow the MCP specification and provide the same functionality through different transport layers:

- **HTTP**: REST-style endpoints for easy integration and testing
- **stdio**: JSON-RPC over stdin/stdout for direct process communication

## License

MIT
