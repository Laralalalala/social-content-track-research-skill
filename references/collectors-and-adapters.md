# Collectors and adapters

This skill is a method and audit layer. It works without `agent-reach` and without any live social-platform client.

You can finish a study when the only input is a CSV the user already exported. Live collection is optional.

## Default path: no collector required

1. Ask the user for an official export, a spreadsheet they downloaded, or a CSV they saved from a page they opened themselves.
2. Place a copy under `raw/` (never overwrite raw later).
3. Run `scripts/audit_csv.py` before analysis.
4. Keep `analysis/` and `audit/` separate from `raw/`.

Record that a user-opened page sample may be personalized.

## Optional live adapters

`agent-reach` is an *optional* live-read helper. If it is installed, you may use it as one adapter: read that skill, run `agent-reach doctor` first, and keep the platform-safety gate in `SKILL.md`.

If `agent-reach` is missing, do not stop the workflow and do not invent a scraper. Use a manual CSV or another authorized adapter instead.

## Bring-your-own adapter

Implement `CollectorAdapter` from `scripts/collectors/base.py`:

- `name`: short source label written into metadata.
- `collect(query, dest_dir) -> CollectedTable`: write a UTF-8 CSV into `dest_dir` and return path, row count, platform, and notes.

Shipped implementations:

| Adapter | What it does |
|---|---|
| `ManualCsvCollector` | Copies a user-provided CSV into `raw/`. No network I/O. This is the supported default. |
| `ExampleApiCollectorStub` | Documentation only. Raises a clear error. It never calls a network API. |

A licensed commercial API that your organization already uses (for example a TikHub-like vendor that sells official or licensed access) can sit behind the same interface *if* the vendor's terms cover the intended research use. Name the vendor in `CollectedTable.notes`. This repository does not bundle API keys, clients, or scraping code for those services.

## Rules that every adapter must follow

- Prefer official, public, authorized, method-transparent sources.
- Do not scrape, crawl, or automate logged-in browsing in a way that violates a platform's Terms of Service.
- Do not rotate backends, proxies, or delays to evade rate limits or risk controls.
- Do not export credentials, cookies, tokens, or unnecessary personal identifiers.
- Stop when verification prompts, rate limits, or abnormal account behavior appear.
- Write a stable `item_id` (or equivalent) so later audits and dual-coding can join rows.

## Suggested CSV columns

These columns are enough for `audit_csv.py` to run a first pass. Extra columns are fine.

```text
item_id,platform,url,author_id,posted_at,title_or_caption,like_count,comment_count,share_count,collected_at,source
```

Example:

```bash
python3 scripts/audit_csv.py raw/posts.csv \
  --id-field item_id \
  --date-field posted_at \
  --numeric-field like_count \
  --numeric-field comment_count
```

Use `ManualCsvCollector` from Python when you want the copy + metadata step:

```python
import sys
from pathlib import Path

# cwd = skill root (the directory that contains SKILL.md and scripts/)
sys.path.insert(0, str(Path("scripts").resolve()))
from collectors.manual_csv import ManualCsvCollector

table = ManualCsvCollector().collect(
    {"source_csv": "exports/posts.csv", "platform": "tiktok"},
    Path("raw"),
)
```

Do not implement `ExampleApiCollectorStub.collect` as a scraper. Replace it, in your own project, with a licensed client or keep using manual CSVs.
