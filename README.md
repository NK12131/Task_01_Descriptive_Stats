# Task 01: Descriptive Statistics
### 2024 Facebook Political Ads — Meta Ad Library

**Author:** Nithin Kumar

**Course:** IST Research Task 1  

---

## Project Description

This project performs descriptive statistical analysis on a dataset of **246,745 Facebook ads** from the 2024 U.S. Presidential election cycle. Each row is an ad purchase by an organization whose ad mentioned at least one presidential candidate. The dataset was sourced from the Meta Ad Library and enriched with 28 binary scored columns by the Illuminating Project, classifying ads by message type, call to action, topic, and incivility signals.

Two independent Python scripts analyze the same data:
- `pure_python_stats.py` — uses **only the Python standard library** (no pandas/numpy)
- `pandas_stats.py` — uses **Pandas** for equivalent analysis with visualizations

The comparison between them is the core intellectual exercise of the task.

---

## Dataset

**File:** `fb_ads_president_scored_anon.csv`  
**Shape:** 246,745 rows × 40 columns  
**Source:** Provided via Google Drive by course instructor  

> ⚠️ Do NOT commit the dataset to GitHub. Download it from the provided Drive link and place it in the project root directory before running scripts.

### Column Overview

| Column Group | Columns | Notes |
|---|---|---|
| Identifiers | `page_id`, `ad_id` | Anonymized |
| Categorical | `page_name`, `bylines`, `currency`, `publisher_platforms` | |
| Dates | `ad_creation_time`, `ad_delivery_start_time`, `ad_delivery_stop_time` | YYYY-MM-DD strings |
| Dict-strings | `spend`, `impressions`, `estimated_audience_size` | Stored as `{'lower_bound': '...', 'upper_bound': '...'}` — must be parsed |
| Binary scored | `illuminating_*` (28 columns) | 0/1 flags for message type, topic, incivility |

---

## Setup

### 1. Clone the repo and enter the directory
```bash
git clone https://github.com/<your-username>/Task_01_Descriptive_Stats.git
cd Task_01_Descriptive_Stats
```

### 2. Place the dataset
```
Task_01_Descriptive_Stats/
├── fb_ads_president_scored_anon.csv   ← place here
├── pure_python_stats.py
├── pandas_stats.py
...
```

### 3. Install dependencies (Pandas script only)
```bash
pip install -r requirements.txt
```

`pure_python_stats.py` requires **no installation** — only the Python standard library.

---

## Running the Scripts

### Pure Python (no dependencies)
```bash
python pure_python_stats.py
# or specify the file explicitly:
python pure_python_stats.py --file fb_ads_president_scored_anon.csv
```
Expected runtime: ~25–35 seconds (246K rows, no C extensions)

### Pandas
```bash
python pandas_stats.py
# with visualizations:
python pandas_stats.py --save-plots
```
Expected runtime: ~3–5 seconds

Visualizations are saved to `./visualizations/`:
| File | Description |
|---|---|
| `01_spend_distribution.png` | Spend per ad histogram (linear + log scale) |
| `02_top_spenders.png` | Top 15 advertisers by total spend |
| `03_monthly_volume.png` | Monthly ad count with election event markers |
| `04_topic_prevalence.png` | Topic flag rates across all ads |
| `05_message_types.png` | Advocacy / attack / issue / image / CTA breakdown |

---

## Summary of Findings

Full narrative analysis: [FINDINGS.md](FINDINGS.md)

**Key insights:**

1. **Spending is highly concentrated.** The top 10 advertisers account for a disproportionate share of total spend. Below them is a very long tail of small spenders.

2. **The election calendar is visible in the data.** Monthly ad volume spikes around Super Tuesday (March), the first debate (June), Biden's withdrawal (July), the Harris-Trump debate (September), and peaks immediately before Election Day (November).

3. **Economy and governance dominate topic flags.** Among the 28 illuminating columns, `illuminating_topic_economy` and `illuminating_topic_governance` are flagged most frequently — consistent with the dominant voter concerns of the 2024 cycle.

4. **Advocacy is the most common message type**, followed by issue-based messaging. Attack ads represent a meaningful minority of the total.

5. **Spend distribution is sharply right-skewed.** The median spend per ad (lower bound) is far below the mean, driven by a small number of very high-spend placements.

---

## Approach Comparison

Full reflection: [COMPARISON.md](COMPARISON.md)

The three `spend` / `impressions` / `estimated_audience_size` columns required explicit parsing in both scripts — they are stored as dict-strings, not numbers. Pandas would have returned no numeric statistics on these columns without the parsing step. Writing the pure Python version first made this parsing requirement unavoidable and forced explicit decisions about how to handle open-ended bounds (e.g., `{'lower_bound': '1000001'}`).

The main numerical difference between scripts: pure Python computes **population standard deviation** (divide by N); Pandas `.std()` computes **sample standard deviation** (divide by N−1). At 246,745 rows, this difference is negligible.

---

## Repository Structure

```
Task_01_Descriptive_Stats/
├── pure_python_stats.py      # Standard library only
├── pandas_stats.py           # Pandas + optional matplotlib/seaborn
├── requirements.txt          # pandas, numpy, matplotlib, seaborn
├── README.md                 # This file
├── FINDINGS.md               # 2-page narrative analysis
├── COMPARISON.md             # Pure Python vs Pandas reflection
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
- **Dataset file name:** `fb_ads_president_scored_anon.csv`
- After downloading, place the file in the project root directory alongside the scripts.
- Both scripts are deterministic — no random seeds needed. Running them twice on the same file produces identical output.

---

## Dependencies

| Package | Version | Required by |
|---|---|---|
| pandas | ≥ 2.0.0 | `pandas_stats.py` |
| numpy | ≥ 1.24.0 | `pandas_stats.py` |
| matplotlib | ≥ 3.7.0 | `pandas_stats.py --save-plots` (optional) |
| seaborn | ≥ 0.12.0 | `pandas_stats.py --save-plots` (optional) |

`pure_python_stats.py` has **zero external dependencies**.
