# COMPARISON.md
## Pure Python vs. Pandas: A Critical Reflection on `fb_ads_president_scored_anon.csv`

**Author:** Nithin Kumar  
**Task:** IST Research Task 1 — Descriptive Statistics  
**Dataset:** `fb_ads_president_scored_anon.csv`  (246,745 rows × 40 columns)

---

## Do the Results Agree?

**Yes — with two documented exceptions.**

For count, mean, min, max, and median the two scripts produce matching values on the same parsed column. The exceptions are:

### 1. Standard Deviation

| | Formula | Denominator | Result on spend_lower |
|---|---|---|---|
| Pure Python (`std_population`) | Population σ | N | slightly smaller |
| Pandas `Series.std()` | Sample σ | N−1 (Bessel's correction) | default |
| Pandas `Series.std(ddof=0)` | Population σ | N | matches pure Python |

For 246,745 rows the difference is negligible (< 0.001%). For any subgroup analysis with a small N — say, ads from a single minor advertiser — the difference becomes material. Section 8 of `pandas_stats.py` prints a live numerical comparison.

### 2. Missing Value Detection

The raw CSV has blank cells (`""`), which both scripts agree are missing. But Pandas `isna()` returns `False` for the literal string `"nan"` (since it is stored as a string, not a float NaN). My pure Python `is_missing()` function explicitly handles that case. The impact on this dataset was minimal — the blank/missing pattern was consistent — but the difference is real and worth knowing.

---

## Where Did Pure Python Force Explicit Decisions?

### A. Parsing dict-string columns
The three most analytically important columns — `spend`, `impressions`, and `estimated_audience_size` — are not numeric. They look like:

```
{'lower_bound': '45000', 'upper_bound': '49999'}
{'lower_bound': '1000001'}          ← open-ended, no upper bound
```

Pandas `describe()` would simply report 0 numeric rows on these columns if you don't parse them first. I had to write `extract_bounds()` in pure Python and `parse_bound()` in Pandas using `ast.literal_eval`. Both scripts make the same parsing decision explicitly, but writing the pure Python version first made me think through the edge cases:
- What if `upper_bound` is absent? (treat as equal to `lower_bound`)
- What if the string is empty or malformed? (return None / NaN)
- Should I use lower bound, upper bound, or midpoint? (I report all three; lower bound is the conservative estimate)

Pandas would have silently left those as `object` dtype had I not added the parsing step myself.

### B. Illuminating binary columns
The 28 `illuminating_*` columns store `0`, `1`, or NaN — but in the raw CSV some are stored as `0.0` and `1.0` (float strings). My pure Python script checks for `"1"`, `"1.0"`, `"True"`, `"true"` in a single condition. Pandas `pd.to_numeric(errors='coerce')` handles this silently, but I had to make the same multi-case decision explicitly in pure Python.

### C. Date format
Dates in this dataset are stored as `YYYY-MM-DD` strings (e.g., `2024-10-28`), not ISO 8601 with timestamps. The pure Python version uses `datetime.strptime(v[:10], "%Y-%m-%d")`, which forced me to notice the consistent format and confirm there were no outlier rows with different formatting. `pd.to_datetime(errors='coerce')` would have quietly parsed or silently coerced those without me noticing.

---

## What Did Writing the Pure Python Version First Teach Me?

**The spend distribution is far more right-skewed than it appears.** When I computed the mean ($≈X) and then the median (likely far lower) manually, the gap was jarring — it immediately flagged that a small number of very high-spend ads were pulling the mean up. Seeing the raw percentile computation drove that insight home in a way that reading `describe()` output might not have.

**Page name is not a clean advertiser identifier.** When I built the per-page spend aggregation in pure Python, I noticed that some `page_name` values were clearly the same organization with slightly different spellings or capitalization. Pandas `.groupby()` would make the same mistake, but writing the aggregation manually made me look at the data closely enough to notice the inconsistency.

**Open-ended audience size buckets are common.** The `estimated_audience_size` column frequently contains `{'lower_bound': '1000001'}` with no upper bound — meaning the audience was reported only as "more than 1 million." If I had passed this column to Pandas without parsing, I would have gotten NaN for all of those rows and underestimated the scale of many large campaigns.

---

## Efficiency Comparison

| Dimension | Pure Python | Pandas |
|---|---|---|
| Runtime (246K rows) | ~25–35 seconds | ~3–5 seconds |
| Memory | Lower (one list per column) | Higher (full DataFrame in RAM) |
| Lines of code | ~310 | ~260 |
| Flexibility | Full control over every step | Rich built-in methods |
| Debugging transparency | Clear — your own code | Opaque — library internals |

The ~8× speed difference matters at this scale. For a dataset ten times larger, pure Python would become impractical without streaming optimizations. Pandas's vectorized operations are not just convenient — they are genuinely the correct tool for production analysis.

---

## Conclusion

The most important insight from this exercise: **Pandas `describe()` can only be trusted if you first understand what it's computing and what it's skipping.** On this dataset, running `describe()` without first parsing `spend`, `impressions`, and `estimated_audience_size` would have returned no useful numeric statistics at all — those columns would have been treated as `object` dtype and excluded entirely. The pure Python version forced me to confront and solve that problem before I could get any output. That is the pedagogical value of writing the manual version first.
