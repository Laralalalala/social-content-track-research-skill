---
name: social-content-market-research
description: "Build evidence-backed market research for social-content ecosystems such as Xiaohongshu (XHS, RedNote, 小红书), Douyin (抖音), TikTok, Bilibili, WeChat Channels (视频号), or similar platforms. Use for content-track / niche research (赛道研究), creator-landscape mapping, audience × problem × content-value segmentation, representative-account and post analysis, 30–90 day topic or format trends, author consistency, hot-event relationships, comment demand/sentiment coding with Cohen's kappa, social listening, platform distribution and rules, brand-cooperation patterns, commercialization paths versus commercial proof, track health, or opportunity validation. Also use when auditing or consolidating historical social-content research data. This is a method and audit layer: bring your own collectors, official exports, or authorized public APIs; it does not scrape or bypass platform controls. Do not use for ordinary copywriting, publishing, account operations, liking/commenting/following, or a generic question about one AI tool."
---

# Social Content Market Research

Produce auditable research that keeps raw observations, derived analysis, and judgment separate. Prefer a smaller defensible conclusion over a platform-wide claim unsupported by the sample.

This skill covers content-track research (赛道研究) on Xiaohongshu (XHS, RedNote, 小红书), Douyin (抖音), TikTok, and similar platforms. It is a method and audit layer with stdlib scripts and tests. It does not collect live platform data by itself.

## Route the task

Choose one or more modes:

1. **Evidence recovery**: inventory existing files, links, exports, screenshots, and historical datasets without turning old conclusions into current facts.
2. **Current landscape**: collect and analyze recent creator, post, comment, platform-rule, and commercial-path evidence.
3. **Decision validation**: test a bounded opportunity or positioning hypothesis. Read `references/decision-validation.md`; treat its unvalidated extensions as experiments, not default truth.

Do not silently change a market-landscape task into account positioning. Keep market findings separate from resource-fit or account-fit decisions unless the user explicitly requests both.

## 1. Freeze the research contract

Record:

- decision to support;
- platforms and as-of date;
- unit of analysis: result position, post, author, comment, rule, or commercial case;
- sample frame, queries, inclusion/exclusion rules, and time windows;
- metric definitions and known missing fields;
- claims the sample can and cannot support;
- safety constraints and authorized read/write scope.

If the user gives examples of creators, topics, or failure signals, treat them as required inclusions or hypotheses, not the complete candidate pool.

A filled-in fictional contract lives in `examples/research-contract.md`.

## 2. Collect data without requiring Agent Reach

This skill is a method and audit layer. It does **not** require `agent-reach` or any built-in collector. A study can be completed from manual CSV exports, official downloads, or a bring-your-own adapter. Read `references/collectors-and-adapters.md` and use `scripts/collectors/` when you need that interface.

Live collection is optional:

1. Prefer user-provided exports and official, public, authorized sources. Place them under `raw/` and run `scripts/audit_csv.py` before analysis.
2. If the separate `agent-reach` skill is installed, you MAY use it as one optional live-read adapter: read that skill, run `agent-reach doctor` before retrieval, and keep the safety rules below. If `agent-reach` is absent, do not block the workflow and do not invent a scraper.
3. To plug in another source, implement `CollectorAdapter` in `scripts/collectors/base.py`. `ManualCsvCollector` copies a user export. `ExampleApiCollectorStub` is documentation only (for example a licensed TikHub-like API you already use); it performs no network I/O.
4. Prefer official, public, authorized, and method-transparent sources.
5. Use an existing login state only for sparse, user-authorized reading. Never export credentials, cookies, tokens, or personal identifiers.
6. Do not automate publishing, liking, following, commenting, messaging, or account changes unless separately and explicitly authorized.
7. Do not scrape or use high-frequency, bulk, fixed-frequency, random-delay, backend-switching, proxy, or other behavior intended to evade platform controls or violate a platform's Terms of Service.
8. Stop new requests when risk controls, rate limits, verification prompts, or abnormal account behavior appear. Preserve already collected evidence and report the safe recovery path.

Manual user-opened pages may be read when authorized, but record that the sample is user-mediated and may be personalized.

## 3. Build three evidence layers

Create separate paths or sheets:

- `raw/`: immutable observations and source metadata;
- `analysis/`: cleaned fields, coding, derived metrics, and reproducible tables;
- `audit/`: method contract, exclusions, quality report, claim ledger, independent reviews, and limitations.

Never overwrite raw fields with interpretations. Every analytical row must retain a stable source-row ID. Every conclusion must link to a source, date, sample definition, evidence level, and limitation.

Read `references/evidence-and-claims.md` before defining schemas or writing conclusions.

## 4. Sample for distinction, not volume alone

Map the market as `audience × problem × content value`, then stratify by:

- platform;
- creator size or role;
- content type and format;
- time window;
- high-, middle-, and low-visible performance;
- hotspot-linked and non-hotspot content;
- repeat performers and one-hit outliers.

Include named required creators, but discover additional creators from multiple query families and high-performing posts. Record search-result position separately from post performance.

Do not describe purposive search samples as platform prevalence. Do not infer a track from a single viral post or a handful of weak posts.

Read `references/sampling-and-coding.md` before sampling authors, posts, or comments.

## 5. Audit data before analysis

For each dataset, check:

- row count and unique unit count;
- duplicate IDs and URLs;
- missingness by field;
- date coverage and future/invalid dates;
- metric type: cumulative, windowed, fixed-age, estimated, or unknown;
- sample selection and personalization risks;
- whether author, post, and comment joins are complete;
- whether public deliverables contain personal identifiers.

Run `scripts/audit_csv.py` for a first deterministic pass, then inspect domain-specific anomalies manually. `audit_csv.py` treats non-finite numbers (`NaN`, `inf`) as missing, flags future dates, and prints RFC 8259-valid JSON. It does not itself strip personal identifiers; reviewers still check public tables by hand.

## 6. Analyze content and author performance

Use medians, quartiles, sample sizes, and author counts. Add heavy-tail diagnostics such as top-1 and top-3 contribution shares. Do not rely on means alone.

For author consistency:

- compare repeated posts, not only the largest post;
- report hit count, median, dispersion, and concentration;
- distinguish sustained performance from one-hit concentration;
- compare within-author before cross-author when possible.

For change over time:

- cumulative likes, views, saves, or comments mix content age with performance;
- recent-window cumulative metrics do not prove decline;
- likes-per-day is only a rough age diagnostic, not exposure normalization;
- label author or format decline only with comparable fixed-age observations, adequate repeated samples, and preferably exposure or completion data.

For hotspots:

- define the event and event window;
- compare hotspot-linked and non-hotspot posts;
- retain low-performing hotspot counterexamples;
- separate product release, platform activity, public event, meme, and evergreen demand;
- write “associated in this sample,” not “caused,” unless the design supports causality.

## 7. Code content and comments independently

Use transparent content labels and preserve `other/unclear`. Validate manual content coding on a stratified blind sample.

For comments:

- minimize personal data; remove usernames, regions, and unnecessary timestamps from public outputs;
- record sampling depth, sorting mode, visible/top-level status, and source-post coverage;
- balance comments across content types instead of collecting only from viral posts;
- code demand/topic, sentiment, intent, and adoption barrier separately;
- do not treat questions as negative sentiment or comment likes as public-opinion weights;
- use two independent coders for high-impact conclusions and adjudicate only disagreements;
- compute agreement with `scripts/coder_agreement.py`.

If Cohen's kappa is below 0.60, do not publish precise label proportions as stable results. At 0.60–0.79, retain uncertainty. At 0.80 or above, still preserve the sample boundary. Kappa is undefined (null) when fewer than two paired rows are available.

## 8. Diagnose track health with competing explanations

Test these explanations separately:

| Diagnosis | Minimum supporting pattern |
|---|---|
| Track fatigue | Multiple authors and comparable content weaken across repeated comparable windows after sample shifts are considered |
| Format fatigue | The same format repeatedly underperforms alternatives within comparable authors/topics |
| Single-creator decline | One creator weakens across sufficient comparable windows, ideally with exposure/completion evidence |
| New demand | Repeated concrete problems appear across authors or platforms and in comments, not only in one viral title |
| Hotspot effect | Hotspot and non-hotspot differences coexist with explicit counterexamples and age/author controls |
| Homogeneity | Supply repeats the same promise, structure, asset, and audience problem; performance concentration alone is insufficient |

When minimum evidence is absent, write “not established” and give the exact missing data.

## 9. Separate commercial path from commercial proof

Distinguish:

1. official platform cooperation capability;
2. visible brand mention or sponsorship label;
3. creator-stated cooperation or case result;
4. verifiable order, revenue, cost, collection, repeat purchase, or contract evidence.

Levels 1–3 prove that a path exists, not its conversion rate or profitability. Never estimate deal size, GMV, commission, or demand from unsourced creator claims.

## 10. Challenge high-impact conclusions

For consequential work, give independent reviewers the same frozen evidence packet before they see one another's conclusions. Cover at least:

- method and sampling;
- platform and content interpretation;
- causal alternatives and counterexamples;
- commercialization and operational feasibility.

Require citations to evidence IDs or fields. A synthesis must retain dissent, downgraded claims, rejected claims, and unresolved tests; majority vote does not erase a valid counterexample.

## 11. Deliver and validate

Deliver:

- market map;
- raw-data inventory and source ledger;
- analytical tables with sample sizes;
- author/head-account continuity findings;
- topic, format, hotspot, comment-demand, and sentiment findings;
- platform/rule and commercial-path findings;
- claim ledger: fact, inference, counterevidence, confidence, limitation;
- risk and missing-data register;
- validation queue rather than a forced ranking when evidence is insufficient.

Validate row counts, joins, hashes, privacy fields, coder agreement, calculations, and report-to-table consistency. Clearly separate completed findings, hypotheses, and unknowns.

## Resources

- `references/evidence-and-claims.md`: L1–L5 evidence levels, claim boundaries, required schemas, and “cannot infer A → B” rules.
- `references/sampling-and-coding.md`: query-family quotas, author consistency, independent content/comment coding, and kappa gates.
- `references/decision-validation.md`: next-stage fixed-age, causal, and commercial validation extensions. They stay unvalidated until promotion gates are met.
- `references/collectors-and-adapters.md`: how to run this skill without `agent-reach`, plus the BYO collector contract.
- `scripts/audit_csv.py`: deterministic CSV structure and quality audit. Non-finite numbers are treated as missing; future dates are counted; output is always valid JSON.
- `scripts/coder_agreement.py`: exact agreement and Cohen's kappa for paired coding files. Kappa is null when n<2 or otherwise undefined.
- `scripts/collectors/`: optional collector adapters (`ManualCsvCollector` for user CSVs; licensed-API stub as an example only, no scraping).
- `tests/`: stdlib `unittest` suite for the audit, agreement, and collector scripts. Run `python3 -m unittest discover -s tests -v` from this skill directory.
- `examples/`: synthetic research-contract, claim-ledger, and fixture CSVs for a five-minute walkthrough. No real creators or private study data.
