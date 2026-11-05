# 社媒内容赛道证据研究

Evidence-backed content-track research for social platforms (Xiaohongshu / XHS / 小红书, Douyin / 抖音, TikTok, and more).

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](scripts/)
[![Tests](https://img.shields.io/badge/tests-unittest-green.svg)](tests/)

> 给 Agent 用的小红书 / 抖音 / TikTok 内容赛道研究契约：分层抽样、证据分级、评论双编码与 kappa、商业路径≠成交证明。这是方法与审计层，请自带合规采集器或官方导出。

**GitHub About (paste into the repository description, ≤160 characters):**

> Evidence-backed social content-track research (Xiaohongshu, Douyin, TikTok & more): sampling, claim audit, Cohen's kappa. Method layer—BYO collectors.

A method and audit layer for Xiaohongshu, Douyin, and TikTok content-track research: freeze the sample, grade evidence, measure coder agreement, and keep commercial paths distinct from commercial proof. Bring your own collectors.

Skill slug (Codex / Agent Skills folder name): `social-content-market-research`.  
This repository may be published as `social-content-track-research-skill`. The skill itself lives at the **repository root** (`SKILL.md` here). Install by copying this directory to `~/.codex/skills/social-content-market-research`.

## 这是什么 / What this is

一套可审计的 **11 步研究契约**，用来做内容生态、作者持续性、热点关系、评论需求/情绪、平台规则与商业化路径的赛道研究（content-track / niche research），而不是先扒一堆「爆款」再事后解释。

- 先冻结研究合同，再采集或导入数据。
- 三个证据层：`raw/`（原观测）/ `analysis/`（清洗与计算）/ `audit/`（合同、质量报告、claim ledger）。
- L1–L5 证据分级，以及明确的「不能从 A 推到 B」边界。
- 按 `受众 × 问题 × 内容价值` 分层抽样；作者持续性看中位数、四分位、Top-1 / Top-3，而不是只报均值。
- 评论需求、情绪、意图、采纳障碍独立编码，并用 Cohen's kappa 设发布门槛。
- 赛道健康度用竞争性解释；证据不够就写「not established」。
- **商业路径 ≠ 商业证明**：官方合作能力 / 可见赞助 / 创作者自述 / 可核验成交，是四件不同的事。
- 附带两个 **只需 Python 标准库** 的脚本：`scripts/audit_csv.py`、`scripts/coder_agreement.py`，以及 `scripts/collectors/` 适配器接口。

It is the research-contract, sampling, coding, and audit layer for social-content ecosystems such as Xiaohongshu, Douyin, TikTok, Bilibili, and WeChat Channels (视频号). Scripts are stdlib-only: no `requirements.txt`.

## 这不是什么 / What this is not

| 不是 / Not | 说明 |
|---|---|
| 爬虫或采集器 / a scraper | 仓库不附带小红书、抖音、TikTok 的爬取代码，也不要求安装 `agent-reach`。 |
| 发布或运营工具 / a posting tool | 不做普通文案、发布、点赞、评论、关注、私信或改号。 |
| GMV 计算器 / a GMV estimator | 创作者自述或品牌露出不能倒推成交额、佣金或需求规模。 |
| 平台占比普查 / a census | 目的性搜索样本 ≠ 平台真实占比。 |

`agent-reach` 如果已经装在本机，可以当作**可选**的只读适配器；没装也不要停下来 invent 一个 scraper。请改用官方导出、用户自己打开的页面（并记录个性化风险），或你有权使用的授权 API。

Optional complements such as TikHub or SocialDataX are **paid third-party data services**. This skill does not bundle them, does not include affiliate links, and does not require them.

## 安装 / Install

需要 [Python 3.10+](https://www.python.org/)（标准库即可）和任一支持 Agent Skills 的运行时。没有额外 pip 依赖。

### Codex

```bash
git clone https://github.com/Laralalalala/social-content-track-research-skill.git
cp -R social-content-track-research-skill ~/.codex/skills/social-content-market-research
```

如果本地已经有这份目录（例如从压缩包解压）：

```bash
cp -R /path/to/social-content-track-research-skill ~/.codex/skills/social-content-market-research
```

目标文件夹名必须是 `social-content-market-research`，以便 `$social-content-market-research` 与 frontmatter `name` 一致。

### 其他 Agent Skills 路径 / Other runtimes

| Runtime | Copy the repo to |
|---|---|
| Codex | `~/.codex/skills/social-content-market-research` |
| Claude Code | `~/.claude/skills/social-content-market-research` |
| Other Agent Skills | `~/.agents/skills/social-content-market-research` |

### `npx skills add`

Once this repository is published under your GitHub account, catalogs that speak the Agent Skills installer can add it with:

```bash
npx skills add Laralalalala/social-content-track-research-skill
```

If the installer asks for a skill slug (frontmatter `name`):

```bash
npx skills add Laralalalala/social-content-track-research-skill --skill social-content-market-research
```

Replace `Laralalalala` with the GitHub user or organization that publishes the repo. This package is the skill; there is no inner nested skill folder.

### 触发示例 / Trigger examples

```text
用 $social-content-market-research 研究一下这个小红书 / 抖音家用咖啡器具赛道，先冻结研究合同和样本框。
```

```text
Use $social-content-market-research to build an evidence-backed Xiaohongshu and Douyin content-track study with raw, analysis, and audit layers.
```

### 自检脚本 / Verify the scripts

```bash
cd ~/.codex/skills/social-content-market-research   # or this clone
python3 -m unittest discover -s tests -v
```

## 五分钟走查 / 5-minute walkthrough

All demo rows are **synthetic**. Author IDs look like `author_demo_01`. There are no real creators, comments, or private study data.

A filled-in fictional contract is in [`examples/research-contract.md`](examples/research-contract.md) (home-coffee gear on Xiaohongshu + Douyin, as-of 2026-10-01, Asia/Shanghai). Compare a careful vs. overclaimed sentence in [`examples/good-vs-bad-conclusions.md`](examples/good-vs-bad-conclusions.md).

### 1. Audit a messy CSV

`examples/fixtures/posts.csv` includes a `NaN`, an `inf`, a mixed `not-a-number` cell, an empty comment count, and a future date `2099-01-01`.

```bash
python3 scripts/audit_csv.py examples/fixtures/posts.csv \
  --id-field item_id \
  --date-field posted_at \
  --numeric-field like_count \
  --numeric-field comment_count
```

You should see RFC 8259 JSON (no `NaN` / `Infinity` tokens) roughly like:

```json
{
  "row_count": 10,
  "date_audit": {
    "future": 1,
    "invalid": 0,
    "valid": 10,
    "minimum": "2026-08-02T00:00:00",
    "maximum": "2099-01-01T00:00:00"
  },
  "numeric_audit": {
    "like_count": {
      "valid": 7,
      "invalid": 1,
      "invalid_examples": ["not-a-number"],
      "nonfinite": 2,
      "missing": 2,
      "minimum": 15.0,
      "median": 45.0,
      "maximum": 800.0
    }
  }
}
```

`path` in the live output is an absolute path on your machine. Future dates are counted; non-finite likes are folded into `missing` and excluded from quartiles.

### 2. Measure coder agreement

`examples/fixtures/coder_a.csv` and `coder_b.csv` share eight synthetic comment IDs. They disagree on one `demand` row and one `sentiment` row.

```bash
python3 scripts/coder_agreement.py \
  examples/fixtures/coder_a.csv \
  examples/fixtures/coder_b.csv \
  --id-field comment_id \
  --field demand \
  --field sentiment \
  --field intent \
  --field barrier
```

Expected agreement (rounded):

| Field | Exact agreement | Cohen's kappa |
|---|---:|---:|
| `demand` | 7/8 = 0.875 | 0.849 |
| `sentiment` | 7/8 = 0.875 | 0.810 |
| `intent` | 8/8 = 1.0 | 1.0 |
| `barrier` | 8/8 = 1.0 | 1.0 |

Both disputed fields sit at or above 0.80, so precise proportions may be reported **for this sample only**. Kappa below 0.60 would block publishing precise label shares; 0.60–0.79 would keep explicit uncertainty. Kappa is `null` when fewer than two paired rows exist.

### 3. Read the claim ledger

[`examples/claim-ledger.csv`](examples/claim-ledger.csv) spans L1–L5 and the statuses `fact`, `inference`, `rejected`, and `not-established`, including four “cannot infer” rows: search rank ≠ exposure; a future-dated row ≠ performance; gift/save language ≠ purchased; brand mention ≠ paid deal.

## 方法要点 / Method spine

The 11 steps live in [`SKILL.md`](SKILL.md). Short map:

1. Freeze the research contract.
2. Collect without requiring `agent-reach` (manual CSV default).
3. Build `raw/` · `analysis/` · `audit/`.
4. Sample `audience × problem × content value`; use several query families.
5. Audit before analysis (`scripts/audit_csv.py`).
6. Report medians, quartiles, *n*, author counts, and heavy tails — not means only.
7. Code content and comments independently; apply kappa gates.
8. Diagnose track health with competing explanations.
9. Separate commercial path from commercial proof.
10. Challenge high-impact conclusions with an independent review packet.
11. Deliver a claim ledger and a validation queue, not a forced ranking.

Details: [`references/evidence-and-claims.md`](references/evidence-and-claims.md) (L1–L5), [`references/sampling-and-coding.md`](references/sampling-and-coding.md), [`references/decision-validation.md`](references/decision-validation.md) (7/14-day fixed-age panels, matching, demand tests, and transaction proof stay **unvalidated extensions**), [`references/collectors-and-adapters.md`](references/collectors-and-adapters.md).

### 术语 / Glossary

| 中文 | English | Do not confuse with |
|---|---|---|
| 赛道 | content track / niche | a single viral post |
| 对标 | structured comparison against named accounts | proof that you can replicate their results |
| 商业路径 | a visible way money *could* move (official coop, sponsor label, creator statement) | 成交证明 / verified orders or revenue |
| 想看看 / 收藏了 | browse or save intent in a comment | a purchase |

## 数据采集怎么接 / Collector options

| Source | When to use it | Notes |
|---|---|---|
| Official export or a spreadsheet the user already has | Default | Copy into `raw/` with `ManualCsvCollector` or by hand, then run `audit_csv.py`. |
| A page the user opened themselves | Sparse, authorized reading | Record that the sample may be personalized. |
| Optional `agent-reach` skill, if installed | Live read adapter | Run `agent-reach doctor` first. Not shipped here. |
| Licensed API you already pay for (examples: TikHub, SocialDataX) | Only with terms that cover the research use | Paid third parties; optional; no client is bundled. Implement `CollectorAdapter` yourself. |
| ToS-violating scraper, proxy pool, or cookie export | Never | Conflicts with the safety gate. |

From the skill root, import `ManualCsvCollector` by adding `scripts/` to `sys.path` (see the example in [`references/collectors-and-adapters.md`](references/collectors-and-adapters.md)). Do not run `from collectors...` without that path step.

Suggested first-pass columns:

```text
item_id,platform,url,author_id,posted_at,title_or_caption,like_count,comment_count,share_count,collected_at,source
```

## 安全 / Safety

- Public or user-authorized data only.
- Never export credentials, cookies, tokens, or unnecessary personal identifiers.
- Do not automate publishing, liking, following, commenting, messaging, or account changes.
- Stop when a captcha, rate limit, risk control, or abnormal account behavior appears.
- Do not rotate backends, proxies, or delays to evade platform controls.
- Minimize comment PII in public tables (the fixture comment files already use synthetic IDs only).

## GitHub topics

Suggested topics (≤20) when the repository is published:

`xiaohongshu`, `xhs`, `rednote`, `douyin`, `tiktok`, `content-research`, `market-research`, `social-listening`, `social-media-research`, `agent-skills`, `claude-skills`, `codex-skill`, `comment-analysis`, `creator-analytics`, `evidence-based`, `content-track`

Optional extras if there is room: `bilibili`, `wechat-channels`. Do not add crawler or scraper topics — they would mis-sell the safety posture.

## 许可 / License

[MIT](LICENSE). Copyright (c) 2026 Lara.

## 作者说明 / Authorship

The method was extracted on 2026-07-27 from a completed V2 content-track study (an AI-creator landscape project) and first installed locally as the Codex skill `social-content-market-research`. This public package ships the method, audit scripts, tests, and **synthetic** fixtures only. It does not include private datasets, screenshots, identifiable comments, or creator identities from that study.
