# Sampling and coding

Sample for distinction, not volume alone. Map the market as `audience × problem × content value` before you collect. Read this page before sampling authors, posts, or comments.

## Query families and quotas

Discover candidates from several query families, not from a single “爆款” or competitor keyword. Freeze a quota matrix in the research contract *before* collection so later digging cannot silently unbalance the sample.

| Family | What it is for | Example query style (fictional) |
|---|---|---|
| Audience (受众) | Who the content is for | beginner home-barista, small kitchen, gift buyer |
| Problem (问题) | The job or pain | bitter coffee, noisy grinder, limited counter space |
| Product (产品) | Named tools, SKUs, categories | hand grinder, pour-over kettle, capsule machine |
| Value (价值) | Promise or payoff | cafe taste at home, faster morning routine |
| Risk (风险) | Failure, waste, distrust | easy to break, hard to clean, overpriced |
| Format (体裁) | Form, not topic | demo, before/after, buying guide, review, tutorial |

Set and record a minimum share or count for each family you use. Include any creators the user named as *required inclusions or hypotheses*, then discover additional creators from these families and from high-performing posts. Do not treat the named list as the complete pool.

A worked fictional frame is in `examples/research-contract.md`.

## Stratification

After the `audience × problem × content value` map, stratify by:

- platform (for example Xiaohongshu / 小红书, Douyin / 抖音, TikTok);
- creator size or role;
- content type and format;
- time window;
- high-, middle-, and low-visible performance;
- hotspot-linked and non-hotspot content;
- repeat performers and one-hit outliers.

Record search-result position separately from post performance. Do not describe a purposive search sample as platform prevalence. Do not infer a track from a single viral post or a handful of weak posts.

## Author consistency

Compare repeated posts, not only the largest post. Report hit count, median, dispersion, and concentration. Distinguish sustained performance from one-hit concentration. Compare within-author before cross-author when possible.

Useful diagnostics (use medians and quartiles; do not rely on means alone):

- posts per author in the sample;
- within-author median and quartile range of the chosen metric;
- top-1 and top-3 share of that author's (or the sample's) metric total;
- hit count under a pre-registered threshold.

Label an author or format *direction* (rising, declining, stable) only when adjacent comparable windows each have at least four posts, age is not silently mixed into the metric, and preferably exposure or completion data exist. Cumulative likes in a recent window do not prove decline. Likes-per-day is a rough age diagnostic, not exposure normalization.

Fixed-age 7-day or 14-day panels remain an *unvalidated extension* (`references/decision-validation.md`). Do not make them the default path.

## Independent content coding

Use transparent content labels and keep `other/unclear`. Code the content itself separately from comments. Validate manual content coding on a stratified blind sample. Adjudicate disagreements only after independent passes; do not “fix” one coder while looking at the other's sheet.

## Independent comment coding

For comments:

- Minimize personal data. Remove usernames, regions, and unnecessary timestamps from public outputs. Example comment CSVs in this repository use synthetic IDs only.
- Record sampling depth, sorting mode, visible/top-level status, and source-post coverage.
- Balance comments across content types instead of collecting only from viral posts.
- Code these dimensions *separately*: demand/topic, sentiment, intent, and adoption barrier.
- Do not treat questions as negative sentiment.
- Do not treat comment-like counts as public-opinion weights.
- Do not infer a purchase from save- or browse-intent language such as “想看看” or “收藏了”.

For high-impact conclusions, use two independent coders. Adjudicate only disagreements. Compute agreement with `scripts/coder_agreement.py`.

Notes on that script (honor them when you interpret the JSON):

- Empty strings count as a label category; the script reports `empty_labels_a` / `empty_labels_b`.
- Both ID sets must match exactly; mismatched IDs are an error, not a silent inner join.
- Kappa is field-level overall agreement, not per-label presence/absence kappa.
- Kappa is `null` when fewer than two paired rows are available, or when it is otherwise undefined.

## Kappa gates

| Cohen's kappa | Publishing rule |
|---|---|
| *n* < 2 or otherwise undefined | Do not report a numeric kappa. Do not publish precise proportions from that field. |
| below 0.60 | Do not publish precise label proportions as stable results. |
| 0.60–0.79 | You may report proportions if you retain uncertainty and the sample boundary. |
| 0.80 or above | Still preserve the sample boundary. High agreement does not make the sample representative of the platform. |

Synthetic paired files for a walkthrough are in `examples/fixtures/coder_a.csv` and `coder_b.csv`.
