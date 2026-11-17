AI assisted with code, verification, and this memo. For education, not investment advice.

# Committee memo

**Decision.** Approve a limited pilot under the tested rule. From October 2024 through September 2026, the strategy’s annualized Sharpe was **1.870006** versus **1.305877** for the 60/40 proxy. All three mandate checks passed at the modeled monthly rebalances. The target was 35% SPY and 65% SGOV, for a minimum tested reserve of 65% against the required 3%.

**Conditions and monitoring.** Review rolling 12-month strategy and benchmark Sharpe and mandate compliance monthly. Pause new allocations and reassess upon discovery of any mandate breach or three consecutive monthly reviews with strategy Sharpe below the benchmark’s. Confirm with the committee whether the reserve must also be maintained between rebalances.

**Changed input.** Lowering only the annual SPY return assumption by two percentage points left the pilot decision intact. Lowering it by six points increased the SPY allocation to 95% and reduced the holdout Sharpe to **1.299253**, below the same benchmark. The 5% reserve still passed. Under that assumption, reject the pilot and retain the benchmark for comparison until the strategy is improved and retested. The benchmark itself has 0% in reserve-eligible assets and requires a separate mandate review before it could serve as the investable reserve portfolio.

**Alternative and limitations.** Inverse volatility produced a holdout Sharpe of 5.001790 with 86.47% SGOV and a training-period modeled annual return of 3.531604%, below the 6.5% objective. That comparison is a reason to confirm how the committee weighs the modeled return objective against lower volatility. The holdout has 24 monthly returns, assumes month-end rebalancing without costs or taxes, and uses an adjusted-price snapshot downloaded after the sample ended. The three constraint checks apply to monthly target weights. The calculation leaves vintage revisions, between-rebalance compliance, and execution prices unverified.

Reproduce the figures using the [README](../README.md) and [Changed-Input Record](../CHANGED_INPUT_RECORD.md).
