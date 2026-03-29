# Task 01: Descriptive Statistics
### 2024 Facebook Political Ads — Meta Ad Library

**Author:** Nithin Kumar

**Course:** IST Research Task 1

---

## Abstract

This project conducts a descriptive statistical analysis of 246,745 Facebook advertisements collected during the 2024 U.S. Presidential election cycle. Each record represents an ad purchase by an organization whose creative content referenced at least one presidential candidate. The dataset was sourced from the Meta Ad Library and enriched by the Illuminating Project with 28 binary classification flags denoting message type, call to action, thematic topic, and incivility signals. Two independent implementations — one using only the Python standard library (`pure_python_stats.py`) and one leveraging Pandas (`pandas_stats.py`) — were developed to perform equivalent analyses, enabling a methodological comparison of approaches.

---

## Dataset

**File:** `fb_ads_president_scored_anon.csv`  
**Shape:** 246,745 rows × 40 columns  
**Source:** Provided via Google Drive by course instructor

| Column Group | Columns | Notes |
|---|---|---|
| Identifiers | `page_id`, `ad_id` | Anonymized |
| Categorical | `page_name`, `bylines`, `currency`, `publisher_platforms` | |
| Dates | `ad_creation_time`, `ad_delivery_start_time`, `ad_delivery_stop_time` | YYYY-MM-DD strings |
| Dict-strings | `spend`, `impressions`, `estimated_audience_size` | Stored as `{'lower_bound': '...', 'upper_bound': '...'}` — requires parsing prior to analysis |
| Binary scored | `illuminating_*` (28 columns) | 0/1 flags for message type, topic, and incivility |

---

## Summary of Findings

Political ad spending across the 2024 election cycle exhibits sharp concentration: a small number of high-spending organizations account for a disproportionate share of total expenditure, while the vast majority of advertisers occupy a long, low-spend tail. This pattern is reflected in a markedly right-skewed spend distribution, where the median spend per ad (lower bound) falls well below the mean — an artifact of a handful of exceptionally high-spend placements inflating the average.

Temporal analysis reveals that monthly ad volume closely tracks the electoral calendar. Pronounced spikes correspond to Super Tuesday (March), the first presidential debate (June), President Biden's withdrawal from the race (July), the Harris-Trump debate (September), and a sustained peak in the weeks immediately preceding Election Day (November), underscoring the responsiveness of political advertising to campaign-defining events.

Among the 28 Illuminating Project classification flags, `illuminating_topic_economy` and `illuminating_topic_governance` register the highest prevalence, consistent with the policy concerns most prominent in public discourse during the 2024 cycle. At the message-type level, advocacy-oriented ads constitute the plurality of the dataset, followed by issue-based messaging; attack advertising, while present, represents a meaningful but secondary share of total volume.

For the full narrative analysis, see [FINDINGS.md](FINDINGS.md).

---

## Methodological Comparison

The three financial columns — `spend`, `impressions`, and `estimated_audience_size` — are stored as dict-strings rather than numeric values, requiring explicit bound extraction before any statistical computation. This parsing requirement surfaced unavoidably in the pure Python implementation, where no abstraction layer could obscure it. The Pandas implementation, without the parsing step, would have silently excluded these columns from all numeric summaries — a meaningful silent failure that the pure Python approach makes impossible.

One statistical discrepancy warrants acknowledgment: the pure Python script computes population standard deviation (dividing by N), whereas Pandas `.std()` applies Bessel's correction and computes sample standard deviation (dividing by N−1). At a sample size of 246,745, the practical difference between the two is negligible.

For the full methodological reflection, see [COMPARISON.md](COMPARISON.md).

---

## Repository Structure

```
Task_01_Descriptive_Stats/
├── pure_python_stats.py      # Standard library only
├── pandas_stats.py           # Pandas + optional matplotlib/seaborn
├── requirements.txt          # pandas, numpy, matplotlib, seaborn
├── README.md                 # This file
├── FINDINGS.md               # Full narrative analysis
├── COMPARISON.md             # Pure Python vs. Pandas reflection
└── visualizations/           # Auto-created by --save-plots
    ├── 01_spend_distribution.png
    ├── 02_top_spenders.png
    ├── 03_monthly_volume.png
    ├── 04_topic_prevalence.png
    └── 05_message_types.png
```

---

## Data Source & Reproducibility

- **Dataset link:** *(insert Google Drive link provided by instructor)*
- **Filename:** `fb_ads_president_scored_anon.csv` — place in the project root alongside the scripts
- Both scripts are fully deterministic. No random seeds are required; repeated execution on the same input file produces identical output.

---

## Dependencies

| Package | Version | Required by |
|---|---|---|
| pandas | ≥ 2.0.0 | `pandas_stats.py` |
| numpy | ≥ 1.24.0 | `pandas_stats.py` |
| matplotlib | ≥ 3.7.0 | `pandas_stats.py --save-plots` (optional) |
| seaborn | ≥ 0.12.0 | `pandas_stats.py --save-plots` (optional) |

`pure_python_stats.py` has **zero external dependencies**.
