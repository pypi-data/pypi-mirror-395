"""Meld MCP Server - Exposes Meld tools via Model Context Protocol."""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from .api_client import MeldAPIClient
from .config import get_access_token

# Create server instance with instructions
# These instructions are included in Claude's system prompt
mcp = Server(
    "meld",
    instructions="""Meld is the user's personal memory system. You have access to meld tools to:
- meld_hello: Check user state at session start (new user vs returning)
- meld_remember/meld_recall: Store and search user's memories
- meld_get_profile/meld_set_slot: Manage user profile information  
- meld_list_projects/meld_create_project: Track user's projects
- meld_start_checkin: Conduct periodic check-ins to update context
- meld_search_sessions: Search past Claude Code and Cursor conversations for context

Use these tools naturally when relevant. For new users, learn about them conversationally.
For returning users, leverage their stored context to be more helpful.

When user says things like "remember when we...", "like we did before", or asks about
past work, use meld_search_sessions to find relevant context from their session history.
This works across tools - conversations from Claude Code and Cursor are both searchable."""
)

# API client instance
api = MeldAPIClient()


# ===========================================
# TOOL DEFINITIONS
# ===========================================

TOOLS = [
    Tool(
        name="meld_hello",
        description="Session start - returns user state and recommended action. Call this at the start of every session to get personalized greeting and know if check-in is recommended.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="meld_start_checkin",
        description="Start a daily check-in session. Returns a session ID and list of questions to ask the user conversationally.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="meld_checkin_respond",
        description="Submit user's response to a check-in question.",
        inputSchema={
            "type": "object",
            "properties": {
                "session_id": {"type": "string", "description": "The check-in session ID from meld_start_checkin"},
                "question_id": {"type": "string", "description": "The question ID (e.g., q1, q_project_xxx)"},
                "response": {"type": "string", "description": "The user's response text"},
            },
            "required": ["session_id", "question_id", "response"],
        },
    ),
    Tool(
        name="meld_remember",
        description="Store a memory for the user. Use when user shares preferences, project updates, decisions, or learnings.",
        inputSchema={
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "The memory content to store"},
                "title": {"type": "string", "description": "Optional title/summary"},
                "kind": {"type": "string", "description": "Memory type: explicit, episodic, semantic, procedural", "default": "explicit"},
            },
            "required": ["content"],
        },
    ),
    Tool(
        name="meld_recall",
        description="Search user's memories semantically. Returns relevant memories based on meaning.",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "What to search for"},
                "limit": {"type": "integer", "description": "Max results (default 5, max 20)", "default": 5},
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="meld_get_profile",
        description="Get user's profile with preferences, slots, and interests.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="meld_set_slot",
        description="Set a profile slot (key-value pair about the user). Common slots: name, company, role, location, timezone.",
        inputSchema={
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "Slot name"},
                "value": {"type": "string", "description": "Slot value"},
                "confidence": {"type": "number", "description": "How confident (0-1)", "default": 0.9},
            },
            "required": ["key", "value"],
        },
    ),
    Tool(
        name="meld_list_projects",
        description="List user's projects.",
        inputSchema={
            "type": "object",
            "properties": {
                "status": {"type": "string", "description": "Filter by status: active, paused, completed"},
            },
            "required": [],
        },
    ),
    Tool(
        name="meld_create_project",
        description="Create a new project.",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Project name"},
                "description": {"type": "string", "description": "What the project is about"},
                "domains": {"type": "array", "items": {"type": "string"}, "description": "Relevant domains/tags"},
                "goals": {"type": "array", "items": {"type": "string"}, "description": "Project goals"},
            },
            "required": ["name"],
        },
    ),
    Tool(
        name="meld_update_project",
        description="Update an existing project.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "The project ID to update"},
                "name": {"type": "string", "description": "New project name"},
                "description": {"type": "string", "description": "New description"},
                "status": {"type": "string", "description": "New status: active, paused, completed"},
                "domains": {"type": "array", "items": {"type": "string"}, "description": "New domains/tags"},
                "goals": {"type": "array", "items": {"type": "string"}, "description": "New goals"},
            },
            "required": ["project_id"],
        },
    ),
    Tool(
        name="meld_add_interest",
        description="Add a domain of interest for the user.",
        inputSchema={
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "The interest domain (e.g., 'machine learning')"},
                "specifics": {"type": "array", "items": {"type": "string"}, "description": "Specific sub-topics"},
                "priority": {"type": "string", "description": "Importance: low, medium, high", "default": "medium"},
            },
            "required": ["domain"],
        },
    ),
    Tool(
        name="meld_search_sessions",
        description="Search user's Claude Code and Cursor session history. Use to recall past conversations, solutions, and context from previous coding sessions.",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "What to search for in past sessions"},
                "limit": {"type": "integer", "description": "Max results (default 5, max 20)", "default": 5},
                "project": {"type": "string", "description": "Optional project filter"},
                "source": {"type": "string", "description": "Filter by source: all (default), claude_code, cursor", "enum": ["all", "claude_code", "cursor"]},
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="meld_session_stats",
        description="Get statistics about indexed session history.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
]


# ===========================================
# MCP HANDLERS
# ===========================================


@mcp.list_tools()
async def list_tools() -> list[Tool]:
    """Return the list of available tools."""
    return TOOLS


@mcp.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool invocations."""
    
    # Check authentication for all tools
    if not get_access_token():
        return [TextContent(
            type="text",
            text="Not logged in to Meld. User needs to run 'meld login' in their terminal first.",
        )]
    
    # Route to appropriate handler
    if name == "meld_hello":
        return await handle_hello()
    elif name == "meld_start_checkin":
        return await handle_start_checkin()
    elif name == "meld_checkin_respond":
        return await handle_checkin_respond(
            arguments["session_id"],
            arguments["question_id"],
            arguments["response"],
        )
    elif name == "meld_remember":
        return await handle_remember(
            arguments["content"],
            arguments.get("title"),
            arguments.get("kind", "explicit"),
        )
    elif name == "meld_recall":
        return await handle_recall(
            arguments["query"],
            arguments.get("limit", 5),
        )
    elif name == "meld_get_profile":
        return await handle_get_profile()
    elif name == "meld_set_slot":
        return await handle_set_slot(
            arguments["key"],
            arguments["value"],
            arguments.get("confidence", 0.9),
        )
    elif name == "meld_list_projects":
        return await handle_list_projects(arguments.get("status"))
    elif name == "meld_create_project":
        return await handle_create_project(
            arguments["name"],
            arguments.get("description"),
            arguments.get("domains"),
            arguments.get("goals"),
        )
    elif name == "meld_update_project":
        return await handle_update_project(
            arguments["project_id"],
            arguments.get("name"),
            arguments.get("description"),
            arguments.get("status"),
            arguments.get("domains"),
            arguments.get("goals"),
        )
    elif name == "meld_add_interest":
        return await handle_add_interest(
            arguments["domain"],
            arguments.get("specifics"),
            arguments.get("priority", "medium"),
        )
    elif name == "meld_search_sessions":
        return await handle_search_sessions(
            arguments["query"],
            arguments.get("limit", 5),
            arguments.get("project"),
            arguments.get("source", "all"),
        )
    elif name == "meld_session_stats":
        return await handle_session_stats()
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


# ===========================================
# TOOL IMPLEMENTATIONS
# ===========================================


async def handle_hello() -> list[TextContent]:
    """Session start - returns user state and recommended action."""
    result = await api.hello()

    if "error" in result:
        return [TextContent(type="text", text=f"Error: {result['error']}")]

    lines = [
        f"**User State:** {result.get('state')}",
        f"**Recommended Action:** {result.get('recommended_action')}",
        f"**Greeting:** {result.get('greeting')}",
        "",
        "**Content Counts:**",
        f"  - Projects: {result.get('content_counts', {}).get('projects', 0)}",
        f"  - Memories: {result.get('content_counts', {}).get('memories', 0)}",
        f"  - Profile slots: {result.get('content_counts', {}).get('slots', 0)}",
    ]

    checkin_info = result.get("checkin_info")
    if checkin_info and checkin_info.get("suggested"):
        lines.extend([
            "",
            "**Check-in Info:**",
            "  - Suggested: Yes",
            f"  - Days since last: {checkin_info.get('days_since_last', 'never')}",
            f"  - Reason: {checkin_info.get('reason')}",
        ])

    # Add getting-started tips for new users
    if result.get("state") == "new_user":
        lines.extend([
            "",
            "**Getting Started:**",
            "• Tell me your name and I'll remember it",
            '• Say "Create a project called [name]" to track your work',
            '• Share preferences like "I prefer TypeScript over JavaScript"',
        ])

    return [TextContent(type="text", text="\n".join(lines))]


async def handle_start_checkin() -> list[TextContent]:
    """Start a daily check-in session."""
    result = await api.start_checkin()

    if "error" in result:
        return [TextContent(type="text", text=f"Error: {result['error']}")]

    lines = [
        f"**Session ID:** {result.get('session_id')}",
        f"**Questions:** {result.get('question_count')}",
        "",
        "**Questions to ask:**",
    ]

    for q in result.get("questions", []):
        lines.append(f"  - [{q.get('id')}] {q.get('text')}")

    lines.extend([
        "",
        "Present questions conversationally, one at a time.",
        "After each response, call meld_checkin_respond() with the session_id, question_id, and response.",
    ])

    return [TextContent(type="text", text="\n".join(lines))]


async def handle_checkin_respond(session_id: str, question_id: str, response: str) -> list[TextContent]:
    """Submit user's response to a check-in question."""
    result = await api.checkin_respond(session_id, question_id, response)

    if "error" in result:
        return [TextContent(type="text", text=f"Error: {result['error']}")]

    lines = [f"**Acknowledged:** {result.get('acknowledged')}"]

    if result.get("is_complete"):
        lines.extend([
            "",
            "**Check-in complete!**",
            f"Summary: {result.get('summary', 'Thanks for the update!')}",
        ])
    elif result.get("next_question"):
        next_q = result["next_question"]
        lines.extend([
            "",
            f"**Next question:** [{next_q.get('id')}] {next_q.get('text')}",
        ])

    return [TextContent(type="text", text="\n".join(lines))]


async def handle_remember(content: str, title: str | None, kind: str) -> list[TextContent]:
    """Store a memory for the user."""
    # Check for duplicate first
    dup_check = await api.check_duplicate(content, kind)
    if dup_check.get("is_duplicate"):
        existing = dup_check.get("existing_memory", {})
        return [TextContent(
            type="text",
            text=f"Similar memory already exists (ID: {existing.get('id')}, similarity: {dup_check.get('similarity', 1.0):.0%}). Not storing duplicate.",
        )]

    result = await api.store_memory(content, kind, title)

    if "error" in result:
        return [TextContent(type="text", text=f"Error: {result['error']}")]

    return [TextContent(
        type="text",
        text=f"Stored memory (ID: {result.get('id')}): {title or content[:50]}...",
    )]


async def handle_recall(query: str, limit: int) -> list[TextContent]:
    """Search user's memories semantically."""
    result = await api.recall(query, min(limit, 20))

    if not result:
        return [TextContent(type="text", text="No memories found matching that query.")]

    lines = [f"**Found {len(result)} memories:**", ""]
    for mem in result:
        title = mem.get("title") or mem.get("content", "")[:50]
        lines.append(f"- [{mem.get('id')}] {title}")
        lines.append(f"  {mem.get('content', '')[:100]}...")
        lines.append("")

    return [TextContent(type="text", text="\n".join(lines))]


async def handle_get_profile() -> list[TextContent]:
    """Get user's profile with preferences, slots, and interests."""
    result = await api.get_profile()

    if "error" in result:
        return [TextContent(type="text", text=f"Error: {result['error']}")]

    lines = [
        "**Preferences:**",
        f"  - Depth: {result.get('preferences', {}).get('depth')}",
        f"  - Format: {result.get('preferences', {}).get('format')}",
        f"  - Autonomy: {result.get('preferences', {}).get('autonomy')}",
        "",
        "**Profile Slots:**",
    ]

    for key, value in result.get("slots", {}).items():
        lines.append(f"  - {key}: {value}")

    if result.get("interests"):
        lines.extend(["", "**Interests:**"])
        for interest in result.get("interests", []):
            lines.append(f"  - {interest.get('domain')} ({interest.get('priority')})")

    return [TextContent(type="text", text="\n".join(lines))]


async def handle_set_slot(key: str, value: str, confidence: float) -> list[TextContent]:
    """Set a profile slot."""
    result = await api.set_slot(key, value, confidence)

    if "error" in result:
        return [TextContent(type="text", text=f"Error: {result['error']}")]

    return [TextContent(
        type="text",
        text=f"Set slot '{key}' = '{value}' (superseded previous: {result.get('superseded_previous', False)})",
    )]


async def handle_list_projects(status: str | None) -> list[TextContent]:
    """List user's projects."""
    result = await api.list_projects(status)

    if not result:
        return [TextContent(type="text", text="No projects found.")]

    lines = [f"**Projects ({len(result)}):**", ""]
    for proj in result:
        proj_id = proj.get('id', '')
        lines.append(f"- [{proj_id[:8]}...] **{proj.get('name')}** ({proj.get('status')})")
        if proj.get("description"):
            lines.append(f"  {proj.get('description')[:100]}")
        lines.append("")

    return [TextContent(type="text", text="\n".join(lines))]


async def handle_create_project(name: str, description: str | None, domains: list | None, goals: list | None) -> list[TextContent]:
    """Create a new project."""
    result = await api.create_project(name, description, domains, goals)

    if "error" in result:
        return [TextContent(type="text", text=f"Error: {result['error']}")]

    return [TextContent(
        type="text",
        text=f"Created project '{name}' (ID: {result.get('id')})",
    )]


async def handle_update_project(project_id: str, name: str | None, description: str | None, status: str | None, domains: list | None, goals: list | None) -> list[TextContent]:
    """Update an existing project."""
    updates = {}
    if name is not None:
        updates["name"] = name
    if description is not None:
        updates["description"] = description
    if status is not None:
        updates["status"] = status
    if domains is not None:
        updates["domains"] = domains
    if goals is not None:
        updates["goals"] = goals

    if not updates:
        return [TextContent(type="text", text="No updates provided.")]

    result = await api.update_project(project_id, **updates)

    if "error" in result:
        return [TextContent(type="text", text=f"Error: {result['error']}")]

    return [TextContent(
        type="text",
        text=f"Updated project '{result.get('name')}' (ID: {project_id})",
    )]


async def handle_add_interest(domain: str, specifics: list | None, priority: str) -> list[TextContent]:
    """Add a domain of interest for the user."""
    result = await api.add_interest(domain, specifics, priority)

    if "error" in result:
        return [TextContent(type="text", text=f"Error: {result['error']}")]

    return [TextContent(
        type="text",
        text=f"Added interest: {domain} (priority: {priority})",
    )]


async def handle_search_sessions(query: str, limit: int, project: str | None, source: str = "all") -> list[TextContent]:
    """Search user's session history."""
    result = await api.search_sessions(query, min(limit, 20), project, source_filter=source)

    if "error" in result:
        return [TextContent(type="text", text=f"Error: {result['error']}")]

    results = result.get("results", [])
    if not results:
        return [TextContent(
            type="text",
            text="No matching sessions found. User may need to run 'meld sync' to index their session history.",
        )]

    lines = [f"**Found {len(results)} relevant sessions:**", ""]
    for i, r in enumerate(results, 1):
        score_pct = int(r.get("score", 0) * 100)
        project_name = r.get("project", "unknown")
        text = r.get("text", "")[:300]
        
        # Add source attribution
        source_name = r.get("source", "claude_code")
        if source_name == "cursor":
            source_label = "Cursor"
        else:
            source_label = "Claude Code"
        
        lines.append(f"**{i}.** [{score_pct}% match] _{source_label} · Project: {project_name}_")
        lines.append(f"```")
        lines.append(text)
        lines.append(f"```")
        lines.append("")

    return [TextContent(type="text", text="\n".join(lines))]


async def handle_session_stats() -> list[TextContent]:
    """Get session indexing statistics."""
    result = await api.get_session_stats()

    if "error" in result:
        return [TextContent(type="text", text=f"Error: {result['error']}")]

    total = result.get("total_chunks", 0)
    if total == 0:
        return [TextContent(
            type="text",
            text="No sessions indexed yet. User should run 'meld sync' to index their Claude Code and Cursor history.",
        )]

    lines = ["**Session History Stats:**", f"- Total chunks indexed: {total}"]
    
    # Show breakdown by source if available
    by_source = result.get("by_source", {})
    if by_source:
        if by_source.get("claude_code"):
            lines.append(f"- Claude Code: {by_source['claude_code']} chunks")
        if by_source.get("cursor"):
            lines.append(f"- Cursor: {by_source['cursor']} chunks")

    return [TextContent(type="text", text="\n".join(lines))]


# ===========================================
# SERVER MAIN
# ===========================================


def main():
    """Run the Meld MCP server."""
    import asyncio

    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await mcp.run(
                read_stream,
                write_stream,
                mcp.create_initialization_options(),
            )

    asyncio.run(run())


if __name__ == "__main__":
    main()
