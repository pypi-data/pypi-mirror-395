"""Session hooks for Claude Code integration.

This hook injects Meld context directly into Claude's context,
avoiding the race condition of asking Claude to call MCP tools
before they're initialized.

Also triggers background session sync on new sessions.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import httpx

# Meld directory for config and state
MELD_DIR = Path.home() / ".meld"

# Session marker directory - use ~/.meld for cross-platform compatibility
SESSION_MARKER_DIR = MELD_DIR / "sessions"


def maybe_trigger_sync():
    """Trigger background session sync if enabled and not already running.
    
    This is called on new sessions to automatically index recent
    Claude Code conversations without user intervention.
    """
    # Check if auto_sync is disabled in config
    config_file = MELD_DIR / "config.json"
    if config_file.exists():
        try:
            config = json.loads(config_file.read_text())
            if not config.get("auto_sync", True):
                return  # User disabled auto-sync
        except json.JSONDecodeError:
            pass  # Malformed config, use defaults
    
    # Check if sync is already running (avoid redundant spawns)
    pid_file = MELD_DIR / "sync.pid"
    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            os.kill(pid, 0)  # Check if process is alive
            return  # Sync already running
        except (ProcessLookupError, ValueError, OSError):
            pass  # PID file stale or invalid, proceed with sync
    
    # Spawn background sync
    try:
        subprocess.Popen(
            [sys.executable, "-m", "meld_cli.main", "sync", "--background"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
    except Exception as e:
        # Log spawn failure for debugging
        log_file = MELD_DIR / "sync.log"
        try:
            MELD_DIR.mkdir(parents=True, exist_ok=True)
            with open(log_file, "a") as f:
                f.write(f"{datetime.now().isoformat()} | ERROR | Auto-sync spawn failed: {e}\n")
        except Exception:
            pass  # Can't log, silently continue


def get_session_marker_path() -> Path:
    """Get the path for the session marker file."""
    SESSION_MARKER_DIR.mkdir(parents=True, exist_ok=True)

    # Try to get Claude session ID from environment
    session_id = os.environ.get("CLAUDE_SESSION_ID")

    if session_id:
        return SESSION_MARKER_DIR / f"session-{session_id}"

    # Fallback: use date + parent process ID
    ppid = os.getppid()
    today = datetime.now().strftime("%Y%m%d")
    return SESSION_MARKER_DIR / f"session-{ppid}-{today}"


def get_credentials() -> dict | None:
    """Load Meld credentials."""
    creds_file = Path.home() / ".meld" / "credentials.json"
    if not creds_file.exists():
        return None
    try:
        return json.loads(creds_file.read_text())
    except Exception:
        return None


def fetch_user_state(token: str, api_url: str) -> dict | None:
    """Fetch user state from Meld API directly.
    
    This avoids the MCP race condition by calling the API
    from the hook instead of asking Claude to call an MCP tool.
    """
    try:
        with httpx.Client(timeout=3.0) as client:
            response = client.get(
                f"{api_url}/session/hello",
                headers={"Authorization": f"Bearer {token}"},
            )
            if response.status_code == 200:
                return response.json()
    except Exception:
        pass
    return None


def check_session():
    """Check if this is a new session and inject Meld context.

    This is called by Claude Code's UserPromptSubmit hook.
    Only outputs on the first prompt of each session.
    
    KEY DESIGN: We fetch user state directly via HTTP and inject
    the context, rather than asking Claude to call an MCP tool.
    This avoids the race condition where MCP servers aren't ready yet.
    """
    marker_path = get_session_marker_path()

    if marker_path.exists():
        # Already handled this session
        return

    # Mark session as having been reminded
    marker_path.touch()

    # Trigger background session sync (fire-and-forget)
    maybe_trigger_sync()

    # Check if user is logged in
    creds = get_credentials()
    if not creds or not creds.get("access_token"):
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": (
                    "[Meld] Not logged in. Run `meld login` in terminal to enable personal memory."
                )
            }
        }))
        return

    # Fetch user state directly (avoids MCP race condition)
    api_url = os.environ.get("MELD_API_URL", "https://api.meld.run")
    state = fetch_user_state(creds["access_token"], api_url)

    if not state:
        # API unreachable - don't block, just skip silently
        # User can still use meld tools once MCP is ready
        return

    # Build context based on user state
    user_state = state.get("state", "unknown")
    greeting = state.get("greeting", "")
    counts = state.get("content_counts", {})
    checkin_info = state.get("checkin_info") or {}

    if user_state == "new_user":
        context = (
            f"[Meld] {greeting}\n\n"
            "This is a new Meld user. When appropriate, offer to learn about them: "
            "their name, what they're working on, their preferences. Keep it conversational, "
            "not an interrogation. Use meld_set_slot and meld_create_project to save what you learn."
        )
    else:
        # Existing user - brief context
        projects = counts.get("projects", 0)
        memories = counts.get("memories", 0)
        
        context_parts = [f"[Meld] {greeting}"]
        context_parts.append(f"User has {projects} project(s) and {memories} memory/memories stored.")
        
        if checkin_info.get("suggested"):
            days = checkin_info.get("days_since_last", "several")
            context_parts.append(
                f"Check-in suggested (last: {days} days ago). "
                "Only offer if user seems open to it - they came here to work."
            )
        
        context = " ".join(context_parts)

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context
        }
    }))


if __name__ == "__main__":
    check_session()

