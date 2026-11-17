AI assisted with building and checking this project. For education, not investment advice.

# Project 2 — Portfolio pilot decision

## Reproduce the decision

From the cloned repository root, use Python 3.9 or later. The first line enters the Project 2 folder. The report runs offline on the bundled data with no package installation.

```sh
cd ZacharyAlvin/Project_2
python3 project2_holdout.py
```

The terminal report prints the holdout dates, baseline comparisons, mandate verdicts, and pilot decision. The default command includes a two-point stress. For the six-point reversal, run `python3 project2_holdout.py --spy-haircut-pp 6`. See the [visible results](docs/visible-output.md) for both runs.

To open the interactive app, install the separate app dependency in a virtual environment.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-app.txt
.venv/bin/python -m streamlit run app.py
```

The app opens with the same holdout report. Change the SPY haircut from 2 to 6 and read the updated decision and three mandate verdicts in the Changed input section.

## Decision and evidence

Approve a limited pilot under the stated rule if the holdout Sharpe meets or exceeds the benchmark’s and all three tested mandate constraints pass. Review rolling 12-month Sharpe against the benchmark and mandate compliance monthly. Pause new allocations and reassess after three consecutive monthly reviews below the benchmark’s rolling Sharpe or upon discovery of a mandate breach.

The [visible results](docs/visible-output.md) show the base case, both stress runs, and the baseline comparisons.

## Method and limits

- **Training** uses 36 monthly returns ending September 30, 2024. The strategy uses the existing [portfolio search](portfolio.py) to find the lowest modeled volatility on a 5 percentage point weight grid, subject to the 6.5% modeled annual return objective and 3% reserve floor. SGOV alone counts toward the reserve.
- **Holdout** uses 24 monthly returns ending October 31, 2024 through September 30, 2026. Portfolio weights are fixed from training and reset at each modeled monthly rebalance. Compliance is measured on target weights at those rebalances. The result covers those checks and leaves intra-month weight drift unmeasured.
- **Benchmark** approximates 60% global equity and 40% U.S. investment-grade bonds with 36% SPY, 24% VXUS, and 40% BND. Both Sharpe ratios use the same months, a zero risk-free rate, sample standard deviation, and annualization by the square root of 12. Results exclude trading costs and taxes.
- **Point-in-time rule** uses only the training-period price returns to select weights. Holdout returns score the frozen weights. The [data card](prices_sources.md) documents the October 2026 adjusted-price snapshot. Historical adjustment vintages and execution at the assumed month-end prices have not been verified.

## Submission

See the [submission manifest](SUBMISSION_MANIFEST.md), [committee memo](docs/decision-memo.md), [cold-run record](COLD_RUN.md), and [video rehearsal scripts](VIDEO_SCRIPTS.md).
