"""Asbury Automotive Group five-year pro forma and equity valuation."""


growth = 0.018
gross_margin = 0.1705
sga_ratios = [0.665, 0.655, 0.645, 0.645, 0.645]
depreciation_ratio = 82.4 / 3_070.4
annual_impairment = 120.0
annual_capex = 250.0
tax_rate = 0.255
inventory_days = 2_135.8 / (17_999.0 - 3_071.7) * 365.0
floor_plan_ratio = 2_027.0 / 2_135.8
other_working_capital_rate = 0.008
minimum_cash = 25.0
revolver_limit = 850.0
revolver_rate = 0.06
annual_repayment = 150.0
annual_buyback = 150.0
floor_plan_rate = 0.0467
debt_rate = 0.0544
cost_of_equity = 0.10
terminal_growth = 0.025
shares_outstanding = 17.951349

opening = {
    "revenue": 17_999.0,
    "inventory": 2_135.8,
    "ppe": 3_070.4,
    "other_assets": 6_371.6,
    "cash": 40.4,
    "floor_plan": 2_027.0,
    "debt": 3_572.0,
    "revolver": 0.0,
    "other_liabilities": 2_127.5,
    "equity": 3_891.7,
}


def project_year(year, prior, sga_ratio):
    revenue = prior["revenue"] * (1.0 + growth)
    revenue_change = revenue - prior["revenue"]
    gross_profit = revenue * gross_margin
    sga = gross_profit * sga_ratio
    depreciation = prior["ppe"] * depreciation_ratio
    impairment = annual_impairment
    operating_income = gross_profit - sga - depreciation - impairment

    floor_plan_interest = prior["floor_plan"] * floor_plan_rate
    debt_interest = prior["debt"] * debt_rate
    revolver_interest = prior["revolver"] * revolver_rate
    interest = floor_plan_interest + debt_interest + revolver_interest
    pretax_income = operating_income - interest
    tax = max(0.0, pretax_income) * tax_rate
    net_income = pretax_income - tax

    inventory = (revenue - gross_profit) * inventory_days / 365.0
    floor_plan = inventory * floor_plan_ratio
    ppe = prior["ppe"] + annual_capex - depreciation
    other_working_capital_change = other_working_capital_rate * revenue_change
    other_assets = (
        prior["other_assets"] + other_working_capital_change - impairment
    )
    repayment = min(annual_repayment, prior["debt"])
    debt = prior["debt"] - repayment
    other_liabilities = prior["other_liabilities"]
    equity = prior["equity"] + net_income - annual_buyback

    inventory_change = inventory - prior["inventory"]
    floor_plan_change = floor_plan - prior["floor_plan"]
    fcfe = (
        net_income
        + depreciation
        + impairment
        - annual_capex
        - inventory_change
        - other_working_capital_change
        + floor_plan_change
        - repayment
    )

    cash_before_revolver = prior["cash"] + fcfe - annual_buyback
    revolver = prior["revolver"]
    revolver_change = 0.0
    if cash_before_revolver < minimum_cash:
        draw = minimum_cash - cash_before_revolver
        if revolver + draw > revolver_limit:
            raise ValueError(f"{year}: required revolver exceeds the limit")
        revolver += draw
        revolver_change = draw
        cash = minimum_cash
    else:
        repayment_capacity = cash_before_revolver - minimum_cash
        revolver_repayment = min(revolver, repayment_capacity)
        revolver -= revolver_repayment
        revolver_change = -revolver_repayment
        cash = cash_before_revolver - revolver_repayment

    total_assets = cash + inventory + ppe + other_assets
    total_liabilities = floor_plan + debt + revolver + other_liabilities
    balance_gap = total_assets - total_liabilities - equity

    return {
        "year": year,
        "revenue": revenue,
        "gross_profit": gross_profit,
        "sga": sga,
        "depreciation": depreciation,
        "impairment": impairment,
        "operating_income": operating_income,
        "interest": interest,
        "pretax_income": pretax_income,
        "tax": tax,
        "net_income": net_income,
        "cash": cash,
        "inventory": inventory,
        "ppe": ppe,
        "other_assets": other_assets,
        "total_assets": total_assets,
        "floor_plan": floor_plan,
        "debt": debt,
        "revolver": revolver,
        "other_liabilities": other_liabilities,
        "total_liabilities": total_liabilities,
        "equity": equity,
        "fcfe": fcfe,
        "buyback": annual_buyback,
        "revolver_change": revolver_change,
        "balance_gap": balance_gap,
        "cash_minimum_met": cash >= minimum_cash,
        "repayment": repayment,
    }


def build_proforma():
    projections = []
    prior = opening.copy()
    for year, sga_ratio in zip(range(2026, 2031), sga_ratios):
        current = project_year(year, prior, sga_ratio)
        projections.append(current)
        prior = current
    return projections


def assert_balanced(projections, tolerance=0.01):
    for row in projections:
        if abs(row["balance_gap"]) > tolerance:
            raise ValueError(
                f"{row['year']}: balance sheet gap is {row['balance_gap']:.6f}"
            )
        if not row["cash_minimum_met"]:
            gap = row["cash"] - minimum_cash
            raise ValueError(
                f"{row['year']}: cash minimum check failed; gap is {gap:.6f}"
            )


def print_statement(title, projections, lines):
    print(f"\n{title}")
    print("USD millions".ljust(27) + "".join(f"{row['year']:>13}" for row in projections))
    print("-" * (27 + 13 * len(projections)))
    for label, key in lines:
        print(label.ljust(27) + "".join(f"{row[key]:13,.1f}" for row in projections))


def value_equity(projections):
    present_value_fcfe = sum(
        row["fcfe"] / (1.0 + cost_of_equity) ** period
        for period, row in enumerate(projections, start=1)
    )
    terminal_cash_flow = projections[-1]["fcfe"] + projections[-1]["repayment"]
    terminal_value = terminal_cash_flow * (1.0 + terminal_growth) / (
        cost_of_equity - terminal_growth
    )
    present_value_terminal = terminal_value / (1.0 + cost_of_equity) ** 5
    equity_value = present_value_fcfe + present_value_terminal
    value_after_2030 = present_value_terminal / equity_value
    value_per_share = equity_value / shares_outstanding
    return equity_value, value_after_2030, value_per_share


projections = build_proforma()

print_statement(
    "INCOME STATEMENT",
    projections,
    [
        ("Revenue", "revenue"),
        ("Gross profit", "gross_profit"),
        ("SG&A", "sga"),
        ("Depreciation", "depreciation"),
        ("Impairment", "impairment"),
        ("Operating income", "operating_income"),
        ("Interest", "interest"),
        ("Pretax income", "pretax_income"),
        ("Tax", "tax"),
        ("Net income", "net_income"),
    ],
)

print_statement(
    "BALANCE SHEET",
    projections,
    [
        ("Cash", "cash"),
        ("Inventory", "inventory"),
        ("PP&E", "ppe"),
        ("Other assets", "other_assets"),
        ("Total assets", "total_assets"),
        ("Floor plan", "floor_plan"),
        ("Debt", "debt"),
        ("Revolver", "revolver"),
        ("Other liabilities", "other_liabilities"),
        ("Total liabilities", "total_liabilities"),
        ("Equity", "equity"),
    ],
)

print_statement(
    "CASH FLOW",
    projections,
    [
        ("FCFE before buyback", "fcfe"),
        ("Share buyback", "buyback"),
        ("Change in revolver", "revolver_change"),
        ("Ending cash", "cash"),
    ],
)

print("\nCHECKS")
for row in projections:
    print(
        f"{row['year']}: assets - liabilities - equity = "
        f"{row['balance_gap']:.1f}; cash >= minimum = {row['cash_minimum_met']}"
    )

assert_balanced(projections)
equity_value, value_after_2030, value_per_share = value_equity(projections)

print("\nVALUATION")
print(f"Equity value: ${equity_value:,.2f} million")
print(f"Share of value after 2030: {value_after_2030:.2%}")
print(f"Value per share: ${value_per_share:,.2f}")
