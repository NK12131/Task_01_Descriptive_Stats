# Pure Python vs. Pandas: A Methodological Reflection

**Author:** Nithin Kumar

**Task:** IST Research Task 1 — Descriptive Statistics

**Dataset:** `fb_ads_president_scored_anon.csv` (246,745 rows × 40 columns)

---

## Do the Results Agree?

**Yes — with two documented exceptions.**

Across all shared metrics — count, mean, minimum, maximum, and median — both implementations produce numerically identical results on the same parsed columns. The two exceptions are as follows.

### 1. Standard Deviation

| Implementation | Formula | Denominator |
|---|---|---|
| Pure Python (`std_population`) | Population σ | N |
| Pandas `Series.std()` | Sample σ (Bessel's correction) | N−1 |
| Pandas `Series.std(ddof=0)` | Population σ | N — matches pure Python |

At 246,745 rows, the divergence is negligible (< 0.001%). However, in any subgroup analysis with a small N, ads from a single minor advertiser, for instance, the distinction becomes material and should be made deliberately rather than inherited from a library default.

### 2. Missing Value Detection

Both scripts agree that blank cells (`""`) constitute missing values. Pandas `isna()`, however, returns `False` for the literal string `"nan"`, since it is stored as a string rather than a float NaN. The pure Python `is_missing()` function handles this case explicitly. The practical impact on this dataset was minimal, but the behavioral difference is real and would matter in dirtier data.

---

## Where Pure Python Forced Explicit Decisions

### Parsing Dict-String Columns

The three analytically central columns, `spend`, `impressions`, and `estimated_audience_size`, are not stored as numeric values. Their raw format is:

```
{'lower_bound': '45000', 'upper_bound': '49999'}
{'lower_bound': '1000001'}          ← open-ended; no upper bound present
```

Without an explicit parsing step, Pandas `describe()` silently treats these columns as `object` dtype and excludes them from all numeric summaries, producing no useful statistics on the most important variables in the dataset. Writing the pure Python implementation first made this failure mode impossible to overlook. It forced deliberate decisions on every edge case: how to handle an absent `upper_bound` (treat as equal to `lower_bound`); how to handle malformed or empty strings (return `None`); and whether to report lower bound, upper bound, or midpoint (all three are reported; lower bound serves as the conservative estimate).

### Binary Classification Columns

The 28 `illuminating_*` columns nominally store `0` or `1`, but the raw CSV contains mixed representations `"0"`, `"1"`, `"0.0"`, `"1.0"` — depending on how the field was serialized. Pandas `pd.to_numeric(errors='coerce') resolves this silently. The pure Python implementation required an explicit multi-case condition covering each representation, which surfaced the inconsistency directly rather than abstracting it away.

### Date Formatting

Dates are stored as `YYYY-MM-DD` strings rather than full ISO 8601 timestamps. The pure Python script parses these with `datetime.strptime(v[:10], "%Y-%m-%d")`, which required confirming the format was consistent across all 246,745 rows before the script could proceed without error. Pandas `pd.to_datetime(errors='coerce') would have handled malformed rows silently, a convenience that can obscure data quality issues in less uniform datasets.

---

## What the Manual Implementation Revealed

**The spend distribution is more skewed than summary statistics suggest.** Computing the mean and median by hand — and watching the gap between them emerge — made the right-skew visceral in a way that reading `describe()` output does not. A small number of very high-spend placements pull the mean substantially above the median, a pattern that became analytically obvious only through the manual computation.

**Page name is an unreliable advertiser identifier.** Building the per-page spend aggregation manually required reading the `page_name` values directly, which revealed that some organizations appear under slightly varying spellings or capitalizations across different ads. Pandas `.groupby()` makes the same mistake, but silently, the manual approach created enough friction to surface the inconsistency.

**Open-ended audience size estimates are pervasive.** The `estimated_audience_size` column frequently reports only a lower bound `{'lower_bound': '1000001'}` with no upper bound — indicating that the audience exceeded one million but was not further quantified. Passing this column to Pandas without parsing would have returned NaN for every such row, systematically underrepresenting the reach of the largest campaigns in the dataset.

---

## Efficiency Comparison

| Dimension | Pure Python | Pandas |
|---|---|---|
| Runtime (246,745 rows) | ~25–35 seconds | ~3–5 seconds |
| Memory footprint | Lower — one list per column | Higher — full DataFrame in RAM |
| Lines of code | ~310 | ~260 |
| Control over computation | Explicit at every step | Delegated to library internals |
| Debugging transparency | High | Low |

The approximately 8× speed differential is consequential at this scale and would become prohibitive on a dataset an order of magnitude larger without streaming optimizations. Pandas' vectorized operations are not merely convenient — for production-scale analysis, they represent the technically appropriate choice.

---

## Conclusion

The central lesson of this exercise is that **Pandas `describe()` can only be trusted if the analyst first understands what it is computing and, critically, what it is silently skipping.** On this dataset, invoking `describe()` without first parsing `spend`, `impressions`, and `estimated_audience_size` would have returned no numeric statistics whatsoever on the three most important columns; they would have been silently excluded as `object` dtype. The pure Python implementation made that failure mode structurally impossible: there was no output until the parsing problem was solved. That is the pedagogical value of writing the manual version first — not to produce a faster or cleaner result, but to ensure that every assumption underlying the analysis is made consciously.
