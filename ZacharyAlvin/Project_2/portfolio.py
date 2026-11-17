"""Lab 13 portfolio comparison using course-authored training values."""

import math
import sys


# Editable inputs: annual returns and volatilities expressed as decimals.
# Correlation rows and columns follow the same order as SLEEVES.
SLEEVES = [
    {"name": "Treasury bills", "return": 0.035, "volatility": 0.005,
     "reserve_eligible": True},
    {"name": "Treasury 10-year note", "return": 0.043, "volatility": 0.070,
     "reserve_eligible": True},
    {"name": "Investment-grade bond fund", "return": 0.050, "volatility": 0.060,
     "reserve_eligible": False},
    {"name": "Global equity index fund", "return": 0.080, "volatility": 0.160,
     "reserve_eligible": False},
]
CORRELATION = [
    [1.00, 0.10, 0.05, 0.00],
    [0.10, 1.00, 0.80, -0.10],
    [0.05, 0.80, 1.00, 0.25],
    [0.00, -0.10, 0.25, 1.00],
]
OBJECTIVE_RETURN = 0.065


def validate_inputs(sleeves, correlation, objective):
    """Reject malformed inputs before performing portfolio calculations."""
    size = len(sleeves)
    if size == 0:
        raise ValueError("At least one sleeve is required.")
    if len(correlation) != size or any(len(row) != size for row in correlation):
        raise ValueError("Correlation table must have one row and column per sleeve.")
    for i in range(size):
        for j in range(size):
            value = correlation[i][j]
            if not math.isfinite(value) or not -1 <= value <= 1:
                raise ValueError(
                    f"Correlation at row {i + 1}, column {j + 1} must be between -1 and 1."
                )
            if value != correlation[j][i]:
                raise ValueError("Correlation table must be symmetric.")
        if correlation[i][i] != 1:
            raise ValueError("Each diagonal correlation must equal 1.")
    for sleeve in sleeves:
        if not math.isfinite(sleeve["return"]):
            raise ValueError("Expected returns must be finite numbers.")
        if not math.isfinite(sleeve["volatility"]) or sleeve["volatility"] <= 0:
            raise ValueError("Volatilities must be finite and greater than zero.")
    if not math.isfinite(objective):
        raise ValueError("Objective return must be a finite number.")


def build_covariance(sleeves, correlation):
    """Covariance(i, j) = correlation(i, j) * volatility(i) * volatility(j)."""
    return [
        [correlation[i][j] * left["volatility"] * right["volatility"]
         for j, right in enumerate(sleeves)]
        for i, left in enumerate(sleeves)
    ]


def benchmark_weights(sleeves):
    allocation = {"Investment-grade bond fund": 0.40, "Global equity index fund": 0.60}
    if not allocation.keys() <= {sleeve["name"] for sleeve in sleeves}:
        raise ValueError("Benchmark requires the investment-grade bond and global equity sleeves.")
    return [allocation.get(sleeve["name"], 0.0) for sleeve in sleeves]


def equal_weights(sleeves):
    return [1 / len(sleeves)] * len(sleeves)


def inverse_volatility_weights(sleeves):
    inverse = [1 / sleeve["volatility"] for sleeve in sleeves]
    total = sum(inverse)
    return [value / total for value in inverse]


def expected_return(weights, sleeves):
    return sum(weight * sleeve["return"] for weight, sleeve in zip(weights, sleeves))


def portfolio_variance(weights, covariance):
    return sum(weights[i] * weights[j] * covariance[i][j]
               for i in range(len(weights)) for j in range(len(weights)))


def portfolio_volatility(weights, covariance):
    variance = portfolio_variance(weights, covariance)
    if variance < 0:
        raise ValueError("Inputs produce negative portfolio variance; check correlations.")
    return math.sqrt(variance)


def reserve_weight(weights, sleeves):
    return sum(weight for weight, sleeve in zip(weights, sleeves)
               if sleeve["reserve_eligible"])


def meets_objective(portfolio_return, objective):
    return portfolio_return >= objective


def search_lowest_volatility(sleeves, correlation, objective, reserve_minimum=0.03):
    """Search all fully invested, long-only weights in 5 percentage point steps.

    Return weights and annual metrics in decimals, or None if infeasible.
    Equal-risk ties keep the first mix encountered in asset order.
    """
    validate_inputs(sleeves, correlation, objective)
    if not math.isfinite(reserve_minimum) or not 0 <= reserve_minimum <= 1:
        raise ValueError("Reserve minimum must be between 0 and 1.")
    covariance = build_covariance(sleeves, correlation)
    best = None

    def visit(units, remaining):
        nonlocal best
        if len(units) < len(sleeves) - 1:
            for amount in range(remaining + 1):
                visit(units + [amount], remaining - amount)
            return
        weights = [amount / 20 for amount in units + [remaining]]
        result = expected_return(weights, sleeves)
        reserve = reserve_weight(weights, sleeves)
        # Allow only floating-point rounding at constraint boundaries.
        if result + 1e-12 < objective or reserve + 1e-12 < reserve_minimum:
            return
        volatility = portfolio_volatility(weights, covariance)
        if best is None or volatility < best["volatility"]:
            best = {"weights": weights, "return": result,
                    "volatility": volatility, "reserve_weight": reserve}

    visit([], 20)
    return best


def estimate_from_prices(csv_file, last_36_months=False):
    """Return (sleeves, correlation) from complete, consecutive monthly prices.

    First column is date, remaining columns are tickers; oldest row first.
    Uses simple returns, arithmetic mean * 12 and sample SD * sqrt(12).
    Annualized arithmetic returns describe the selected history, not forecasts.
    The optional window takes 36 RETURNS (37 price rows), not 36 prices.
    Reserve eligibility defaults to False because ticker roles are unknown.
    """
    import pandas as pd

    prices = pd.read_csv(csv_file)
    if prices.shape[1] < 2 or len(prices) < 3:
        raise ValueError("CSV needs a date column, at least one ticker, and three price rows.")
    dates = pd.to_datetime(prices.iloc[:, 0], errors="raise")
    if dates.isna().any() or not dates.is_monotonic_increasing or dates.duplicated().any():
        raise ValueError("Dates must be unique and ordered oldest first.")
    months = dates.dt.to_period("M").astype("int64")
    if not months.diff().iloc[1:].eq(1).all():
        raise ValueError("Use exactly one price row per consecutive month, with no gaps.")
    values = prices.iloc[:, 1:].apply(pd.to_numeric, errors="raise")
    if not all(math.isfinite(float(x)) and x > 0 for x in values.to_numpy().flat):
        raise ValueError("All prices must be finite, positive, and present.")
    returns = values.pct_change(fill_method=None).iloc[1:]
    if last_36_months:
        if len(returns) < 36:
            raise ValueError("Last 36 months requires at least 37 monthly price rows.")
        returns = returns.tail(36)
    means = returns.mean() * 12
    volatilities = returns.std(ddof=1) * math.sqrt(12)
    if (volatilities <= 0).any():
        raise ValueError("Each ticker needs varying monthly returns to estimate correlations.")
    correlation = returns.corr().to_numpy().tolist()
    sleeves = [{"name": str(ticker), "return": float(means[ticker]),
                "volatility": float(volatilities[ticker]), "reserve_eligible": False}
               for ticker in values.columns]
    validate_inputs(sleeves, correlation, OBJECTIVE_RETURN)
    return sleeves, correlation


# Quiz: For each print the weights in percent to one decimal, expected return and
# volatility in percent to two decimals, the reserve-eligible weight (bills plus
# the 10-year note),
def print_portfolio(name, weights, sleeves, covariance, objective):
    result = expected_return(weights, sleeves)
    print(f"\n{name}")
    for sleeve, weight in zip(sleeves, weights):
        print(f"  {sleeve['name']}: {weight:.1%}")
    print(f"  Expected return: {result:.2%}")
    print(f"  Volatility: {portfolio_volatility(weights, covariance):.2%}")
    print(f"  Reserve-eligible weight: {reserve_weight(weights, sleeves):.1%}")
    print(f"  Meets objective: {'Yes' if meets_objective(result, objective) else 'No'}")


def main():
    try:
        validate_inputs(SLEEVES, CORRELATION, OBJECTIVE_RETURN)
        covariance = build_covariance(SLEEVES, CORRELATION)
        portfolios = [
            ("Benchmark", benchmark_weights(SLEEVES)),
            ("Equal weight", equal_weights(SLEEVES)),
            ("Inverse volatility", inverse_volatility_weights(SLEEVES)),
        ]
        # Calculate risks before printing so invalid inputs produce no partial report.
        for _, weights in portfolios:
            portfolio_volatility(weights, covariance)
        print("Lab 13 — course-authored training values (annual)")
        print(f"Objective return: {OBJECTIVE_RETURN:.2%}")
        for name, weights in portfolios:
            print_portfolio(name, weights, SLEEVES, covariance, OBJECTIVE_RETURN)
    except (ValueError, TypeError, KeyError) as error:
        print(f"Cannot run: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
