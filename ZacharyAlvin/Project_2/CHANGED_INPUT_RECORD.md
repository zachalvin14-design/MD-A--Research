# Changed-Input Record

The [prediction](LOCKED_PREDICTION.md) was written and hashed before the six-point run. It is attributed to AI. A student-authored prediction remains open. Prediction SHA-256 `322f310bbc5b3c96dcb72546dec2e1f504ecdd6e434f33f87e6ef57b82b2026c`.

Run `python3 project2_holdout.py --spy-haircut-pp 6`.

| Measure | Base | Changed |
|---|---:|---:|
| SPY annual return assumption | 12.706676% | 6.706676% |
| SPY / SGOV target weights | 35% / 65% | 95% / 5% |
| Strategy Sharpe | 1.870006 | 1.299253 |
| Benchmark Sharpe | 1.305877 | 1.305877 |
| Mandate verdicts at monthly rebalances | All three pass | All three pass |
| Pilot decision | Approve limited pilot | Reject pilot and retain benchmark |

The prediction matched the result. The lower assumed SPY return pushed the optimizer toward a heavier equity allocation to reach the same modeled 6.5% return objective. The resulting strategy Sharpe fell 0.006624 below the benchmark. The reserve remained above 3%. A separate two-point reduction left the pilot decision unchanged, with a Sharpe of 1.669381.

The stress perturbs a training assumption. Evaluation dates, realized returns, benchmark, covariance and constraint settings are held fixed. The stress does not estimate the likelihood of a six-point forecast error.

The base section matched exactly before and during the changed run. A fresh default run after the changed-input run also reproduced the original output byte-for-byte. See the [cold-run record](COLD_RUN.md).

For a fresh student-authored record, use a four-percentage-point reduction, which was not run while preparing this bundle. First record the predicted allocation direction, whether the strategy’s Sharpe will clear the benchmark, the resulting decision, and your reason. Save that prediction before running `python3 project2_holdout.py --spy-haircut-pp 4`. Then record the actual result and explain any difference.
