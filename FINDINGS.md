# FINDINGS.md
## Money, Messages, and the 2024 Presidential Race: What 246,745 Facebook Ads Reveal

**Author:** Nithin Kumar

**Task:** IST Research Task 1 — Descriptive Statistics

**Dataset:** `fb_ads_president_scored_anon.csv`  246,745 rows × 40 columns

**Source:** Meta Ad Library (2024 U.S. Presidential Election cycle)

---

## What This Data Is

Each row represents a single Facebook ad purchase by an organization whose creative content referenced one or more 2024 presidential candidates. The dataset spans July 2021 through Election Day on November 5, 2024, a 1,218-day window. It was scored by the Illuminating Project, which appended 28 binary flag columns that classify each ad's message type, call to action, policy topics, and signals of incivility or election integrity concerns.

Three columns,  `spend`, `impressions`, and `estimated_audience_size` are stored as JSON-like range strings rather than exact figures, reflecting Meta's policy of disclosing only bounds. All monetary figures in this report use lower-bound estimates and therefore represent a floor on actual expenditure; true totals are higher throughout.

The dataset is remarkably complete. Of 12,090,505 total cells, only 5,484 are missing (0.045%). Missingness is concentrated in three columns: `ad_delivery_stop_time` (2,159 missing, 0.9%), `bylines` (1,009 missing, 0.4%), and `estimated_audience_size` (579 missing, 0.2%). Every remaining column is fully populated. One structural anomaly warrants note: the `scored_message` and `mentions` columns carry 246,745 missing values each — both are entirely unpopulated in this version of the dataset and cannot be used in any analysis.

---

## The Scale and Distribution of Spending

The 246,745 ads in this dataset represent a lower-bound total spend of **$227,487,000**  over $227 million on Facebook advertising across roughly three years. The true total is necessarily higher.

The per-ad spend distribution is sharply right-skewed. The mean is **$921.95**, while the median is **$0**,  meaning more than half of all ads (55.1%, or 135,950 ads) reported a lower-bound spend of zero. This is not a data quality issue; Meta's lowest spend bucket reports $0 as its lower bound for very small purchases. The substantive story lies in the upper tail: 454 ads (0.2%) each carried a spend of $50,000 or more, and the single largest placement reached **$450,000**.

The result is a bimodal landscape, a vast mass of micro-targeted, low-cost ads coexisting with a small number of very large placements. The $0 and $100–$499 buckets together account for 77% of all ads, while just 2.1% of ads account for all spending above $5,000. When the mean and median are this far apart, neither figure alone accurately characterizes the distribution; they must be read together.

---

## Concentration of Spending

Spending is highly concentrated among a small number of advertisers. The single top spender accounts for **32.0% of all lower-bound expenditure**. The top 10 advertisers collectively account for **63.7%**, and the top 50 for **83.1%**. Below that threshold, thousands of organizations each contributed a marginal share of the total.

The top 15 spenders reflect the structure of the 2024 race directly:

| Rank | Page Name | Ads | Total Spend (LB) | Avg per Ad |
|---|---|---|---|---|
| 1 | Kamala Harris | 55,503 | $72,902,800 | $1,313 |
| 2 | Joe Biden | 14,822 | $23,357,200 | $1,576 |
| 3 | Donald J. Trump | 23,988 | $16,795,100 | $700 |
| 4 | Kamala HQ | 7,564 | $7,076,300 | $936 |
| 5 | Tim Walz | 6,581 | $6,670,300 | $1,014 |
| 6 | The Daily Scroll | 10,461 | $5,153,500 | $493 |
| 7 | Future Forward | 1,210 | $3,828,500 | $3,164 |
| 8 | Barack Obama | 2,203 | $3,755,100 | $1,705 |
| 9 | America PAC | 1,243 | $2,880,400 | $2,317 |
| 10 | Robert F. Kennedy, Jr. | 2,005 | $2,529,800 | $1,262 |

Kamala Harris's official page alone accounts for nearly $73 million in lower-bound spend, more than four times Donald Trump's $16.8 million. The per-ad averages, however, suggest divergent strategic approaches: Harris ran fewer, larger placements ($1,313 average) while Trump prioritized volume at lower per-ad cost ($700 average). Combined, the Biden and Harris pages represent over $96 million in Democratic digital spend across the full cycle, reflecting the unusual dynamic of two successive nominees sharing a single dataset.

**The Daily Scroll** (rank 6, $5.2 million) is analytically notable, as it is neither a candidate committee nor a registered party organization, yet it ranks among the top spenders. This reflects the common practice of routing campaign expenditure through affiliated but non-obvious pages, a structural feature that complicates transparency in political advertising disclosures.

**Future Forward** (rank 7) and **America PAC** (rank 9) represent Super PAC activity on both sides of the race. Despite running comparatively few ads, both carry high average spend per placement ($3,164 and $2,317, respectively), consistent with large audience-targeted buys rather than broad-reach volume strategies.

---

## The Election Calendar in the Data

Monthly ad volume tracks the 2024 campaign with considerable precision. Activity before 2023 was negligible; volume built gradually through late 2023 before accelerating sharply in the spring and summer of 2024.

| Month | Ads | Spend (LB) | Associated Event |
|---|---|---|---|
| 2024-06 | 12,325 | $12,033,600 | Trump–Biden debate |
| 2024-07 | 17,673 | $27,653,900 | Biden withdrawal |
| 2024-08 | 33,777 | $29,985,500 | Democratic National Convention |
| 2024-09 | 35,893 | $38,715,100 | Trump–Harris debate |
| 2024-10 | peak | peak | Final campaign push |
| 2024-11 | ends | ends | Election Day (November 5) |

The transition from June to July represents the most abrupt single-month inflection in the dataset: a 43% increase in ad volume accompanied by a 130% increase in spend. Biden's withdrawal in July effectively restarted the Democratic campaign, and the data reflect that disruption clearly. September's $38.7 million marks the highest single-month spend in the dataset, coinciding with the Trump–Harris debate and the final campaign mobilization period.

---

## What the Ads Were Communicating

The five most prevalent content flags across all 246,745 ads are as follows:

| Flag | Count | % of Ads |
|---|---|---|
| Call to action (CTA) | 141,328 | 57.3% |
| Advocacy messaging | 135,372 | 54.9% |
| Issue-based messaging | 94,170 | 38.2% |
| Attack messaging | 67,079 | 27.2% |
| Fundraising CTA | 56,378 | 22.8% |

More than half of all ads carried both a call to action and an advocacy classification. Attack ads appeared in more than one in four placements (27.2%), a proportion consistent with the characteristically negative tone of the 2024 campaign.

Incivility was flagged in 46,271 ads (18.8%) — nearly one in five. Scam indicators appeared in 17,675 ads (7.2%), and election integrity concerns in 12,359 ads (5.0%). The scam indicator figure is particularly notable: nearly 18,000 ads in a presidential election dataset were classified as potentially deceptive, suggesting a meaningful share of political-adjacent Facebook advertising may be designed to mislead rather than persuade.

Among policy topics, **economy** (12.2%) and **health** (10.9%) were the most prevalent, followed by **social and cultural issues** (10.6%) and **women's issues** (8.1%). Immigration appeared in only 3.4% of ads — a conspicuously low figure given its prominence in campaign rhetoric and media coverage. This discrepancy suggests that immigration functioned primarily as a debate and earned-media strategy rather than a paid digital advertising priority.

Notably, **69.5% of ads were flagged for zero policy topics**, meaning the majority of placements were classified by message format and call-to-action type rather than by substantive policy content. Most Facebook political advertising in this dataset was mobilizational and transactional, not issue-driven.

---

## Limitations

All spend figures represent lower bounds; true totals are higher throughout. The dataset is scoped to ads referencing presidential candidates only, excluding Senate races, ballot measures, and issue-only advertising that did not name a candidate. Illuminating Project classifications are model-generated and carry inherent error rates. The `scored_message` and `mentions` columns are entirely unpopulated and cannot be analyzed. Despite these constraints, this dataset represents one of the most granular publicly available records of digital political advertising from the 2024 election cycle.
