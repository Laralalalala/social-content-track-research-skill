# Changelog

All notable changes to this skill are documented here.

## 0.2.1 — 2026-11-05

Review-arm polish (no method change):

- Claim ledger now includes an L1 (direct observation) row so the example spans L1–L5.
- `references/decision-validation.md` now names Route-the-task mode 3 explicitly, so it is not confused with method step 3.
- Collector docs use `python3` and show how to put `scripts/` on `sys.path` before importing `ManualCsvCollector`.

## 0.2.0 — 2026-11-05

Public packaging release. The installable skill slug remains
`social-content-market-research`. The public repository name is
`social-content-track-research-skill` so GitHub search can find Xiaohongshu,
Douyin, and TikTok content-track research (赛道研究).

### Correctness

- `scripts/audit_csv.py` now treats non-finite numeric values (`NaN`, `inf`,
  `-inf`, and overflow) as missing instead of writing illegal JSON tokens.
  Output is always RFC 8259 JSON (`json.dumps(..., allow_nan=False)`).
- Date audit counts empty, invalid, and **future** dates, not only min/max.
- Mixed-type numeric cells are listed under `invalid_examples`.
- `scripts/coder_agreement.py` reports `cohen_kappa: null` with
  `kappa_undefined_reason` when *n* < 2 or kappa is otherwise undefined.
- Empty coding cells still count as a category, and are now tallied.
- Mismatched coder ID sets, missing files, and unknown fields return clear
  `error:` messages instead of a traceback.
- Stdlib tests cover normal CSVs, NaN/inf, future dates, duplicate IDs,
  mismatched coder IDs, and the *n* = 1 kappa guard.

### Collectors

- `agent-reach` is optional and is not shipped. The skill is a method and
  audit layer: bring your own collectors, official exports, or authorized APIs.
- Added `references/collectors-and-adapters.md` and `scripts/collectors/`
  (`ManualCsvCollector` copies a user CSV; `ExampleApiCollectorStub` is
  documentation only and performs no network I/O).
- No scraper, proxy rotation, or cookie/token export is included or instructed.

### Packaging and SEO

- Added bilingual `README.md`, MIT `LICENSE`, this `CHANGELOG.md`, synthetic
  `examples/`, and `tests/`.
- `SKILL.md` frontmatter description now includes Xiaohongshu / XHS / RedNote /
  小红书, Douyin / 抖音, TikTok, 赛道研究, social listening, Cohen's kappa, and
  the bring-your-own-collector boundary.
- `agents/openai.yaml` keeps the Chinese display name 「社媒内容赛道证据研究」
  and a discoverable short description.
- Method reference pages for L1–L5 evidence grades, sampling and coding, and
  unvalidated decision-validation extensions are included so a clone has the
  full contract. They restore the method from `SKILL.md` and the 2026-11-05
  evaluation notes (original sibling copies were not present in the public
  staging tree). No private study rows are included.

### Safety

- README restates the platform-safety gate: public or authorized data only;
  no credential export; no automated publish / like / follow / comment; stop
  on captcha or rate limit; no evasion of risk controls.

## 0.1.0 — 2026-07-27

Initial method extract from a completed V2 content-track study. Eleven-step
research contract, L1–L5 evidence grades, comment dual-coding with kappa
gates, commercial-path ≠ commercial-proof, and platform-safety rules.
Shipped locally as the Codex skill `social-content-market-research`.
