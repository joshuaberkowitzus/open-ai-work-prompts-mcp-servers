# Workplace Prompts MCP Server

A Model Context Protocol (MCP) server that exposes workplace productivity prompts as resources, prompts, and tools. Available in both HTTP and stdio implementations.

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

## Configuration with Claude Desktop

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

**For HTTP version:**
Start the HTTP server separately, then configure Claude Desktop to connect to `http://localhost:3000`

## Architecture

Both implementations follow the MCP specification and provide the same functionality through different transport layers:

- **HTTP**: REST-style endpoints for easy integration and testing
- **stdio**: JSON-RPC over stdin/stdout for direct process communication

## License

MIT
