"""Configuration for Meld MCP Server."""

import json
import os
from pathlib import Path

# Default API URL
DEFAULT_API_URL = "https://api.meld.run"

# Credentials file
MELD_DIR = Path.home() / ".meld"
CREDENTIALS_FILE = MELD_DIR / "credentials.json"


def get_api_url() -> str:
    """Get the Meld API URL."""
    return os.environ.get("MELD_API_URL", DEFAULT_API_URL)


def get_access_token() -> str | None:
    """Get the saved access token from ~/.meld/credentials.json."""
    if not CREDENTIALS_FILE.exists():
        return None
    try:
        creds = json.loads(CREDENTIALS_FILE.read_text())
        return creds.get("access_token")
    except Exception:
        return None


def get_user_info() -> dict | None:
    """Get saved user info."""
    if not CREDENTIALS_FILE.exists():
        return None
    try:
        return json.loads(CREDENTIALS_FILE.read_text())
    except Exception:
        return None

