"""Meld CLI - Main entry point."""

import asyncio
import json
import webbrowser
from pathlib import Path

import click
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .api import MeldAPI, MeldAPIError
from .config import (
    clear_credentials,
    get_api_url,
    load_config,
    load_credentials,
    save_config,
    save_credentials,
)
from .ide import (
    _is_meld_configured,
    _verify_meld_mcp_importable,
    setup_claude_code,
    setup_cursor,
    verify_claude_code,
    verify_cursor,
)
from .indexer import IncrementalIndexer, SessionIndexer, get_cursor_db_path
from .sync import run_sync
from .version import check_for_update
from . import __version__

console = Console()


@click.group()
@click.version_option(version=__version__, package_name="meld-memory")
def cli():
    """Meld - Personal memory system for Claude Code."""
    pass


# ===========================================
# AUTH COMMANDS
# ===========================================


@cli.command()
def login():
    """Log in to Meld via browser."""
    console.print(Panel.fit("[bold]Meld Login[/bold]"))

    # Check if already logged in
    creds = load_credentials()
    if creds:
        console.print(f"[yellow]Already logged in as {creds.get('email', 'unknown')}[/yellow]")
        if not click.confirm("Log in again?", default=False):
            return

    # Open the sign-in page served by the API
    signin_url = f"{get_api_url()}/signin"

    console.print(f"\n[bold]Opening browser for sign-in...[/bold]")
    webbrowser.open(signin_url)

    console.print(f"Opened: {signin_url}\n")
    console.print("Sign in and copy the token shown on the page.")
    console.print("")

    token = click.prompt("Paste your Clerk session token")

    if not token:
        console.print("[red]No token provided[/red]")
        return

    # Exchange the short-lived Clerk token for a long-lived Meld token
    api = MeldAPI(token=token)

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Exchanging token...", total=None)
            result = asyncio.run(api.exchange_token())
            progress.remove_task(task)

        if "error" in result:
            console.print(f"[red]Error: {result.get('error')}[/red]")
            return

        # Save the long-lived Meld token
        save_credentials(
            token=result.get("access_token", ""),
            user_id=result.get("user_id", ""),
            email=result.get("email", ""),
        )

        expires_days = result.get("expires_in", 0) // 86400
        console.print(f"\n[green]✓[/green] Logged in as {result.get('email', 'user')}")
        console.print(f"[dim]Token valid for {expires_days} days[/dim]")

    except MeldAPIError as e:
        console.print(f"[red]Login failed: {e.message}[/red]")
    except httpx.ConnectError:
        console.print(f"[red]Cannot connect to Meld API[/red]")
        console.print(f"[dim]Check your internet connection and try again[/dim]")
    except httpx.TimeoutException:
        console.print(f"[red]Connection timed out[/red]")
        console.print(f"[dim]The server may be slow. Try again in a moment.[/dim]")
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        console.print(f"[dim]If this persists, try: meld doctor[/dim]")


@cli.command()
def logout():
    """Log out and clear credentials."""
    clear_credentials()
    console.print("[green]✓[/green] Logged out successfully")


@cli.command()
def whoami():
    """Show current user info."""
    creds = load_credentials()
    if not creds:
        console.print("Not logged in. Run [bold]meld login[/bold]")
        return

    console.print(f"Email: {creds.get('email')}")
    console.print(f"User ID: {creds.get('user_id')}")


# ===========================================
# STATUS COMMAND
# ===========================================


@cli.command()
def status():
    """Check Meld status, connection, and sync progress."""
    import os
    import time as time_module

    creds = load_credentials()

    console.print(Panel.fit("[bold]Meld Status[/bold]"))

    # Check credentials
    if creds:
        console.print(f"[green]✓[/green] Logged in as: {creds.get('email', 'unknown')}")
    else:
        console.print("[yellow]⚠[/yellow] Not logged in. Run [bold]meld login[/bold]")
        return

    # Check API connection
    api = MeldAPI()

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Checking API connection...", total=None)
            health = asyncio.run(api.health_check())
            progress.remove_task(task)

        if health.get("status") == "healthy":
            console.print(f"[green]✓[/green] API: Connected ({get_api_url()})")
        else:
            console.print(f"[yellow]⚠[/yellow] API: {health}")
    except Exception as e:
        console.print(f"[red]✗[/red] API: Connection failed - {e}")

    # ========== Sync Status ==========
    console.print()
    console.print("[bold]Session Sync:[/bold]")

    # Show auto-sync setting
    cfg = load_config()
    auto_sync = cfg.get("auto_sync", True)
    auto_sync_display = "[green]enabled[/green]" if auto_sync else "[dim]disabled[/dim]"
    default_note = " (default)" if "auto_sync" not in cfg else ""
    console.print(f"  Auto-sync: {auto_sync_display}{default_note}")

    indexer = SessionIndexer()
    inc_indexer = IncrementalIndexer(indexer)
    stats = inc_indexer.get_sync_stats()

    # Show Claude Code stats
    console.print(f"  Claude Code: {stats['files_synced']:,} files ({stats['chunks_synced'] - stats.get('cursor_chunks', 0):,} chunks)")

    # Show Cursor stats if available
    cursor_convs = stats.get('cursor_conversations', 0)
    cursor_chunks = stats.get('cursor_chunks', 0)
    if cursor_convs > 0:
        console.print(f"  Cursor: {cursor_convs:,} conversations ({cursor_chunks:,} chunks)")
    elif get_cursor_db_path():
        console.print(f"  Cursor: [dim]Not synced yet[/dim]")

    if stats['last_sync']:
        last_sync_ago = time_module.time() - stats['last_sync']
        if last_sync_ago < 60:
            ago_str = f"{int(last_sync_ago)}s ago"
        elif last_sync_ago < 3600:
            ago_str = f"{int(last_sync_ago / 60)}m ago"
        else:
            ago_str = f"{int(last_sync_ago / 3600)}h ago"
        console.print(f"  Last sync: {ago_str}")

    # Check for pending files
    pending = inc_indexer.find_new_or_modified_files()
    pending_cursor = inc_indexer.find_new_or_modified_cursor_conversations() if get_cursor_db_path() else []
    total_pending = len(pending) + len(pending_cursor)
    if total_pending:
        pending_details = []
        if pending:
            pending_details.append(f"{len(pending)} Claude Code")
        if pending_cursor:
            pending_details.append(f"{len(pending_cursor)} Cursor")
        console.print(f"  Pending: [yellow]{' + '.join(pending_details)}[/yellow]")
    else:
        console.print(f"  Pending: [green]None - up to date![/green]")

    # Check for failed files
    failed_count = stats.get('failed_files_count', 0)
    if failed_count > 0:
        console.print(f"  Failed: [red]{failed_count} files[/red]")
        if stats.get('last_error'):
            error_msg = stats['last_error'][:60] + "..." if len(stats.get('last_error', '')) > 60 else stats.get('last_error')
            console.print(f"    [dim]{error_msg}[/dim]")

    # Check for background process
    pid_file = Path.home() / ".meld" / "sync.pid"

    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            os.kill(pid, 0)  # Check if running
            console.print(f"  Background: [green]Running[/green] (PID: {pid})")
        except (ProcessLookupError, OSError, ValueError):
            pid_file.unlink(missing_ok=True)
            console.print(f"  Background: [dim]Not running[/dim]")
    else:
        console.print(f"  Background: [dim]Not running[/dim]")

    # ========== IDE Integrations ==========
    console.print()
    console.print("[bold]IDE Integrations:[/bold]")

    # Check Claude Code
    claude_mcp_file = Path.home() / ".claude.json"
    if claude_mcp_file.exists():
        try:
            config = json.loads(claude_mcp_file.read_text())
            if config.get("mcpServers", {}).get("meld"):
                console.print(f"  Claude Code: [green]Configured[/green]")
            else:
                console.print(f"  Claude Code: [yellow]Not configured[/yellow] (run [bold]meld setup[/bold])")
        except Exception:
            console.print(f"  Claude Code: [yellow]Config error[/yellow]")
    else:
        claude_dir = Path.home() / ".claude"
        if claude_dir.exists():
            console.print(f"  Claude Code: [yellow]Not configured[/yellow] (run [bold]meld setup[/bold])")
        else:
            console.print(f"  Claude Code: [dim]Not installed[/dim]")

    # Check Cursor
    cursor_mcp_file = Path.home() / ".cursor" / "mcp.json"
    cursor_dir = Path.home() / ".cursor"
    if cursor_mcp_file.exists():
        try:
            config = json.loads(cursor_mcp_file.read_text())
            if config.get("mcpServers", {}).get("meld"):
                console.print(f"  Cursor: [green]Configured[/green]")
            else:
                console.print(f"  Cursor: [yellow]Not configured[/yellow] (run [bold]meld setup --cursor[/bold])")
        except Exception:
            console.print(f"  Cursor: [yellow]Config error[/yellow]")
    elif cursor_dir.exists():
        console.print(f"  Cursor: [yellow]Not configured[/yellow] (run [bold]meld setup --cursor[/bold])")
    else:
        console.print(f"  Cursor: [dim]Not installed[/dim]")

    # ========== User State ==========
    try:
        state = asyncio.run(api.get_user_state())
        console.print(f"\n[bold]User State:[/bold] {state.get('state')}")
        console.print(f"  Projects: {state.get('content_counts', {}).get('projects', 0)}")
        console.print(f"  Memories: {state.get('content_counts', {}).get('memories', 0)}")

        checkin_info = state.get("checkin_info") or {}
        if checkin_info.get("suggested"):
            console.print(
                f"\n[yellow]ℹ[/yellow] Check-in suggested: {state.get('greeting')}"
            )
    except MeldAPIError as e:
        console.print(f"[red]✗[/red] Failed to get user state: {e.message}")

    # ========== Update Check ==========
    has_update, latest = check_for_update(__version__)
    if has_update:
        console.print(f"\n[yellow]Update available: {__version__} → {latest}[/yellow]")
        console.print("[dim]Run: pip install -U meld-memory[/dim]")


# ===========================================
# DOCTOR COMMAND
# ===========================================


@cli.command()
def doctor():
    """Diagnose Meld installation and configuration issues."""
    import sys
    import platform
    
    console.print(Panel.fit("[bold]Meld Doctor[/bold]"))
    console.print()
    
    all_ok = True
    
    # 1. Check Python version
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    py_min = "3.11"
    if sys.version_info >= (3, 11):
        console.print(f"[green]✓[/green] Python: {py_version} (>={py_min} required)")
    else:
        console.print(f"[red]✗[/red] Python: {py_version} (>={py_min} required)")
        console.print(f"  [dim]Upgrade Python or use pyenv/homebrew to install 3.11+[/dim]")
        all_ok = False
    
    # 2. Check meld-memory version
    try:
        from . import __version__ as meld_version
        console.print(f"[green]✓[/green] meld-memory: {meld_version}")
    except Exception as e:
        console.print(f"[red]✗[/red] meld-memory: import error - {e}")
        all_ok = False
    
    # 3. Check meld-mcp version
    try:
        from meld_mcp import __version__ as mcp_version
        console.print(f"[green]✓[/green] meld-mcp: {mcp_version}")
    except ImportError:
        console.print("[red]✗[/red] meld-mcp: not installed")
        console.print("  [dim]Run: pip install meld-mcp[/dim]")
        all_ok = False
    except Exception as e:
        console.print(f"[red]✗[/red] meld-mcp: import error - {e}")
        all_ok = False
    
    # 4. Check critical dependencies
    deps = ["packaging", "httpx", "click", "rich"]
    missing_deps = []
    for dep in deps:
        try:
            __import__(dep)
        except ImportError:
            missing_deps.append(dep)
    
    if not missing_deps:
        console.print(f"[green]✓[/green] Dependencies: all present")
    else:
        console.print(f"[red]✗[/red] Dependencies: missing {', '.join(missing_deps)}")
        console.print(f"  [dim]Run: pip install -U meld-memory[/dim]")
        all_ok = False
    
    # 5. Check credentials
    creds = load_credentials()
    if creds and creds.get("access_token"):
        email = creds.get("email") or creds.get("user_id", "unknown")
        console.print(f"[green]✓[/green] Credentials: logged in as {email}")
    else:
        console.print("[yellow]⚠[/yellow] Credentials: not logged in")
        console.print("  [dim]Run: meld login[/dim]")
    
    # 6. Check API connection
    if creds and creds.get("access_token"):
        api = MeldAPI()
        try:
            health = asyncio.run(api.health_check())
            if health.get("status") == "healthy":
                console.print(f"[green]✓[/green] API: healthy ({get_api_url()})")
            else:
                console.print(f"[yellow]⚠[/yellow] API: {health.get('status', 'unknown')}")
        except Exception as e:
            console.print(f"[red]✗[/red] API: connection failed")
            console.print(f"  [dim]Check your network connection[/dim]")
            all_ok = False
    else:
        console.print("[dim]-[/dim] API: skipped (not logged in)")
    
    # 7. Check Claude Code config
    claude_mcp_file = Path.home() / ".claude.json"
    if claude_mcp_file.exists():
        try:
            config = json.loads(claude_mcp_file.read_text())
            if config.get("mcpServers", {}).get("meld"):
                console.print("[green]✓[/green] Claude Code: configured")
            else:
                console.print("[yellow]⚠[/yellow] Claude Code: not configured")
                console.print("  [dim]Run: meld setup[/dim]")
        except Exception:
            console.print("[yellow]⚠[/yellow] Claude Code: config error")
    else:
        claude_dir = Path.home() / ".claude"
        if claude_dir.exists():
            console.print("[yellow]⚠[/yellow] Claude Code: not configured")
            console.print("  [dim]Run: meld setup[/dim]")
        else:
            console.print("[dim]-[/dim] Claude Code: not installed")
    
    # 8. Check Cursor config
    cursor_mcp_file = Path.home() / ".cursor" / "mcp.json"
    cursor_dir = Path.home() / ".cursor"
    if cursor_mcp_file.exists():
        try:
            config = json.loads(cursor_mcp_file.read_text())
            if config.get("mcpServers", {}).get("meld"):
                console.print("[green]✓[/green] Cursor: configured")
            else:
                console.print("[yellow]⚠[/yellow] Cursor: not configured")
                console.print("  [dim]Run: meld setup --cursor[/dim]")
        except Exception:
            console.print("[yellow]⚠[/yellow] Cursor: config error")
    elif cursor_dir.exists():
        console.print("[yellow]⚠[/yellow] Cursor: not configured")
        console.print("  [dim]Run: meld setup --cursor[/dim]")
    else:
        console.print("[dim]-[/dim] Cursor: not installed")
    
    # Summary
    console.print()
    if all_ok:
        console.print("[green]All checks passed![/green]")
    else:
        console.print("[yellow]Some issues found. See above for fixes.[/yellow]")


# ===========================================
# DATA VISIBILITY COMMAND
# ===========================================


@cli.command()
def data():
    """Show what data Meld has stored about you."""
    creds = load_credentials()
    if not creds:
        console.print("[yellow]⚠[/yellow] Not logged in. Run [bold]meld login[/bold]")
        return

    console.print(Panel.fit("[bold]Your Meld Data[/bold]"))
    console.print()

    api = MeldAPI()

    try:
        # Get profile
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Loading data...", total=None)
            profile = asyncio.run(api.get_profile())
            projects = asyncio.run(api.list_projects())
            memories = asyncio.run(api.list_memories(limit=50))
            session_stats = asyncio.run(api.get_session_stats())
            progress.remove_task(task)

        # Profile slots
        slots = profile.get("slots", {})
        if slots:
            console.print("[bold]Profile:[/bold]")
            for key, value in slots.items():
                console.print(f"  {key}: {value}")
        else:
            console.print("[bold]Profile:[/bold] [dim]No profile data yet[/dim]")
        console.print()

        # Projects
        if projects:
            active_count = sum(1 for p in projects if p.get("status") == "active")
            console.print(f"[bold]Projects:[/bold] {len(projects)} total ({active_count} active)")
            for p in projects[:5]:  # Show first 5
                status_color = "green" if p.get("status") == "active" else "dim"
                console.print(f"  [{status_color}]•[/{status_color}] {p.get('name')} ({p.get('status')})")
            if len(projects) > 5:
                console.print(f"  [dim]... and {len(projects) - 5} more[/dim]")
        else:
            console.print("[bold]Projects:[/bold] [dim]None[/dim]")
        console.print()

        # Memories
        if memories:
            console.print(f"[bold]Memories:[/bold] {len(memories)} stored")
            for m in memories[:3]:  # Show first 3
                title = m.get("title") or m.get("content", "")[:50]
                console.print(f"  • {title}")
            if len(memories) > 3:
                console.print(f"  [dim]... and {len(memories) - 3} more[/dim]")
        else:
            console.print("[bold]Memories:[/bold] [dim]None[/dim]")
        console.print()

        # Session stats
        total_chunks = session_stats.get("total_chunks", 0)
        if total_chunks > 0:
            console.print(f"[bold]Sessions:[/bold] {total_chunks:,} chunks indexed")
            by_source = session_stats.get("by_source", {})
            if by_source.get("claude_code"):
                console.print(f"  Claude Code: {by_source['claude_code']:,} chunks")
            if by_source.get("cursor"):
                console.print(f"  Cursor: {by_source['cursor']:,} chunks")
        else:
            console.print("[bold]Sessions:[/bold] [dim]Not synced yet[/dim]")
            console.print("  [dim]Run: meld sync[/dim]")
        console.print()

        # Local sync state
        indexer = SessionIndexer()
        inc_indexer = IncrementalIndexer(indexer)
        stats = inc_indexer.get_sync_stats()
        if stats.get("last_sync"):
            import time as time_module
            last_sync_ago = time_module.time() - stats["last_sync"]
            if last_sync_ago < 3600:
                ago_str = f"{int(last_sync_ago / 60)}m ago"
            else:
                ago_str = f"{int(last_sync_ago / 3600)}h ago"
            console.print(f"[dim]Last sync: {ago_str}[/dim]")

        console.print()
        console.print("[dim]To delete data: meld forget --help[/dim]")

    except MeldAPIError as e:
        if e.status_code == 401:
            console.print(f"[red]Session expired. Run: meld login[/red]")
        else:
            console.print(f"[red]Error: {e.message}[/red]")
    except httpx.ConnectError:
        console.print(f"[red]Cannot connect to Meld API[/red]")
        console.print(f"[dim]Check your internet connection[/dim]")
    except Exception as e:
        console.print(f"[red]Error loading data: {e}[/red]")
        console.print(f"[dim]Try: meld doctor[/dim]")


# ===========================================
# FORGET (DELETE DATA) COMMANDS
# ===========================================


@cli.group()
def forget():
    """Delete your Meld data.

    Examples:
        meld forget memory 123     # Delete a specific memory
        meld forget sessions       # Delete all synced sessions
        meld forget --all          # Delete everything
    """
    pass


@forget.command("memory")
@click.argument("memory_id", type=int)
def forget_memory(memory_id: int):
    """Delete a specific memory by ID."""
    creds = load_credentials()
    if not creds:
        console.print("[yellow]⚠[/yellow] Not logged in. Run [bold]meld login[/bold]")
        return

    if not click.confirm(f"Delete memory {memory_id}?", default=False):
        console.print("Cancelled.")
        return

    api = MeldAPI()

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Deleting...", total=None)
            result = asyncio.run(api.delete_memory(memory_id))
            progress.remove_task(task)

        console.print(f"[green]✓[/green] Memory {memory_id} deleted")

    except MeldAPIError as e:
        if e.status_code == 404:
            console.print(f"[red]Memory {memory_id} not found[/red]")
            console.print(f"[dim]Use 'meld data' to see your memories[/dim]")
        elif e.status_code == 401:
            console.print(f"[red]Session expired. Run: meld login[/red]")
        else:
            console.print(f"[red]Error: {e.message}[/red]")
    except httpx.ConnectError:
        console.print(f"[red]Cannot connect to Meld API[/red]")
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")


@forget.command("sessions")
def forget_sessions():
    """Delete all synced session history."""
    creds = load_credentials()
    if not creds:
        console.print("[yellow]⚠[/yellow] Not logged in. Run [bold]meld login[/bold]")
        return

    console.print("[yellow]This will delete ALL your synced session history.[/yellow]")
    console.print("This includes Claude Code and Cursor conversations.")
    console.print()

    if not click.confirm("Are you sure?", default=False):
        console.print("Cancelled.")
        return

    api = MeldAPI()

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Deleting sessions...", total=None)
            result = asyncio.run(api.delete_all_sessions())
            progress.remove_task(task)

        # Also clear local sync state
        import shutil
        session_dir = Path.home() / ".meld" / "sessions"
        if session_dir.exists():
            shutil.rmtree(session_dir)

        console.print("[green]✓[/green] All session history deleted")

    except MeldAPIError as e:
        if e.status_code == 401:
            console.print(f"[red]Session expired. Run: meld login[/red]")
        else:
            console.print(f"[red]Error: {e.message}[/red]")
    except httpx.ConnectError:
        console.print(f"[red]Cannot connect to Meld API[/red]")
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")


@forget.command("all")
def forget_all():
    """Delete ALL your Meld data (profile, projects, memories, sessions)."""
    creds = load_credentials()
    if not creds:
        console.print("[yellow]⚠[/yellow] Not logged in. Run [bold]meld login[/bold]")
        return

    console.print("[bold red]WARNING: This will delete ALL your Meld data![/bold red]")
    console.print()
    console.print("This includes:")
    console.print("  • Your profile (name, preferences)")
    console.print("  • All projects")
    console.print("  • All memories")
    console.print("  • All synced session history")
    console.print("  • Check-in history")
    console.print()
    console.print("[yellow]This action cannot be undone.[/yellow]")
    console.print()

    if not click.confirm("Type 'yes' to confirm deletion", default=False):
        console.print("Cancelled.")
        return

    api = MeldAPI()

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Deleting all data...", total=None)
            # Delete sessions first (Turbopuffer)
            try:
                asyncio.run(api.delete_all_sessions())
            except Exception:
                pass  # Continue even if this fails
            # Reset profile data (Postgres)
            result = asyncio.run(api.reset_user())
            progress.remove_task(task)

        # Clear local state
        import shutil
        session_dir = Path.home() / ".meld" / "sessions"
        if session_dir.exists():
            shutil.rmtree(session_dir)

        # Clear credentials
        clear_credentials()

        console.print()
        console.print("[green]✓[/green] All data deleted")
        console.print()
        console.print("Run [bold]meld login[/bold] to start fresh.")

    except MeldAPIError as e:
        if e.status_code == 401:
            console.print(f"[red]Session expired. Run: meld login[/red]")
        else:
            console.print(f"[red]Error: {e.message}[/red]")
    except httpx.ConnectError:
        console.print(f"[red]Cannot connect to Meld API[/red]")
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")


# ===========================================
# IDE SETUP COMMANDS
# ===========================================


@cli.command()
@click.option("--cursor", is_flag=True, help="Configure for Cursor IDE instead of Claude Code")
def setup(cursor: bool):
    """Configure Claude Code or Cursor to use Meld."""
    if cursor:
        setup_cursor()
    else:
        setup_claude_code()


@cli.command()
@click.option("--cursor", is_flag=True, help="Verify Cursor setup instead of Claude Code")
def verify(cursor: bool):
    """Verify Meld setup is correct before restarting your IDE."""
    if cursor:
        verify_cursor()
    else:
        verify_claude_code()


@cli.command()
@click.option("--cursor", is_flag=True, help="Configure for Cursor instead of Claude Code")
def quickstart(cursor: bool):
    """One-command setup: login + configure + sync.

    Examples:
        meld quickstart --cursor  # For Cursor users
        meld quickstart           # For Claude Code users
    """
    ctx = click.get_current_context()
    ide_name = "Cursor" if cursor else "Claude Code"
    console.print(Panel.fit(f"[bold]Meld Quickstart for {ide_name}[/bold]"))

    try:
        # Step 1: Login (if needed)
        creds = load_credentials()
        if not creds:
            console.print("\n[bold]Step 1: Login[/bold]")
            ctx.invoke(login)

            # Re-check after login attempt
            creds = load_credentials()
            if not creds:
                console.print("[red]Login failed. Run 'meld login' manually.[/red]")
                return
        else:
            console.print(f"\n[green]✓ Already logged in as {creds.get('email')}[/green]")

        # Step 2: Setup (skip if already configured to avoid confirmation prompt)
        console.print(f"\n[bold]Step 2: Configure {ide_name}[/bold]")
        if _is_meld_configured(cursor):
            console.print(f"[green]✓ {ide_name} already configured[/green]")
        else:
            if cursor:
                setup_cursor()
            else:
                setup_claude_code()

        # Verify configuration
        console.print("\n[dim]Verifying...[/dim]")
        if not _verify_meld_mcp_importable():
            console.print("[yellow]⚠ Verification failed. Run 'meld verify' for details.[/yellow]")
            # Continue anyway - might still work
        else:
            console.print("[green]✓ Verified[/green]")

        # Step 3: Sync (optional)
        if click.confirm("\nSync conversation history? (recent now, older in background)", default=True):
            console.print("\n[bold]Step 3: Sync[/bold]")
            source = "cursor" if cursor else "claude"
            ctx.invoke(sync, source=source)

        # Done
        console.print(Panel.fit(f"""
[bold green]✓ Ready![/bold green]

Quit and reopen {ide_name}, then try:
[cyan]"What do you remember about me?"[/cyan]
"""))

    except MeldAPIError as e:
        console.print(f"\n[red]Error: {e.message}[/red]")
        console.print("[dim]Check network and try again, or run commands individually.[/dim]")
    except Exception as e:
        console.print(f"\n[red]Unexpected error: {e}[/red]")
        console.print("[dim]Run 'meld login', 'meld setup', 'meld sync' individually to troubleshoot.[/dim]")


# ===========================================
# CONFIG COMMANDS
# ===========================================


def parse_config_value(val: str):
    """Parse a config value string into the appropriate Python type."""
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    try:
        return int(val)
    except ValueError:
        pass
    try:
        return float(val)
    except ValueError:
        pass
    return val


@cli.group()
def config():
    """Manage Meld configuration settings."""
    pass


@config.command("list")
def config_list():
    """List all configuration settings."""
    cfg = load_config()

    console.print(Panel.fit("[bold]Meld Configuration[/bold]"))

    # Show auto_sync with default
    auto_sync = cfg.get("auto_sync", True)
    auto_sync_display = "[green]enabled[/green]" if auto_sync else "[red]disabled[/red]"
    default_note = " [dim](default)[/dim]" if "auto_sync" not in cfg else ""
    console.print(f"  auto_sync: {auto_sync_display}{default_note}")

    # Show any other settings
    for key, value in cfg.items():
        if key != "auto_sync":
            console.print(f"  {key}: {value}")


@config.command("get")
@click.argument("key")
def config_get(key: str):
    """Get a configuration value."""
    cfg = load_config()

    # Handle known defaults
    defaults = {"auto_sync": True}

    if key in cfg:
        console.print(f"{key}: {cfg[key]}")
    elif key in defaults:
        console.print(f"{key}: {defaults[key]} [dim](default)[/dim]")
    else:
        console.print(f"[yellow]Unknown setting: {key}[/yellow]")


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str):
    """Set a configuration value."""
    # Known settings with their expected types
    known_settings = {"auto_sync": bool}

    parsed_value = parse_config_value(value)

    # Validate known settings
    if key in known_settings:
        expected_type = known_settings[key]
        if not isinstance(parsed_value, expected_type):
            console.print(f"[red]Error: {key} must be {expected_type.__name__} (true/false)[/red]")
            return

    save_config(key, parsed_value)
    console.print(f"[green]✓[/green] Set {key} = {parsed_value}")


# ===========================================
# SYNC COMMAND
# ===========================================


@cli.command()
@click.option("--full", is_flag=True, help="Force full re-sync (ignore previous state)")
@click.option("--dry-run", is_flag=True, help="Show what would be synced without uploading")
@click.option("--all", "sync_all", is_flag=True, help="Sync everything in foreground (no auto-background)")
@click.option("--background", is_flag=True, help="Run entirely in background")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed logging output")
@click.option("--source", type=click.Choice(["all", "claude", "cursor"]), default="all",
              help="Which source to sync: all (default), claude, or cursor")
def sync(full: bool, dry_run: bool, sync_all: bool, background: bool, verbose: bool, source: str):
    """Sync session history to Meld cloud.

    Syncs conversations from Claude Code and/or Cursor to enable cross-tool
    session search with meld_search_sessions.

    \b
    Sources:
    • Claude Code: ~/.claude/projects/**/*.jsonl
    • Cursor: composerData conversations from state.vscdb

    Smart sync: quickly syncs recent sessions (last 7 days) in foreground,
    then automatically continues with older sessions in background.

    \b
    Features:
    • Quick start - recent sessions ready in ~1 minute
    • Auto-background - older sessions sync while you work
    • True resume - Ctrl+C anytime, progress saved per-file
    • Cross-tool search - find context from any tool

    \b
    Examples:
        meld sync                 # Smart: recent fast, rest in background
        meld sync --source cursor # Sync only Cursor conversations
        meld sync --all           # Sync everything in foreground
        meld sync --full          # Force complete re-sync
        meld sync -v              # Show detailed logging
        meld status               # Check background sync progress
    """
    run_sync(full, dry_run, sync_all, background, verbose, source)


# ===========================================
# OTHER COMMANDS
# ===========================================


@cli.command()
def reset():
    """Reset all your Meld data (for testing fresh user experience)."""
    creds = load_credentials()
    if not creds:
        console.print("[yellow]⚠[/yellow] Not logged in. Run [bold]meld login[/bold] first.")
        return

    console.print("[yellow]⚠ This will delete ALL your Meld data:[/yellow]")
    console.print("  - Profile slots (name, etc.)")
    console.print("  - Projects")
    console.print("  - Memories")
    console.print("  - Check-in history")
    console.print("")

    if not click.confirm("Are you sure you want to reset?", default=False):
        console.print("Cancelled.")
        return

    api = MeldAPI()

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Resetting data...", total=None)
            result = asyncio.run(api.reset_user())
            progress.remove_task(task)

        if result.get("reset"):
            # Clear local session markers
            import shutil
            session_dir = Path.home() / ".meld" / "sessions"
            if session_dir.exists():
                shutil.rmtree(session_dir)

            # Clear local credentials (full reset)
            clear_credentials()

            console.print("\n[green]✓[/green] All data cleared!")
            console.print("Run [bold]meld login[/bold] to start fresh.")
        else:
            console.print(f"[red]Error: {result}[/red]")

    except MeldAPIError as e:
        if e.status_code == 401:
            console.print(f"[red]Session expired. Run: meld login[/red]")
        else:
            console.print(f"[red]Reset failed: {e.message}[/red]")
    except httpx.ConnectError:
        console.print(f"[red]Cannot connect to Meld API[/red]")
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")


@cli.command()
@click.argument("query")
@click.option("--limit", "-n", default=5, help="Number of results")
@click.option("--project", "-p", default=None, help="Filter by project")
def recall(query: str, limit: int, project: str):
    """Search your session history.

    Semantic search across all your synced Claude Code and Cursor conversations.
    """
    creds = load_credentials()
    if not creds:
        console.print("[yellow]⚠[/yellow] Not logged in. Run [bold]meld login[/bold] first.")
        return

    api = MeldAPI()

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Searching...", total=None)
            result = asyncio.run(api.search_sessions(query, limit, project))
            progress.remove_task(task)

        results = result.get("results", [])
        if not results:
            console.print("[yellow]No matching sessions found[/yellow]")
            console.print("[dim]Try running 'meld sync' to index your sessions first[/dim]")
            return

        console.print(f"\n[bold]Found {len(results)} results:[/bold]\n")

        for i, r in enumerate(results, 1):
            score_pct = int(r.get("score", 0) * 100)
            console.print(f"[bold]{i}.[/bold] [{score_pct}%] [dim]{r.get('project', 'unknown')}[/dim]")
            # Show snippet
            text = r.get("text", "")[:200]
            console.print(f"   {text}...")
            console.print()

    except MeldAPIError as e:
        if e.status_code == 401:
            console.print(f"[red]Session expired. Run: meld login[/red]")
        else:
            console.print(f"[red]Search failed: {e.message}[/red]")
    except httpx.ConnectError:
        console.print(f"[red]Cannot connect to Meld API[/red]")
        console.print(f"[dim]Check your internet connection[/dim]")
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")


if __name__ == "__main__":
    cli()
