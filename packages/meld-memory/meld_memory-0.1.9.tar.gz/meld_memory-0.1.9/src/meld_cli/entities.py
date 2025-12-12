"""
Entity extraction for technical conversation logs.

Extracts high-signal fields for field-weighted BM25 search:
- Error messages and error types
- Code identifiers (functions, classes, variables)
- File paths (absolute and relative)
- Command outputs and exit codes
- Stack trace symbols

Ported from recall-mcp for session indexing.
"""

import re
from typing import Dict, List, Set


# Reserved words to filter out
STOPWORDS = {"the", "and", "or", "a", "to", "in", "of", "for", "on", "with", "at", "by"}
KEYWORDS = {
    "function",
    "class",
    "var",
    "let",
    "const",
    "def",
    "fn",
    "package",
    "import",
    "from",
    "return",
}
RESERVED = STOPWORDS | KEYWORDS


# Regex patterns for extraction
ID_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]{2,}\b")
CAMEL_SPLIT_RE = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")
PATH_RE = re.compile(r"(?:[A-Za-z]:\\|/)(?:[^\s\:\"'`<>]|\\ )+")
ERR_NAME_RE = re.compile(
    r"\b([A-Z][A-Za-z0-9_]*(?:Error|Exception|Failure|Fault|Abort|Panic))\b"
)
NODE_FRAME_RE = re.compile(r"^\s*at\s+.*?\((.+?):(\d+):(\d+)\)")
PY_FILE_RE = re.compile(r'^\s*File\s+"(.+?)",\s+line\s+(\d+),\s+in\s+(.+)')
HTTP_STATUS_RE = re.compile(r"\b(4\d{2}|5\d{2})\b")  # HTTP error codes
EXIT_CODE_RE = re.compile(r"exit code:?\s*(\d+)", re.IGNORECASE)
ERRNO_RE = re.compile(r"\b(E[A-Z]{2,})\b")  # ENOENT, EACCES, ECONNRESET, etc.


def split_identifier(tok: str) -> List[str]:
    """
    Split identifier into components for better matching.

    Examples:
        PrismaClientKnownRequestError → [PrismaClientKnownRequestError, Prisma, Client, Known, Request, Error]
        user_authentication → [user_authentication, user, authentication]
    """
    parts = CAMEL_SPLIT_RE.split(tok)
    components = [tok]

    for part in parts:
        for segment in part.split("_"):
            if segment and segment.lower() not in RESERVED:
                components.append(segment)

    return list(set(components))


def extract_entities(text: str) -> Dict[str, List[str]]:
    """
    Extract technical entities from conversation text.

    Returns:
        Dict with keys: error_tokens, identifier_tokens, path_tokens,
                       command_tokens, stack_tokens
    """
    error_tokens: Set[str] = set()
    identifier_tokens: Set[str] = set()
    path_tokens: Set[str] = set()
    command_tokens: Set[str] = set()
    stack_tokens: Set[str] = set()

    lines = text.splitlines()

    # Extract error names (TypeError, ValueError, PrismaClientKnownRequestError, etc.)
    for err_name in ERR_NAME_RE.findall(text):
        error_tokens.add(err_name)
        # Also add components for better matching
        for component in split_identifier(err_name):
            if component and len(component) > 2:
                error_tokens.add(component)

    # Extract HTTP status codes and errno symbols
    for status in HTTP_STATUS_RE.findall(text):
        error_tokens.add(status)

    for errno in ERRNO_RE.findall(text):
        error_tokens.add(errno)

    for exit_code in EXIT_CODE_RE.findall(text):
        error_tokens.add(f"exit{exit_code}")

    # Extract stack frame information
    for line in lines:
        # Node.js stack frame: "at function (file:line:col)"
        m1 = NODE_FRAME_RE.search(line)
        if m1:
            file_path = m1.group(1)
            path_tokens.add(file_path)
            # Extract path components
            for segment in file_path.replace("\\", "/").split("/"):
                if segment and segment not in {".", ".."}:
                    path_tokens.add(segment)
            continue

        # Python stack frame: 'File "file", line N, in function'
        m2 = PY_FILE_RE.search(line)
        if m2:
            file_path = m2.group(1)
            func_name = m2.group(3)
            path_tokens.add(file_path)
            stack_tokens.add(func_name)
            # Extract path components
            for segment in file_path.replace("\\", "/").split("/"):
                if segment and segment not in {".", ".."}:
                    path_tokens.add(segment)
            continue

    # Extract file paths (Unix/Windows)
    for m in PATH_RE.finditer(text):
        path = m.group(0)
        # Normalize separators to '/'
        normalized = path.replace("\\", "/")
        path_tokens.add(normalized)

        # Extract path components
        for segment in normalized.split("/"):
            if segment and segment not in {".", ".."}:
                path_tokens.add(segment)

    # Extract code identifiers from text
    for tok in ID_RE.findall(text):
        if tok.lower() in RESERVED:
            continue

        # Split into components
        for component in split_identifier(tok):
            if (
                component
                and component.lower() not in RESERVED
                and 2 < len(component) <= 64
            ):
                identifier_tokens.add(component)

    # Extract command lines (simple heuristic: lines starting with $ or >)
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("$", ">")):
            # Extract command and first few arguments
            cmd = stripped.lstrip("$>").strip().split()
            if cmd:
                command_tokens.add(cmd[0])
                # Add first 2 non-flag arguments
                for arg in cmd[1:4]:
                    if not arg.startswith("-") and len(arg) > 1:
                        command_tokens.add(arg)

    # Return sorted lists (turbopuffer expects arrays)
    return {
        "error_tokens": sorted(error_tokens)[:100],  # Limit to prevent explosion
        "identifier_tokens": sorted(identifier_tokens)[:200],
        "path_tokens": sorted(path_tokens)[:100],
        "command_tokens": sorted(command_tokens)[:50],
        "stack_tokens": sorted(stack_tokens)[:50],
    }


# Query expansion with technical synonyms
TECH_SYNONYMS = {
    "auth": [
        "authentication",
        "login",
        "signin",
        "oauth",
        "jwt",
        "bearer",
        "401",
        "unauthorized",
    ],
    "db": ["database", "postgres", "postgresql", "prisma", "sql", "mysql"],
    "rate": ["429", "ratelimit", "throttle", "too many requests"],
    "permission": ["authorization", "rbac", "access", "403", "forbidden"],
    "connection": ["econnreset", "eai_again", "timeout", "econnrefused"],
    "token": ["jwt", "bearer", "session", "cookie"],
    "api": ["endpoint", "route", "handler", "controller"],
    "test": ["testing", "spec", "suite", "assertion"],
    "build": ["compile", "bundle", "webpack", "vite", "rollup"],
    "type": ["typescript", "typing", "interface", "generic"],
}


def expand_query(query: str) -> Dict[str, List[str]]:
    """
    Expand query with technical synonyms and token variants.

    Returns:
        Dict with 'tokens' key containing expanded token list
    """
    # Extract tokens
    tokens = re.findall(r"[A-Za-z0-9_\.\-]+", query)

    expansions: Set[str] = set()

    for tok in tokens:
        # Add original token
        expansions.add(tok)

        # Add synonyms for known technical terms
        tok_lower = tok.lower()
        if tok_lower in TECH_SYNONYMS:
            expansions.update(TECH_SYNONYMS[tok_lower])

        # Add split variants for identifiers (camelCase, snake_case)
        for component in split_identifier(tok):
            if component and len(component) > 2:
                expansions.add(component)
                expansions.add(component.lower())

    return {
        "tokens": sorted(expansions),
        "original_tokens": tokens,
    }

