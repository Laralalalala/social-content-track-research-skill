#!/usr/bin/env python3
"""Tests for optional collector adapters (no agent-reach required)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))



import tempfile
import unittest
from pathlib import Path


from collectors.base import CollectorAdapter, CollectorError
from collectors.manual_csv import ManualCsvCollector
from collectors.stub import ExampleApiCollectorStub


class ManualCsvTests(unittest.TestCase):
    def test_copies_user_csv(self) -> None:
        collector = ManualCsvCollector()
        self.assertIsInstance(collector, CollectorAdapter)
        with tempfile.TemporaryDirectory() as tmp:
            table = collector.collect(
                {"source_csv": str(FIXTURES / "numeric_nan_inf.csv"), "platform": "tiktok"},
                Path(tmp),
            )
            self.assertTrue(table.path.exists())
            self.assertEqual(table.row_count, 10)
            self.assertEqual(table.source, "manual_csv")
            self.assertEqual(table.platform, "tiktok")
            self.assertGreater(table.path.stat().st_size, 0)

    def test_missing_source_is_clear(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(CollectorError) as ctx:
                ManualCsvCollector().collect(
                    {"source_csv": str(FIXTURES / "missing.csv")},
                    Path(tmp),
                )
            self.assertIn("not found", str(ctx.exception).lower())

    def test_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "numeric_nan_inf.csv"
            dest.write_text("already here\n", encoding="utf-8")
            with self.assertRaises(CollectorError) as ctx:
                ManualCsvCollector().collect(
                    {"source_csv": str(FIXTURES / "numeric_nan_inf.csv")},
                    Path(tmp),
                )
            self.assertIn("overwrite", str(ctx.exception).lower())


class StubTests(unittest.TestCase):
    def test_stub_never_fetches(self) -> None:
        stub = ExampleApiCollectorStub()
        self.assertIsInstance(stub, CollectorAdapter)
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)
            with self.assertRaises(CollectorError) as ctx:
                stub.collect({"query": "demo"}, dest)
            message = str(ctx.exception)
            self.assertIn("documentation-only", message)
            self.assertIn("ManualCsvCollector", message)
            self.assertEqual(list(dest.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
