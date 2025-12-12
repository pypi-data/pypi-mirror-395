"""
Secret scrubber for Claude Code session logs.

Format-preserving redaction with HMAC tagging for traceability.
Detects API keys, tokens, passwords, and sensitive data patterns.

Ported from recall-mcp for cloud sync security.
"""

import hashlib
import hmac
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class SecretFinding:
    """A detected secret with metadata."""

    type: str
    original: str
    redacted: str
    location: str  # Context about where it was found


class SecretScrubber:
    """Scrubs secrets from text while preserving format."""

    def __init__(self, hmac_key: str = "meld-secret-key"):
        """Initialize scrubber with HMAC key for consistent tagging."""
        self.hmac_key = hmac_key.encode()

        # Provider-specific patterns
        self.patterns = {
            "openai_api_key": re.compile(r"\b(sk-[a-zA-Z0-9]{20,})\b"),
            "openai_org_id": re.compile(r"\b(org-[a-zA-Z0-9]{20,})\b"),
            "anthropic_api_key": re.compile(r"\b(sk-ant-[a-zA-Z0-9\-]{20,})\b"),
            "github_pat": re.compile(r"\b(ghp_[a-zA-Z0-9]{36,})\b"),
            "github_oauth": re.compile(r"\b(gho_[a-zA-Z0-9]{36,})\b"),
            "aws_access_key": re.compile(r"\b(AKIA[A-Z0-9]{16})\b"),
            "aws_secret_key": re.compile(
                r"\b([A-Za-z0-9/+=]{40})\b(?=.*aws)", re.IGNORECASE
            ),
            "google_api_key": re.compile(r"\b(AIza[a-zA-Z0-9\-_]{35})\b"),
            "slack_token": re.compile(r"\b(xox[baprs]-[a-zA-Z0-9\-]{10,})\b"),
            "stripe_key": re.compile(r"\b(sk_live_[a-zA-Z0-9]{24,})\b"),
            "stripe_test_key": re.compile(r"\b(sk_test_[a-zA-Z0-9]{24,})\b"),
            "jwt": re.compile(
                r"\b(eyJ[a-zA-Z0-9\-_]+\.eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+)\b"
            ),
            "pem_private_key": re.compile(
                r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----.+?-----END (?:RSA |EC )?PRIVATE KEY-----",
                re.DOTALL,
            ),
            "ssh_private_key": re.compile(
                r"-----BEGIN OPENSSH PRIVATE KEY-----.+?-----END OPENSSH PRIVATE KEY-----",
                re.DOTALL,
            ),
            "generic_api_key": re.compile(
                r"\b([a-zA-Z0-9]{32,})\b"
            ),  # Last resort, high false positive
            "password_in_url": re.compile(r"://[^:]+:([^@]+)@"),
            "db_connection_string": re.compile(
                r"((?:postgres|mysql|mongodb)://[^:]+:[^@]+@[^\s]+)", re.IGNORECASE
            ),
        }

        # Allowlist patterns to avoid false positives
        self.allowlist = {
            "hex_color": re.compile(r"^#?[0-9a-fA-F]{6}$"),
            "uuid": re.compile(
                r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
                re.IGNORECASE,
            ),
            "git_sha": re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE),
            "timestamp": re.compile(r"^\d{10,13}$"),
        }

    def _hmac_tag(self, secret: str, secret_type: str) -> str:
        """Generate consistent HMAC tag for a secret."""
        tag_input = f"{secret_type}:{secret}".encode()
        tag = hmac.new(self.hmac_key, tag_input, hashlib.sha256).hexdigest()[:8]
        return tag

    def _is_allowlisted(self, text: str) -> bool:
        """Check if text matches allowlist patterns (not a real secret)."""
        for pattern in self.allowlist.values():
            if pattern.match(text):
                return True
        return False

    def _redact_secret(self, secret: str, secret_type: str) -> str:
        """Format-preserving redaction with HMAC tag."""
        if self._is_allowlisted(secret):
            return secret

        tag = self._hmac_tag(secret, secret_type)

        # Preserve prefix and length
        if secret_type == "openai_api_key":
            # sk-... → sk-[REDACTED:tag]
            return f"sk-[REDACTED:{tag}]"
        elif secret_type == "anthropic_api_key":
            return f"sk-ant-[REDACTED:{tag}]"
        elif secret_type == "github_pat":
            return f"ghp_[REDACTED:{tag}]"
        elif secret_type == "aws_access_key":
            return f"AKIA[REDACTED:{tag}]"
        elif secret_type in ("pem_private_key", "ssh_private_key"):
            # Preserve structure
            lines = secret.split("\n")
            begin_line = lines[0]
            end_line = lines[-1]
            return f"{begin_line}\n[REDACTED:{tag}]\n{end_line}"
        elif secret_type == "password_in_url":
            # Preserve colon delimiter
            return f"[REDACTED:{tag}]"
        else:
            # Generic: preserve prefix (first 4 chars) if long enough
            if len(secret) > 8:
                prefix = secret[:4]
                return f"{prefix}[REDACTED:{tag}]"
            else:
                return f"[REDACTED:{tag}]"

    def scrub(self, text: str) -> Tuple[str, List[SecretFinding]]:
        """
        Scrub secrets from text.

        Returns:
            (scrubbed_text, findings)
        """
        findings = []
        scrubbed = text

        # Process patterns in priority order (most specific first)
        priority_order = [
            "openai_api_key",
            "openai_org_id",
            "anthropic_api_key",
            "github_pat",
            "github_oauth",
            "aws_access_key",
            "google_api_key",
            "slack_token",
            "stripe_key",
            "stripe_test_key",
            "jwt",
            "pem_private_key",
            "ssh_private_key",
            "db_connection_string",
            "password_in_url",
            # 'generic_api_key',  # Disabled by default (too many false positives)
        ]

        for secret_type in priority_order:
            pattern = self.patterns[secret_type]

            for match in pattern.finditer(scrubbed):
                if secret_type == "password_in_url":
                    # Extract password from capture group
                    original = match.group(1)
                else:
                    original = match.group(0)

                # Skip if allowlisted
                if self._is_allowlisted(original):
                    continue

                redacted = self._redact_secret(original, secret_type)

                # Record finding
                findings.append(
                    SecretFinding(
                        type=secret_type,
                        original=original,
                        redacted=redacted,
                        location=f"char {match.start()}-{match.end()}",
                    )
                )

                # Replace in text
                scrubbed = scrubbed.replace(original, redacted, 1)

        return scrubbed, findings

    def scrub_dict(self, data: Dict) -> Tuple[Dict, List[SecretFinding]]:
        """
        Recursively scrub secrets from dictionary values.

        Useful for processing JSONL records.
        """
        all_findings = []
        scrubbed_data = {}

        for key, value in data.items():
            if isinstance(value, str):
                scrubbed_value, findings = self.scrub(value)
                scrubbed_data[key] = scrubbed_value
                all_findings.extend(findings)
            elif isinstance(value, dict):
                scrubbed_value, findings = self.scrub_dict(value)
                scrubbed_data[key] = scrubbed_value
                all_findings.extend(findings)
            elif isinstance(value, list):
                scrubbed_list = []
                for item in value:
                    if isinstance(item, str):
                        scrubbed_item, findings = self.scrub(item)
                        scrubbed_list.append(scrubbed_item)
                        all_findings.extend(findings)
                    elif isinstance(item, dict):
                        scrubbed_item, findings = self.scrub_dict(item)
                        scrubbed_list.append(scrubbed_item)
                        all_findings.extend(findings)
                    else:
                        scrubbed_list.append(item)
                scrubbed_data[key] = scrubbed_list
            else:
                scrubbed_data[key] = value

        return scrubbed_data, all_findings

