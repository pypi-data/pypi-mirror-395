"""CLI configuration and credential management."""

import json
import os
from pathlib import Path
from typing import Any

# Default API URL (can be overridden via env)
DEFAULT_API_URL = "https://api.meld.run"

# Config directory
MELD_DIR = Path.home() / ".meld"
CREDENTIALS_FILE = MELD_DIR / "credentials.json"
CONFIG_FILE = MELD_DIR / "config.json"


def get_api_url() -> str:
    """Get the Meld API URL."""
    return os.environ.get("MELD_API_URL", DEFAULT_API_URL)


def ensure_meld_dir():
    """Ensure ~/.meld directory exists."""
    MELD_DIR.mkdir(parents=True, exist_ok=True)


def save_credentials(token: str, user_id: str, email: str):
    """Save authentication credentials."""
    ensure_meld_dir()
    creds = {
        "access_token": token,
        "user_id": user_id,
        "email": email,
    }
    CREDENTIALS_FILE.write_text(json.dumps(creds, indent=2))
    # Secure permissions
    CREDENTIALS_FILE.chmod(0o600)


def load_credentials() -> dict[str, str] | None:
    """Load saved credentials."""
    if not CREDENTIALS_FILE.exists():
        return None
    try:
        return json.loads(CREDENTIALS_FILE.read_text())
    except Exception:
        return None


def clear_credentials():
    """Clear saved credentials."""
    if CREDENTIALS_FILE.exists():
        CREDENTIALS_FILE.unlink()


def get_access_token() -> str | None:
    """Get the saved access token."""
    creds = load_credentials()
    return creds.get("access_token") if creds else None


def save_config(key: str, value: Any):
    """Save a config value."""
    ensure_meld_dir()
    config = {}
    if CONFIG_FILE.exists():
        try:
            config = json.loads(CONFIG_FILE.read_text())
        except Exception:
            pass
    config[key] = value
    CONFIG_FILE.write_text(json.dumps(config, indent=2))


def load_config() -> dict[str, Any]:
    """Load all config values."""
    if not CONFIG_FILE.exists():
        return {}
    try:
        return json.loads(CONFIG_FILE.read_text())
    except Exception:
        return {}

