# Portfolio mandate

**Objective.** Find the lowest modeled volatility portfolio that reaches a 6.5% modeled annual return objective on the existing five-percentage-point weight grid. Treat the 6.5% objective as a modeling input.

**Hard constraints.** Long-only target weights, fully invested, and at least 3% in reserve-eligible assets. In this ETF universe, SGOV alone counts toward the reserve. The tested checks apply at modeled monthly rebalances.

**Pilot approval.** Approve a limited pilot only if the strategy’s holdout Sharpe at least matches the 60/40 proxy and all three mandate constraints pass. The holdout and benchmark conventions are in the [README](README.md).

**Monitor and reversal.** At monthly reviews compare rolling 12-month strategy and benchmark Sharpe and check mandate compliance. Pause new allocations and reassess after three consecutive reviews below the benchmark’s rolling Sharpe or upon discovery of a mandate breach.

**Client question.** Does the committee accept compliance measured at monthly rebalances, or does the 3% reserve floor need to hold between rebalances? If it must hold continuously, what buffer and trading authority should the pilot use?
