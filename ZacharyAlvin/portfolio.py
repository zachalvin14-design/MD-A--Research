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
    if size != 4:
        raise ValueError("Exactly four sleeves are required.")
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
