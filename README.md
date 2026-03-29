# Task 01: Descriptive Statistics
### 2024 Facebook Political Ads — Meta Ad Library

**Author:** Nithin Kumar
**Course:** IST Research Task 1

---

## What This Project Does

This project takes a close look at **246,745 Facebook ads** from the 2024 U.S. Presidential election cycle — every row a real ad purchase by an organization whose ad mentioned at least one presidential candidate. The data comes from Meta's Ad Library, enriched by the Illuminating Project with 28 binary flags classifying each ad by message type, call to action, topic, and markers of incivility.

The analysis is split across two independent Python scripts that crunch the same dataset:

- **`pure_python_stats.py`** — built entirely from the Python standard library, no installs required
- **`pandas_stats.py`** — the faster, visualization-enabled version using Pandas and Matplotlib

Both scripts produce the same findings. The side-by-side comparison is intentional — it's a chance to see what each approach forces you to think about explicitly.

---

## The Dataset

**File:** `fb_ads_president_scored_anon.csv`
**Shape:** 246,745 rows × 40 columns
**Source:** Provided via Google Drive by course instructor

| Column Group | Columns | Notes |
|---|---|---|
| Identifiers | `page_id`, `ad_id` | Anonymized |
| Categorical | `page_name`, `bylines`, `currency`, `publisher_platforms` | |
| Dates | `ad_creation_time`, `ad_delivery_start_time`, `ad_delivery_stop_time` | YYYY-MM-DD strings |
| Dict-strings | `spend`, `impressions`, `estimated_audience_size` | Stored as `{'lower_bound': '...', 'upper_bound': '...'}` — must be parsed before analysis |
| Binary scored | `illuminating_*` (28 columns) | 0/1 flags for message type, topic, and incivility |

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/Task_01_Descriptive_Stats.git
cd Task_01_Descriptive_Stats
```

### 2. Place the dataset

Drop the CSV file into the project root — right alongside the scripts:

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

The pure Python script needs nothing beyond a standard Python installation.

---

## Running the Scripts

### Pure Python

```bash
python pure_python_stats.py
# or specify the file explicitly:
python pure_python_stats.py --file fb_ads_president_scored_anon.csv
```

Expect a runtime of roughly **25–35 seconds** on the full 246K-row dataset — no C extensions means it does the work the hard way.

### Pandas

```bash
python pandas_stats.py
# with visualizations:
python pandas_stats.py --save-plots
```

Substantially faster at **3–5 seconds**. The `--save-plots` flag writes five charts to `./visualizations/`:

| File | What It Shows |
|---|---|
| `01_spend_distribution.png` | Per-ad spend histogram, both linear and log scale |
| `02_top_spenders.png` | Top 15 advertisers ranked by total spend |
| `03_monthly_volume.png` | Monthly ad count with key election events marked |
| `04_topic_prevalence.png` | How often each topic flag appears across all ads |
| `05_message_types.png` | Breakdown of advocacy, attack, issue, image, and CTA ads |

---

## What the Data Shows

Full narrative analysis: [FINDINGS.md](FINDINGS.md)

- **Spending is extremely concentrated.** A handful of top advertisers account for a disproportionate share of total spend, with everyone else forming a very long tail of small placements.

- **The election calendar is visible in the data.** Monthly ad volume spikes around Super Tuesday (March), the June debate, Biden's July withdrawal, the Harris-Trump September debate, and peaks sharply in the final days before November.

- **Economy and governance lead topic coverage.** The `illuminating_topic_economy` and `illuminating_topic_governance` flags are the most frequently triggered — a clean reflection of the issues voters cared most about in 2024.

- **Advocacy ads dominate.** Issue-based messaging comes second. Attack ads make up a meaningful minority of the total.

- **Spend distributions are sharply right-skewed.** The median spend per ad sits well below the mean — a small number of very high-spend placements pull the average up considerably.

---

## Pure Python vs. Pandas: What the Comparison Reveals

Full reflection: [COMPARISON.md](COMPARISON.md)

The three financial columns — `spend`, `impressions`, and `estimated_audience_size` — are stored as dict-strings, not numbers. Both scripts require an explicit parsing step before any statistics can be computed.

Writing the pure Python version first made this unavoidable; there was no way to accidentally skip it. Pandas, by contrast, would have silently returned nothing on those columns without the parsing step — a good reminder that a tool doing less work for you isn't always a disadvantage.

One numerical difference worth noting: pure Python computes **population standard deviation** (÷ N) while Pandas `.std()` defaults to **sample standard deviation** (÷ N−1). At 246,745 rows, the difference is negligible in practice.

---

## Repository Structure

```
Task_01_Descriptive_Stats/
├── pure_python_stats.py      # Standard library only
├── pandas_stats.py           # Pandas + optional matplotlib/seaborn
├── requirements.txt          # pandas, numpy, matplotlib, seaborn
├── README.md                 # This file
├── FINDINGS.md               # 2-page narrative analysis
├── COMPARISON.md             # Reflection on the two approaches
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
- Both scripts are fully deterministic — no random seeds needed. Running them twice on the same file produces identical output.

---

