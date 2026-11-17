AI assisted with building and checking this project. For education, not investment advice.

# Project 2 — Portfolio pilot decision

## Reproduce the decision

From the repository root, use Python 3.9 or later. Setup requires access to install pandas. The report uses the included prices and makes no network requests.

```sh
python3 -m venv .project2-venv
.project2-venv/bin/python -m pip install pandas==2.3.3
.project2-venv/bin/python project2_holdout.py
```

The report prints to the terminal. It includes the holdout dates, benchmark and strategy Sharpe ratios, three mandate verdicts, minimum reserve weight, and pilot decision for both cases.

## Decision and evidence

Approve a limited pilot under the stated rule if the holdout Sharpe meets or exceeds the benchmark’s and all three tested mandate constraints pass. Review rolling 12-month Sharpe against the benchmark and mandate compliance monthly. Pause new allocations and reassess after three consecutive monthly reviews below the benchmark’s rolling Sharpe or upon discovery of a mandate breach.

| Evidence | Base case | Changed input |
|---|---:|---:|
| SPY annual return assumption | 12.706676% | 10.706676% |
| Strategy target weights | 35% SPY, 65% SGOV | 45% SPY, 55% SGOV |
| Strategy Sharpe | 1.870006 | 1.669381 |
| Benchmark Sharpe | 1.305877 | 1.305877 |
| Long-only at rebalances | Pass | Pass |
| Fully invested at rebalances | Pass | Pass |
| Minimum reserve at rebalances, required ≥3% | 65.00%, pass | 55.00%, pass |
| Pilot decision under the tested rule | Approve limited pilot | Approve limited pilot |

The decision held after reducing only SPY’s annual return assumption by 2 percentage points. The lower forecast required a larger SPY weight to reach the 6.5% modeled return objective. The resulting holdout Sharpe declined and stayed above the benchmark.

## Method and limits

- **Training** uses 36 monthly returns ending September 30, 2024. The strategy uses the existing [portfolio search](portfolio.py) to find the lowest modeled volatility on a 5 percentage point weight grid, subject to the 6.5% modeled annual return objective and 3% reserve floor. SGOV alone counts toward the reserve.
- **Holdout** uses 24 monthly returns ending October 31, 2024 through September 30, 2026. Portfolio weights are fixed from training and reset at each modeled monthly rebalance. Compliance is measured on target weights at those rebalances. The result covers those checks and leaves intra-month weight drift unmeasured.
- **Benchmark** approximates 60% global equity and 40% U.S. investment-grade bonds with 36% SPY, 24% VXUS, and 40% BND. Both Sharpe ratios use the same months, a zero risk-free rate, sample standard deviation, and annualization by the square root of 12. Results exclude trading costs and taxes.
- **Point-in-time rule** uses only the training-period price returns to select weights. Holdout returns score the frozen weights. The [data card](prices_sources.md) documents the October 2026 adjusted-price snapshot. Historical adjustment vintages and execution at the assumed month-end prices have not been verified.

## Studio records

- **Partner cold run** is unresolved. Give the partner only the GitHub README link and have them record the command, first failure, elapsed time, and result location.
- **Locked Changed-Input Record** is unresolved. The one-input comparison above is a reproducible sensitivity result. A locked record requires the student’s prediction to be recorded before viewing the result of its test.
