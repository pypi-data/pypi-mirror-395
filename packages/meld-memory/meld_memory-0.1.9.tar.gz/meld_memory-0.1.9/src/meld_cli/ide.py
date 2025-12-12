"""
IDE setup and verification for Meld.

Supports multiple IDEs (Claude Code, Cursor) with a data-driven configuration
approach to minimize code duplication.

Public API:
- setup_claude_code(), setup_cursor() - Configure IDEs to use Meld
- verify_claude_code(), verify_cursor() - Verify IDE setup is correct
- is_meld_configured(ide: str) - Check if Meld is configured for an IDE
- verify_meld_mcp_importable() - Check if meld_mcp package is available
"""

import asyncio
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel

from .api import MeldAPI
from .config import get_api_url, load_credentials

console = Console()


# =============================================================================
# Constants
# =============================================================================

MELD_SERVER_KEY = "meld"  # Key used in mcpServers config

MELD_TOOL_NAMES = [
    "meld_hello",
    "meld_start_checkin",
    "meld_checkin_respond",
    "meld_remember",
    "meld_recall",
    "meld_get_profile",
    "meld_set_slot",
    "meld_list_projects",
    "meld_create_project",
    "meld_update_project",
    "meld_add_interest",
    "meld_search_sessions",
    "meld_session_stats",
]


# =============================================================================
# IDE Configuration
# =============================================================================

@dataclass(frozen=True)
class IDEConfig:
    """Configuration for an IDE integration (immutable)."""
    
    name: str                         # Display name: "Claude Code" or "Cursor"
    config_path: Path                 # MCP config file path
    detection_dir: Path               # Directory proving IDE is installed
    
    # MCP entry customization
    mcp_type: Optional[str] = None    # "stdio" for Claude Code, None for Cursor
    auto_approve_tools: bool = False  # Add alwaysAllow list (Claude Code)
    
    # Hooks support (Claude Code only)
    supports_hooks: bool = False
    hooks_path: Optional[Path] = None
    
    # User-facing messages
    restart_instruction: str = ""
    extra_setup_step: Optional[str] = None   # Additional step (Cursor: "Open Composer...")
    setup_tip: Optional[str] = None          # Tip shown after setup
    verify_tip: Optional[str] = None         # Tip shown after verify
    setup_cmd_hint: str = "meld setup"       # Command to run for setup


IDE_CONFIGS = {
    "claude": IDEConfig(
        name="Claude Code",
        config_path=Path.home() / ".claude.json",
        detection_dir=Path.home() / ".claude",
        mcp_type="stdio",
        auto_approve_tools=True,
        supports_hooks=True,
        hooks_path=Path.home() / ".claude" / "settings.json",
        restart_instruction="Restart Claude Code",
        setup_cmd_hint="meld setup",
    ),
    "cursor": IDEConfig(
        name="Cursor",
        config_path=Path.home() / ".cursor" / "mcp.json",
        detection_dir=Path.home() / ".cursor",
        mcp_type=None,
        auto_approve_tools=False,
        supports_hooks=False,
        hooks_path=None,
        restart_instruction="Quit and reopen Cursor",
        extra_setup_step="Open Composer in Agent mode ([cyan]Cmd+I → Agent[/cyan])",
        setup_tip="[dim]Tip: Enable auto-approval in Settings > Features > Auto-Run[/dim]",
        verify_tip="[dim]Tip: Enable Auto-Run in Cursor Settings > Features for automatic tool approval.[/dim]",
        setup_cmd_hint="meld setup --cursor",
    ),
}


# =============================================================================
# Helper Functions
# =============================================================================

def _read_json_config(path: Path, warn_on_error: bool = True) -> dict:
    """Read JSON config file, returning empty dict if not exists or invalid.
    
    Args:
        path: Path to JSON config file
        warn_on_error: If True, print warning when file exists but can't be parsed
    """
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        if warn_on_error:
            console.print(f"[yellow]⚠[/yellow] Failed to read {path}: {e}")
        return {}


def _write_json_config(path: Path, config: dict) -> None:
    """Write JSON config file, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config, indent=2))


def _has_meld_hook(hook_group: dict) -> bool:
    """Check if a hook group contains a meld_mcp hook."""
    return any(
        "meld_mcp" in h.get("command", "")
        for h in hook_group.get("hooks", [])
    )


def _setup_hooks(hooks_path: Path, python_path: str) -> None:
    """Configure Claude Code session hooks."""
    settings = _read_json_config(hooks_path)
    
    hooks = settings.get("hooks", {})
    existing_hooks = hooks.get("UserPromptSubmit", [])
    
    # Remove any existing meld_mcp hooks (to update the Python path)
    hooks["UserPromptSubmit"] = [
        hook for hook in existing_hooks
        if not _has_meld_hook(hook)
    ]
    
    # Add meld session hook with correct Python path
    hooks["UserPromptSubmit"].append({
        "hooks": [
            {
                "type": "command",
                "command": f"{python_path} -m meld_mcp.hooks",
                "timeout": 5,
            }
        ]
    })
    settings["hooks"] = hooks
    
    _write_json_config(hooks_path, settings)
    console.print(f"[green]✓[/green] Added session hook to {hooks_path}")


def _build_mcp_entry(config: IDEConfig, python_path: str) -> dict:
    """Build the MCP server entry for the config file."""
    entry = {
        "command": python_path,
        "args": ["-m", "meld_mcp"],
        "env": {"MELD_API_URL": get_api_url()},
    }
    
    if config.mcp_type:
        entry["type"] = config.mcp_type
    
    if config.auto_approve_tools:
        entry["alwaysAllow"] = MELD_TOOL_NAMES
    
    return entry


def _show_setup_success(config: IDEConfig) -> None:
    """Show the success panel after setup."""
    lines = [
        f"[bold green]✓ Meld configured for {config.name}![/bold green]",
        "",
        "[bold]Next:[/bold]",
        f"1. {config.restart_instruction}",
    ]
    
    step_num = 2
    if config.extra_setup_step:
        lines.append(f"{step_num}. {config.extra_setup_step}")
        step_num += 1
    
    lines.append(f'{step_num}. Try: [cyan]"What do you remember about me?"[/cyan]')
    
    if config.setup_tip:
        lines.append("")
        lines.append(config.setup_tip)
    
    console.print(Panel.fit("\n".join(lines)))


# =============================================================================
# Core Functions
# =============================================================================

def verify_meld_mcp_importable() -> bool:
    """Verify meld_mcp is importable from current Python."""
    python_path = sys.executable
    try:
        result = subprocess.run(
            [python_path, "-c", "import meld_mcp"],
            capture_output=True,
            timeout=10,
        )
        if result.returncode != 0:
            console.print("[red]✗[/red] meld_mcp not found in this Python installation")
            console.print(f"[dim]Python: {python_path}[/dim]")
            console.print("[yellow]Try: pip install meld-mcp[/yellow]")
            return False
        return True
    except subprocess.TimeoutExpired:
        console.print("[red]✗[/red] meld_mcp import check timed out")
        return False


def is_meld_configured(ide: str) -> bool:
    """Check if Meld is already configured for the specified IDE.
    
    Args:
        ide: "claude" or "cursor"
    
    Returns:
        True if Meld is configured in the IDE's MCP config
    """
    config = IDE_CONFIGS.get(ide)
    if not config:
        return False
    
    if not config.config_path.exists():
        return False
    
    try:
        mcp_config = json.loads(config.config_path.read_text())
        return MELD_SERVER_KEY in mcp_config.get("mcpServers", {})
    except Exception:
        return False


def setup_ide(ide: str) -> None:
    """Configure an IDE to use Meld.
    
    Args:
        ide: "claude" or "cursor"
    """
    config = IDE_CONFIGS.get(ide)
    if not config:
        console.print(f"[red]Unknown IDE: {ide}[/red]")
        return
    
    console.print(Panel.fit(f"[bold]Meld Setup for {config.name}[/bold]"))
    
    # 1. Check credentials
    creds = load_credentials()
    if not creds:
        console.print("[yellow]⚠[/yellow] Not logged in. Run [bold]meld login[/bold] first.")
        return
    
    # 2. Check IDE is installed
    if not config.detection_dir.exists():
        console.print(f"[yellow]⚠[/yellow] {config.name} not detected ({config.detection_dir} not found)")
        console.print(f"Make sure {config.name} is installed and has been run at least once.")
        return
    
    console.print(f"[green]✓[/green] Found {config.name} at {config.detection_dir}")
    
    # 3. Verify meld_mcp is importable
    if not verify_meld_mcp_importable():
        return
    
    python_path = sys.executable
    console.print(f"[dim]Using Python: {python_path}[/dim]")
    
    # 4. Read existing config and check if already configured
    mcp_config = _read_json_config(config.config_path)
    
    if "mcpServers" not in mcp_config:
        mcp_config["mcpServers"] = {}
    
    if MELD_SERVER_KEY in mcp_config.get("mcpServers", {}):
        console.print("[green]✓[/green] Meld MCP server already configured")
        if not click.confirm("Update configuration?", default=False):
            return
    
    # 5. Add/update Meld MCP server entry
    mcp_config["mcpServers"][MELD_SERVER_KEY] = _build_mcp_entry(config, python_path)
    _write_json_config(config.config_path, mcp_config)
    console.print(f"[green]✓[/green] Added Meld MCP server to {config.config_path}")
    
    # 6. Setup hooks if supported (Claude Code only)
    if config.supports_hooks and config.hooks_path:
        _setup_hooks(config.hooks_path, python_path)
    
    # 7. Show success
    _show_setup_success(config)


def verify_ide(ide: str) -> None:
    """Verify IDE setup is correct.
    
    Args:
        ide: "claude" or "cursor"
    """
    config = IDE_CONFIGS.get(ide)
    if not config:
        console.print(f"[red]Unknown IDE: {ide}[/red]")
        return
    
    console.print(Panel.fit(f"[bold]Meld Setup Verification ({config.name})[/bold]"))
    
    all_ok = True
    
    # 1. Check credentials
    creds = load_credentials()
    if creds and creds.get("access_token"):
        console.print("[green]✓[/green] Credentials: Found")
    else:
        console.print("[red]✗[/red] Credentials: Not found. Run [bold]meld login[/bold]")
        all_ok = False
    
    # 2. Check API connection
    if creds:
        api = MeldAPI()
        try:
            health = asyncio.run(api.health_check())
            if health.get("status") == "healthy":
                console.print("[green]✓[/green] API: Connected")
            else:
                console.print(f"[yellow]⚠[/yellow] API: Unexpected response - {health}")
        except Exception as e:
            console.print(f"[red]✗[/red] API: Connection failed - {e}")
            all_ok = False
    
    # 3. Check MCP server config
    if config.config_path.exists():
        mcp_config = _read_json_config(config.config_path)
        meld_config = mcp_config.get("mcpServers", {}).get(MELD_SERVER_KEY)
        if meld_config:
            cmd = meld_config.get("command", "")
            console.print("[green]✓[/green] MCP Server: Configured")
            console.print(f"[dim]    Command: {cmd}[/dim]")
            
            # Verify the Python path exists
            if not cmd or not Path(cmd).exists():
                console.print(f"[yellow]⚠[/yellow] Warning: Python path doesn't exist: {cmd}")
                console.print(f"    Run [bold]{config.setup_cmd_hint}[/bold] to reconfigure")
        else:
            console.print(f"[red]✗[/red] MCP Server: Not configured. Run [bold]{config.setup_cmd_hint}[/bold]")
            all_ok = False
    else:
        console.print(f"[red]✗[/red] MCP Server: {config.config_path} not found")
        console.print(f"    Run [bold]{config.setup_cmd_hint}[/bold] to configure")
        all_ok = False
    
    # 4. Check hooks if supported (Claude Code only)
    if config.supports_hooks and config.hooks_path:
        if config.hooks_path.exists():
            settings = _read_json_config(config.hooks_path)
            hooks = settings.get("hooks", {}).get("UserPromptSubmit", [])
            
            # Find meld hook using helper
            meld_hook_group = next((hg for hg in hooks if _has_meld_hook(hg)), None)
            
            if meld_hook_group:
                # Extract command for display
                meld_cmd = next(
                    (h.get("command", "") for h in meld_hook_group.get("hooks", [])
                     if "meld_mcp" in h.get("command", "")),
                    ""
                )
                console.print("[green]✓[/green] Session Hook: Configured")
                console.print(f"[dim]    Command: {meld_cmd[:60]}...[/dim]")
            else:
                console.print("[yellow]⚠[/yellow] Session Hook: Not configured")
                console.print(f"    This is optional but recommended. Run [bold]{config.setup_cmd_hint}[/bold] to add it.")
        else:
            console.print(f"[yellow]⚠[/yellow] Session Hook: {config.hooks_path} not found")
    
    # 5. Test MCP server startup
    console.print("\n[bold]Testing MCP server...[/bold]")
    python_path = sys.executable
    try:
        result = subprocess.run(
            [python_path, "-c", "from meld_mcp.server import main; print('OK')"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0 and "OK" in result.stdout:
            console.print("[green]✓[/green] MCP Server: Importable")
        else:
            console.print("[red]✗[/red] MCP Server: Failed to import")
            console.print(f"[dim]    {result.stderr[:200]}[/dim]")
            all_ok = False
    except subprocess.TimeoutExpired:
        console.print("[red]✗[/red] MCP Server: Timed out (>5s)")
        all_ok = False
    
    # 6. Summary
    console.print("")
    if all_ok:
        console.print("[bold green]All checks passed![/bold green]")
        console.print(f"{config.restart_instruction} to activate Meld.")
        if config.verify_tip:
            console.print(f"\n{config.verify_tip}")
    else:
        console.print("[bold yellow]Some issues found.[/bold yellow]")
        console.print(f"Fix the issues above and run [bold]meld verify{' --cursor' if ide == 'cursor' else ''}[/bold] again.")


# =============================================================================
# Backward-Compatible Public API
# =============================================================================

def setup_claude_code() -> None:
    """Configure Claude Code to use Meld."""
    setup_ide("claude")


def setup_cursor() -> None:
    """Configure Cursor IDE to use Meld."""
    setup_ide("cursor")


def verify_claude_code() -> None:
    """Verify Claude Code setup is correct."""
    verify_ide("claude")


def verify_cursor() -> None:
    """Verify Cursor setup is correct."""
    verify_ide("cursor")


# Legacy aliases (deprecated, kept for backward compatibility)
_verify_meld_mcp_importable = verify_meld_mcp_importable


def _is_meld_configured(cursor: bool) -> bool:
    """Legacy function - use is_meld_configured(ide) instead."""
    return is_meld_configured("cursor" if cursor else "claude")
