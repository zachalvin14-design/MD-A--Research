# Project 2 video rehearsal scripts

## Video 1 · How it changed

Open with “I used AI to help develop and check this project. This is for education, not investment advice.”

Show the original mandate and the holdout report. Explain in your own words how your initial mandate became a measurable pilot rule and what changed in your thinking. Show one AI output you personally checked. A check to rehearse is confirming that 5% SGOV passes the 3% reserve floor in the six-point run and that Sharpe, rather than reserve compliance, reverses the decision.

## Video 2 · Technical walkthrough

Open with “I used AI to help develop and check this project. This is for education, not investment advice.”

Start with the README and run `python3 project2_holdout.py`. Show the saved monthly prices, the September 2024 training cutoff, and the October 2024–September 2026 holdout. Explain the 5-point grid, the 6.5% modeled return objective, and SGOV’s reserve role. Point to the base Sharpe of 1.870006 and benchmark Sharpe of 1.305877. Run the six-point haircut and show the Sharpe comparison failing at 1.299253 while the three mandate constraints pass. State that weights are checked at modeled monthly rebalances.

## Video 3 · Committee presentation

Open with “I used AI to help develop and check this project. This is for education, not investment advice.”

“Under the tested rule, I recommend a limited pilot. The holdout Sharpe was 1.870006 against 1.305877 for our benchmark proxy, and all three mandate checks passed at monthly rebalances. I would monitor rolling 12-month Sharpe against the benchmark and review mandate compliance every month. Pause new allocations on a mandate breach or when our rolling Sharpe trails the benchmark’s for three consecutive reviews. A six-point reduction in the SPY return assumption reversed the holdout decision. Sharpe fell to 1.299253 even though the reserve still passed at 5%.”

**Skeptical question.** Can you establish that the reserve stayed above 3% between rebalances?

**Answer.** “My system cannot establish that. I checked the target weights at monthly rebalances. I would clarify with the committee when the reserve floor must apply.”
