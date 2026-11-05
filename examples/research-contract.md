# Example research contract (synthetic)

This is a **fictional** walkthrough contract for the fixture CSVs. It is not a
real study and cites no live creators.

## Decision to support

Decide whether a “beginner home-coffee gear” content track (赛道) on
Xiaohongshu (小红书 / XHS / RedNote) and Douyin (抖音), with a small TikTok
comparison slice, shows enough repeatable how-to and comparison demand to
justify further *descriptive* monitoring. This contract does **not** decide
whether anyone should start an account, run ads, or expect revenue.

## Platforms and as-of date

- Platforms: Xiaohongshu, Douyin, plus a single TikTok slice for format contrast.
- As-of date: 2026-10-01 (Asia/Shanghai, UTC+8).
- Collection window: posts dated 2026-08-01 through 2026-09-30 in the fixture.
- Unit of analysis: post as the primary row; author as a roll-up; comment as a
  separately coded layer.

## Sample frame

- Track map: audience (beginner home brewer) × problem (bitter taste, noise,
  limited counter space) × content value (clear how-to, honest comparison).
- Query families planned: audience, problem, product, value, risk, format.
- Inclusion: synthetic posts in `examples/fixtures/posts.csv` whose captions
  mention brewing, grinders, kettles, or tasting notes.
- Exclusion: live platform crawls; any row with a future `posted_at` from
  performance analysis (keep it in `raw/` and flag it in `audit/`).
- Required inclusions: none. All `author_demo_*` IDs are fictional.

## Metric definitions

- `like_count`, `comment_count`, `share_count` are labeled `cumulative` unless
  `metric_type` says otherwise.
- Cumulative totals mix age with performance. They are not fixed-age results.
- Search-result position is not in this fixture and will not be inferred from
  like counts.

## Claims the sample can support

- Descriptive counts, medians, and missingness for these 10 synthetic rows.
- A demonstration of future-date and non-finite (`NaN` / `inf`) audit flags.
- Dual-coding agreement on 8 synthetic comments, including known disagreements.

## Claims the sample cannot support

- Platform prevalence of home-coffee content on Xiaohongshu or Douyin.
- Causal statements such as “this hotspot caused a spike.”
- Track fatigue, format decline, or “the track is dead.”
- GMV, commission, or that a comment intent equals a purchase.
- That search rank equals exposure.

## Safety and scope

- Public-looking demo URLs use the reserved `example.invalid` host.
- No cookies, tokens, or live logins.
- No publishing, liking, following, or commenting.
- Comment tables contain no usernames, regions, or real timestamps.
