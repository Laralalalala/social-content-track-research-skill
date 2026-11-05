"""Accept a user-provided CSV export. This is the default collector path."""

from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any, Mapping

from .base import CollectedTable, CollectorError


class ManualCsvCollector:
    """Copy an already-exported spreadsheet into the research `raw/` folder.

    Typical inputs: official platform downloads, browser "save as CSV"
    exports the user made themselves, or licensed-vendor dumps they already
    possess. This adapter performs no network I/O.
    """

    name = "manual_csv"

    def collect(self, query: Mapping[str, Any], dest_dir: Path) -> CollectedTable:
        source = query.get("source_csv")
        if not source:
            raise CollectorError(
                "manual_csv requires query['source_csv'] pointing at an existing CSV export."
            )
        src = Path(source).expanduser()
        if not src.exists():
            raise CollectorError(f"manual_csv source CSV not found: {src}")
        if not src.is_file():
            raise CollectorError(f"manual_csv source path is not a file: {src}")

        dest_dir = Path(dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_name = str(query.get("dest_name") or src.name)
        if not dest_name.lower().endswith(".csv"):
            dest_name += ".csv"
        dest = dest_dir / dest_name
        if dest.resolve() != src.resolve():
            if dest.exists():
                raise CollectorError(
                    f"manual_csv refuses to overwrite existing file: {dest}"
                )
            shutil.copy2(src, dest)

        try:
            with dest.open(encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                if not reader.fieldnames:
                    raise CollectorError(
                        f"{dest}: CSV has no header row. Add a first row of column names."
                    )
                row_count = sum(1 for _ in reader)
        except UnicodeDecodeError as exc:
            raise CollectorError(f"{dest}: could not decode as UTF-8 ({exc})") from exc
        except csv.Error as exc:
            raise CollectorError(f"{dest}: could not parse CSV ({exc})") from exc

        platform = query.get("platform")
        notes = query.get("notes") or (
            "User-provided CSV. Sample may be personalized if it came from a "
            "logged-in page the user opened."
        )
        return CollectedTable(
            path=dest,
            source=self.name,
            platform=str(platform) if platform else None,
            query=dict(query),
            notes=str(notes),
            row_count=row_count,
        )
