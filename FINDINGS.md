# FINDINGS.md
## Money, Messages, and the 2024 Presidential Race: What 246,745 Facebook Ads Reveal

**Author:** Nithin Kumar

**Task:** IST Research Task 1 — Descriptive Statistics

**Dataset:** `fb_ads_president_scored_anon.csv` — 246,745 rows × 40 columns

**Source:** Meta Ad Library (2024 U.S. Presidential Election cycle)

---

## What This Data Is

Each row represents a single Facebook ad purchase by an organization whose ad mentioned
one or more 2024 presidential candidates. The dataset spans from July 2021 through
Election Day on November 5, 2024 — a period of 1,218 days. It was scored by the
Illuminating Project, which added 28 binary flag columns classifying each ad's message
type, call to action, topics covered, and signals of incivility or election integrity
concerns.

Three columns — `spend`, `impressions`, and `estimated_audience_size` — are stored as
JSON-like range strings rather than exact numbers, reflecting Meta's policy of reporting
only bounds. All monetary figures in this report use lower-bound estimates and therefore
represent a floor on actual spending.

The dataset is remarkably complete. Of 12,090,505 total cells, only 5,484 are missing
(0.045%). The columns with any missingness are `ad_delivery_stop_time` (2,159 missing,
0.9%), `bylines` (1,009 missing, 0.4%), and `estimated_audience_size` (579 missing,
0.2%). Every other column is fully populated.

---

## The Scale of Spending

The 246,745 ads in this dataset represent a lower-bound total spend of **$227,487,000** —
over $227 million on Facebook advertising alone across a roughly three-year window. The
true total is higher since Meta reports only spend ranges.

The distribution of spend per ad is sharply right-skewed. The mean spend per ad is
**$921.95**, but the median is **$0** — meaning more than half of all ads (55.1%, or
135,950 ads) reported a lower-bound spend of zero. This is not an error; Meta's lowest
spend bucket reports $0 as its lower bound for very small purchases. The real story is in
the tail: 454 ads (0.2%) each spent $50,000 or more, and the single largest ad buy
reached **$450,000**.

This creates a distribution where a tiny number of massive placements coexist with a sea
of micro-targeted, low-cost ads. The $0 and $100–$499 buckets together account for 77% of
all ads, while just 2.1% of ads account for spend above $5,000.

---

## Who Spent the Money

Spending concentration is extreme. The **single top advertiser accounts for 32.0% of all
spending**. The top 10 advertisers account for **63.7%**, and the top 50 account for
**83.1%**. Below that threshold, thousands of organizations each contributed a tiny
fraction of the total.

The top 15 spenders tell a clear story about the 2024 race:

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
| 10 | Robert F. Kennedy, Jr | 2,005 | $2,529,800 | $1,262 |

Kamala Harris's official page alone spent nearly $73 million in lower-bound Facebook ad
spend — more than four times Trump's $16.8 million. However, Trump ran more ads (23,988
vs Harris's 55,503 for a lower average of $700 vs $1,313), suggesting different strategic
approaches: Harris ran fewer but larger placements; Trump ran high volume at lower cost.

Joe Biden at rank 2 ($23.4 million) reflects his role as the presumptive nominee before
withdrawing in July 2024. Combined, Biden and Harris represent the Democratic digital
footprint across the full cycle at over $96 million.

**The Daily Scroll** at rank 6 is analytically interesting — not a candidate or party
committee, but an obscure Facebook page that spent over $5 million. This reflects how
campaign dollars are routed through non-obvious affiliated pages, a practice that
complicates transparency in political advertising.

**Future Forward** (rank 7, $3,164 avg) and **America PAC** (rank 9, $2,317 avg)
represent Super PAC spending on both sides. Despite fewer total ads, both had very high
average spend per ad, indicating larger placements targeting specific swing audiences.

---

## The Election Calendar in the Data

Monthly ad volume tracks the 2024 campaign with remarkable precision. Activity before
2023 was negligible. Volume built through late 2023, then accelerated sharply:

| Month | Ads | Spend (LB) | Event |
|---|---|---|---|
| 2024-06 | 12,325 | $12,033,600 | Trump-Biden Debate |
| 2024-07 | 17,673 | $27,653,900 | Biden withdraws |
| 2024-08 | 33,777 | $29,985,500 | Democratic National Convention |
| 2024-09 | 35,893 | $38,715,100 | Trump-Harris Debate |
| 2024-10 | (peak) | (peak) | Final campaign push |
| 2024-11 | ends | ends | Election Day (Nov 5) |

The jump from June to July (+43% in ad volume, +130% in spend) marks Biden's withdrawal
as the single most disruptive event in the timeline. July's $27.6 million more than
doubled June's $12 million in a single month. September's $38.7 million is the highest
single-month spend in the dataset, coinciding with the Trump-Harris debate and the final
campaign stretch.

---

## What Ads Were Saying

The five most prevalent content flags across all 246,745 ads:

| Flag | Count | % of Ads |
|---|---|---|
| Call to action (CTA) | 141,328 | 57.3% |
| Advocacy messaging | 135,372 | 54.9% |
| Issue-based messaging | 94,170 | 38.2% |
| Attack messaging | 67,079 | 27.2% |
| Fundraising CTA | 56,378 | 22.8% |

More than half of all ads contained a call to action and were classified as advocacy.
Attack ads appeared in over one in four ads (27.2%) — a substantial presence reflecting
the intensely negative tone of the 2024 campaign.

**Incivility** was flagged in 46,271 ads (18.8%) — nearly one in five. **Scam indicators**
appeared in 17,675 ads (7.2%), and **election integrity concerns** in 12,359 ads (5.0%).

Among policy topics, **economy** (12.2%) and **health** (10.9%) were most prevalent,
followed by **social and cultural issues** (10.6%) and **women's issues** (8.1%).
Immigration appeared in only 3.4% of ads — surprisingly low given its dominance in media
coverage of the campaign. This suggests immigration was used more as a debate talking
point than a Facebook advertising strategy.

Notably, **69.5% of ads were flagged for zero policy topics**, meaning most ads were
classified by message type and CTA rather than substantive policy content.

---

## What Surprised Me

**The median spend is $0.** The mean ($921.95) and median ($0) are so far apart that
neither number alone gives an accurate picture — the classic sign of extreme skew.

**Harris outspent Trump by more than 4 to 1 on Facebook.** $72.9M vs $16.8M in
lower-bound spend from official pages alone. This is one of the starkest asymmetries in
the dataset.

**7.2% of ads showed scam indicators.** Nearly 18,000 ads in a presidential election
dataset were flagged as potential scams — a significant integrity concern suggesting a
meaningful fraction of political-adjacent Facebook advertising may be designed to mislead
donors.

**The `scored_message` and `mentions` columns are entirely null.** Both have 246,745
missing values — these two illuminating columns were never populated in this version of
the dataset. Any analysis relying on them would silently return nothing.

---

## Limitations

All spend figures use lower bounds — true totals are higher. The dataset covers only ads
mentioning presidential candidates, excluding Senate races, ballot measures, and
issue-only advertising. Illuminating scores are model-generated classifications carrying
inherent error. Despite these limitations, this dataset is one of the most detailed
publicly available records of digital political advertising from the 2024 election cycle.
