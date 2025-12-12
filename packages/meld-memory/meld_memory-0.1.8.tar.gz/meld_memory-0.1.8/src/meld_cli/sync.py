"""Sync command logic for Meld CLI."""

import asyncio
import logging
import signal
import subprocess
import sys
import time as time_module
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)

from .api import MeldAPI, MeldAPIError
from .config import load_credentials
from .indexer import IncrementalIndexer, SessionIndexer, get_cursor_db_path

console = Console()


def get_sync_logger(verbose: bool = False) -> logging.Logger:
    """Get logger for sync operations. Logs to ~/.meld/sync.log and optionally console."""
    logger = logging.getLogger("meld.sync")
    logger.setLevel(logging.DEBUG)

    # Clear any existing handlers
    logger.handlers = []

    # File handler - always log to file
    log_dir = Path.home() / ".meld"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "sync.log"

    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler - only if verbose
    if verbose:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger


def spawn_background_sync(full_flag: bool = False, source_flag: str = "all") -> tuple[int, Path]:
    """Spawn a background sync process."""
    log_dir = Path.home() / ".meld"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "sync.log"
    pid_file = log_dir / "sync.pid"

    cmd = [sys.executable, "-m", "meld_cli.main", "sync", "--all", f"--source={source_flag}"]
    if full_flag:
        cmd.append("--full")

    with open(log_file, "a") as f:
        f.write(f"\n{'=' * 50}\n")
        f.write(f"Background sync started at {time_module.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")

    with open(log_file, "a") as log:
        proc = subprocess.Popen(
            cmd,
            stdout=log,
            stderr=log,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )

    # Save PID for status checking
    pid_file.write_text(str(proc.pid))
    return proc.pid, log_file


def run_sync(
    full: bool,
    dry_run: bool,
    sync_all: bool,
    background: bool,
    verbose: bool,
    source: str,
) -> None:
    """Run the sync command.

    Args:
        full: Force full re-sync (ignore previous state)
        dry_run: Show what would be synced without uploading
        sync_all: Sync everything in foreground (no auto-background)
        background: Run entirely in background
        verbose: Show detailed logging output
        source: Which source to sync: all, claude, or cursor
    """
    QUICK_SYNC_DAYS = 7  # Phase 1: sync this many days in foreground

    # Initialize logger
    log = get_sync_logger(verbose=verbose)
    log.info("=" * 50)
    log.info(f"SYNC START full={full} dry_run={dry_run} sync_all={sync_all} background={background} source={source}")

    creds = load_credentials()
    if not creds:
        console.print("[yellow]⚠[/yellow] Not logged in. Run [bold]meld login[/bold] first.")
        log.warning("Not logged in - aborting")
        return

    # Background-only mode
    if background:
        console.print(Panel.fit("[bold cyan]Meld Session Sync[/bold cyan]"))
        console.print()
        pid, log_file = spawn_background_sync(full, source)
        console.print(f"[green]✓[/green] Sync started in background (PID: {pid})")
        console.print()
        console.print(f"  [dim]Check progress:[/dim] [bold]meld status[/bold]")
        console.print(f"  [dim]View logs:[/dim]      [bold]tail -f {log_file}[/bold]")
        console.print()
        console.print("[dim]You can close this terminal - sync will continue.[/dim]")
        return

    console.print(Panel.fit("[bold cyan]Meld Session Sync[/bold cyan]"))
    console.print()

    # Handle Ctrl+C gracefully
    interrupted = False

    def handle_interrupt(sig, frame):
        nonlocal interrupted
        interrupted = True
        log.warning("Sync interrupted by user (Ctrl+C)")
        console.print("\n\n[yellow]⚠ Stopping after current file... (progress is saved)[/yellow]")

    original_handler = signal.signal(signal.SIGINT, handle_interrupt)

    try:
        # Initialize indexer
        indexer = SessionIndexer()
        inc_indexer = IncrementalIndexer(indexer)

        # Check source availability
        sync_claude = source in ("all", "claude")
        sync_cursor = source in ("all", "cursor")

        cursor_available = get_cursor_db_path() is not None
        if sync_cursor and not cursor_available:
            if source == "cursor":
                console.print("[yellow]⚠[/yellow] Cursor database not found")
                console.print("[dim]Make sure Cursor has been used at least once[/dim]")
                return
            else:
                console.print("[dim]Cursor not found, syncing Claude Code only[/dim]")
                sync_cursor = False

        # Show current sync state
        sync_stats = inc_indexer.get_sync_stats()
        log.info(f"Previous state: files_synced={sync_stats['files_synced']} chunks_synced={sync_stats['chunks_synced']}")
        if sync_stats["files_synced"] > 0 and not full:
            console.print(f"[dim]Previously synced: {sync_stats['files_synced']:,} files ({sync_stats['chunks_synced']:,} chunks)[/dim]")
        if sync_stats.get("cursor_conversations", 0) > 0 and not full:
            console.print(f"[dim]Cursor: {sync_stats['cursor_conversations']:,} conversations ({sync_stats['cursor_chunks']:,} chunks)[/dim]")

        if full:
            console.print("[yellow]⚠ Full sync requested - clearing saved state[/yellow]\n")
            log.info("Full sync - resetting state")
            inc_indexer.reset_state()

        # Find sessions to process from each source
        claude_files = []
        cursor_conversations = []

        if sync_claude:
            console.print("[dim]Scanning ~/.claude for sessions...[/dim]")
            claude_files = inc_indexer.find_new_or_modified_files()
            log.info(f"Found {len(claude_files)} Claude Code files to process")

        if sync_cursor and cursor_available:
            console.print("[dim]Scanning Cursor conversations...[/dim]")
            cursor_conversations = inc_indexer.find_new_or_modified_cursor_conversations()
            log.info(f"Found {len(cursor_conversations)} Cursor conversations to process")
            # Track skipped bubble-only conversations
            skipped_cursor = inc_indexer.get_cursor_skipped_count()
            if skipped_cursor > 0:
                log.info(f"Skipped {skipped_cursor} bubble-only Cursor conversations (Phase 2)")

        total_to_sync = len(claude_files) + len(cursor_conversations)

        if total_to_sync == 0:
            console.print("\n[green]✓ Already up to date![/green] No new sessions to sync.")
            console.print("[dim]Tip: Use --full to force a complete re-sync[/dim]")
            log.info("Already up to date - nothing to sync")
            return

        # Split Claude Code files into recent and older for smart sync
        recent_files = inc_indexer.find_new_or_modified_files(max_age_days=QUICK_SYNC_DAYS) if sync_claude else []
        older_file_count = len(claude_files) - len(recent_files)
        log.info(f"Claude Code split: recent={len(recent_files)} older={older_file_count}")

        # Decide sync strategy
        # For Cursor, we always sync all in foreground (no file age)
        if sync_all or older_file_count == 0:
            files_to_process = claude_files
            will_background = False
        else:
            files_to_process = recent_files
            will_background = older_file_count > 0

        # Display what we're syncing
        if sync_claude and sync_cursor:
            console.print(f"\n[bold]Sources:[/bold]")
            if files_to_process:
                if will_background:
                    console.print(f"  • Claude Code: {len(files_to_process)} recent + {older_file_count} older (background)")
                else:
                    console.print(f"  • Claude Code: {len(files_to_process)} sessions")
            if cursor_conversations:
                console.print(f"  • Cursor: {len(cursor_conversations)} conversations")
        elif sync_claude:
            if will_background:
                console.print(f"\n[bold]⚡ Quick sync:[/bold] {len(files_to_process)} sessions from last {QUICK_SYNC_DAYS} days")
                console.print(f"[dim]   + {older_file_count} older sessions will sync in background[/dim]")
            else:
                console.print(f"\nFound [bold]{len(files_to_process)}[/bold] Claude Code sessions to sync")
        elif sync_cursor:
            console.print(f"\nFound [bold]{len(cursor_conversations)}[/bold] Cursor conversations to sync")

        if dry_run:
            console.print("\n[dim]Dry run - sessions that would be processed:[/dim]\n")
            if files_to_process:
                console.print("  [bold]Claude Code:[/bold]")
                for file_path, is_incremental in files_to_process[:5]:
                    status = "[yellow]updated[/yellow]" if is_incremental else "[green]new[/green]"
                    console.print(f"    {status} {file_path.name}")
                if len(files_to_process) > 5:
                    console.print(f"    [dim]... and {len(files_to_process) - 5} more[/dim]")
            if cursor_conversations:
                console.print("  [bold]Cursor:[/bold]")
                for conv in cursor_conversations[:5]:
                    console.print(f"    [green]new[/green] {conv.id[:8]}... ({conv.message_count} msgs)")
                if len(cursor_conversations) > 5:
                    console.print(f"    [dim]... and {len(cursor_conversations) - 5} more[/dim]")
            if will_background:
                console.print(f"\n  [dim]Background phase: {older_file_count} older Claude Code files[/dim]")
            console.print("\n[dim]Run without --dry-run to sync[/dim]")
            return

        if not files_to_process and not cursor_conversations:
            # Nothing recent, but older files exist
            console.print("\n[dim]No recent sessions - starting background sync of older files...[/dim]")
            pid, _ = spawn_background_sync(full, source)
            console.print(f"\n[green]✓[/green] Background sync started (PID: {pid})")
            console.print("[dim]Check progress:[/dim] [bold]meld status[/bold]")
            return

        # ========== PHASE 1: Sync in foreground ==========
        console.print()
        start_time = time_module.time()
        api = MeldAPI()

        # Stats
        claude_files_synced = 0
        cursor_convs_synced = 0
        total_chunks = 0
        total_errors = 0
        parse_errors = 0
        incremental_count = 0

        # Batch size for API calls - stay well under server's 500 limit
        BATCH_SIZE = 100
        pending_chunks = []
        pending_items = []  # (item, chunk_count, is_incremental, is_cursor)

        last_error = None

        def flush_batch():
            """Upload pending chunks in batches, mark items synced only if all succeed."""
            nonlocal pending_chunks, pending_items, total_chunks, total_errors, claude_files_synced, cursor_convs_synced, incremental_count, last_error
            if not pending_chunks:
                return True

            # Split into smaller batches to stay under API limit
            all_succeeded = True
            chunks_uploaded = 0
            num_batches = (len(pending_chunks) + BATCH_SIZE - 1) // BATCH_SIZE

            log.debug(f"flush_batch: {len(pending_chunks)} chunks in {num_batches} batches for {len(pending_items)} items")

            for i in range(0, len(pending_chunks), BATCH_SIZE):
                batch = pending_chunks[i:i + BATCH_SIZE]
                batch_num = i // BATCH_SIZE + 1
                
                # Retry logic with exponential backoff
                max_retries = 3
                retry_delay = 1.0  # Start with 1 second
                
                for attempt in range(max_retries):
                    batch_start = time_module.time()
                    try:
                        result = asyncio.run(api.ingest_sessions(batch))
                        ingested = result.get("ingested", 0)
                        chunks_uploaded += ingested
                        batch_duration = time_module.time() - batch_start
                        log.debug(f"  batch {batch_num}/{num_batches}: {len(batch)} chunks -> {ingested} ingested ({batch_duration:.2f}s)")
                        break  # Success, exit retry loop
                    except MeldAPIError as e:
                        # Retry on server errors (5xx) and rate limiting (429)
                        if (e.status_code >= 500 or e.status_code == 429) and attempt < max_retries - 1:
                            wait_time = retry_delay
                            if e.status_code == 429:
                                # Rate limited - wait longer
                                wait_time = max(retry_delay, 5.0)
                                log.warning(f"  batch {batch_num}/{num_batches} rate limited, waiting {wait_time}s...")
                            else:
                                log.warning(f"  batch {batch_num}/{num_batches} attempt {attempt + 1} failed (server error), retrying in {wait_time}s...")
                            time_module.sleep(wait_time)
                            retry_delay *= 2  # Exponential backoff
                            continue
                        last_error = f"API error: {e.message}"
                        log.error(f"  batch {batch_num}/{num_batches} FAILED: {e.message}")
                        total_errors += len(batch)
                        all_succeeded = False
                        break
                    except Exception as e:
                        error_str = str(e)
                        # Retry on connection/timeout errors
                        if attempt < max_retries - 1 and ("connect" in error_str.lower() or "timeout" in error_str.lower()):
                            log.warning(f"  batch {batch_num}/{num_batches} attempt {attempt + 1} failed ({error_str}), retrying in {retry_delay}s...")
                            time_module.sleep(retry_delay)
                            retry_delay *= 2
                            continue
                        last_error = f"Error: {error_str}"
                        log.error(f"  batch {batch_num}/{num_batches} FAILED: {error_str}")
                        total_errors += len(batch)
                        all_succeeded = False
                        break
                else:
                    # All retries exhausted
                    pass
                
                if not all_succeeded:
                    break  # Stop on persistent error

            total_chunks += chunks_uploaded

            # Only mark items as synced if ALL batches succeeded
            if all_succeeded:
                for item, item_chunks, is_inc, is_cursor in pending_items:
                    if is_cursor:
                        inc_indexer.mark_cursor_conversation_synced(item, item_chunks)
                        cursor_convs_synced += 1
                        log.debug(f"  marked synced: cursor:{item.id[:8]}... ({item_chunks} chunks)")
                    else:
                        inc_indexer.mark_file_synced(item, item_chunks)
                        inc_indexer.clear_file_failure(item)
                        claude_files_synced += 1
                        log.debug(f"  marked synced: {item.name} ({item_chunks} chunks)")
                        if is_inc:
                            incremental_count += 1
            else:
                log.warning(f"  batch failed - NOT marking {len(pending_items)} items as synced")
                # Track failed files for retry (Claude Code only)
                for item, item_chunks, is_inc, is_cursor in pending_items:
                    if not is_cursor:
                        inc_indexer.mark_file_failed(item, last_error or "Unknown error")

            pending_chunks = []
            pending_items = []
            return all_succeeded

        phase_label = "⚡ Quick sync" if will_background else "Syncing"
        total_items = len(files_to_process) + len(cursor_conversations)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=30),
            TaskProgressColumn(),
            TextColumn("•"),
            TimeRemainingColumn(),
            console=console,
            transient=False,
        ) as progress:
            task = progress.add_task(
                f"[cyan]{phase_label}[/cyan]",
                total=total_items
            )

            # Process Claude Code files
            for file_path, is_incremental in files_to_process:
                if interrupted:
                    break

                file_start = time_module.time()
                chunks, file_stats = inc_indexer.process_file(file_path)
                parse_errors += file_stats.get("parse_errors", 0)

                if chunks:
                    pending_chunks.extend(chunks)
                    pending_items.append((file_path, len(chunks), is_incremental, False))
                    log.debug(f"processed: {file_path.name} -> {len(chunks)} chunks (pending={len(pending_chunks)}) [{time_module.time() - file_start:.2f}s]")
                    if len(pending_chunks) >= BATCH_SIZE:
                        flush_batch()

                progress.update(task, advance=1)

            # Process Cursor conversations
            for conv in cursor_conversations:
                if interrupted:
                    break

                conv_start = time_module.time()
                chunks, conv_stats = inc_indexer.process_cursor_conversation(conv)

                if chunks:
                    pending_chunks.extend(chunks)
                    pending_items.append((conv, len(chunks), False, True))
                    log.debug(f"processed: cursor:{conv.id[:8]}... -> {len(chunks)} chunks (pending={len(pending_chunks)}) [{time_module.time() - conv_start:.2f}s]")
                    if len(pending_chunks) >= BATCH_SIZE:
                        flush_batch()

                progress.update(task, advance=1)

            if not interrupted and pending_chunks:
                flush_batch()

        elapsed = time_module.time() - start_time
        total_synced = claude_files_synced + cursor_convs_synced
        log.info(f"SYNC COMPLETE: claude={claude_files_synced} cursor={cursor_convs_synced} chunks={total_chunks} errors={total_errors} duration={elapsed:.1f}s")

        # ========== Results ==========
        if interrupted:
            log.info(f"Interrupted: claude={claude_files_synced} cursor={cursor_convs_synced}")
            console.print(f"\n[yellow]⚠ Sync interrupted[/yellow]")
            console.print(f"\n  [green]Synced:[/green] {total_synced:,} sessions ({total_chunks:,} chunks)")
            console.print()
            console.print("[dim]Progress saved! Run 'meld sync' to continue.[/dim]")
            return

        # Success!
        console.print(f"\n[bold green]✓ Sync complete![/bold green] [dim]({elapsed:.1f}s)[/dim]")

        # Show breakdown by source
        if claude_files_synced > 0 and cursor_convs_synced > 0:
            console.print(f"  Claude Code: {claude_files_synced:,} sessions")
            console.print(f"  Cursor: {cursor_convs_synced:,} conversations")
        elif claude_files_synced > 0:
            console.print(f"  {claude_files_synced:,} Claude Code sessions ({total_chunks:,} chunks)")
        elif cursor_convs_synced > 0:
            console.print(f"  {cursor_convs_synced:,} Cursor conversations ({total_chunks:,} chunks)")

        if total_errors:
            log.warning(f"Completed with errors: {total_errors} chunks failed. Last error: {last_error}")
            console.print(f"  [yellow]({total_errors} chunks failed)[/yellow]")
            if last_error:
                console.print(f"  [dim]Last error: {last_error}[/dim]")

        # Show skipped bubble-only conversations (Phase 2 deferral)
        skipped_cursor = inc_indexer.get_cursor_skipped_count()
        if skipped_cursor > 0:
            console.print(f"\n[dim]Skipped {skipped_cursor} older Cursor conversations (ordering unavailable)[/dim]")

        console.print()
        console.print("[dim]Search now:[/dim] [bold]meld recall \"your query\"[/bold]")

        # ========== PHASE 2: Background the rest ==========
        if will_background and not interrupted:
            console.print()
            pid, log_file = spawn_background_sync(source_flag=source)
            console.print(f"[dim]📦 Syncing {older_file_count} older sessions in background (PID: {pid})[/dim]")
            console.print(f"[dim]   Check progress:[/dim] [bold]meld status[/bold]")

    finally:
        # Clean up resources
        inc_indexer.close()
        signal.signal(signal.SIGINT, original_handler)
