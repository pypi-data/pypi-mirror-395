# Meld MCP Server

Model Context Protocol server that connects Claude Code to the Meld cloud.

## Installation

```bash
pip install meld-mcp
```

## Usage

The MCP server is automatically started by Claude Code after running `meld setup`.

## Tools

### Session
- **meld_hello()** - Session start, returns user state and greeting
- **meld_start_checkin()** - Start a check-in session
- **meld_checkin_respond(session_id, question_id, response)** - Respond to question

### Memory
- **meld_remember(content, title?, kind?)** - Store a memory
- **meld_recall(query, limit?)** - Semantic search memories

### Profile
- **meld_get_profile()** - Get user profile
- **meld_set_slot(key, value, confidence?)** - Set profile slot

### Projects
- **meld_list_projects(status?)** - List projects
- **meld_create_project(name, description?, domains?, goals?)** - Create project

## Configuration

The MCP server reads credentials from `~/.meld/credentials.json` (created by `meld login`).

Environment variables:
- `MELD_API_URL` - Override the API URL (default: https://api.meld.run)

## Session Hook

The hook at `meld_mcp.hooks.check_session()` is called by Claude Code on each prompt.
It reminds Claude to call `meld_hello()` on the first prompt of each session.

