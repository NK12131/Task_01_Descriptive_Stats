"""
pure_python_stats.py
====================
Descriptive statistics for: fb_ads_president_scored_anon.csv
246,745 rows × 40 columns — 2024 Facebook Political Ads (Meta Ad Library)
Uses ONLY Python standard library: csv, math, collections, ast, datetime.
No pandas, no numpy, no third-party packages.

Author: Nithin Kumar
Course: IST Research Task 1 — Descriptive Statistics

Dataset columns (40 total):
  Identifiers  : page_id, ad_id
  Categorical  : page_name, bylines, currency, publisher_platforms
  Date strings : ad_creation_time, ad_delivery_start_time, ad_delivery_stop_time
  Dict-strings : estimated_audience_size, impressions, spend
                 (stored as "{'lower_bound': '1000', 'upper_bound': '4999'}")
  Binary/scored: illuminating_* (28 columns, values 0/1/NaN)

Usage:
    python pure_python_stats.py
    python pure_python_stats.py --file fb_ads_president_scored_anon.csv
"""

import csv
import math
import collections
import sys
import os
import ast
import argparse
from datetime import datetime

# ─────────────────────────────────────────────────
DEFAULT_FILE = "fb_ads_president_scored_anon.csv"
SEP = "─" * 72

# The 28 illuminating binary columns
ILLUMINATING_COLS = [
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
]

# Dict-string columns (spend/impressions/audience stored as {'lower_bound':...})
DICT_STRING_COLS = ["estimated_audience_size", "impressions", "spend"]

DATE_COLS = ["ad_creation_time", "ad_delivery_start_time", "ad_delivery_stop_time"]

CATEGORICAL_COLS = ["page_name", "bylines", "currency", "publisher_platforms"]


# ─────────────────────────────────────────────────
# UTILITIES
# ─────────────────────────────────────────────────
def is_missing(v):
    return v is None or str(v).strip() in ("", "nan", "NaN", "None", "N/A", "NA")


def safe_float(v):
    """Return (float, True) or (None, False)."""
    if is_missing(v):
        return None, False
    try:
        return float(str(v).strip().replace(",", "")), True
    except ValueError:
        return None, False


def parse_dict_string(s):
    """
    Parse Meta Ad Library dict-strings like:
      "{'lower_bound': '45000', 'upper_bound': '49999'}"
    Returns dict or None on failure.
    """
    if is_missing(s):
        return None
    try:
        return ast.literal_eval(s.strip())
    except Exception:
        return None


def extract_bounds(s):
    """
    From a dict-string, return (lower_float, upper_float).
    If upper_bound missing (open-ended like ≥1,000,001), upper = lower.
    """
    d = parse_dict_string(s)
    if d is None:
        return None, None
    lb_val, lb_ok = safe_float(d.get("lower_bound", ""))
    ub_val, ub_ok = safe_float(d.get("upper_bound", ""))
    lb = lb_val if lb_ok else None
    ub = ub_val if ub_ok else (lb if lb is not None else None)
    return lb, ub


# ─────────────────────────────────────────────────
# STATISTICAL FUNCTIONS (pure Python)
# ─────────────────────────────────────────────────
def mean(values):
    return sum(values) / len(values) if values else None


def std_population(values):
    if len(values) < 2:
        return None
    m = mean(values)
    return math.sqrt(sum((x - m) ** 2 for x in values) / len(values))


def median(values):
    if not values:
        return None
    sv = sorted(values)
    n = len(sv)
    mid = n // 2
    return (sv[mid - 1] + sv[mid]) / 2.0 if n % 2 == 0 else float(sv[mid])


def percentile(values, p):
    if not values:
        return None
    sv = sorted(values)
    idx = (p / 100.0) * (len(sv) - 1)
    lo, hi = int(idx), int(idx) + 1
    frac = idx - lo
    return sv[lo] if hi >= len(sv) else sv[lo] + frac * (sv[hi] - sv[lo])


def numeric_stats(values_raw):
    """Full stats dict from a list of raw strings or floats."""
    parsed, missing = [], 0
    for v in values_raw:
        f, ok = safe_float(v)
        if ok:
            parsed.append(f)
        else:
            missing += 1
    if not parsed:
        return dict(count=0, missing=missing, mean=None, std=None,
                    median=None, min=None, max=None, q25=None, q75=None)
    return dict(
        count=len(parsed), missing=missing,
        mean=mean(parsed), std=std_population(parsed),
        median=median(parsed), min=min(parsed), max=max(parsed),
        q25=percentile(parsed, 25), q75=percentile(parsed, 75),
    )


def categorical_stats(values_raw, top_n=5):
    non_null, missing = [], 0
    for v in values_raw:
        if is_missing(v):
            missing += 1
        else:
            non_null.append(str(v).strip())
    if not non_null:
        return dict(count=0, missing=missing, unique=0,
                    mode=None, mode_freq=0, top_values=[])
    freq = collections.Counter(non_null)
    top = freq.most_common(top_n)
    return dict(count=len(non_null), missing=missing, unique=len(freq),
                mode=top[0][0], mode_freq=top[0][1], top_values=top)


# ─────────────────────────────────────────────────
# DISPLAY HELPERS
# ─────────────────────────────────────────────────
def f(val, dec=2):
    if val is None: return "N/A"
    if isinstance(val, float): return f"{val:,.{dec}f}"
    return str(val)


def print_num(label, stats, n_total):
    pct_miss = stats["missing"] / n_total * 100 if n_total else 0
    print(f"\n  ┌ {label}  [numeric]")
    print(f"  │  non-null: {stats['count']:>9,}  missing: {stats['missing']:>7,} ({pct_miss:.1f}%)")
    print(f"  │  mean    : {f(stats['mean']):>14}   std    : {f(stats['std']):>14}")
    print(f"  │  min     : {f(stats['min']):>14}   max    : {f(stats['max']):>14}")
    print(f"  │  Q25     : {f(stats['q25']):>14}   median : {f(stats['median']):>14}   Q75: {f(stats['q75'])}")
    print(f"  └{'─'*60}")


def print_cat(label, stats, n_total):
    pct_miss = stats["missing"] / n_total * 100 if n_total else 0
    print(f"\n  ┌ {label}  [categorical]")
    print(f"  │  non-null: {stats['count']:>9,}  missing: {stats['missing']:>7,} ({pct_miss:.1f}%)")
    print(f"  │  unique  : {stats['unique']:>9,}  mode   : {(str(stats['mode'])[:45] if stats['mode'] else 'N/A')}")
    print(f"  │  top values:")
    for val, cnt in stats["top_values"]:
        pct = cnt / stats["count"] * 100 if stats["count"] else 0
        disp = (str(val)[:55] + "…") if len(str(val)) > 56 else str(val)
        print(f"  │    {cnt:>8,}  ({pct:5.1f}%)  {disp}")
    print(f"  └{'─'*60}")


# ─────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────
def load_csv(filepath):
    if not os.path.exists(filepath):
        print(f"\n[ERROR] File not found: {filepath}")
        print("  Place fb_ads_president_scored_anon.csv in the same directory.")
        print("  Then run: python pure_python_stats.py")
        sys.exit(1)

    col_data = collections.OrderedDict()
    total_rows = 0
    print(f"  Reading: {filepath}  (this may take ~30 sec for 246K rows) …")

    with open(filepath, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        for col in headers:
            col_data[col] = []
        for row in reader:
            total_rows += 1
            for col in headers:
                col_data[col].append(row.get(col, ""))
            if total_rows % 50000 == 0:
                print(f"    … {total_rows:,} rows loaded")

    print(f"  Done. {total_rows:,} rows × {len(headers)} columns")
    return headers, col_data, total_rows


# ─────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────
def analyze(filepath):
    print(f"\n{'═'*72}")
    print("  PURE PYTHON DESCRIPTIVE STATISTICS")
    print("  Dataset: fb_ads_president_scored_anon.csv")
    print(f"{'═'*72}")

    headers, col_data, N = load_csv(filepath)

    # ── OVERVIEW ──────────────────────────────────
    print(f"\n{SEP}")
    print("  DATASET OVERVIEW")
    print(SEP)
    print(f"  Rows    : {N:,}")
    print(f"  Columns : {len(headers)}")
    print()
    # Missing value table
    print(f"  {'Column':<48} {'Missing':>8}  {'%':>6}")
    print(f"  {'─'*48} {'─'*8}  {'─'*6}")
    for col in headers:
        miss = sum(1 for v in col_data[col] if is_missing(v))
        pct = miss / N * 100
        disp = (col[:46] + "…") if len(col) > 47 else col
        print(f"  {disp:<48} {miss:>8,}  {pct:>5.1f}%")

    # ── CATEGORICAL COLUMNS ───────────────────────
    print(f"\n{SEP}")
    print("  CATEGORICAL COLUMNS")
    print(SEP)
    for col in CATEGORICAL_COLS:
        if col in col_data:
            stats = categorical_stats(col_data[col])
            print_cat(col, stats, N)

    # Identifier cardinality
    print(f"\n  Identifier cardinality:")
    for col in ["page_id", "ad_id"]:
        if col in col_data:
            unique = len(set(v for v in col_data[col] if not is_missing(v)))
            print(f"    {col:<30}  unique: {unique:,}")

    # ── DATE COLUMNS ──────────────────────────────
    print(f"\n{SEP}")
    print("  DATE COLUMNS")
    print(SEP)
    for col in DATE_COLS:
        if col not in col_data:
            continue
        valid_dates, missing = [], 0
        for v in col_data[col]:
            if is_missing(v):
                missing += 1
                continue
            try:
                valid_dates.append(datetime.strptime(v.strip()[:10], "%Y-%m-%d"))
            except ValueError:
                missing += 1
        if valid_dates:
            print(f"\n  {col}")
            print(f"    non-null : {len(valid_dates):,}  missing: {missing:,}")
            print(f"    earliest : {min(valid_dates).date()}")
            print(f"    latest   : {max(valid_dates).date()}")
            span = (max(valid_dates) - min(valid_dates)).days
            print(f"    span     : {span:,} days")

    # ── DICT-STRING COLUMNS (spend / impressions / audience) ───
    print(f"\n{SEP}")
    print("  DICT-STRING COLUMNS: spend / impressions / estimated_audience_size")
    print(f"  (Each stored as {{'lower_bound': '...', 'upper_bound': '...'}})")
    print(SEP)

    for col in DICT_STRING_COLS:
        if col not in col_data:
            continue
        lowers, uppers, midpoints, missing = [], [], [], 0
        for v in col_data[col]:
            lb, ub = extract_bounds(v)
            if lb is None:
                missing += 1
            else:
                lowers.append(lb)
                if ub is not None:
                    uppers.append(ub)
                midpoints.append((lb + (ub or lb)) / 2.0)

        print(f"\n  {col}  (parsed lower bounds):")
        s = numeric_stats(lowers)
        s["missing"] = missing
        print_num(col + " [lower_bound]", s, N)

        print(f"  {col}  (midpoint estimates):")
        sm = numeric_stats(midpoints)
        sm["missing"] = missing
        print_num(col + " [midpoint]", sm, N)

        # Spend distribution buckets (lower bound)
        if col == "spend" and lowers:
            buckets = collections.Counter()
            for v in lowers:
                if v == 0:       buckets["$0"] += 1
                elif v < 100:    buckets["$1–99"] += 1
                elif v < 500:    buckets["$100–499"] += 1
                elif v < 1000:   buckets["$500–999"] += 1
                elif v < 5000:   buckets["$1K–4.9K"] += 1
                elif v < 10000:  buckets["$5K–9.9K"] += 1
                elif v < 50000:  buckets["$10K–49.9K"] += 1
                else:             buckets["≥$50K"] += 1
            total = len(lowers)
            print(f"\n  Spend Distribution (lower_bound):")
            for bucket in ["$0", "$1–99", "$100–499", "$500–999",
                           "$1K–4.9K", "$5K–9.9K", "$10K–49.9K", "≥$50K"]:
                cnt = buckets.get(bucket, 0)
                pct = cnt / total * 100
                bar = "█" * int(pct / 1.5)
                print(f"    {bucket:>12}  {cnt:>8,}  ({pct:5.1f}%)  {bar}")

    # ── TOP SPENDERS ──────────────────────────────
    print(f"\n{SEP}")
    print("  TOP 15 SPENDERS (by page_name, summing spend lower_bound)")
    print(SEP)
    if "page_name" in col_data and "spend" in col_data:
        page_spend = collections.defaultdict(float)
        page_count = collections.defaultdict(int)
        for i in range(N):
            page = col_data["page_name"][i].strip() if not is_missing(col_data["page_name"][i]) else "Unknown"
            lb, _ = extract_bounds(col_data["spend"][i])
            if lb is not None:
                page_spend[page] += lb
                page_count[page] += 1
        top = sorted(page_spend.items(), key=lambda x: x[1], reverse=True)[:15]
        print(f"\n  {'Rank':<5} {'Page Name':<50} {'Ads':>7} {'Total Spend (LB)':>18}")
        print(f"  {'─'*5} {'─'*50} {'─'*7} {'─'*18}")
        for rank, (page, total) in enumerate(top, 1):
            disp = (page[:48] + "…") if len(page) > 49 else page
            print(f"  {rank:<5} {disp:<50} {page_count[page]:>7,} ${total:>17,.0f}")

    # ── ILLUMINATING BINARY COLUMNS ───────────────
    print(f"\n{SEP}")
    print("  ILLUMINATING SCORED COLUMNS (binary 0/1, % of valid rows flagged)")
    print(SEP)
    print(f"\n  {'Column':<50} {'Flagged (=1)':>12} {'%':>7}  {'Missing':>8}")
    print(f"  {'─'*50} {'─'*12} {'─'*7}  {'─'*8}")
    for col in ILLUMINATING_COLS:
        if col not in col_data:
            continue
        ones, zeros, missing = 0, 0, 0
        for v in col_data[col]:
            if is_missing(v):
                missing += 1
            elif str(v).strip() in ("1", "1.0", "True", "true"):
                ones += 1
            else:
                zeros += 1
        valid = ones + zeros
        pct = ones / valid * 100 if valid else 0
        label = col.replace("illuminating_", "")
        print(f"  {label:<50} {ones:>12,} {pct:>6.1f}%  {missing:>8,}")

    # ── TEMPORAL ANALYSIS ─────────────────────────
    print(f"\n{SEP}")
    print("  TEMPORAL ANALYSIS — Monthly Ad Volume")
    print(SEP)
    if "ad_delivery_start_time" in col_data:
        monthly = collections.Counter()
        monthly_spend = collections.defaultdict(float)
        for i, v in enumerate(col_data["ad_delivery_start_time"]):
            if is_missing(v):
                continue
            try:
                dt = datetime.strptime(v.strip()[:10], "%Y-%m-%d")
                key = dt.strftime("%Y-%m")
                monthly[key] += 1
                lb, _ = extract_bounds(col_data["spend"][i]) if "spend" in col_data else (None, None)
                if lb is not None:
                    monthly_spend[key] += lb
            except ValueError:
                pass
        if monthly:
            max_cnt = max(monthly.values())
            print(f"\n  {'Month':<10} {'Ads':>8}  {'Spend (LB $)':>14}  Chart")
            print(f"  {'─'*10} {'─'*8}  {'─'*14}  {'─'*35}")
            for month in sorted(monthly):
                cnt = monthly[month]
                sp = monthly_spend.get(month, 0)
                bar = "█" * int(cnt / max_cnt * 35)
                print(f"  {month:<10} {cnt:>8,}  ${sp:>13,.0f}  {bar}")

    print(f"\n{'═'*72}")
    print("  PURE PYTHON ANALYSIS COMPLETE")
    print(f"{'═'*72}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", default=DEFAULT_FILE)
    args = parser.parse_args()
    analyze(args.file)
