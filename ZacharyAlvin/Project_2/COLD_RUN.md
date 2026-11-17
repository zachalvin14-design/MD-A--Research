# Cold-run record

## Local verification · November 17, 2026

- README command: `python3 project2_holdout.py`.
- First failure: none in the local command run.
- Elapsed: 0.038 seconds for the default report on this machine.
- Result location: terminal standard output. The app’s Holdout decision report matched the terminal report in both stress cases.
- Isolated replay: the same output was reproduced on Python 3.9.6 with user environment and site packages disabled using `-I -S`.
- Reconciliation: running the six-point case left the base section unchanged, and rerunning the default report reproduced its original output byte-for-byte.

## Partner cold run

Unresolved. A partner must start from the GitHub README link in their own folder and record the command, first failure, elapsed time, and result location independently.
