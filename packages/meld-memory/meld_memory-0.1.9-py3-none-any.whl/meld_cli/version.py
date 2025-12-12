"""Version checking with update notifications."""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx
from packaging import version

CACHE_FILE = Path.home() / ".meld" / "version_cache.json"
CACHE_TTL = timedelta(hours=24)
PYPI_URL = "https://pypi.org/pypi/meld-memory/json"
TIMEOUT = 5.0


def _read_cache() -> dict | None:
    """Read cache file, returning None if missing or corrupt."""
    if not CACHE_FILE.exists():
        return None
    try:
        return json.loads(CACHE_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def _write_cache(latest: str) -> None:
    """Write version to cache."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps({
        "latest": latest,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }))


def _cache_is_fresh(cache: dict) -> bool:
    """Check if cache entry is still valid."""
    checked_at = cache.get("checked_at")
    if not checked_at:
        return False
    try:
        checked = datetime.fromisoformat(checked_at)
        if checked.tzinfo is None:
            checked = checked.replace(tzinfo=timezone.utc)
        return checked > datetime.now(timezone.utc) - CACHE_TTL
    except ValueError:
        return False


def get_latest_version() -> str | None:
    """Fetch latest version from PyPI (cached for 24h)."""
    cache = _read_cache()
    if cache and _cache_is_fresh(cache) and cache.get("latest"):
        return cache["latest"]

    try:
        resp = httpx.get(PYPI_URL, timeout=TIMEOUT)
        resp.raise_for_status()
        latest = resp.json()["info"]["version"]
        _write_cache(latest)
        return latest
    except httpx.HTTPError:
        # HTTP error (network, 404, 500, etc.) - return stale cache if available
        return cache.get("latest") if cache else None
    except (KeyError, TypeError, json.JSONDecodeError):
        # Bad response format - don't cache
        return None


def check_for_update(current: str) -> tuple[bool, str | None]:
    """Returns (has_update, latest_version)."""
    latest = get_latest_version()
    if not latest:
        return False, None
    try:
        return version.parse(latest) > version.parse(current), latest
    except version.InvalidVersion:
        return False, latest


def show_update_notice(current: str, console) -> None:
    """Show update notice if a newer version is available.
    
    Uses cached version check (24h TTL) to avoid network calls on every command.
    """
    has_update, latest = check_for_update(current)
    if has_update:
        console.print(f"[yellow]⚠ Update available: {current} → {latest}[/yellow]")
        console.print(f"  [dim]Run: pipx upgrade meld-memory[/dim]")
        console.print()

