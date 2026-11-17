"""Reproduce the Project 2 holdout decision and a one-input sensitivity."""
from datetime import date
from pathlib import Path
from statistics import mean, stdev
import argparse
import csv
import math
import sys

from portfolio import (OBJECTIVE_RETURN, equal_weights, expected_return, inverse_volatility_weights,
                       search_lowest_volatility)

TICKERS = ("SPY", "VXUS", "BND", "SGOV")
BENCHMARK = (0.36, 0.24, 0.40, 0.0)
TRAIN_END = date(2024, 9, 30)
HOLDOUT_END = date(2026, 9, 30)
RESERVE_MINIMUM = 0.03
SPY_HAIRCUT = 0.02


def sharpe(returns):
    volatility = stdev(returns)
    if volatility == 0:
        raise ValueError("Sharpe ratio is undefined for zero sample volatility")
    return math.sqrt(12) * mean(returns) / volatility


def portfolio_returns(monthly_returns, weights):
    return [sum(w * r for w, r in zip(weights, row)) for row in monthly_returns]


def show_compliance(weights, sleeves, emit):
    reserve = sum(weight for weight, sleeve in zip(weights, sleeves) if sleeve["reserve_eligible"])
    checks = {
        "Long-only": min(weights) >= 0,
        "Fully invested": math.isclose(sum(weights), 1.0, rel_tol=0, abs_tol=1e-12),
        "Reserve at least 3%": reserve >= RESERVE_MINIMUM - 1e-12,
    }
    for name, passed in checks.items():
        emit(f"{name}: {'PASS' if passed else 'FAIL'}")
    emit(f"Minimum reserve at tested rebalances: {reserve:.2%}")
    return all(checks.values())


def evaluate(label, sleeves, correlation, monthly_returns, benchmark_sharpe, emit):
    emit(f"\n{label}")
    equity_return = sleeves[TICKERS.index("SPY")]["return"]
    emit(f"SPY annual return assumption: {equity_return:.6%}")
    result = search_lowest_volatility(sleeves, correlation, OBJECTIVE_RETURN, RESERVE_MINIMUM)
    if result is None:
        emit("No feasible portfolio. Strategy Sharpe and mandate verdicts unavailable.")
        emit("Decision: Reject pilot and retain benchmark.")
        return "Reject pilot and retain benchmark"

    weights = result["weights"]
    emit("Target weights: " + ", ".join(f"{t} {w:.2%}" for t, w in zip(TICKERS, weights)))
    emit(f"Modeled annual return: {result['return']:.6%}")
    strategy_sharpe = sharpe(portfolio_returns(monthly_returns, weights))
    emit(f"Strategy Sharpe: {strategy_sharpe:.6f}")
    passes = show_compliance(weights, sleeves, emit) and strategy_sharpe >= benchmark_sharpe
    decision = "Approve limited pilot" if passes else "Reject pilot and retain benchmark"
    emit(f"Decision: {decision}.")
    return decision


def training_inputs(rows):
    columns = list(zip(*rows))
    means = [mean(column) for column in columns]
    deviations = [stdev(column) for column in columns]
    if any(deviation == 0 for deviation in deviations):
        raise ValueError("Each training series must have nonzero volatility")
    centered = [[value - average for value in column]
                for column, average in zip(columns, means)]
    correlation = [[1.0] * len(TICKERS) for _ in TICKERS]
    for i in range(len(TICKERS)):
        for j in range(i):
            covariance = sum(a * b for a, b in zip(centered[i], centered[j])) / (len(rows) - 1)
            value = covariance / (deviations[i] * deviations[j])
            correlation[i][j] = correlation[j][i] = max(-1.0, min(1.0, value))
    sleeves = [
        {"name": ticker, "return": average * 12, "volatility": deviation * math.sqrt(12),
         "reserve_eligible": ticker == "SGOV"}
        for ticker, average, deviation in zip(TICKERS, means, deviations)
    ]
    return sleeves, correlation


def run_report(spy_haircut=SPY_HAIRCUT, output=sys.stdout):
    def emit(line):
        print(line, file=output)

    path = Path(__file__).with_name("prices.csv")
    with path.open(newline="") as file:
        rows = list(csv.reader(file))
    if not rows or rows[0] != ["Date", *TICKERS]:
        raise ValueError("Expected Date,SPY,VXUS,BND,SGOV")
    dates = [date.fromisoformat(row[0]) for row in rows[1:]]
    if len(dates) != 61 or dates[36] != TRAIN_END or dates[-1] != HOLDOUT_END:
        raise ValueError("Expected 36 training months and 24 holdout months ending on the fixed dates")
    if any(b.year * 12 + b.month - a.year * 12 - a.month != 1 for a, b in zip(dates, dates[1:])):
        raise ValueError("Expected consecutive price months")
    prices = [[float(value) for value in row[1:]] for row in rows[1:]]
    if any(len(row) != len(TICKERS) or any(not math.isfinite(p) or p <= 0 for p in row) for row in prices):
        raise ValueError("Expected four finite positive prices each month")

    returns = [
        [new / old - 1 for old, new in zip(previous, current)]
        for previous, current in zip(prices, prices[1:])
    ]
    split = dates.index(TRAIN_END)
    sleeves, correlation = training_inputs(returns[:split])
    monthly_returns = returns[split:]
    benchmark_sharpe = sharpe(portfolio_returns(monthly_returns, BENCHMARK))
    emit(f"Training return dates: {dates[1]} to {TRAIN_END}")
    emit(f"Holdout return dates: {dates[37]} to {HOLDOUT_END} ({len(monthly_returns)} monthly returns)")
    emit("Benchmark weights: 36% SPY, 24% VXUS, 40% BND")
    emit(f"Benchmark Sharpe: {benchmark_sharpe:.6f} (both portfolios use zero risk-free rate)")
    emit(f"Annual return objective: {OBJECTIVE_RETURN:.2%}")
    emit("Compliance checked at monthly rebalances.")
    for name, weights in (
        ("Benchmark", BENCHMARK),
        ("Equal weight", equal_weights(sleeves)),
        ("Inverse volatility", inverse_volatility_weights(sleeves)),
    ):
        emit(f"\n{name} reference portfolio")
        emit("Target weights: " + ", ".join(f"{t} {w:.2%}" for t, w in zip(TICKERS, weights)))
        emit(f"Modeled annual return: {expected_return(weights, sleeves):.6%}")
        emit(f"Holdout Sharpe: {sharpe(portfolio_returns(monthly_returns, weights)):.6f}")
        show_compliance(weights, sleeves, emit)
    base = evaluate("Base case", sleeves, correlation, monthly_returns, benchmark_sharpe, emit)
    changed = [
        {**sleeve, "return": sleeve["return"] - spy_haircut} if sleeve["name"] == "SPY" else sleeve
        for sleeve in sleeves
    ]
    stress = evaluate(f"Changed input: SPY return assumption down {spy_haircut * 100:g} percentage points",
                      changed, correlation, monthly_returns, benchmark_sharpe, emit)
    emit(f"\nDecision after the change: {'unchanged' if base == stress else 'reversed'}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spy-haircut-pp", type=float, default=SPY_HAIRCUT * 100,
                        help="Reduction in the SPY training return assumption in percentage points")
    args = parser.parse_args()
    if not math.isfinite(args.spy_haircut_pp) or args.spy_haircut_pp < 0:
        parser.error("--spy-haircut-pp must be finite and nonnegative")
    run_report(args.spy_haircut_pp / 100)
