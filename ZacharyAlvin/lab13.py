"""Lab 13: course-authored training inputs, not market estimates."""

import numpy as np


sleeves = ["Treasury bills", "Treasury 10-year note", "IG bond fund", "Global equity"]
returns = np.array([0.035, 0.043, 0.050, 0.080])
volatility = np.array([0.005, 0.070, 0.060, 0.160])
correlation = np.array([
    [1.00, 0.10, 0.05, 0.00],
    [0.10, 1.00, 0.80, -0.10],
    [0.05, 0.80, 1.00, 0.25],
    [0.00, -0.10, 0.25, 1.00],
])
covariance = np.outer(volatility, volatility) * correlation
inverse_volatility = 1 / volatility
portfolios = {
    "Benchmark": np.array([0.00, 0.00, 0.40, 0.60]),
    "Equal weight": np.full(4, 0.25),
    "Inverse volatility": inverse_volatility / inverse_volatility.sum(),
}


def main():
    print("Lab 13 — annual course-authored training values, not market estimates")
    print("Expected-return objective: 6.5%; minimum eligible reserve: 3%")
    for name, weights in portfolios.items():
        expected_return = weights @ returns
        portfolio_volatility = np.sqrt(weights @ covariance @ weights)
        reserve = weights[0] + weights[1]
        print(f"\n{name}")
        for sleeve, weight in zip(sleeves, weights):
            print(f"  {sleeve}: {weight:.2%}")
        print(f"  Expected annual return: {expected_return:.3%}")
        print(f"  Annual volatility: {portfolio_volatility:.3%}")
        print(f"  Expected gain on $100m: ${100_000_000 * expected_return:,.0f}")
        print(f"  Meets expected-return objective: {expected_return >= 0.065}")
        print(f"  Eligible reserve: {reserve:.2%}; passes: {reserve >= 0.03}")
    print("\nExpected returns are not guarantees; volatility is not a maximum loss.")
    print("Full mandate compliance still requires the remaining Meridian checks.")


if __name__ == "__main__":
    main()
