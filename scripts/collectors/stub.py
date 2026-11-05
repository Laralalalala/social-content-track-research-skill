"""Documentation-only stub for a licensed, API-style collector.

This module never performs network I/O. It exists so integrators can see the
expected CSV shape before they wire a vendor they already pay for (for
example a TikHub-like commercial API) behind `CollectorAdapter`.

It is not a scraper, not a client, and not permission to call any third-party
service.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .base import CollectedTable, CollectorError


class ExampleApiCollectorStub:
    """Non-functional example of a licensed-API collector.

    Replace this stub in your own codebase with an implementation that:

    - calls an official or licensed API your organization already uses;
    - respects that vendor's terms, rate limits, and attribution rules;
    - writes the columns listed in `SUGGESTED_COLUMNS`;
    - records `collected_at` and a stable `item_id`.

    Do not implement page scraping, cookie reuse, proxy rotation, or any
    other method intended to evade platform controls.
    """

    name = "example_licensed_api_stub"

    SUGGESTED_COLUMNS = (
        "item_id",
        "platform",
        "url",
        "author_id",
        "posted_at",
        "title_or_caption",
        "like_count",
        "comment_count",
        "share_count",
        "collected_at",
        "source",
    )

    def collect(self, query: Mapping[str, Any], dest_dir: Path) -> CollectedTable:
        raise CollectorError(
            "example_licensed_api_stub is documentation-only and does not "
            "call any API or scrape any site. Provide a manual CSV via "
            "ManualCsvCollector, or implement CollectorAdapter against a "
            "licensed API you already have permission to use. Suggested "
            f"columns: {', '.join(self.SUGGESTED_COLUMNS)}. See "
            "references/collectors-and-adapters.md."
        )
