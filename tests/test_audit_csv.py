#!/usr/bin/env python3
"""Tests for scripts/audit_csv.py, including NaN/inf JSON safety."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))



import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path


import audit_csv


class JsonSafetyTests(unittest.TestCase):
    def test_nan_inf_are_missing_and_json_is_legal(self) -> None:
        result = audit_csv.audit_csv(
            FIXTURES / "numeric_nan_inf.csv",
            id_field="item_id",
            date_field="posted_at",
            numeric_fields=["likes"],
        )
        likes = result["numeric_audit"]["likes"]
        self.assertEqual(likes["valid"], 2)  # 10 and 20
        self.assertEqual(likes["minimum"], 10.0)
        self.assertEqual(likes["maximum"], 20.0)
        self.assertEqual(likes["median"], 15.0)
        self.assertEqual(likes["empty"], 1)
        # NaN, inf, -inf, Infinity, -Infinity, 1e309 (overflows to inf)
        self.assertEqual(likes["nonfinite"], 6)
        self.assertEqual(likes["missing"], likes["empty"] + likes["nonfinite"])
        self.assertEqual(likes["invalid"], 1)
        self.assertIn("not-a-number", likes["invalid_examples"])
        self.assertTrue(all(isinstance(likes[key], (int, float, list, type(None))) for key in ("minimum", "median", "maximum")))
        for key in ("minimum", "q25", "median", "q75", "maximum"):
            value = likes[key]
            if isinstance(value, float):
                self.assertTrue(value == value and abs(value) != float("inf"))

        raw = audit_csv.dumps_json(result)
        parsed = json.loads(raw)
        self.assertEqual(parsed["numeric_audit"]["likes"]["valid"], 2)
        self.assertNotIn("NaN", raw)
        self.assertNotIn("Infinity", raw)
        self.assertNotIn("-Infinity", raw)
        json.dumps(parsed, allow_nan=False)

    def test_dumps_json_rejects_nothing_when_nonfinite_slips_in(self) -> None:
        payload = {"value": float("nan"), "nested": [float("inf"), -float("inf")]}
        raw = audit_csv.dumps_json(payload)
        parsed = json.loads(raw)
        self.assertIsNone(parsed["value"])
        self.assertEqual(parsed["nested"], [None, None])
        json.dumps(parsed, allow_nan=False)


class HardeningTests(unittest.TestCase):
    def test_empty_cells_and_mixed_types(self) -> None:
        result = audit_csv.audit_csv(
            FIXTURES / "empty_and_mixed.csv",
            id_field="item_id",
            date_field="posted_at",
            numeric_fields=["likes", "saves"],
            now=datetime(2026, 11, 5),
        )
        self.assertEqual(result["row_count"], 6)
        self.assertEqual(result["missing"]["likes"]["count"], 2)  # p2 empty, p5 whitespace
        self.assertGreater(result["missing"]["note"]["count"], 0)

        likes = result["numeric_audit"]["likes"]
        self.assertEqual(likes["valid"], 3)  # 100, 250, 1? wait p6=1, p1=100, p4=250 → 3; p3 N/A invalid
        self.assertEqual(likes["invalid"], 1)
        self.assertIn("N/A", likes["invalid_examples"])
        self.assertEqual(likes["empty"], 2)

        saves = result["numeric_audit"]["saves"]
        self.assertEqual(saves["valid"], 5)  # 12,15,21, empty p4, 0, 2 → empty is p4 only so valid=5
        self.assertEqual(saves["empty"], 1)
        self.assertEqual(saves["minimum"], 0.0)

        dates = result["date_audit"]
        self.assertEqual(dates["empty"], 0)
        self.assertEqual(dates["invalid"], 1)  # not-a-date
        self.assertEqual(dates["future"], 1)  # 2029-01-01 vs now 2026-11-05
        self.assertGreaterEqual(dates["valid"], 4)

    def test_duplicate_ids_are_reported(self) -> None:
        result = audit_csv.audit_csv(FIXTURES / "duplicate_ids.csv", id_field="item_id")
        self.assertEqual(result["id_audit"]["duplicate_values"], ["x1"])
        self.assertEqual(result["id_audit"]["duplicate_count"], 1)
        self.assertEqual(result["id_audit"]["unique_nonempty"], 2)

    def test_header_only_csv_warns_and_stays_valid_json(self) -> None:
        result = audit_csv.audit_csv(
            FIXTURES / "header_only.csv",
            id_field="item_id",
            numeric_fields=["likes"],
        )
        self.assertEqual(result["row_count"], 0)
        self.assertTrue(any("no data rows" in warning for warning in result["warnings"]))
        self.assertEqual(result["numeric_audit"]["likes"]["valid"], 0)
        self.assertIsNone(result["numeric_audit"]["likes"]["median"])
        raw = audit_csv.dumps_json(result)
        json.loads(raw)
        json.dumps(json.loads(raw), allow_nan=False)

    def test_unknown_field_has_clear_error(self) -> None:
        with self.assertRaises(audit_csv.AuditError) as ctx:
            audit_csv.audit_csv(FIXTURES / "dates.csv", id_field="missing_id")
        message = str(ctx.exception)
        self.assertIn("Unknown ID field", message)
        self.assertIn("item_id", message)
        self.assertIn("posted_at", message)

    def test_missing_file_has_clear_error(self) -> None:
        missing = FIXTURES / "does_not_exist.csv"
        with self.assertRaises(audit_csv.AuditError) as ctx:
            audit_csv.audit_csv(missing)
        self.assertIn("not found", str(ctx.exception).lower())

    def test_future_and_invalid_dates(self) -> None:
        result = audit_csv.audit_csv(
            FIXTURES / "dates.csv",
            date_field="posted_at",
            now=datetime(2026, 11, 5),
        )
        audit = result["date_audit"]
        self.assertEqual(audit["empty"], 1)
        self.assertEqual(audit["invalid"], 1)
        self.assertEqual(audit["valid"], 3)
        self.assertEqual(audit["future"], 1)


class CliTests(unittest.TestCase):
    def test_cli_prints_valid_json_for_nan_fixture(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "audit_csv.py"),
                str(FIXTURES / "numeric_nan_inf.csv"),
                "--id-field",
                "item_id",
                "--numeric-field",
                "likes",
            ],
            check=False,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["numeric_audit"]["likes"]["nonfinite"], 6)
        self.assertNotIn("NaN", completed.stdout)
        json.dumps(payload, allow_nan=False)

    def test_cli_unknown_field_exits_with_error_prefix(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "audit_csv.py"),
                str(FIXTURES / "dates.csv"),
                "--id-field",
                "nope",
            ],
            check=False,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("error:", completed.stderr)
        self.assertIn("Unknown ID field", completed.stderr)


class ParseNumericTests(unittest.TestCase):
    def test_tokens(self) -> None:
        self.assertEqual(audit_csv.parse_numeric_cell("")[0], "empty")
        self.assertEqual(audit_csv.parse_numeric_cell("  ")[0], "empty")
        self.assertEqual(audit_csv.parse_numeric_cell("nan")[0], "nonfinite")
        self.assertEqual(audit_csv.parse_numeric_cell("NaN")[0], "nonfinite")
        self.assertEqual(audit_csv.parse_numeric_cell("inf")[0], "nonfinite")
        self.assertEqual(audit_csv.parse_numeric_cell("-inf")[0], "nonfinite")
        self.assertEqual(audit_csv.parse_numeric_cell("Infinity")[0], "nonfinite")
        self.assertEqual(audit_csv.parse_numeric_cell("1,234.5"), ("valid", 1234.5))
        self.assertEqual(audit_csv.parse_numeric_cell("abc")[0], "invalid")
        status, value = audit_csv.parse_numeric_cell("10")
        self.assertEqual(status, "valid")
        self.assertEqual(value, 10.0)


if __name__ == "__main__":
    unittest.main()
