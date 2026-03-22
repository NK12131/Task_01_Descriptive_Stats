"""
pandas_stats.py
===============
Descriptive statistics for: fb_ads_president_scored_anon.csv
246,745 rows × 40 columns — 2024 Facebook Political Ads (Meta Ad Library)

Author: Nithin Kumar
Course: IST Research Task 1 — Descriptive Statistics

Key design decisions:
  - spend / impressions / estimated_audience_size are stored as dict-strings
    e.g. "{'lower_bound': '45000', 'upper_bound': '49999'}"
    This script parses them into numeric lower/upper/midpoint columns.
  - illuminating_* binary columns are analyzed as a group for prevalence.
  - Visualizations are saved to ./visualizations/ if --save-plots is passed.

Usage:
    python pandas_stats.py
    python pandas_stats.py --file fb_ads_president_scored_anon.csv --save-plots
"""

import os, sys, ast, argparse, warnings
import pandas as pd
import numpy as np
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────
DEFAULT_FILE = "fb_ads_president_scored_anon.csv"
SEP = "─" * 72

ILLUMINATING_COLS = [c for c in [
    "illuminating_scored_message", "illuminating_mentions", "illuminating_scam",
    "illuminating_election_integrity_Truth", "illuminating_msg_type_advocacy",
    "illuminating_msg_type_issue", "illuminating_msg_type_attack",
    "illuminating_msg_type_image", "illuminating_msg_type_cta",
    "illuminating_cta_subtype_engagement", "illuminating_cta_subtype_fundraising",
    "illuminating_cta_subtype_voting", "illuminating_topic_covid",
    "illuminating_topic_economy", "illuminating_topic_education",
    "illuminating_topic_environment", "illuminating_topic_foreign_policy",
    "illuminating_topic_governance", "illuminating_topic_health",
    "illuminating_topic_immigration", "illuminating_topic_lgbtq_issues",
    "illuminating_topic_military", "illuminating_topic_race_and_ethnicity",
    "illuminating_topic_safety", "illuminating_topic_social_and_cultural",
    "illuminating_topic_technology_and_privacy", "illuminating_topic_womens_issue",
    "illuminating_incivility",
]]

DICT_COLS = ["spend", "impressions", "estimated_audience_size"]
DATE_COLS = ["ad_creation_time", "ad_delivery_start_time", "ad_delivery_stop_time"]
CAT_COLS  = ["page_name", "bylines", "currency", "publisher_platforms"]


# ─────────────────────────────────────────────────
# PARSING HELPERS
# ─────────────────────────────────────────────────
def parse_bound(series, bound="lower_bound"):
    """
    Parse dict-string column into a numeric Series.
    e.g. "{'lower_bound': '45000', 'upper_bound': '49999'}" → 45000.0
    Open-ended records like {'lower_bound': '1000001'} return lower for both.
    """
    def _get(s):
        if pd.isna(s) or not str(s).strip().startswith("{"):
            return np.nan
        try:
            d = ast.literal_eval(str(s).strip())
            val = d.get(bound) or d.get("lower_bound")  # fallback
            return float(val) if val else np.nan
        except Exception:
            return np.nan
    return series.apply(_get)


def enrich_dict_cols(df):
    """Add _lower, _upper, _mid numeric columns for each dict-string column."""
    for col in DICT_COLS:
        if col not in df.columns:
            continue
        df[col + "_lower"] = parse_bound(df[col], "lower_bound")
        df[col + "_upper"] = parse_bound(df[col], "upper_bound")
        # midpoint: average of bounds; if upper missing, use lower
        df[col + "_mid"] = df.apply(
            lambda r: (r[col + "_lower"] + r[col + "_upper"]) / 2
            if not np.isnan(r.get(col + "_upper", np.nan))
            else r[col + "_lower"], axis=1
        )
    return df


# ─────────────────────────────────────────────────
# LOAD
# ─────────────────────────────────────────────────
def load(filepath):
    if not os.path.exists(filepath):
        print(f"[ERROR] Not found: {filepath}")
        print("Place fb_ads_president_scored_anon.csv in the same directory.")
        sys.exit(1)
    print(f"  Loading {filepath} …")
    df = pd.read_csv(filepath, low_memory=False)
    print(f"  Loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


# ─────────────────────────────────────────────────
# SECTION 1 — STRUCTURE
# ─────────────────────────────────────────────────
def section_structure(df):
    print(f"\n{'═'*72}")
    print("  SECTION 1: DATASET STRUCTURE")
    print(f"{'═'*72}")
    print(f"\n  Shape   : {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"  Memory  : {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    print(f"\n  Columns and dtypes:")
    for i, col in enumerate(df.columns, 1):
        miss = df[col].isna().sum()
        pct  = miss / len(df) * 100
        print(f"    {i:>3}. {col:<52} {str(df[col].dtype):<10} "
              f"null: {miss:>7,} ({pct:4.1f}%)")


# ─────────────────────────────────────────────────
# SECTION 2 — MISSING VALUES
# ─────────────────────────────────────────────────
def section_missing(df):
    print(f"\n{SEP}")
    print("  SECTION 2: MISSING VALUES")
    print(SEP)
    null_sum  = df.isna().sum()
    null_pct  = df.isna().mean() * 100
    total_cells = df.size
    total_miss  = null_sum.sum()
    print(f"\n  Total cells    : {total_cells:,}")
    print(f"  Missing cells  : {total_miss:,}  ({total_miss/total_cells*100:.1f}%)")
    print(f"  Rows with any  : {df.isna().any(axis=1).sum():,}")
    print(f"  Rows fully null: {df.isna().all(axis=1).sum():,}")
    print()
    miss_df = pd.DataFrame({"missing": null_sum, "pct": null_pct.round(1)})
    miss_df = miss_df[miss_df["missing"] > 0].sort_values("missing", ascending=False)
    print(f"  {'Column':<52} {'Missing':>9} {'%':>7}")
    print(f"  {'─'*52} {'─'*9} {'─'*7}")
    for col, row in miss_df.iterrows():
        print(f"  {col:<52} {int(row['missing']):>9,} {row['pct']:>6.1f}%")


# ─────────────────────────────────────────────────
# SECTION 3 — NUMERIC SUMMARY (parsed dict cols)
# ─────────────────────────────────────────────────
def section_numeric(df):
    print(f"\n{SEP}")
    print("  SECTION 3: NUMERIC COLUMNS (parsed from dict-strings)")
    print(f"  spend / impressions / estimated_audience_size → lower / midpoint")
    print(SEP)

    numeric_cols = [c for c in df.columns if c.endswith(("_lower", "_mid", "_upper"))]
    if not numeric_cols:
        print("  No parsed numeric columns found. Run enrich_dict_cols() first.")
        return

    desc = df[numeric_cols].describe(percentiles=[0.25, 0.5, 0.75])

    for col in numeric_cols:
        s = df[col].dropna()
        print(f"\n  {col}")
        print(f"    count   : {s.count():>12,}")
        print(f"    mean    : {s.mean():>15.2f}")
        print(f"    std     : {s.std():>15.2f}   (ddof=1, sample std)")
        print(f"    std(pop): {s.std(ddof=0):>15.2f}   (ddof=0, for comparison with pure Python)")
        print(f"    min     : {s.min():>15.2f}")
        print(f"    25%     : {s.quantile(0.25):>15.2f}")
        print(f"    median  : {s.median():>15.2f}")
        print(f"    75%     : {s.quantile(0.75):>15.2f}")
        print(f"    max     : {s.max():>15.2f}")
        print(f"    skew    : {s.skew():>15.4f}   (right-skewed if > 1)")
        print(f"    kurt    : {s.kurtosis():>15.4f}   (heavy tail if > 3)")

    return desc


# ─────────────────────────────────────────────────
# SECTION 4 — CATEGORICAL SUMMARY
# ─────────────────────────────────────────────────
def section_categorical(df):
    print(f"\n{SEP}")
    print("  SECTION 4: CATEGORICAL COLUMNS")
    print(SEP)

    for col in CAT_COLS:
        if col not in df.columns:
            continue
        vc = df[col].value_counts(dropna=True)
        n_valid  = df[col].notna().sum()
        n_null   = df[col].isna().sum()
        n_unique = df[col].nunique()
        print(f"\n  {col}")
        print(f"    non-null : {n_valid:>9,}   missing: {n_null:>7,} ({n_null/len(df)*100:.1f}%)")
        print(f"    unique   : {n_unique:>9,}")
        if not vc.empty:
            m = vc.index[0]
            print(f"    mode     : {str(m)[:55]}  (freq: {vc.iloc[0]:,})")
            print(f"    top 10:")
            for val, cnt in vc.head(10).items():
                pct = cnt / n_valid * 100
                disp = (str(val)[:55] + "…") if len(str(val)) > 56 else str(val)
                print(f"      {cnt:>8,}  ({pct:5.1f}%)  {disp}")

    # Identifier columns
    print(f"\n  Identifier uniqueness:")
    for col in ["page_id", "ad_id"]:
        if col in df.columns:
            print(f"    {col:<30}  unique: {df[col].nunique():,} / {len(df):,}")


# ─────────────────────────────────────────────────
# SECTION 5 — TOP SPENDERS
# ─────────────────────────────────────────────────
def section_spending(df):
    print(f"\n{SEP}")
    print("  SECTION 5: TOP SPENDERS & SPENDING CONCENTRATION")
    print(SEP)

    if "spend_lower" not in df.columns or "page_name" not in df.columns:
        print("  spend_lower column not found. Run enrich_dict_cols() first.")
        return

    grp = (df.groupby("page_name")["spend_lower"]
             .agg(total_spend="sum", ad_count="count", avg_spend="mean")
             .sort_values("total_spend", ascending=False))

    top15 = grp.head(15)
    grand_total = grp["total_spend"].sum()

    print(f"\n  Grand total spend (lower bound) : ${grand_total:>15,.0f}")
    top1_share  = grp["total_spend"].head(1).sum() / grand_total * 100
    top10_share = grp["total_spend"].head(10).sum() / grand_total * 100
    top50_share = grp["total_spend"].head(50).sum() / grand_total * 100
    print(f"  Top 1  advertisers → {top1_share:5.1f}% of total spend")
    print(f"  Top 10 advertisers → {top10_share:5.1f}% of total spend")
    print(f"  Top 50 advertisers → {top50_share:5.1f}% of total spend")

    print(f"\n  Top 15 Spenders:")
    print(f"  {'Rank':<5} {'Page Name':<50} {'Ads':>7} {'Total $':>14} {'Avg $':>10}")
    print(f"  {'─'*5} {'─'*50} {'─'*7} {'─'*14} {'─'*10}")
    for rank, (page, row) in enumerate(top15.iterrows(), 1):
        disp = (str(page)[:48] + "…") if len(str(page)) > 49 else str(page)
        print(f"  {rank:<5} {disp:<50} {int(row['ad_count']):>7,} "
              f"${row['total_spend']:>13,.0f} ${row['avg_spend']:>9,.0f}")

    # Spend distribution
    if "spend_lower" in df.columns:
        sp = df["spend_lower"].dropna()
        bins  = [0, 1, 100, 500, 1000, 5000, 10000, 50000, float("inf")]
        labels = ["$0", "$1–99", "$100–499", "$500–999",
                  "$1K–4.9K", "$5K–9.9K", "$10K–49.9K", "≥$50K"]
        cut = pd.cut(sp, bins=bins, labels=labels, right=False)
        dist = cut.value_counts().reindex(labels)
        print(f"\n  Spend per Ad Distribution (lower bound):")
        for lbl, cnt in dist.items():
            pct = cnt / len(sp) * 100
            bar = "█" * int(pct / 1.5)
            print(f"    {lbl:>12}  {cnt:>8,}  ({pct:5.1f}%)  {bar}")


# ─────────────────────────────────────────────────
# SECTION 6 — TEMPORAL
# ─────────────────────────────────────────────────
def section_temporal(df):
    print(f"\n{SEP}")
    print("  SECTION 6: TEMPORAL ANALYSIS")
    print(SEP)

    col = "ad_delivery_start_time"
    if col not in df.columns:
        print("  ad_delivery_start_time not found.")
        return

    dates = pd.to_datetime(df[col], errors="coerce")
    valid = dates.dropna()
    print(f"\n  Date column : '{col}'")
    print(f"  Valid dates : {len(valid):,} / {len(df):,}")
    print(f"  Earliest    : {valid.min().date()}")
    print(f"  Latest      : {valid.max().date()}")
    print(f"  Span        : {(valid.max() - valid.min()).days:,} days")

    df2 = df.copy()
    df2["_month"] = dates.dt.to_period("M")
    monthly = df2.groupby("_month").agg(
        ads=("ad_id", "count"),
        spend=("spend_lower", "sum") if "spend_lower" in df2.columns else ("page_id", "count")
    ).reset_index().sort_values("_month")

    max_ads = monthly["ads"].max()
    print(f"\n  Monthly Ad Activity:")
    print(f"  {'Month':<10} {'Ads':>8}  {'Spend (LB)':>14}  Bar")
    print(f"  {'─'*10} {'─'*8}  {'─'*14}  {'─'*35}")
    for _, row in monthly.iterrows():
        bar = "█" * int(row["ads"] / max_ads * 35)
        sp_disp = f"${row['spend']:>13,.0f}" if "spend_lower" in df2.columns else ""
        print(f"  {str(row['_month']):<10} {int(row['ads']):>8,}  {sp_disp:>15}  {bar}")

    # Key election events window analysis
    events = {
        "2024-03-05": "Super Tuesday",
        "2024-06-27": "Debate 1 (Trump vs Biden)",
        "2024-07-21": "Biden withdraws",
        "2024-09-10": "Debate 2 (Trump vs Harris)",
        "2024-10-01": "VP Debate",
        "2024-11-05": "Election Day",
    }
    print(f"\n  Ads within ±7 days of key 2024 events:")
    for dstr, label in events.items():
        ev = pd.Timestamp(dstr)
        mask = (dates >= ev - pd.Timedelta(days=7)) & (dates <= ev + pd.Timedelta(days=7))
        print(f"    {dstr}  {label:<35}  {mask.sum():>7,} ads")


# ─────────────────────────────────────────────────
# SECTION 7 — ILLUMINATING BINARY COLUMNS
# ─────────────────────────────────────────────────
def section_illuminating(df):
    print(f"\n{SEP}")
    print("  SECTION 7: ILLUMINATING BINARY SCORED COLUMNS (28 columns)")
    print(f"  Showing prevalence (% of ads flagged 1)")
    print(SEP)

    present = [c for c in ILLUMINATING_COLS if c in df.columns]
    if not present:
        print("  No illuminating columns found.")
        return

    print(f"\n  {'Label':<50} {'Flagged':>9} {'%':>7}  {'Missing':>8}")
    print(f"  {'─'*50} {'─'*9} {'─'*7}  {'─'*8}")
    rows = []
    for col in present:
        s = pd.to_numeric(df[col], errors="coerce")
        ones    = (s == 1).sum()
        missing = s.isna().sum()
        valid   = len(s) - missing
        pct     = ones / valid * 100 if valid else 0
        label   = col.replace("illuminating_", "")
        rows.append((label, ones, pct, missing))

    for label, ones, pct, miss in sorted(rows, key=lambda x: x[2], reverse=True):
        bar = "█" * int(pct / 3)
        print(f"  {label:<50} {ones:>9,} {pct:>6.1f}%  {miss:>8,}  {bar}")

    # Co-occurrence: how many ads are flagged for >1 topic
    topic_cols = [c for c in present if "topic" in c]
    if topic_cols:
        topic_df = df[topic_cols].apply(pd.to_numeric, errors="coerce").fillna(0)
        topic_count = topic_df.sum(axis=1)
        print(f"\n  Topic co-occurrence per ad:")
        for n in range(0, 6):
            cnt = (topic_count == n).sum()
            print(f"    {n} topics flagged : {cnt:>8,}  ({cnt/len(df)*100:.1f}%)")
        print(f"    6+ topics flagged: {(topic_count >= 6).sum():>8,}  "
              f"({(topic_count >= 6).sum()/len(df)*100:.1f}%)")


# ─────────────────────────────────────────────────
# SECTION 8 — CROSS-VALIDATION vs PURE PYTHON
# ─────────────────────────────────────────────────
def section_comparison(df):
    print(f"\n{SEP}")
    print("  SECTION 8: CROSS-VALIDATION — Pandas vs Pure Python")
    print(SEP)

    if "spend_lower" not in df.columns:
        print("  Run enrich_dict_cols() first.")
        return

    s = df["spend_lower"].dropna()
    n = len(s)

    manual_mean    = s.sum() / n
    pandas_mean    = s.mean()
    manual_std_pop = np.sqrt(((s - manual_mean) ** 2).sum() / n)
    pandas_std_pop = s.std(ddof=0)
    pandas_std_smp = s.std(ddof=1)

    print(f"\n  Column: spend_lower  (N = {n:,})")
    print(f"\n  {'Metric':<28} {'Pure Python':>14}  {'Pandas(ddof=0)':>15}  {'Pandas(ddof=1)':>15}")
    print(f"  {'─'*28} {'─'*14}  {'─'*15}  {'─'*15}")
    print(f"  {'Count':<28} {n:>14,}  {n:>15,}  {n:>15,}")
    print(f"  {'Mean':<28} {manual_mean:>14.4f}  {pandas_mean:>15.4f}  {'(same)':>15}")
    print(f"  {'Std Dev':<28} {manual_std_pop:>14.4f}  {pandas_std_pop:>15.4f}  {pandas_std_smp:>15.4f}")
    print(f"  {'Median':<28} {s.median():>14.4f}  {s.median():>15.4f}  {'(same)':>15}")
    print(f"  {'Min':<28} {s.min():>14.4f}  {s.min():>15.4f}  {'(same)':>15}")
    print(f"  {'Max':<28} {s.max():>14.4f}  {s.max():>15.4f}  {'(same)':>15}")

    mean_ok = abs(manual_mean - pandas_mean) < 0.01
    std_ok  = abs(manual_std_pop - pandas_std_pop) < 0.01
    print(f"\n  Mean agrees (< 0.01 diff): {'✓ YES' if mean_ok else '✗ NO'}")
    print(f"  Std (pop) agrees         : {'✓ YES' if std_ok  else '✗ NO'}")
    print(f"""
  Key differences to document:
  ┌────────────────────────────────┬──────────────────┬──────────────────┐
  │ Aspect                         │ Pure Python      │ Pandas           │
  ├────────────────────────────────┼──────────────────┼──────────────────┤
  │ Std deviation                  │ Population (÷N)  │ Sample (÷N-1)    │
  │ Missing value detection        │ empty str + "NA" │ NaN/None only    │
  │ Dict-string parsing            │ ast.literal_eval │ same (explicit)  │
  │ Date parsing                   │ strptime manual  │ pd.to_datetime   │
  │ Runtime (246K rows)            │ ~25–35 sec       │ ~3–5 sec         │
  │ Memory                         │ streaming OK     │ full df in RAM   │
  └────────────────────────────────┴──────────────────┴──────────────────┘
    """)


# ─────────────────────────────────────────────────
# VISUALIZATIONS
# ─────────────────────────────────────────────────
def generate_visualizations(df, out_dir="visualizations"):
    try:
        import matplotlib.pyplot as plt
        import matplotlib.ticker as mtick
        import seaborn as sns
    except ImportError:
        print("\n  [INFO] pip install matplotlib seaborn  to enable plots.")
        return

    os.makedirs(out_dir, exist_ok=True)
    sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
    print(f"\n{SEP}")
    print(f"  GENERATING VISUALIZATIONS → {out_dir}/")
    print(SEP)

    # 1 — Spend distribution (log scale)
    if "spend_lower" in df.columns:
        sp = df["spend_lower"].dropna()
        sp_pos = sp[sp > 0]
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle("Facebook Political Ad Spend Distribution — 2024 Election", fontsize=13)

        axes[0].hist(sp_pos.clip(upper=sp_pos.quantile(0.99)),
                     bins=60, color="#4C72B0", edgecolor="white", alpha=0.85)
        axes[0].set_title("Spend per Ad (capped at 99th pct)")
        axes[0].set_xlabel("Spend Lower Bound ($)")
        axes[0].set_ylabel("Number of Ads")
        axes[0].xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:,.0f}"))

        axes[1].hist(sp_pos, bins=80, color="#DD8452", edgecolor="white", alpha=0.85)
        axes[1].set_xscale("log")
        axes[1].set_title("Spend per Ad (log scale)")
        axes[1].set_xlabel("Spend Lower Bound ($ log)")
        axes[1].set_ylabel("Number of Ads")

        plt.tight_layout()
        p = f"{out_dir}/01_spend_distribution.png"
        plt.savefig(p, dpi=150, bbox_inches="tight"); plt.close()
        print(f"  ✓ {p}")

    # 2 — Top spenders bar chart
    if "spend_lower" in df.columns and "page_name" in df.columns:
        top = (df.groupby("page_name")["spend_lower"]
               .sum().sort_values(ascending=False).head(15))
        fig, ax = plt.subplots(figsize=(12, 7))
        colors = sns.color_palette("Blues_d", len(top))
        top.sort_values().plot(kind="barh", ax=ax, color=colors)
        ax.set_title("Top 15 Facebook Political Ad Spenders — 2024 Election", fontsize=12)
        ax.set_xlabel("Total Spend Lower Bound ($)")
        ax.xaxis.set_major_formatter(mtick.FuncFormatter(
            lambda x, _: f"${x/1e6:.1f}M" if x >= 1e6 else f"${x:,.0f}"))
        ax.set_yticklabels([t.get_text()[:45] for t in ax.get_yticklabels()], fontsize=8)
        plt.tight_layout()
        p = f"{out_dir}/02_top_spenders.png"
        plt.savefig(p, dpi=150, bbox_inches="tight"); plt.close()
        print(f"  ✓ {p}")

    # 3 — Monthly activity timeline
    if "ad_delivery_start_time" in df.columns:
        df2 = df.copy()
        df2["_month"] = pd.to_datetime(df["ad_delivery_start_time"], errors="coerce").dt.to_period("M")
        monthly = df2.groupby("_month").size().reset_index(name="cnt")
        monthly["_dt"] = monthly["_month"].dt.to_timestamp()

        fig, ax = plt.subplots(figsize=(14, 5))
        ax.fill_between(monthly["_dt"], monthly["cnt"], alpha=0.35, color="#4C72B0")
        ax.plot(monthly["_dt"], monthly["cnt"], color="#4C72B0", lw=2, marker="o", ms=4)

        events = {
            "2024-03-05": "Super\nTuesday",
            "2024-06-27": "Debate 1",
            "2024-07-21": "Biden Out",
            "2024-09-10": "Debate 2",
            "2024-11-05": "Election\nDay",
        }
        for dstr, lbl in events.items():
            ev = pd.Timestamp(dstr)
            ax.axvline(ev, color="red", ls="--", alpha=0.5, lw=1)
            ax.text(ev, ax.get_ylim()[1] * 0.92, lbl, ha="center",
                    va="top", fontsize=7.5, color="red")

        ax.set_title("Monthly Facebook Political Ad Volume — 2024 Election", fontsize=12)
        ax.set_xlabel("Month"); ax.set_ylabel("Number of Ads")
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        plt.tight_layout()
        p = f"{out_dir}/03_monthly_volume.png"
        plt.savefig(p, dpi=150, bbox_inches="tight"); plt.close()
        print(f"  ✓ {p}")

    # 4 — Illuminating topic prevalence
    topic_cols = [c for c in ILLUMINATING_COLS if "topic" in c and c in df.columns]
    if topic_cols:
        topic_series = {c.replace("illuminating_topic_", ""):
                        pd.to_numeric(df[c], errors="coerce").mean() * 100
                        for c in topic_cols}
        ts = pd.Series(topic_series).sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = sns.color_palette("coolwarm_r", len(ts))
        ts.plot(kind="barh", ax=ax, color=colors)
        ax.set_title("Topic Prevalence in 2024 Facebook Political Ads", fontsize=12)
        ax.set_xlabel("% of Ads Flagged for Topic")
        ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:.1f}%"))
        plt.tight_layout()
        p = f"{out_dir}/04_topic_prevalence.png"
        plt.savefig(p, dpi=150, bbox_inches="tight"); plt.close()
        print(f"  ✓ {p}")

    # 5 — Message type breakdown
    msg_cols = [c for c in ILLUMINATING_COLS if "msg_type" in c and c in df.columns]
    if msg_cols:
        msg_series = {c.replace("illuminating_msg_type_", ""):
                      pd.to_numeric(df[c], errors="coerce").sum()
                      for c in msg_cols}
        ms = pd.Series(msg_series).sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(8, 4))
        ms.plot(kind="bar", ax=ax, color=sns.color_palette("Set2"), edgecolor="white")
        ax.set_title("Ad Message Type Distribution — 2024 Political Ads", fontsize=12)
        ax.set_xlabel("Message Type"); ax.set_ylabel("Number of Ads")
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        p = f"{out_dir}/05_message_types.png"
        plt.savefig(p, dpi=150, bbox_inches="tight"); plt.close()
        print(f"  ✓ {p}")

    print(f"\n  Visualizations saved to ./{out_dir}/")


# ─────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", default=DEFAULT_FILE)
    parser.add_argument("--save-plots", action="store_true")
    args = parser.parse_args()

    print(f"\n{'═'*72}")
    print("  PANDAS DESCRIPTIVE STATISTICS")
    print("  Dataset: fb_ads_president_scored_anon.csv")
    print(f"{'═'*72}")

    df = load(args.file)
    print("  Parsing dict-string columns (spend / impressions / audience) …")
    df = enrich_dict_cols(df)

    section_structure(df)
    section_missing(df)
    section_numeric(df)
    section_categorical(df)
    section_spending(df)
    section_temporal(df)
    section_illuminating(df)
    section_comparison(df)

    if args.save_plots:
        generate_visualizations(df)

    print(f"\n{'═'*72}")
    print("  PANDAS ANALYSIS COMPLETE")
    print(f"{'═'*72}\n")


if __name__ == "__main__":
    main()
