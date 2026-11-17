# Changed-input prediction

Recorded before running the six-point sensitivity at 2026-11-17T22:24:29Z.

Reduce only the annualized SPY training return assumption by 6 percentage points. Keep the dataset, training dates, holdout dates, covariance, portfolio constraints, return objective, benchmark, and Sharpe convention fixed.

AI-generated prediction for Zachary to review. The selected SPY allocation will increase, the strategy's holdout Sharpe ratio will fall below the benchmark's, and the pilot decision will reverse. The rationale is that a lower expected equity return pushes the optimizer toward greater equity exposure to reach the same fixed return target.

Run `python3 project2_holdout.py --spy-haircut-pp 6`.
