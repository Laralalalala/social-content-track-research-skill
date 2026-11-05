# Evidence levels and claim boundaries

Use these rules before you design schemas or write conclusions. Every analytical row keeps a stable source-row ID. Every conclusion cites a source, an as-of date, a sample definition, an evidence level, and a limitation.

## Three evidence layers

```text
raw/        immutable observations and source metadata
   ↓
analysis/   cleaned fields, coding, derived metrics, reproducible tables
   ↓
audit/      research contract, exclusions, quality report, claim ledger, reviews
```

Never overwrite a raw field with an interpretation. Derived columns belong in `analysis/`. Judgments belong in `audit/` and must point back to row IDs.

## L1–L5 evidence levels

Grade each supporting item and each written claim.

| Level | Name | What counts | Typical home |
|---|---|---|---|
| **L1** | Direct observation | A captured post, comment, official rule page, export row, or screenshot stored in `raw/` with URL or capture reference, collection timestamp, and stable ID. You can point to the artifact. | `raw/` |
| **L2** | Transparent extraction | Fields copied or parsed from L1 without added meaning: `posted_at`, a visible count, a sponsorship label present or absent, search-result position, author ID. | `analysis/` extracts |
| **L3** | Sample statistic | A count, median, quartile, share, heavy-tail ratio, or Cohen's kappa computed from a defined sample of L2 rows. Report *n*, the frame, and missingness. | `analysis/` tables |
| **L4** | Pattern diagnosis | An interpretive claim (author consistency, hotspot association, track-health explanation) that cites L3 patterns plus explicit counterexamples. Write “associated in this sample,” not “caused,” unless the design supports causality. | `audit/` ledger |
| **L5** | Extra-sample or decision claim | A recommendation, forecast, platform-wide prevalence statement, GMV or profit estimate, or any claim that goes beyond the frozen sample. Not licensed as a sample fact. Default status: `not-established` unless `references/decision-validation.md` promotion gates are met. | `audit/` queue |

A stronger sentence cannot sit on weaker evidence. An L4 sentence needs L3 numbers; those numbers need L2 fields; those fields need L1 artifacts.

## Required fields

Extra columns are fine. Missing required fields must be listed in the research contract and the quality report.

**Posts.** `item_id`, `platform`, URL or capture reference, `author_id`, `posted_at`, `collected_at`, `source`, caption or title reference, metric columns each labeled as `cumulative`, `windowed`, `fixed-age`, `estimated`, or `unknown`. Record `search_result_position` separately from post performance. Optional but useful: format, content type, hotspot flag.

**Authors.** `author_id`, `platform`, profile reference, size or role band if you stratify on it, number of posts in the sample, `collected_at`.

**Comments.** `comment_id`, parent `item_id`, `collected_at`, sampling depth, sort mode, visible or top-level status, and source-post coverage. Keep raw text in `raw/`. Strip usernames, regions, and unnecessary timestamps from public `analysis/` or deliverable tables.

**Rules and official pages.** `rule_id`, `platform`, official URL, as-of or effective date, captured excerpt or content hash, `collected_at`.

**Commercial cases.** A stable case ID, platform, the commercial-path level (1–4 in `SKILL.md` section 9), the observed marker, and whether level-4 proof (order, revenue, contract) is present or absent.

## Claim ledger

Keep a ledger in `audit/` (CSV or table). Suggested columns:

| Column | Role |
|---|---|
| `claim_id` | Stable ID |
| `claim` | One sentence |
| `status` | `fact` / `inference` / `hypothesis` / `not-established` / `rejected` / `downgraded` |
| `evidence_level` | L1–L5 |
| `source_ids` | Raw or analysis row IDs |
| `sample_definition` | Frame, platforms, window |
| `counterevidence` | Named rows or “none observed” |
| `confidence` | Bound to the sample; not a platform-wide score |
| `limitation` | What the sample cannot support |

**State machine.** New claims start as `hypothesis`. Promote to `fact` only with L1–L3 support and no contradiction. Promote to `inference` only with an L3+ pattern, a stated limitation, and counterexamples considered. Move to `not-established` when a minimum supporting pattern is missing (give the exact missing data). Move to `rejected` when named counterevidence contradicts the claim. Move to `downgraded` after review finds overclaim. Majority vote does not erase a valid counterexample. Never silently recode an L5 decision sentence as a `fact`.

A worked synthetic ledger is in `examples/claim-ledger.csv`.

## Cannot infer A → B

These substitutions are out of bounds even when they look convenient:

| Observed (A) | Does not prove (B) |
|---|---|
| Search-result position or rank | Exposure, reach, or recommendation distribution |
| Cumulative likes, views, saves, or comments | Fixed-age performance, or that newer posts are “in decline” |
| Likes-per-day | Exposure or completion normalization |
| A purposive search sample | Platform prevalence |
| One viral post, or a handful of weak posts | The character of a whole track (赛道) |
| Hotspot-linked outperformance in this sample | The hotspot *caused* the spike |
| Visible brand mention or sponsorship-like text | A paid deal, official campaign, or conversion |
| Official cooperation capability (path level 1) | Booked deals or profitability |
| Creator-stated cooperation or case result (path level 3) | Verifiable revenue, GMV, commission, or repeat purchase |
| Comment text such as “想看看”, “收藏了”, or similar save/intent language | A purchase |
| A question in comments | Negative sentiment |
| Comment-like counts | Public-opinion weights |
| Means without medians, quartiles, *n*, and author counts | A stable performance picture |

Commercial path (levels 1–3) shows that a path *exists*. It is not commercial *proof*. Never estimate deal size, GMV, commission, or demand from unsourced creator claims.

## Public outputs and identifiers

Before sharing tables, check that public deliverables do not contain raw personal identifiers from comments or private profile fields. `scripts/audit_csv.py` does not perform this privacy pass; reviewers do.
