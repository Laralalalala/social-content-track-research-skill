#!/usr/bin/env python3
"""Audit a CSV's structure, missingness, IDs, dates, and numeric fields.

Non-finite numeric values (NaN, +inf, -inf) are treated as missing and are
never written into output. JSON is always RFC 8259 valid (`allow_nan=False`).
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


class AuditError(Exception):
    """Clear, user-facing failure while auditing a CSV."""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit a CSV and print RFC 8259-valid JSON to stdout."
    )
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--id-field")
    parser.add_argument("--date-field")
    parser.add_argument("--numeric-field", action="append", default=[])
    return parser.parse_args(argv)


def parse_date_value(value: str) -> datetime | None:
    value = (value or "").strip()
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
    return None


def parse_date(value: str) -> str | None:
    parsed = parse_date_value(value)
    return parsed.isoformat() if parsed is not None else None


def as_naive_utc(value: datetime) -> datetime:
    if value.tzinfo is not None:
        return value.astimezone(timezone.utc).replace(tzinfo=None)
    return value


def percentile(values: list[float], q: float) -> float | None:
    finite = [value for value in values if math.isfinite(value)]
    if not finite:
        return None
    xs = sorted(finite)
    if len(xs) == 1:
        return xs[0]
    position = (len(xs) - 1) * q
    low = math.floor(position)
    high = math.ceil(position)
    if low == high:
        return xs[low]
    return xs[low] + (xs[high] - xs[low]) * (position - low)


def parse_numeric_cell(raw: str | None) -> tuple[str, float | None]:
    """Classify one cell as empty, nonfinite, invalid, or valid.

    Non-finite parsed floats (NaN / ±inf) are treated as missing, not as
    numeric values and not as parse errors.
    """
    text = (raw or "").strip().replace(",", "")
    if not text:
        return "empty", None
    try:
        number = float(text)
    except ValueError:
        return "invalid", None
    if not math.isfinite(number):
        return "nonfinite", None
    return "valid", number


def json_safe(obj: Any) -> Any:
    """Replace remaining non-finite floats with None so dumps cannot emit NaN."""
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


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str | None]]]:
    if not path.exists():
        raise AuditError(f"CSV not found: {path}")
    if not path.is_file():
        raise AuditError(f"CSV path is not a file: {path}")
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = list(reader.fieldnames or [])
            if not fields or all(not (field or "").strip() for field in fields):
                raise AuditError(
                    f"{path}: CSV has no header row. Add a first row of column names."
                )
            rows = list(reader)
    except UnicodeDecodeError as exc:
        raise AuditError(f"{path}: could not decode as UTF-8 ({exc})") from exc
    except csv.Error as exc:
        raise AuditError(f"{path}: could not parse CSV ({exc})") from exc
    return fields, rows


def audit_csv(
    csv_path: Path | str,
    *,
    id_field: str | None = None,
    date_field: str | None = None,
    numeric_fields: Sequence[str] | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    path = Path(csv_path)
    fields, rows = load_csv(path)
    warnings: list[str] = []

    if any(field is None or not str(field).strip() for field in fields):
        warnings.append(
            "CSV header contains an empty or missing column name; extra cells "
            "in some rows may have been dropped or stored under a blank key."
        )
    if not rows:
        warnings.append("CSV has a header but no data rows.")

    result: dict[str, Any] = {
        "path": str(path.resolve()),
        "row_count": len(rows),
        "field_count": len(fields),
        "fields": fields,
        "missing": {
            field: {
                "count": sum(not (row.get(field) or "").strip() for row in rows),
                "rate": round(
                    sum(not (row.get(field) or "").strip() for row in rows) / len(rows),
                    6,
                )
                if rows
                else 0,
            }
            for field in fields
            if field is not None
        },
        "warnings": warnings,
    }

    if id_field:
        if id_field not in fields:
            raise AuditError(
                f"Unknown ID field {id_field!r}. Available columns: {_available_columns(fields)}"
            )
        values = [(row.get(id_field) or "").strip() for row in rows]
        counts = Counter(value for value in values if value)
        result["id_audit"] = {
            "field": id_field,
            "nonempty": sum(bool(value) for value in values),
            "empty": sum(not value for value in values),
            "unique_nonempty": len(counts),
            "duplicate_values": sorted(value for value, count in counts.items() if count > 1),
            "duplicate_count": sum(count > 1 for count in counts.values()),
        }

    if date_field:
        if date_field not in fields:
            raise AuditError(
                f"Unknown date field {date_field!r}. Available columns: {_available_columns(fields)}"
            )
        raw_dates = [(row.get(date_field) or "").strip() for row in rows]
        parsed_dates = [parse_date_value(value) for value in raw_dates if value]
        valid_dates = [value for value in parsed_dates if value is not None]
        reference = as_naive_utc(now) if now is not None else datetime.now(timezone.utc).replace(tzinfo=None)
        future = sum(as_naive_utc(value) > reference for value in valid_dates)
        iso_values = [value.isoformat() for value in valid_dates]
        result["date_audit"] = {
            "field": date_field,
            "nonempty": sum(bool(value) for value in raw_dates),
            "empty": sum(not value for value in raw_dates),
            "valid": len(valid_dates),
            "invalid": sum(value is None for value in parsed_dates),
            "future": future,
            "minimum": min(iso_values) if iso_values else None,
            "maximum": max(iso_values) if iso_values else None,
        }

    numeric: dict[str, Any] = {}
    for field in numeric_fields or []:
        if field not in fields:
            raise AuditError(
                f"Unknown numeric field {field!r}. Available columns: {_available_columns(fields)}"
            )
        values: list[float] = []
        empty = 0
        invalid = 0
        nonfinite = 0
        invalid_examples: list[str] = []
        for row in rows:
            status, number = parse_numeric_cell(row.get(field))
            if status == "empty":
                empty += 1
            elif status == "nonfinite":
                nonfinite += 1
            elif status == "invalid":
                invalid += 1
                sample = (row.get(field) or "").strip()
                if sample and sample not in invalid_examples and len(invalid_examples) < 5:
                    invalid_examples.append(sample)
            elif number is not None:
                values.append(number)
        numeric[field] = {
            "valid": len(values),
            "invalid": invalid,
            "invalid_examples": invalid_examples,
            "empty": empty,
            "nonfinite": nonfinite,
            "missing": empty + nonfinite,
            "minimum": min(values) if values else None,
            "q25": percentile(values, 0.25),
            "median": statistics.median(values) if values else None,
            "q75": percentile(values, 0.75),
            "maximum": max(values) if values else None,
        }
    result["numeric_audit"] = numeric
    return result


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    try:
        result = audit_csv(
            args.csv_path,
            id_field=args.id_field,
            date_field=args.date_field,
            numeric_fields=args.numeric_field,
        )
    except AuditError as exc:
        raise SystemExit(f"error: {exc}") from exc
    print(dumps_json(result))


if __name__ == "__main__":
    main()
