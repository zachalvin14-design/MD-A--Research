"""Reproduce the Project 2 holdout decision and a one-input sensitivity."""
from datetime import date
from io import StringIO
from pathlib import Path
from statistics import mean, stdev
import csv
import math

from portfolio import OBJECTIVE_RETURN, estimate_from_prices, search_lowest_volatility

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


def evaluate(label, sleeves, correlation, monthly_returns, benchmark_sharpe):
    print(f"\n{label}")
    equity_return = sleeves[TICKERS.index("SPY")]["return"]
    print(f"SPY annual return assumption: {equity_return:.6%}")
    result = search_lowest_volatility(sleeves, correlation, OBJECTIVE_RETURN, RESERVE_MINIMUM)
    if result is None:
        print("No feasible portfolio. Strategy Sharpe and mandate verdicts unavailable.")
        print("Decision: Reject pilot and retain benchmark.")
        return "Reject pilot and retain benchmark"

    weights = result["weights"]
    print("Target weights: " + ", ".join(f"{t} {w:.2%}" for t, w in zip(TICKERS, weights)))
    strategy_sharpe = sharpe(portfolio_returns(monthly_returns, weights))
    print(f"Strategy Sharpe: {strategy_sharpe:.6f}")
    checks = {
        "Long-only": min(weights) >= 0,
        "Fully invested": math.isclose(sum(weights), 1.0, rel_tol=0, abs_tol=1e-12),
        "Reserve at least 3%": result["reserve_weight"] >= RESERVE_MINIMUM - 1e-12,
    }
    for name, passed in checks.items():
        print(f"{name}: {'PASS' if passed else 'FAIL'}")
    print(f"Minimum reserve at tested rebalances: {result['reserve_weight']:.2%}")
    passes = all(checks.values()) and strategy_sharpe >= benchmark_sharpe
    decision = "Approve limited pilot" if passes else "Reject pilot and retain benchmark"
    print(f"Decision: {decision}.")
    return decision


def main():
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

    sleeves, correlation = estimate_from_prices(StringIO("\n".join(",".join(row) for row in rows[:38])))
    for sleeve in sleeves:
        sleeve["reserve_eligible"] = sleeve["name"] == "SGOV"
    monthly_returns = [
        [new / old - 1 for old, new in zip(prices[i - 1], prices[i])]
        for i in range(37, len(prices))
    ]
    benchmark_sharpe = sharpe(portfolio_returns(monthly_returns, BENCHMARK))
    print(f"Training return dates: {dates[1]} to {TRAIN_END}")
    print(f"Holdout return dates: {dates[37]} to {HOLDOUT_END} ({len(monthly_returns)} monthly returns)")
    print("Benchmark weights: 36% SPY, 24% VXUS, 40% BND")
    print(f"Benchmark Sharpe: {benchmark_sharpe:.6f} (both portfolios use zero risk-free rate)")
    print(f"Annual return objective: {OBJECTIVE_RETURN:.2%}")
    print("Compliance checked at monthly rebalances.")
    base = evaluate("Base case", sleeves, correlation, monthly_returns, benchmark_sharpe)
    changed = [
        {**sleeve, "return": sleeve["return"] - SPY_HAIRCUT} if sleeve["name"] == "SPY" else sleeve
        for sleeve in sleeves
    ]
    stress = evaluate("Changed input: SPY return assumption down 2 percentage points",
                      changed, correlation, monthly_returns, benchmark_sharpe)
    print(f"\nDecision after the change: {'unchanged' if base == stress else 'reversed'}.")


if __name__ == "__main__":
    main()
