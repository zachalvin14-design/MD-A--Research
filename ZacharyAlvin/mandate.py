"""Screen the Meridian common-case portfolios; amounts are in dollars."""

portfolio_value = 100_000_000
quarterly_payout = 750_000
quarters_to_cover = 4
reserve_minimum = quarters_to_cover * quarterly_payout / portfolio_value * 100

# Each holding has: issuer, business days to redeem, reserve eligibility.
# None means exempt from the single-issuer cap in this assigned case.
holdings = {
    "Cash": (None, 0, True),
    "Treasury bills": (None, 1, True),
    "Treasury 10-year note": (None, 1, True),
    "Global equity index fund": (None, 2, False),
    "Investment-grade bond fund": (None, 3, False),
    "Private real estate fund": (None, 90, False),
    "Acme Corp bonds": ("Acme Corp", 4, False),
    "Acme Corp stock": ("Acme Corp", 1, False),
}

# Percent of the portfolio, in the same order as holdings above.
candidates = {
    "A": [2, 2, 10, 60, 26, 0, 0, 0],
    "B": [1, 0, 0, 55, 20, 15, 5, 4],
    "C": [1, 1, 0, 70, 20, 0, 0, 8],
    "D": [100, 0, 0, 0, 0, 0, 0, 0],
}

def check_portfolio(weights):
    reserve_pct = 0
    liquid_pct = 0
    issuer_totals = {}

    for holding, weight in zip(holdings, weights):
        issuer, redemption_days, reserve_eligible = holdings[holding]
        if reserve_eligible:
            reserve_pct += weight
        if redemption_days <= 5:
            liquid_pct += weight
        if issuer is not None:
            issuer_totals[issuer] = issuer_totals.get(issuer, 0) + weight

    largest_issuer_pct = max(issuer_totals.values(), default=0)
    return [
        ("Weights sum to 100", sum(weights), sum(weights) == 100),
        ("Long-only (lowest weight)", min(weights), min(weights) >= 0),
        (f"Reserve >= {reserve_minimum:.1f}%", reserve_pct,
         reserve_pct >= reserve_minimum),
        ("Redeemable in 5 days >= 90%", liquid_pct, liquid_pct >= 90),
        ("Largest single company <= 8%", largest_issuer_pct,
         largest_issuer_pct <= 8),
    ]


def main():
    print(f"Reserve minimum: {reserve_minimum:.1f}% of the portfolio.")
    for name, weights in candidates.items():
        print(f"\nCandidate {name}")
        rules = check_portfolio(weights)
        for rule, value, passed in rules:
            print(f"  {rule}: {value:.1f} {'pass' if passed else 'FAIL'}")
        print("  Calendar-year loss: requires CIO clarification")
        failures = sum(not passed for _, _, passed in rules)
        verdict = (f"fails {failures} rule(s)" if failures
                   else "passes every checkable rule")
        print(f"  Verdict: {verdict}")
    print("\nFull compliance also requires horizon/rebalancing implementation, "
          "ongoing payouts, and turnover data or approval.")
    print("Before optimization: CIO must define the pilot's criterion and S9.")


if __name__ == "__main__":
    main()
