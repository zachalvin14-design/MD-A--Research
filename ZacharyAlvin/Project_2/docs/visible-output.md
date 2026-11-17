# Visible output

**Decision under the tested rule.** Approve a limited pilot in the base case. It passes all three mandate checks at modeled monthly rebalances and has a higher holdout Sharpe than the 60/40 benchmark proxy.

**Dates and convention.** Training returns ran from October 31, 2021 through September 30, 2024. The holdout ran from October 31, 2024 through September 30, 2026 and contained 24 monthly returns. All Sharpe ratios are annualized using a zero risk-free rate.

| Holdout evidence | Base | SPY assumption −2 pp | SPY assumption −6 pp |
|---|---:|---:|---:|
| SPY annual training return assumption | 12.706676% | 10.706676% | 6.706676% |
| Strategy target weights (SPY / SGOV) | 35% / 65% | 45% / 55% | 95% / 5% |
| Strategy Sharpe | 1.870006 | 1.669381 | 1.299253 |
| Benchmark Sharpe | 1.305877 | 1.305877 | 1.305877 |
| Long-only at rebalances | Pass | Pass | Pass |
| Fully invested at rebalances | Pass | Pass | Pass |
| Reserve at rebalances, required ≥3% | 65% · Pass | 55% · Pass | 5% · Pass |
| Decision | Approve limited pilot | Approve limited pilot | Reject pilot |

| Reference portfolio | Holdout Sharpe | Modeled annual return from training | 3% reserve check |
|---|---:|---:|---|
| 60/40 proxy | 1.305877 | 5.418173% | Fail (0%) |
| Equal weight | 1.514858 | 5.115559% | Pass (25%) |
| Inverse volatility | 5.001790 | 3.531604% | Pass (86.47%) |

All three reference portfolios passed the long-only and fully invested checks. The fixed 6.5% modeled annual return objective applies to the strategy search. A six-point haircut reverses the decision through the Sharpe comparison while the reserve check still passes.

**Pilot monitoring.** Check rolling 12-month Sharpe against the benchmark and review mandate compliance monthly. Pause new allocations and reassess on discovery of a mandate breach or after three consecutive reviews below the benchmark’s rolling Sharpe. Between-rebalance compliance remains unverified.

See the [run command](../README.md#reproduce-the-decision), [decision memo](decision-memo.md), and [changed-input record](../CHANGED_INPUT_RECORD.md).
