# As-of data gate — Zachary Alvin

Decision date: **31 March 2026**. Script: `asof.py` (run with `python3 asof.py`).

## Filter verification

The filter matches the known answer. Rules were applied in the required order, preserving original row numbers.

| Funnel step | Original row numbers | Rows remaining |
|---|---|---:|
| Starting data | 1–12 | 12 |
| Quarantine: missing ticker | 11 | 11 |
| Remove: exact duplicate | 7 | 10 |
| Remove: published after 31 March | 3, 8, 10 | 7 |
| Remove: older publication replaced by revision | 2 | 6 |
| Final as-of panel | 1, 4, 5, 6, 9, 12 | 6 |

Signal = latest knowable month’s price ÷ previous calendar month’s price − 1.

| Ticker | 31 March as-of signal | Naive signal |
|---|---:|---:|
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | −1.02% (February) | −5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February, revised) |

AAA uses row 4’s revised February price of 103, which was published on 25 March. Keeping row 2’s older price of 104 would incorrectly produce +2.97%.

## Partner check

The partner’s script reproduced the known 31 March results. Its decision date was temporarily changed to **15 April 2026** and the script was run again. Every as-of signal then matched its naive signal exactly:

| Ticker | 15 April as-of signal | Naive signal |
|---|---:|---:|
| AAA | +5.83% | +5.83% |
| BBB | −5.15% | −5.15% |
| CCC | +1.82% | +1.82% |

By 15 April, rows 3 and 8 (March prices published 10 April) and row 10 (February’s CCC revision published 5 April) were knowable. Row 10 replaced row 12. The partner’s original file was restored byte for byte, including its 31 March decision date.

## What the comparison shows

The original gap comes from publications unavailable on 31 March. For AAA and BBB, the naive calculation also advances the return period from February to March; CCC’s gap comes from a later revision to February. Using these future publications for a 31 March decision creates look-ahead bias.

Passing the timing filter does not establish economic validity. Under the exercise’s assumptions, rows 1, 4, 9, and 12 imply negative yields, and CCC is priced above both AAA and BBB in both months. Those are separate sanity-check flags.

AI assistance: used to implement the filter, run the scripts, verify the outputs, and prepare this summary. This is an individual submission artifact; no upload or external submission has been performed.
