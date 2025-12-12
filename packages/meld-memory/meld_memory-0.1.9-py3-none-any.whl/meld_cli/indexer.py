"""
Session log indexer for Meld.

Supports multiple sources:
- Claude Code: JSONL chat logs from ~/.claude/projects/
- Cursor: SQLite conversations from state.vscdb

Chunks conversations into turn-windows and prepares data for cloud sync.
"""

import glob
import hashlib
import json
import logging
import os
import sqlite3
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple

from .entities import extract_entities
from .scrubber import SecretScrubber

# Logger for indexer operations
logger = logging.getLogger("meld.indexer")


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class SessionInfo:
    """Metadata about a session to be indexed."""
    id: str
    source: str  # "claude_code" or "cursor"
    file_path: Optional[Path] = None  # For Claude Code (file-based)
    created_at: Optional[float] = None  # Unix timestamp
    message_count: int = 0
    storage_type: str = "file"  # "file" (Claude Code), "composer", or "bubble"


# =============================================================================
# Base Indexer
# =============================================================================

class BaseIndexer(ABC):
    """Abstract base class for session indexers."""

    def __init__(
        self,
        window_size: int = 6,
        stride: int = 3,
    ):
        self.window_size = window_size
        self.stride = stride
        self.scrubber = SecretScrubber()

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Return the source identifier (e.g., 'claude_code', 'cursor')."""
        pass

    @abstractmethod
    def find_sessions(self) -> List[SessionInfo]:
        """Find all sessions available to index."""
        pass

    @abstractmethod
    def get_session_messages(self, session: SessionInfo) -> List[Dict]:
        """Get messages for a session, in order."""
        pass

    @abstractmethod
    def extract_project(self, session: SessionInfo, messages: List[Dict]) -> str:
        """Extract project name from session context."""
        pass

    def chunk_turns(self, turns: List[Dict]) -> Iterator[Tuple[List[Dict], int]]:
        """Chunk conversation turns using sliding window."""
        if len(turns) < self.window_size:
            if turns:
                yield (turns, 0)
            return

        chunk_idx = 0
        for i in range(0, len(turns), self.stride):
            chunk = turns[i : i + self.window_size]
            if len(chunk) > 0:
                yield (chunk, chunk_idx)
                chunk_idx += 1
            if i + self.window_size >= len(turns):
                break

    def format_chunk_text(self, turns: List[Dict]) -> str:
        """Format chunk turns into text for embedding."""
        lines = []
        for turn in turns:
            role = turn.get("role", "unknown")
            text = turn.get("text", "")
            lines.append(f"{role}: {text}")
        return "\n\n".join(lines)

    def content_hash(self, text: str) -> str:
        """Generate SHA-256 hash for deduplication."""
        return hashlib.sha256(text.encode()).hexdigest()[:16]

    def process_session(self, session: SessionInfo) -> Tuple[List[Dict], Dict]:
        """Process a session into chunks ready for upload."""
        messages = self.get_session_messages(session)
        if not messages:
            return [], {"parse_errors": 0, "secrets_found": 0}

        project = self.extract_project(session, messages)

        # Convert messages to turn format and scrub secrets
        # Strip _raw field after project extraction to free memory
        scrubbed_turns = []
        total_secrets = 0
        secrets_per_turn = []

        for msg in messages:
            turn = {"role": msg.get("role", "unknown"), "text": msg.get("text", "")}
            scrubbed_turn, findings = self.scrubber.scrub_dict(turn)
            scrubbed_turns.append(scrubbed_turn)
            secrets_per_turn.append(len(findings))
            total_secrets += len(findings)
            # Clear _raw to free memory (used only for project extraction)
            msg.pop("_raw", None)

        # Chunk turns
        chunks = list(self.chunk_turns(scrubbed_turns))

        # Prepare chunk data
        chunk_data = []
        turn_idx = 0
        for chunk_turns, chunk_idx in chunks:
            text = self.format_chunk_text(chunk_turns)
            content_id = self.content_hash(text)

            # Extract entities for field-weighted BM25
            entities = extract_entities(text)

            # Generate unique chunk ID
            chunk_id = f"{session.id}_chunk{chunk_idx}_{content_id}"

            # Calculate secrets in this chunk's turns
            chunk_secrets = sum(
                secrets_per_turn[turn_idx + i]
                for i in range(len(chunk_turns))
                if turn_idx + i < len(secrets_per_turn)
            )

            # file_path: actual path for Claude Code, synthetic for Cursor
            file_path = str(session.file_path) if session.file_path else f"cursor://conversations/{session.id}"

            chunk_data.append({
                "chunk_id": chunk_id,
                "text": text,
                "chunk_index": chunk_idx,
                "content_hash": content_id,
                "turn_count": len(chunk_turns),
                "secrets_scrubbed": chunk_secrets > 0,
                "project": project,
                "session_id": session.id,
                "source": self.source_name,
                "file_path": file_path,
                **entities,
            })
            turn_idx += self.stride

        stats = {"parse_errors": 0, "secrets_found": total_secrets}
        return chunk_data, stats


# =============================================================================
# Claude Code Indexer
# =============================================================================

class ClaudeCodeIndexer(BaseIndexer):
    """Indexes Claude Code session logs (JSONL files)."""

    source_name = "claude_code"

    def __init__(
        self,
        claude_dir: str = "~/.claude",
        window_size: int = 6,
        stride: int = 3,
    ):
        super().__init__(window_size, stride)
        self.claude_dir = Path(claude_dir).expanduser()

    def find_sessions(self) -> List[SessionInfo]:
        """Find all Claude Code session JSONL files."""
        pattern = str(self.claude_dir / "projects" / "**" / "*.jsonl")
        files = glob.glob(pattern, recursive=True)
        
        sessions = []
        for f in files:
            if f.endswith(".jsonl"):
                path = Path(f)
                sessions.append(SessionInfo(
                    id=path.stem,  # UUID filename
                    source=self.source_name,
                    file_path=path,
                ))
        return sessions

    def get_session_messages(self, session: SessionInfo) -> List[Dict]:
        """Parse JSONL file and extract messages."""
        if not session.file_path:
            return []

        messages = []
        try:
            with open(session.file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                        # Extract from nested message field (Claude Code format)
                        if "message" in record and isinstance(record["message"], dict):
                            msg = record["message"]
                            role = msg.get("role", "unknown")
                            content = msg.get("content", "")
                        else:
                            role = record.get("role", "unknown")
                            content = record.get("content", "")

                        # Handle content formats
                        if isinstance(content, list):
                            text_parts = []
                            for block in content:
                                if isinstance(block, dict) and block.get("type") == "text":
                                    text_parts.append(block.get("text", ""))
                            content = "\n".join(text_parts)
                        elif not isinstance(content, str):
                            content = str(content)

                        messages.append({"role": role, "text": content})
                    except json.JSONDecodeError:
                        continue
        except Exception:
            pass

        return messages

    def extract_project(self, session: SessionInfo, messages: List[Dict]) -> str:
        """Extract project name from file path."""
        if session.file_path:
            parts = session.file_path.parts
            if len(parts) >= 2:
                return parts[-2]  # Parent directory name
        return "unknown"

    # Legacy compatibility methods
    def find_session_files(self, claude_dir: str = None) -> List[Path]:
        """Legacy method for backward compatibility."""
        if claude_dir:
            self.claude_dir = Path(claude_dir).expanduser()
        sessions = self.find_sessions()
        return [s.file_path for s in sessions if s.file_path]

    def parse_jsonl(self, file_path: Path) -> Tuple[List[Dict], int]:
        """Legacy method: parse JSONL file with error counting."""
        records = []
        parse_errors = 0

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    records.append(record)
                except json.JSONDecodeError:
                    parse_errors += 1

        return records, parse_errors

    def extract_session_metadata(self, file_path: Path) -> Dict:
        """Legacy method: extract metadata from file path."""
        parts = file_path.parts
        project_name = parts[-2] if len(parts) >= 2 else "unknown"
        return {
            "project": project_name,
            "session_id": file_path.stem,
            "file_path": str(file_path),
        }

    def process_session_file(self, file_path: Path) -> Tuple[List[Dict], Dict]:
        """Legacy method: process a single session file."""
        session = SessionInfo(
            id=file_path.stem,
            source=self.source_name,
            file_path=file_path,
        )
        return self.process_session(session)

    def process_all_sessions(self, claude_dir: str = None) -> Tuple[List[Dict], Dict]:
        """Legacy method: process all session files."""
        if claude_dir:
            self.claude_dir = Path(claude_dir).expanduser()

        sessions = self.find_sessions()
        all_chunks = []
        stats = {
            "total_files": 0,
            "total_chunks": 0,
            "files_with_secrets": 0,
            "total_parse_errors": 0,
        }

        for session in sessions:
            try:
                chunks, file_stats = self.process_session(session)
                if chunks:
                    all_chunks.extend(chunks)
                    stats["total_files"] += 1
                    stats["total_chunks"] += len(chunks)
                    stats["total_parse_errors"] += file_stats.get("parse_errors", 0)
                    if any(c.get("secrets_scrubbed") for c in chunks):
                        stats["files_with_secrets"] += 1
            except Exception as e:
                print(f"Error processing {session.file_path}: {e}")

        return all_chunks, stats


# =============================================================================
# Cursor Indexer
# =============================================================================

def get_cursor_db_path() -> Optional[Path]:
    """Get Cursor database path for the current platform.
    
    Prefers the .backup file (avoids SQLite locking) but falls back
    to the main state.vscdb if backup doesn't exist.
    """
    if sys.platform == "darwin":
        base_dir = Path.home() / "Library" / "Application Support" / "Cursor" / "User" / "globalStorage"
    elif sys.platform == "win32":
        appdata = os.environ.get("APPDATA", "")
        if not appdata:
            return None
        base_dir = Path(appdata) / "Cursor" / "User" / "globalStorage"
    else:  # Linux
        xdg_config = os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))
        base_dir = Path(xdg_config) / "Cursor" / "User" / "globalStorage"
    
    # Prefer backup file (avoids locking issues)
    backup_path = base_dir / "state.vscdb.backup"
    if backup_path.exists():
        return backup_path
    
    # Fall back to main DB
    main_path = base_dir / "state.vscdb"
    if main_path.exists():
        return main_path
    
    return None


class CursorIndexer(BaseIndexer):
    """Indexes Cursor IDE conversations from SQLite storage."""

    source_name = "cursor"

    def __init__(
        self,
        db_path: Optional[Path] = None,
        window_size: int = 6,
        stride: int = 3,
    ):
        super().__init__(window_size, stride)
        self.db_path = db_path or get_cursor_db_path()
        self._conn: Optional[sqlite3.Connection] = None
        self._composer_cache: Dict[str, Dict] = {}

    def _get_connection(self) -> Optional[sqlite3.Connection]:
        """Get SQLite connection, caching for reuse."""
        if self._conn is not None:
            return self._conn
        if not self.db_path or not self.db_path.exists():
            return None
        try:
            self._conn = sqlite3.connect(str(self.db_path))
            return self._conn
        except sqlite3.Error as e:
            logger.warning(f"Failed to connect to Cursor DB: {e}")
            return None

    def close(self):
        """Close database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None

    def find_sessions(self) -> List[SessionInfo]:
        """Find all Cursor conversations (composer and bubble-only)."""
        conn = self._get_connection()
        if not conn:
            return []

        sessions = []

        try:
            # 1. Get composer sessions FIRST (with composerData.conversation[])
            cursor = conn.execute(
                "SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%'"
            )

            for key, value in cursor:
                if not value:
                    continue
                try:
                    data = json.loads(value)
                    conversation = data.get("conversation", [])
                    headers = data.get("fullConversationHeadersOnly", [])
                    composer_id = data.get("composerId", key.split(":")[-1])

                    # Cache composer data for later
                    self._composer_cache[composer_id] = data

                    # Skip only if BOTH are empty (truly unused session)
                    if len(conversation) == 0 and len(headers) == 0:
                        continue

                    # Count messages from whichever format has data
                    message_count = len(conversation) if conversation else len(headers)

                    sessions.append(SessionInfo(
                        id=composer_id,
                        source=self.source_name,
                        storage_type="composer",
                        created_at=data.get("createdAt", 0) / 1000 if data.get("createdAt") else None,
                        message_count=message_count,
                    ))
                except (json.JSONDecodeError, KeyError):
                    continue

            # 2. Get bubble-only sessions (not in composer)
            indexed_ids = {s.id for s in sessions}
            bubble_cursor = conn.execute("""
                SELECT substr(key, 10, 36) as conv_id, COUNT(*) as msg_count
                FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'
                GROUP BY 1
            """)

            for conv_id, msg_count in bubble_cursor:
                if conv_id and conv_id not in indexed_ids:
                    sessions.append(SessionInfo(
                        id=conv_id,
                        source=self.source_name,
                        storage_type="bubble",
                        created_at=None,  # No timestamp available for bubble-only
                        message_count=msg_count,
                    ))

        except sqlite3.Error as e:
            logger.warning(f"Error reading Cursor sessions: {e}")

        return sessions


    def get_session_messages(self, session: SessionInfo) -> List[Dict]:
        """Get messages for a session, routing by storage_type."""
        if session.storage_type == "bubble":
            return self._get_bubble_messages(session.id)
        return self._get_composer_messages(session)

    def _get_composer_messages(self, session: SessionInfo) -> List[Dict]:
        """Get messages from composerData (conversation[] or fullConversationHeadersOnly)."""
        composer_data = self._composer_cache.get(session.id)
        if not composer_data:
            # Try to fetch from DB
            conn = self._get_connection()
            if conn:
                try:
                    cursor = conn.execute(
                        "SELECT value FROM cursorDiskKV WHERE key = ?",
                        (f"composerData:{session.id}",)
                    )
                    row = cursor.fetchone()
                    if row and row[0]:
                        composer_data = json.loads(row[0])
                        self._composer_cache[session.id] = composer_data
                except (sqlite3.Error, json.JSONDecodeError):
                    pass

        if not composer_data:
            return []

        # Try conversation[] first (v1/NULL format)
        conversation = composer_data.get("conversation", [])
        if conversation:
            return self._parse_conversation_array(conversation, session.id)

        # Try fullConversationHeadersOnly (v3/v9/v10 format)
        headers = composer_data.get("fullConversationHeadersOnly", [])
        if headers:
            return self._get_messages_from_headers(session.id, headers)

        return []

    def _parse_conversation_array(self, conversation: List[Dict], session_id: str) -> List[Dict]:
        """Parse messages from conversation[] array (v1/NULL format)."""
        messages = []
        unknown_versions = set()

        for i, msg in enumerate(conversation):
            # Check message version - v1, v2, v3 are known formats, None is implicit v1
            msg_version = msg.get("_v")
            if msg_version not in (None, 1, 2, 3):
                if msg_version not in unknown_versions:
                    unknown_versions.add(msg_version)
                    logger.warning(f"Unknown Cursor message version {msg_version} in conversation {session_id[:8]}..., skipping these messages")
                continue

            # Map type to role: 1=user, 2=assistant
            msg_type = msg.get("type", 2)
            role = "user" if msg_type == 1 else "assistant"
            text = msg.get("text", "")

            messages.append({
                "role": role,
                "text": text,
                "order": i,
                "_raw": msg,  # Keep raw for project detection
            })

        return messages

    def _get_messages_from_headers(self, composer_id: str, headers: List[Dict]) -> List[Dict]:
        """Fetch messages from bubbleId keys using header references (v3/v9/v10 format)."""
        conn = self._get_connection()
        if not conn:
            return []

        messages = []
        unknown_versions = set()

        for i, header in enumerate(headers):
            bubble_id = header.get("bubbleId")
            if not bubble_id:
                continue

            key = f"bubbleId:{composer_id}:{bubble_id}"
            try:
                cursor = conn.execute(
                    "SELECT value FROM cursorDiskKV WHERE key = ?", (key,)
                )
                row = cursor.fetchone()
                if row and row[0]:
                    data = json.loads(row[0])

                    # Version check - v1, v2, v3 are known
                    msg_version = data.get("_v")
                    if msg_version is not None and msg_version not in (1, 2, 3):
                        if msg_version not in unknown_versions:
                            unknown_versions.add(msg_version)
                            logger.warning(f"Unknown message version {msg_version} in conversation {composer_id[:8]}...")
                        continue

                    messages.append({
                        "role": "user" if data.get("type") == 1 else "assistant",
                        "text": data.get("text", ""),
                        "order": i,
                        "_raw": data,  # Keep raw for project detection
                    })
            except (sqlite3.Error, json.JSONDecodeError) as e:
                logger.debug(f"Error fetching bubble {bubble_id}: {e}")

        return messages

    def _get_bubble_messages(self, conv_id: str) -> List[Dict]:
        """Get messages from bubbleId keys, ordered by SQLite rowid."""
        conn = self._get_connection()
        if not conn:
            return []

        messages = []
        unknown_versions = set()

        try:
            cursor = conn.execute("""
                SELECT value FROM cursorDiskKV 
                WHERE key LIKE ? ORDER BY rowid
            """, (f"bubbleId:{conv_id}:%",))

            for (value,) in cursor:
                data = json.loads(value)

                # Defensive version check - v1, v2, v3 are known
                msg_version = data.get("_v")
                if msg_version is not None and msg_version not in (1, 2, 3):
                    if msg_version not in unknown_versions:
                        unknown_versions.add(msg_version)
                        logger.warning(f"Unknown bubble message version {msg_version} in conversation {conv_id[:8]}...")
                    continue

                messages.append({
                    "role": "user" if data.get("type") == 1 else "assistant",
                    "text": data.get("text", ""),
                    "_raw": data,  # Keep raw for project detection
                })
        except (sqlite3.Error, json.JSONDecodeError) as e:
            logger.warning(f"Error reading bubble messages for {conv_id[:8]}...: {e}")

        return messages

    def extract_project(self, session: SessionInfo, messages: List[Dict]) -> str:
        """Extract project name from file paths in conversation context."""
        for msg in messages:
            raw = msg.get("_raw", {})
            
            # Try context.fileSelections first (most reliable)
            context = raw.get("context", {})
            for sel in context.get("fileSelections", []):
                uri = sel.get("uri", {})
                path = uri.get("fsPath", "")
                if path:
                    project = self._path_to_project(path)
                    if project != "cursor-general":
                        return project

            # Try tokenDetailsUpUntilHere
            for detail in raw.get("tokenDetailsUpUntilHere", []):
                path = detail.get("relativeWorkspacePath", "")
                if path and path.startswith("/"):
                    project = self._path_to_project(path)
                    if project != "cursor-general":
                        return project

            # Try relevantFiles (can be string or object format)
            for f in raw.get("relevantFiles", []):
                if isinstance(f, str) and f.startswith("/"):
                    # String format (some versions)
                    project = self._path_to_project(f)
                    if project != "cursor-general":
                        return project
                elif isinstance(f, dict):
                    # Object format: {"uri": {"fsPath": "/path"}} (bubble messages)
                    path = f.get("uri", {}).get("fsPath", "")
                    if path:
                        project = self._path_to_project(path)
                        if project != "cursor-general":
                            return project

        return "cursor-general"

    def _path_to_project(self, path: str) -> str:
        """Convert file path to project name using project markers."""
        try:
            p = Path(path)
            # Walk up looking for project root markers
            for parent in p.parents:
                markers = [".git", "package.json", "pyproject.toml", "Cargo.toml", "go.mod"]
                if any((parent / m).exists() for m in markers):
                    return parent.name

            # Fallback: use 4th path component (e.g., /Users/user/Projects/myapp/...)
            parts = p.parts
            if len(parts) > 4:
                return parts[4]
            elif len(parts) > 3:
                return parts[3]
        except Exception:
            pass

        return "cursor-general"

    def get_skipped_conversation_count(self) -> int:
        """Return count of skipped conversations (now always 0 - bubble-only are indexed)."""
        return 0


# =============================================================================
# Legacy Aliases
# =============================================================================

# Backward compatibility: SessionIndexer = ClaudeCodeIndexer
SessionIndexer = ClaudeCodeIndexer


# =============================================================================
# Incremental Indexer (Multi-Source)
# =============================================================================

class IncrementalIndexer:
    """
    Incremental indexer with state tracking for efficient updates.
    
    Supports multiple sources (Claude Code, Cursor) with per-source state tracking.
    State is saved per-file/conversation after successful upload.
    """

    STATE_VERSION = 3

    def __init__(
        self,
        indexer: ClaudeCodeIndexer = None,
        state_file: str = None,
        claude_dir: str = "~/.claude",
    ):
        """
        Initialize incremental indexer.

        Args:
            indexer: Base ClaudeCodeIndexer instance (legacy, for backward compat)
            state_file: Path to JSON state file
            claude_dir: Claude directory to scan
        """
        # Legacy: accept SessionIndexer/ClaudeCodeIndexer
        if indexer is None:
            indexer = ClaudeCodeIndexer(claude_dir=claude_dir)
        self.indexer = indexer
        self.claude_dir = Path(claude_dir).expanduser()

        # Cursor indexer (lazy init)
        self._cursor_indexer: Optional[CursorIndexer] = None

        # Default state file location
        if state_file is None:
            state_dir = Path.home() / ".meld"
            state_dir.mkdir(parents=True, exist_ok=True)
            state_file = str(state_dir / "sync_state.json")

        self.state_file = Path(state_file)
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """Load state from file, migrating if necessary."""
        if self.state_file.exists():
            try:
                state = json.loads(self.state_file.read_text())
                return self._migrate_state(state)
            except Exception:
                pass
        return self._default_state()

    def _default_state(self) -> Dict:
        """Return default state structure."""
        return {
            "version": self.STATE_VERSION,
            "claude_code": {"files": {}},
            "cursor": {"conversations": {}, "last_sync": None, "db_mtime": None},
            "last_sync": None,
            "failed_files": {},
        }

    def _migrate_state(self, state: Dict) -> Dict:
        """Migrate state from older versions."""
        version = state.get("version", 1)

        if version < 3:
            # v1/v2 -> v3: Wrap files under claude_code, add cursor
            old_files = state.get("files", {})
            new_state = self._default_state()
            new_state["claude_code"]["files"] = old_files
            new_state["last_sync"] = state.get("last_sync")
            new_state["failed_files"] = state.get("failed_files", {})
            return new_state

        return state

    def _save_state(self):
        """Save state to file."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(self.state, indent=2))

    @property
    def cursor_indexer(self) -> Optional[CursorIndexer]:
        """Lazy-init Cursor indexer."""
        if self._cursor_indexer is None:
            db_path = get_cursor_db_path()
            if db_path:
                self._cursor_indexer = CursorIndexer(db_path)
        return self._cursor_indexer

    # =========================================================================
    # Claude Code methods (file-based)
    # =========================================================================

    def find_new_or_modified_files(self, max_age_days: int = None) -> List[Tuple[Path, bool]]:
        """Find Claude Code files that need processing."""
        files_to_process = []
        all_files = self.indexer.find_session_files(str(self.claude_dir))

        now = time.time()
        max_age_seconds = max_age_days * 86400 if max_age_days else None

        # Get Claude Code file state
        file_state_dict = self.state.get("claude_code", {}).get("files", {})
        # Backward compat: also check top-level files
        if not file_state_dict and "files" in self.state:
            file_state_dict = self.state["files"]

        for file_path in all_files:
            path_str = str(file_path)

            try:
                stat = file_path.stat()
                current_size = stat.st_size
                current_mtime = stat.st_mtime
            except OSError:
                continue

            if max_age_seconds and (now - current_mtime) > max_age_seconds:
                continue

            file_state = file_state_dict.get(path_str, {})

            if not file_state:
                files_to_process.append((file_path, False, current_mtime))
            elif file_state.get("size", 0) < current_size:
                files_to_process.append((file_path, True, current_mtime))
            elif file_state.get("mtime", 0) < current_mtime:
                files_to_process.append((file_path, False, current_mtime))

        files_to_process.sort(key=lambda x: x[2], reverse=True)
        return [(f[0], f[1]) for f in files_to_process]

    def process_file(self, file_path: Path) -> Tuple[List[Dict], Dict]:
        """Process a single Claude Code file into chunks."""
        try:
            session = SessionInfo(
                id=file_path.stem,
                source="claude_code",
                file_path=file_path,
            )
            chunks, file_stats = self.indexer.process_session(session)
            return chunks, file_stats
        except Exception as e:
            return [], {"error": str(e), "parse_errors": 0}

    def mark_file_synced(self, file_path: Path, chunk_count: int):
        """Mark a Claude Code file as successfully synced."""
        try:
            stat = file_path.stat()
            if "claude_code" not in self.state:
                self.state["claude_code"] = {"files": {}}
            if "files" not in self.state["claude_code"]:
                self.state["claude_code"]["files"] = {}

            self.state["claude_code"]["files"][str(file_path)] = {
                "size": stat.st_size,
                "mtime": stat.st_mtime,
                "last_indexed": time.time(),
                "chunk_count": chunk_count,
            }
            self.state["last_sync"] = time.time()
            self._save_state()
        except OSError:
            pass

    # =========================================================================
    # Cursor methods (conversation-based)
    # =========================================================================

    def find_new_or_modified_cursor_conversations(self) -> List[SessionInfo]:
        """Find Cursor conversations that need processing."""
        if not self.cursor_indexer:
            return []

        sessions = self.cursor_indexer.find_sessions()
        cursor_state = self.state.get("cursor", {})
        conv_state = cursor_state.get("conversations", {})

        to_process = []
        for session in sessions:
            state = conv_state.get(session.id, {})
            if not state:
                # New conversation
                to_process.append(session)
            elif state.get("message_count", 0) < session.message_count:
                # Conversation has new messages
                to_process.append(session)

        return to_process

    def process_cursor_conversation(self, session: SessionInfo) -> Tuple[List[Dict], Dict]:
        """Process a single Cursor conversation into chunks."""
        if not self.cursor_indexer:
            return [], {"error": "Cursor not available"}
        try:
            return self.cursor_indexer.process_session(session)
        except Exception as e:
            return [], {"error": str(e)}

    def mark_cursor_conversation_synced(self, session: SessionInfo, chunk_count: int):
        """Mark a Cursor conversation as successfully synced."""
        if "cursor" not in self.state:
            self.state["cursor"] = {"conversations": {}}
        if "conversations" not in self.state["cursor"]:
            self.state["cursor"]["conversations"] = {}

        self.state["cursor"]["conversations"][session.id] = {
            "message_count": session.message_count,
            "synced_at": time.time(),
            "chunk_count": chunk_count,
        }
        self.state["cursor"]["last_sync"] = time.time()
        self.state["last_sync"] = time.time()
        self._save_state()

    def get_cursor_skipped_count(self) -> int:
        """Get count of skipped bubble-only Cursor conversations."""
        if self.cursor_indexer:
            return self.cursor_indexer.get_skipped_conversation_count()
        return 0

    # =========================================================================
    # Shared methods
    # =========================================================================

    def get_sync_stats(self) -> Dict:
        """Get statistics about current sync state."""
        claude_files = self.state.get("claude_code", {}).get("files", {})
        # Backward compat
        if not claude_files and "files" in self.state:
            claude_files = self.state["files"]

        total_files = len(claude_files)
        total_chunks = sum(f.get("chunk_count", 0) for f in claude_files.values())

        cursor_convs = self.state.get("cursor", {}).get("conversations", {})
        cursor_chunks = sum(c.get("chunk_count", 0) for c in cursor_convs.values())

        return {
            "files_synced": total_files,
            "chunks_synced": total_chunks + cursor_chunks,
            "cursor_conversations": len(cursor_convs),
            "cursor_chunks": cursor_chunks,
            "last_sync": self.state.get("last_sync"),
            "failed_files_count": len(self.state.get("failed_files", {})),
            "last_error": self.state.get("last_error"),
        }

    def mark_file_failed(self, file_path: Path, error: str):
        """Track a file that failed to sync."""
        if "failed_files" not in self.state:
            self.state["failed_files"] = {}

        path_str = str(file_path)
        self.state["failed_files"][path_str] = {
            "error": error[:200],
            "failed_at": time.time(),
            "retry_count": self.state["failed_files"].get(path_str, {}).get("retry_count", 0) + 1,
        }
        self.state["last_error"] = error[:200]
        self._save_state()

    def clear_file_failure(self, file_path: Path):
        """Clear failure tracking for a file."""
        path_str = str(file_path)
        if "failed_files" in self.state and path_str in self.state["failed_files"]:
            del self.state["failed_files"][path_str]
            self._save_state()

    def get_failed_files(self) -> Dict:
        """Get info about files that failed to sync."""
        return self.state.get("failed_files", {})

    def reset_state(self):
        """Clear all state for full reindex."""
        self.state = self._default_state()
        self._save_state()

    def close(self):
        """Close any open connections (call after sync completes)."""
        if self._cursor_indexer:
            self._cursor_indexer.close()
            self._cursor_indexer = None

    # =========================================================================
    # Legacy methods for backward compatibility
    # =========================================================================

    def process_incremental(self, progress_callback=None) -> Tuple[List[Dict], Dict]:
        """Legacy batch mode (deprecated)."""
        files_to_process = self.find_new_or_modified_files()

        if not files_to_process:
            return [], {"files_processed": 0, "chunks_indexed": 0}

        all_chunks = []
        stats = {
            "files_processed": 0,
            "chunks_indexed": 0,
            "incremental_files": 0,
            "new_files": 0,
            "parse_errors": 0,
        }
        self._pending_states = {}

        for file_path, is_incremental in files_to_process:
            try:
                chunks, file_stats = self.process_file(file_path)
                if chunks:
                    all_chunks.extend(chunks)
                    stats["files_processed"] += 1
                    stats["chunks_indexed"] += len(chunks)
                    stats["parse_errors"] += file_stats.get("parse_errors", 0)

                    if is_incremental:
                        stats["incremental_files"] += 1
                    else:
                        stats["new_files"] += 1

                    stat = file_path.stat()
                    self._pending_states[str(file_path)] = {
                        "size": stat.st_size,
                        "mtime": stat.st_mtime,
                        "last_indexed": time.time(),
                        "chunk_count": len(chunks),
                    }

            except Exception as e:
                print(f"Error processing {file_path}: {e}")

            if progress_callback:
                progress_callback()

        return all_chunks, stats

    def commit_state(self):
        """Legacy: commit pending state changes."""
        if hasattr(self, '_pending_states') and self._pending_states:
            if "claude_code" not in self.state:
                self.state["claude_code"] = {"files": {}}
            self.state["claude_code"]["files"].update(self._pending_states)
            self.state["last_sync"] = time.time()
            self._save_state()
            self._pending_states = {}
