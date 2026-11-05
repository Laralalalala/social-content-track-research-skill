#!/usr/bin/env python3
"""Tests for scripts/coder_agreement.py, including kappa n<2 edges."""

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
import unittest


import coder_agreement


class KappaUnitTests(unittest.TestCase):
    def test_n_less_than_two_is_undefined(self) -> None:
        value, reason = coder_agreement.kappa([], [])
        self.assertIsNone(value)
        self.assertIn("n=0", reason or "")

        value, reason = coder_agreement.kappa(["yes"], ["yes"])
        self.assertIsNone(value)
        self.assertIn("n=1", reason or "")

    def test_perfect_agreement(self) -> None:
        value, reason = coder_agreement.kappa(["a", "b", "a"], ["a", "b", "a"])
        self.assertIsNone(reason)
        self.assertAlmostEqual(value or 0.0, 1.0)

    def test_complete_disagreement_two_labels(self) -> None:
        value, reason = coder_agreement.kappa(["yes", "no"], ["no", "yes"])
        self.assertIsNone(reason)
        self.assertAlmostEqual(value or 0.0, -1.0)

    def test_expected_one_and_observed_one(self) -> None:
        value, reason = coder_agreement.kappa(["yes", "yes"], ["yes", "yes"])
        self.assertEqual(value, 1.0)
        self.assertIsNone(reason)


class AgreementFileTests(unittest.TestCase):
    def test_matched_files_report_kappa(self) -> None:
        result = coder_agreement.compute_agreement(
            FIXTURES / "coder_a.csv",
            FIXTURES / "coder_b.csv",
            "item_id",
            ["demand", "sentiment"],
        )
        self.assertEqual(result["matched_rows"], 4)
        self.assertEqual(result["fields"]["demand"]["cohen_kappa"], 1.0)
        self.assertIsNone(result["fields"]["demand"]["kappa_undefined_reason"])
        raw = coder_agreement.dumps_json(result)
        json.loads(raw)
        json.dumps(json.loads(raw), allow_nan=False)

    def test_n1_kappa_is_null_with_reason(self) -> None:
        result = coder_agreement.compute_agreement(
            FIXTURES / "coder_n1_a.csv",
            FIXTURES / "coder_n1_b.csv",
            "item_id",
            ["label"],
        )
        field = result["fields"]["label"]
        self.assertEqual(field["paired_rows"], 1)
        self.assertEqual(field["exact_agreement_count"], 1)
        self.assertEqual(field["exact_agreement_rate"], 1.0)
        self.assertIsNone(field["cohen_kappa"])
        self.assertIn("n=1", field["kappa_undefined_reason"])
        self.assertTrue(any("kappa" in warning.lower() for warning in result["warnings"]))

    def test_empty_coding_cells_are_counted(self) -> None:
        result = coder_agreement.compute_agreement(
            FIXTURES / "coder_empty_a.csv",
            FIXTURES / "coder_empty_b.csv",
            "item_id",
            ["label"],
        )
        field = result["fields"]["label"]
        self.assertEqual(field["empty_labels_a"], 1)
        self.assertEqual(field["empty_labels_b"], 0)
        self.assertEqual(field["exact_agreement_count"], 2)  # c1 yes/yes, c3 no/no
        self.assertTrue(any("empty cell" in warning for warning in result["warnings"]))

    def test_id_mismatch_is_clear(self) -> None:
        with self.assertRaises(coder_agreement.AgreementError) as ctx:
            coder_agreement.compute_agreement(
                FIXTURES / "coder_mismatch_a.csv",
                FIXTURES / "coder_mismatch_b.csv",
                "item_id",
                ["label"],
            )
        message = str(ctx.exception)
        self.assertIn("ID mismatch", message)
        self.assertIn("c2", message)
        self.assertIn("c3", message)

    def test_empty_file_is_clear(self) -> None:
        with self.assertRaises(coder_agreement.AgreementError) as ctx:
            coder_agreement.compute_agreement(
                FIXTURES / "coder_empty_file.csv",
                FIXTURES / "coder_empty_file.csv",
                "item_id",
                ["label"],
            )
        self.assertIn("no data rows", str(ctx.exception))

    def test_unknown_field_is_clear(self) -> None:
        with self.assertRaises(coder_agreement.AgreementError) as ctx:
            coder_agreement.compute_agreement(
                FIXTURES / "coder_a.csv",
                FIXTURES / "coder_b.csv",
                "item_id",
                ["does_not_exist"],
            )
        self.assertIn("Unknown coding field", str(ctx.exception))

    def test_missing_file_is_clear(self) -> None:
        with self.assertRaises(coder_agreement.AgreementError) as ctx:
            coder_agreement.read_rows(FIXTURES / "nope.csv", "item_id")
        self.assertIn("not found", str(ctx.exception).lower())

    def test_duplicate_id_is_clear(self) -> None:
        with self.assertRaises(coder_agreement.AgreementError) as ctx:
            coder_agreement.read_rows(FIXTURES / "duplicate_ids.csv", "item_id")
        self.assertIn("duplicate ID", str(ctx.exception))


class CliTests(unittest.TestCase):
    def test_cli_n1_json(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "coder_agreement.py"),
                str(FIXTURES / "coder_n1_a.csv"),
                str(FIXTURES / "coder_n1_b.csv"),
                "--id-field",
                "item_id",
                "--field",
                "label",
            ],
            check=False,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertIsNone(payload["fields"]["label"]["cohen_kappa"])
        self.assertIn("n=1", payload["fields"]["label"]["kappa_undefined_reason"])
        json.dumps(payload, allow_nan=False)


if __name__ == "__main__":
    unittest.main()
