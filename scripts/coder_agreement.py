#!/usr/bin/env python3
"""Compute exact agreement and Cohen's kappa for two coding CSV files.

Cohen's kappa is reported as null (with a reason) when it is undefined:
fewer than two paired rows, or expected agreement of 1.0 with imperfect
observed agreement. JSON is always RFC 8259 valid.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence


KAPPA_MIN_PAIRS = 2


class AgreementError(Exception):
    """Clear, user-facing failure while comparing coding files."""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare two coding CSVs and print RFC 8259-valid JSON."
    )
    parser.add_argument("coder_a", type=Path)
    parser.add_argument("coder_b", type=Path)
    parser.add_argument("--id-field", required=True)
    parser.add_argument("--field", action="append", required=True)
    return parser.parse_args(argv)


def json_safe(obj: Any) -> Any:
    if isinstance(obj, float):
        return obj if math.isfinite(obj) else None
    if isinstance(obj, Mapping):
        return {key: json_safe(value) for key, value in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [json_safe(value) for value in obj]
    return obj


def dumps_json(obj: Any) -> str:
    return json.dumps(
        json_safe(obj),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        allow_nan=False,
    )


def _available_columns(fields: Sequence[str | None]) -> str:
    names = [field for field in fields if field]
    return ", ".join(names) if names else "(none)"


def _preview(values: Sequence[str], limit: int = 8) -> str:
    if not values:
        return "[]"
    shown = list(values[:limit])
    suffix = ", ..." if len(values) > limit else ""
    return "[" + ", ".join(repr(value) for value in shown) + suffix + "]"


def kappa(labels_a: Sequence[str], labels_b: Sequence[str]) -> tuple[float | None, str | None]:
    """Return (kappa, undefined_reason).

    Kappa is undefined for n < 2. When every coder used a single shared label
    (expected agreement = 1 and observed agreement = 1), kappa is defined as
    1.0 by convention. If expected agreement is 1 but observed is not, kappa
    is undefined.
    """
    if len(labels_a) != len(labels_b):
        return None, (
            "Cohen's kappa requires paired labels of equal length "
            f"(got {len(labels_a)} and {len(labels_b)})"
        )
    n = len(labels_a)
    if n < KAPPA_MIN_PAIRS:
        return None, (
            f"Cohen's kappa is undefined for n={n} paired row(s); "
            f"need at least {KAPPA_MIN_PAIRS}"
        )
    count_a = Counter(labels_a)
    count_b = Counter(labels_b)
    labels = set(count_a) | set(count_b)
    observed = sum(left == right for left, right in zip(labels_a, labels_b)) / n
    expected = sum((count_a[label] / n) * (count_b[label] / n) for label in labels)
    if expected == 1:
        if observed == 1:
            return 1.0, None
        return None, (
            "Cohen's kappa is undefined when expected agreement is 1.0 "
            "but observed agreement is not 1.0"
        )
    value = (observed - expected) / (1 - expected)
    if not math.isfinite(value):
        return None, "Cohen's kappa was non-finite and is reported as missing"
    return value, None


def read_rows(path: Path, id_field: str) -> dict[str, dict[str, str | None]]:
    path = Path(path)
    if not path.exists():
        raise AgreementError(f"Coding CSV not found: {path}")
    if not path.is_file():
        raise AgreementError(f"Coding CSV path is not a file: {path}")
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            if not fieldnames or all(not (field or "").strip() for field in fieldnames):
                raise AgreementError(
                    f"{path}: CSV has no header row. Add a first row of column names."
                )
            if id_field not in fieldnames:
                raise AgreementError(
                    f"{path}: unknown ID field {id_field!r}. "
                    f"Available columns: {_available_columns(fieldnames)}"
                )
            rows = list(reader)
    except UnicodeDecodeError as exc:
        raise AgreementError(f"{path}: could not decode as UTF-8 ({exc})") from exc
    except csv.Error as exc:
        raise AgreementError(f"{path}: could not parse CSV ({exc})") from exc

    output: dict[str, dict[str, str | None]] = {}
    for index, row in enumerate(rows, start=2):
        row_id = (row.get(id_field) or "").strip()
        if not row_id:
            raise AgreementError(
                f"{path}: empty ID in field {id_field!r} at data row {index - 1} "
                f"(file line {index})"
            )
        if row_id in output:
            raise AgreementError(
                f"{path}: duplicate ID {row_id!r} in field {id_field!r}"
            )
        output[row_id] = row
    if not output:
        raise AgreementError(f"{path}: no data rows after the header")
    return output


def compute_agreement(
    coder_a: Path | str,
    coder_b: Path | str,
    id_field: str,
    fields: Sequence[str],
) -> dict[str, Any]:
    rows_a = read_rows(Path(coder_a), id_field)
    rows_b = read_rows(Path(coder_b), id_field)
    ids_a, ids_b = set(rows_a), set(rows_b)
    if ids_a != ids_b:
        missing_a = sorted(ids_b - ids_a)
        missing_b = sorted(ids_a - ids_b)
        raise AgreementError(
            "ID mismatch between coding files: "
            f"{len(missing_a)} ID(s) present in B but missing in A {_preview(missing_a)}; "
            f"{len(missing_b)} ID(s) present in A but missing in B {_preview(missing_b)}. "
            "Both files must contain the exact same set of IDs."
        )

    ids = sorted(ids_a)
    sample_a = rows_a[ids[0]]
    sample_b = rows_b[ids[0]]
    result: dict[str, Any] = {
        "matched_rows": len(ids),
        "id_field": id_field,
        "fields": {},
        "warnings": [],
    }
    if len(ids) < KAPPA_MIN_PAIRS:
        result["warnings"].append(
            f"Only {len(ids)} paired row(s); Cohen's kappa is undefined until at least "
            f"{KAPPA_MIN_PAIRS} paired rows are present."
        )

    for field in fields:
        if field not in sample_a:
            raise AgreementError(
                f"Unknown coding field {field!r} in coder A. "
                f"Available columns: {_available_columns(sample_a.keys())}"
            )
        if field not in sample_b:
            raise AgreementError(
                f"Unknown coding field {field!r} in coder B. "
                f"Available columns: {_available_columns(sample_b.keys())}"
            )
        labels_a = [(rows_a[row_id].get(field) or "").strip() for row_id in ids]
        labels_b = [(rows_b[row_id].get(field) or "").strip() for row_id in ids]
        agreements = sum(left == right for left, right in zip(labels_a, labels_b))
        field_kappa, kappa_reason = kappa(labels_a, labels_b)
        empty_a = sum(not label for label in labels_a)
        empty_b = sum(not label for label in labels_b)
        if empty_a or empty_b:
            result["warnings"].append(
                f"Field {field!r} has {empty_a} empty cell(s) in coder A and "
                f"{empty_b} in coder B; empty strings are treated as a label "
                "category for agreement and kappa."
            )
        result["fields"][field] = {
            "paired_rows": len(ids),
            "exact_agreement_count": agreements,
            "exact_agreement_rate": round(agreements / len(ids), 6) if ids else None,
            "cohen_kappa": round(field_kappa, 6) if field_kappa is not None else None,
            "kappa_undefined_reason": kappa_reason,
            "empty_labels_a": empty_a,
            "empty_labels_b": empty_b,
            "labels_a": dict(sorted(Counter(labels_a).items())),
            "labels_b": dict(sorted(Counter(labels_b).items())),
        }
    return result


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    try:
        result = compute_agreement(args.coder_a, args.coder_b, args.id_field, args.field)
    except AgreementError as exc:
        raise SystemExit(f"error: {exc}") from exc
    print(dumps_json(result))


if __name__ == "__main__":
    main()
