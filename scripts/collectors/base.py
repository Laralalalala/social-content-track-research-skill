"""Collector adapter interface used by this skill.

Implementations must stay inside authorized, Terms-of-Service-compliant
sources. Do not scrape, automate logged-in browsing, rotate proxies, or
otherwise evade platform controls.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Protocol, runtime_checkable


class CollectorError(Exception):
    """Clear, user-facing collector failure."""


@dataclass(frozen=True)
class CollectedTable:
    """A CSV written under raw/ plus enough metadata to audit the source."""

    path: Path
    source: str
    platform: str | None
    query: Mapping[str, Any] = field(default_factory=dict)
    notes: str = ""
    row_count: int = 0


@runtime_checkable
class CollectorAdapter(Protocol):
    """Minimal interface for a bring-your-own collector.

    A collector must:

    - write an immutable UTF-8 CSV (typically under `raw/`);
    - keep a stable row ID column so `audit_csv.py` and `coder_agreement.py` can join;
    - record how the sample was obtained (source name, query, time);
    - use only official, public, authorized, or licensed channels;
    - never export credentials, cookies, tokens, or unnecessary personal identifiers;
    - never scrape or automate behavior that violates a platform's Terms of Service.
    """

    name: str

    def collect(self, query: Mapping[str, Any], dest_dir: Path) -> CollectedTable:
        """Fetch or accept data and write a CSV into `dest_dir`."""
        ...
