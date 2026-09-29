"""Costco Wholesale (COST): five-year forecast and enterprise DCF.

Amounts are USD millions except per-share values.  FY2025 is the audited anchor.
FY2026 net sales are reported; the remaining FY2026 statement values are estimates.
Educational use only; this is not investment advice.
"""


# ---------------------------- MODEL ASSUMPTIONS ----------------------------
years = [2026, 2027, 2028, 2029, 2030]

# FY2026 net sales were reported in Costco's September 2, 2026 sales release.
net_sales = [297_300.0]
sales_growth = [0.075, 0.070, 0.065, 0.060]  # FY2027-FY2030

# Membership growth normalizes after the 2024 fee increase rolls through.
membership_growth = [0.110, 0.075, 0.070, 0.065, 0.060]

# Merchandise margin remains narrow; modest scale benefits are mostly reinvested.
gross_margin = [0.1115, 0.1117, 0.1119, 0.1120, 0.1120]
sga_percent_sales = [0.0923, 0.0921, 0.0919, 0.0918, 0.0918]
tax_rate = 0.252

# Cash-flow and balance-sheet drivers, normalized from Costco's recent history.
depreciation_percent_sales = 0.0090
capex_percent_sales = [0.0210, 0.0205, 0.0200, 0.0195, 0.0190]
operating_nwc_percent_sales = -0.0520  # supplier financing makes NWC negative
stock_comp_percent_sales = 0.0031
dividend_payout = 0.28
annual_buybacks = 1_000.0

# DCF assumptions.  WACC is intentionally above a low-beta CAPM point estimate.
wacc = 0.085
terminal_growth = 0.030
net_cash_2025 = 14_161.0 + 1_123.0 - 5_788.0
diluted_shares = 444.803

# Audited FY2025 anchors from Costco's 2025 Form 10-K.
opening = {
    "net_sales": 269_912.0,
    "membership_fees": 5_323.0,
    "cash_and_investments": 15_284.0,
    "other_current_assets": 23_096.0,
    "ppe": 31_909.0,
    "other_long_term_assets": 6_810.0,
    "operating_liabilities": 42_147.0,
    "debt": 5_788.0,
    "equity": 29_164.0,
    "operating_nwc": -14_012.0,
}
# ---------------------------------------------------------------------------


def build_forecast():
    for growth in sales_growth:
        net_sales.append(net_sales[-1] * (1.0 + growth))

    rows = []
    prior = opening.copy()
    for i, year in enumerate(years):
        sales = net_sales[i]
        fees = prior["membership_fees"] * (1.0 + membership_growth[i])
        merchandise_costs = sales * (1.0 - gross_margin[i])
        gross_profit = sales - merchandise_costs
        sga = sales * sga_percent_sales[i]
        ebit = gross_profit + fees - sga
        nopat = ebit * (1.0 - tax_rate)

        depreciation = sales * depreciation_percent_sales
        capex = sales * capex_percent_sales[i]
        operating_nwc = sales * operating_nwc_percent_sales
        change_nwc = operating_nwc - prior["operating_nwc"]
        fcff = nopat + depreciation - capex - change_nwc

        # Net interest income is modest and excluded from FCFF; it is included
        # below only to complete the estimated income statement.
        net_interest_income = 0.0014 * sales
        pretax_income = ebit + net_interest_income
        taxes = pretax_income * tax_rate
        net_income = pretax_income - taxes

        dividends = net_income * dividend_payout
        stock_comp = sales * stock_comp_percent_sales
        equity = prior["equity"] + net_income + stock_comp - dividends - annual_buybacks

        other_current_assets = sales * (opening["other_current_assets"] / opening["net_sales"])
        ppe = prior["ppe"] + capex - depreciation
        other_long_term_assets = sales * (
            opening["other_long_term_assets"] / opening["net_sales"]
        )
        operating_liabilities = sales * (
            opening["operating_liabilities"] / opening["net_sales"]
        )
        debt = opening["debt"]

        # Cash and investments are the balance-sheet plug.  This is preferable
        # to inventing a debt repayment or special dividend policy.
        cash_and_investments = (
            operating_liabilities + debt + equity
            - other_current_assets - ppe - other_long_term_assets
        )
        total_assets = (
            cash_and_investments + other_current_assets + ppe + other_long_term_assets
        )
        total_liabilities_equity = operating_liabilities + debt + equity

        rows.append(
            {
                "year": year,
                "sales": sales,
                "fees": fees,
                "gross_profit": gross_profit,
                "sga": sga,
                "ebit": ebit,
                "nopat": nopat,
                "net_interest": net_interest_income,
                "pretax": pretax_income,
                "taxes": taxes,
                "net_income": net_income,
                "depreciation": depreciation,
                "capex": capex,
                "change_nwc": change_nwc,
                "fcff": fcff,
                "dividends": dividends,
                "buybacks": annual_buybacks,
                "cash_investments": cash_and_investments,
                "other_current_assets": other_current_assets,
                "ppe": ppe,
                "other_long_term_assets": other_long_term_assets,
                "total_assets": total_assets,
                "operating_liabilities": operating_liabilities,
                "debt": debt,
                "equity": equity,
                "total_liabilities_equity": total_liabilities_equity,
                "balance_check": total_assets - total_liabilities_equity,
                "operating_nwc": operating_nwc,
                "membership_fees": fees,
            }
        )
        prior = rows[-1]
    return rows


def value_business(rows, discount_rate=wacc, growth=terminal_growth):
    if growth >= discount_rate:
        raise ValueError("Terminal growth must be below WACC.")
    pv_forecast = sum(
        row["fcff"] / (1.0 + discount_rate) ** period
        for period, row in enumerate(rows, start=1)
    )
    terminal_value = rows[-1]["fcff"] * (1.0 + growth) / (discount_rate - growth)
    pv_terminal = terminal_value / (1.0 + discount_rate) ** len(rows)
    enterprise_value = pv_forecast + pv_terminal
    equity_value = enterprise_value + net_cash_2025
    return {
        "pv_forecast": pv_forecast,
        "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "per_share": equity_value / diluted_shares,
        "terminal_share": pv_terminal / enterprise_value,
    }


def print_table(title, rows, items):
    print(f"\n{title}")
    print("USD millions".ljust(28) + "".join(str(row["year"]).rjust(13) for row in rows))
    print("-" * (28 + 13 * len(rows)))
    for label, key in items:
        print(label.ljust(28) + "".join(f"{row[key]:13,.1f}" for row in rows))


forecast = build_forecast()
valuation = value_business(forecast)

for row in forecast:
    assert abs(row["balance_check"]) < 0.001
    assert row["cash_investments"] > 0
assert terminal_growth < wacc

print("COSTCO WHOLESALE (COST) — FIVE-YEAR STATEMENTS AND VALUE")
print("FY2026E-FY2030E; USD millions except per-share data")

print_table(
    "FORECAST INCOME STATEMENT",
    forecast,
    [
        ("Net sales", "sales"),
        ("Membership fees", "fees"),
        ("Merchandise gross profit", "gross_profit"),
        ("SG&A", "sga"),
        ("Operating income", "ebit"),
        ("Net interest income", "net_interest"),
        ("Pretax income", "pretax"),
        ("Income taxes", "taxes"),
        ("Net income", "net_income"),
    ],
)

print_table(
    "FORECAST CASH FLOW / FCFF",
    forecast,
    [
        ("NOPAT", "nopat"),
        ("Depreciation", "depreciation"),
        ("Capital spending", "capex"),
        ("Change in operating NWC", "change_nwc"),
        ("Free cash flow to firm", "fcff"),
        ("Common dividends", "dividends"),
        ("Share repurchases", "buybacks"),
    ],
)

print_table(
    "FORECAST BALANCE SHEET",
    forecast,
    [
        ("Cash + investments", "cash_investments"),
        ("Other current assets", "other_current_assets"),
        ("Property & equipment", "ppe"),
        ("Other long-term assets", "other_long_term_assets"),
        ("Total assets", "total_assets"),
        ("Operating liabilities", "operating_liabilities"),
        ("Debt", "debt"),
        ("Equity", "equity"),
        ("Liabilities + equity", "total_liabilities_equity"),
        ("Balance check", "balance_check"),
    ],
)

print("\nBASE-CASE DCF")
print(f"WACC: {wacc:.1%}; terminal growth: {terminal_growth:.1%}")
print(f"PV of five-year FCFF: ${valuation['pv_forecast']:,.1f} million")
print(f"PV of terminal value: ${valuation['pv_terminal']:,.1f} million")
print(f"Enterprise value: ${valuation['enterprise_value']:,.1f} million")
print(f"Equity value: ${valuation['equity_value']:,.1f} million")
print(f"Estimated value per share: ${valuation['per_share']:,.2f}")
print(f"Terminal-value share: {valuation['terminal_share']:.1%}")

print("\nVALUE-PER-SHARE SENSITIVITY")
growth_rates = [0.025, 0.030, 0.035]
print("WACC / terminal growth".ljust(27) + "".join(f"{g:.1%}".rjust(12) for g in growth_rates))
for discount_rate in [0.075, 0.085, 0.095]:
    line = f"{discount_rate:.1%}".ljust(27)
    for growth in growth_rates:
        line += f"${value_business(forecast, discount_rate, growth)['per_share']:,.2f}".rjust(12)
    print(line)

print("\nKEY ASSUMPTIONS")
print("FY2026 net sales: reported $297.3B; all other FY2026 figures are estimates.")
print("Sales growth fades from 7.5% in FY2027 to 6.0% in FY2030.")
print("Merchandise gross margin holds near 11.2%; SG&A improves to 9.18% of sales.")
print("Capex declines from 2.10% to 1.90% of sales as expansion normalizes.")
print("Used for educational purposes; forecast accuracy depends on these assumptions.")
