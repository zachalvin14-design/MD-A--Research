# Validation and AI use

| Check | Result | Evidence |
|---|---|---|
| Baseline comparison | Benchmark Sharpe 1.305877, equal weight 1.514858, inverse volatility 5.001790 | [Visible output](visible-output.md) |
| Mandate check | Long-only, fully invested, and at least 3% reserve all passed at tested rebalances for the base and both stress portfolios | [Visible output](visible-output.md) |
| Stress runs | A two-point SPY haircut preserved the pilot decision. A six-point haircut reversed it on Sharpe. | [Changed-Input Record](../CHANGED_INPUT_RECORD.md) |
| Locked Changed-Input Record | Six-point AI prediction saved before execution. A separate student-authored prediction remains open. | [Prediction](../LOCKED_PREDICTION.md), [reconciliation](../CHANGED_INPUT_RECORD.md) |
| Reproduction | Offline terminal report and app agreed. The partner cold run remains open. | [Cold-run record](../COLD_RUN.md) |
| Data timing | Weights use returns through the training cutoff. The later downloaded adjusted-price snapshot leaves historical vintages and execution timing unverified. | [Data card](../prices_sources.md) |

AI helped implement the report and app, draft documentation, and verify that the app output matched the terminal report. It also generated the recorded six-point prediction. The student’s personally checked AI output and reflection belong in Video 1.
