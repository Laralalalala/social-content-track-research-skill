"""Optional bring-your-own collector adapters.

This skill analyzes research CSVs. It does not require `agent-reach` and it
does not ship a live social-platform scraper. Provide a manual export or
implement `CollectorAdapter` against a source you are authorized to use.
"""

from .base import CollectedTable, CollectorAdapter, CollectorError
from .manual_csv import ManualCsvCollector
from .stub import ExampleApiCollectorStub

__all__ = [
    "CollectedTable",
    "CollectorAdapter",
    "CollectorError",
    "ExampleApiCollectorStub",
    "ManualCsvCollector",
]
