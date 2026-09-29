"""Deere & Company (DE): five-year forecast and sum-of-parts valuation.

Amounts are USD millions except per-share values. FY2025 is the audited anchor.
FY2026 is estimated from Deere's August 2026 outlook and first nine months.
Educational use only; this is not investment advice.
"""


years = [2026, 2027, 2028, 2029, 2030]

history = {
    2023: [61_251.0, 17_850.0, 4_595.0, 10_166.0, 8_160.0, 6_879.0, 21_785.0],
    2024: [51_716.0, 13_984.0, 4_840.0, 7_100.0, 7_093.0, 7_580.0, 22_836.0],
    2025: [45_684.0, 10_758.0, 4_663.0, 5_027.0, 7_406.0, 8_079.0, 25_950.0],
}

reported_opening = {
    "Cash + marketable securities": 9_687.0,
    "Trade receivables": 5_317.0,
    "Financing receivables": 51_406.0,
    "Equipment on operating leases": 7_600.0,
    "Inventory": 7_406.0,
    "Net PP&E": 8_079.0,
    "Other assets": 16_501.0,
    "Total assets": 105_996.0,
    "Short-term borrowings": 13_796.0,
    "Securitization borrowings": 6_596.0,
    "Long-term borrowings": 43_544.0,
    "Other liabilities": 16_060.0,
    "Stockholders' equity": 25_950.0,
    "Noncontrolling interest": 50.0,
    "Liabilities + equity": 105_996.0,
}

# Deere's FY2026 segment outlook: PPA -10%, SAT +15%, and CF +20%.
# Later years assume a measured recovery from the agricultural-equipment trough.
segment_sales_2025 = {"ppa": 17_311.0, "sat": 10_224.0, "cf": 11_382.0}
segment_growth = {
    "ppa": [-0.10, 0.12, 0.09, 0.06, 0.04],
    "sat": [0.15, 0.06, 0.05, 0.04, 0.035],
    "cf": [0.20, 0.05, 0.04, 0.04, 0.035],
}
segment_margin = {
    "ppa": [0.115, 0.140, 0.160, 0.172, 0.180],
    "sat": [0.165, 0.160, 0.155, 0.152, 0.150],
    "cf": [0.110, 0.120, 0.130, 0.137, 0.140],
}

# Consolidated statement assumptions.
finance_income = [5_400.0, 5_550.0, 5_750.0, 5_950.0, 6_150.0]
other_income_percent_sales = 0.025
equipment_da_percent_sales = 0.031
capex_percent_sales = [0.034, 0.033, 0.032, 0.031, 0.030]
equipment_nwc_percent_sales = 0.105
tax_rate = 0.235
fs_net_income = [870.0, 900.0, 930.0, 960.0, 990.0]
corporate_and_net_interest = [-150.0, -170.0, -190.0, -210.0, -230.0]
annual_dividend_per_share = [6.48, 6.65, 6.85, 7.05, 7.25]
annual_buybacks = [900.0, 1_000.0, 1_100.0, 1_200.0, 1_300.0]

# Sum-of-parts valuation. Financial Services is valued separately because its
# borrowings fund earning receivables and should not all be treated as net debt.
wacc = 0.090
terminal_growth = 0.025
equipment_net_debt = 414.0 + 8_756.0 - 6_340.0 - 217.0
fs_book_equity = 7_069.0
fs_price_to_book = 1.40
diluted_shares = 270.8
minimum_cash = 5_000.0
market_price = 697.33
market_quote_date = "September 24, 2026 at 2:30 p.m. EDT"

assumption_reasons = [
    ("FY2026 segment growth", "PPA -10%, SAT +15%, and CF +20% follow Deere's August 2026 guidance."),
    ("FY2027-FY2030 growth", "A measured recovery follows management's description of FY2026 as the cycle bottom, then fades toward mature-industry growth."),
    ("Segment margins", "Margins recover with volume but PPA reaches only 18.0%, below its 21.7% FY2024 level, avoiding a peak-cycle assumption."),
    ("Finance income", "Growth from $5.4B to $6.15B assumes modest portfolio and yield normalization rather than a return to unusually rapid credit growth."),
    ("Other income at 2.5% of sales", "This approximates FY2025 other income relative to equipment sales and holds the noncore contribution stable."),
    ("D&A at 3.1% of sales", "The rate is close to Deere's recent equipment-operations depreciation burden."),
    ("Capital spending", "Capex begins near management's $1.4B FY2026 plan and declines from 3.4% to 3.0% of sales as the cycle normalizes."),
    ("Operating NWC at 10.5% of sales", "The ratio normalizes inventory and operating working capital near recent reported levels."),
    ("Tax rate at 23.5%", "The rate is near Deere's normalized three-year effective rate and above the unusually low FY2025 reported rate."),
    ("Financial Services earnings", "FY2026 uses management's approximately $870M outlook, followed by modest growth with the finance portfolio."),
    ("Corporate and net interest", "The increasing expense recognizes higher operating scale without applying Financial Services funding interest twice."),
    ("Dividends", "Per-share dividends rise slowly from the current annualized level, preserving Deere's established payout while retaining cycle liquidity."),
    ("Share repurchases", "Buybacks rebuild gradually from $0.9B as earnings recover instead of assuming the exceptional FY2023 pace."),
    ("Borrowings growth at 1.5%", "Most consolidated debt funds Financial Services assets, so it grows modestly with that portfolio."),
    ("Equipment WACC at 9.0%", "The rate reflects Deere's cyclicality and operating risk despite its strong market position."),
    ("Terminal growth at 2.5%", "The rate is consistent with mature nominal economic growth and remains below WACC."),
    ("Financial Services at 1.4x book", "A roughly 12% expected ROE supports a moderate premium to book at a 9%-10% required return."),
    ("$5.0B cash floor", "The floor preserves liquidity through an agricultural downturn and remains below FY2025 equipment cash and securities."),
    ("270.8M diluted shares", "The count matches Deere's FY2026 nine-month diluted weighted-average shares."),
]

# Audited FY2025 balance-sheet and cash-flow anchors.
opening = {
    "sales": 38_917.0,
    "equipment_nwc": 38_917.0 * equipment_nwc_percent_sales,
    "ppe": 8_079.0,
    "cash_securities": 9_687.0,
    "finance_assets": 59_006.0,  # financing receivables plus leased equipment
    "other_assets": 29_224.0,
    "borrowings": 63_936.0,
    "other_liabilities": 16_053.0,
    "equity": 25_956.0,
}


def build_forecast():
    segment_sales = segment_sales_2025.copy()
    prior = opening.copy()
    rows = []

    for i, year in enumerate(years):
        for segment in segment_sales:
            segment_sales[segment] *= 1.0 + segment_growth[segment][i]

        sales = sum(segment_sales.values())
        segment_profit = sum(
            segment_sales[segment] * segment_margin[segment][i]
            for segment in segment_sales
        )
        equipment_pretax = segment_profit + corporate_and_net_interest[i]
        equipment_net_income = equipment_pretax * (1.0 - tax_rate)
        net_income = equipment_net_income + fs_net_income[i]

        # The consolidated income statement is simplified but reconciles to the
        # bottom-up segment earnings forecast.
        other_income = sales * other_income_percent_sales
        total_revenue = sales + finance_income[i] + other_income
        pretax = equipment_pretax + fs_net_income[i] / (1.0 - tax_rate)
        taxes = pretax - net_income
        total_costs = total_revenue - pretax

        depreciation = sales * equipment_da_percent_sales
        capex = sales * capex_percent_sales[i]
        equipment_nwc = sales * equipment_nwc_percent_sales
        change_nwc = equipment_nwc - prior["equipment_nwc"]
        equipment_nopat = segment_profit * (1.0 - tax_rate)
        equipment_fcff = equipment_nopat + depreciation - capex - change_nwc

        dividends = annual_dividend_per_share[i] * diluted_shares
        equity = prior["equity"] + net_income - dividends - annual_buybacks[i]

        finance_assets = prior["finance_assets"] * 1.02
        ppe = prior["ppe"] + capex - depreciation
        other_assets = sales * (opening["other_assets"] / opening["sales"])
        borrowings = prior["borrowings"] * 1.015
        net_borrowing = borrowings - prior["borrowings"]
        other_liabilities = sales * (opening["other_liabilities"] / opening["sales"])
        cash_securities = borrowings + other_liabilities + equity - finance_assets - ppe - other_assets
        total_assets = cash_securities + finance_assets + ppe + other_assets
        total_liabilities_equity = borrowings + other_liabilities + equity

        # Simplified consolidated FCFE. Deere Financial makes consolidated cash
        # flow harder to interpret, so the sum-of-parts FCFF remains the primary
        # valuation. This line makes loss cases visible instead of hiding them.
        fcfe = net_income + depreciation - capex - change_nwc + net_borrowing

        row = {
            "year": year,
            "ppa_sales": segment_sales["ppa"],
            "sat_sales": segment_sales["sat"],
            "cf_sales": segment_sales["cf"],
            "sales": sales,
            "finance_income": finance_income[i],
            "other_income": other_income,
            "total_revenue": total_revenue,
            "total_costs": total_costs,
            "pretax": pretax,
            "taxes": taxes,
            "net_income": net_income,
            "segment_profit": segment_profit,
            "depreciation": depreciation,
            "capex": capex,
            "change_nwc": change_nwc,
            "equipment_fcff": equipment_fcff,
            "net_borrowing": net_borrowing,
            "fcfe": fcfe,
            "dividends": dividends,
            "buybacks": annual_buybacks[i],
            "cash_securities": cash_securities,
            "finance_assets": finance_assets,
            "ppe": ppe,
            "other_assets": other_assets,
            "total_assets": total_assets,
            "borrowings": borrowings,
            "other_liabilities": other_liabilities,
            "equity": equity,
            "total_liabilities_equity": total_liabilities_equity,
            "balance_check": total_assets - total_liabilities_equity,
            "cash_floor_met": cash_securities >= minimum_cash,
            "revolver_draw": 0.0,
            "equipment_nwc": equipment_nwc,
        }
        rows.append(row)
        prior = row
    return rows


def value_business(rows, discount_rate=wacc, growth=terminal_growth, fs_multiple=fs_price_to_book):
    if growth >= discount_rate:
        raise ValueError("Terminal growth must be below WACC.")
    pv_forecast = sum(
        row["equipment_fcff"] / (1.0 + discount_rate) ** period
        for period, row in enumerate(rows, start=1)
    )
    terminal_value = rows[-1]["equipment_fcff"] * (1.0 + growth) / (discount_rate - growth)
    pv_terminal = terminal_value / (1.0 + discount_rate) ** len(rows)
    equipment_ev = pv_forecast + pv_terminal
    equipment_equity = equipment_ev - equipment_net_debt
    fs_value = fs_book_equity * fs_multiple
    equity_value = equipment_equity + fs_value
    return {
        "pv_forecast": pv_forecast,
        "pv_terminal": pv_terminal,
        "equipment_ev": equipment_ev,
        "equipment_equity": equipment_equity,
        "fs_value": fs_value,
        "equity_value": equity_value,
        "per_share": equity_value / diluted_shares,
        "terminal_share": pv_terminal / equipment_ev,
    }


def value_positive_fcfe_only(rows, discount_rate=wacc, growth=terminal_growth):
    """Diagnostic equity DCF that never capitalizes a negative cash flow."""
    pv_positive_fcfe = sum(
        max(row["fcfe"], 0.0) / (1.0 + discount_rate) ** period
        for period, row in enumerate(rows, start=1)
    )
    terminal_value = 0.0
    terminal_note = "Terminal value included because final-year FCFE is positive."
    if rows[-1]["fcfe"] > 0:
        terminal_value = rows[-1]["fcfe"] * (1.0 + growth) / (discount_rate - growth)
    else:
        terminal_note = (
            "No terminal value: capitalizing a negative cash flow does not produce "
            "a meaningful going-concern value."
        )
    pv_terminal = terminal_value / (1.0 + discount_rate) ** len(rows)
    return pv_positive_fcfe + pv_terminal, terminal_note


def print_table(title, rows, items):
    print(f"\n{title}")
    print("USD millions".ljust(29) + "".join(str(row["year"]).rjust(13) for row in rows))
    print("-" * (29 + 13 * len(rows)))
    for label, key in items:
        print(label.ljust(29) + "".join(f"{row[key]:13,.1f}" for row in rows))


def print_inputs():
    print("DEERE HISTORICAL INPUT TABLE")
    print("USD millions".ljust(29) + "".join(f"{year:>13}" for year in history))
    print("-" * 68)
    labels = ["Revenue", "Equipment gross profit", "SG&A", "Net income",
              "Inventory", "Net PP&E", "Stockholders' equity"]
    for index, label in enumerate(labels):
        print(label.ljust(29) + "".join(f"{history[y][index]:13,.1f}" for y in history))

    print("\nOPENING BALANCE SHEET — FY2025")
    for label, amount in reported_opening.items():
        print(f"{label:<38}{amount:>13,.1f}")
    opening_gap = reported_opening["Total assets"] - reported_opening["Liabilities + equity"]
    if abs(opening_gap) > 0.01:
        raise ValueError(f"2025: opening balance sheet gap is {opening_gap:.6f}")
    print(f"Opening balance check: {opening_gap:.1f}")

    print("\nLABELLED FORECAST AND VALUATION ASSUMPTIONS")
    for label, reason in assumption_reasons:
        print(f"- {label}: {reason}")


forecast = build_forecast()
valuation = value_business(forecast)
fcfe_diagnostic_value, fcfe_terminal_note = value_positive_fcfe_only(forecast)

for row in forecast:
    assert abs(row["balance_check"]) < 0.001
    assert row["cash_securities"] > 0
assert terminal_growth < wacc

print_inputs()
print()
print("DEERE & COMPANY (DE) — FIVE-YEAR STATEMENTS AND VALUE")
print("FY2026E-FY2030E; USD millions except per-share data")

print_table("FORECAST REVENUE BY BUSINESS", forecast, [
    ("Production & Precision Ag", "ppa_sales"),
    ("Small Ag & Turf", "sat_sales"),
    ("Construction & Forestry", "cf_sales"),
    ("Equipment net sales", "sales"),
    ("Finance and interest income", "finance_income"),
    ("Other income", "other_income"),
    ("Total net sales and revenues", "total_revenue"),
])

print_table("FORECAST INCOME STATEMENT", forecast, [
    ("Total net sales and revenues", "total_revenue"),
    ("Costs and expenses", "total_costs"),
    ("Pretax income", "pretax"),
    ("Income taxes", "taxes"),
    ("Net income", "net_income"),
])

print_table("FORECAST EQUIPMENT CASH FLOW", forecast, [
    ("Segment operating profit", "segment_profit"),
    ("Depreciation & amortization", "depreciation"),
    ("Capital expenditures", "capex"),
    ("Change in operating NWC", "change_nwc"),
    ("Equipment operations FCFF", "equipment_fcff"),
    ("Net borrowing", "net_borrowing"),
    ("Simplified consolidated FCFE", "fcfe"),
    ("Consolidated dividends", "dividends"),
    ("Share repurchases", "buybacks"),
])

print_table("FORECAST CONSOLIDATED BALANCE SHEET", forecast, [
    ("Cash + marketable securities", "cash_securities"),
    ("Finance assets + leases", "finance_assets"),
    ("Property & equipment", "ppe"),
    ("Other assets", "other_assets"),
    ("Total assets", "total_assets"),
    ("Borrowings", "borrowings"),
    ("Other liabilities", "other_liabilities"),
    ("Stockholders' equity", "equity"),
    ("Liabilities + equity", "total_liabilities_equity"),
    ("Balance check", "balance_check"),
])

print("\nCHECKS")
for row in forecast:
    if abs(row["balance_check"]) > 0.01:
        raise ValueError(
            f"{row['year']}: balance sheet gap is {row['balance_check']:.6f}"
        )
    if not row["cash_floor_met"]:
        gap = row["cash_securities"] - minimum_cash
        raise ValueError(f"{row['year']}: cash floor gap is {gap:.6f}")
    print(
        f"{row['year']}: balance gap = {row['balance_check']:.1f}; "
        f"cash ${row['cash_securities']:,.1f} >= ${minimum_cash:,.1f} floor = True"
    )

print("\nBASE-CASE SUM-OF-PARTS DCF")
print(f"Equipment WACC: {wacc:.1%}; terminal growth: {terminal_growth:.1%}")
print(f"PV of five-year equipment FCFF: ${valuation['pv_forecast']:,.1f} million")
print(f"PV of equipment terminal value: ${valuation['pv_terminal']:,.1f} million")
print(f"Equipment enterprise value: ${valuation['equipment_ev']:,.1f} million")
print(f"Less equipment net debt: ${equipment_net_debt:,.1f} million")
print(f"Financial Services value ({fs_price_to_book:.1f}x book): ${valuation['fs_value']:,.1f} million")
print(f"Equity value: ${valuation['equity_value']:,.1f} million")
print(f"Estimated value per share: ${valuation['per_share']:,.2f}")
print(f"Equipment terminal-value share: {valuation['terminal_share']:.1%}")

print("\nFCFE LOSS CHECK")
for row in forecast:
    status = "negative FCFE" if row["fcfe"] < 0 else "positive FCFE"
    print(f"{row['year']}: {status} (${row['fcfe']:,.1f} million)")
print(f"Positive-only FCFE diagnostic value: ${fcfe_diagnostic_value:,.1f} million")
print(fcfe_terminal_note)

print("\nKEY ASSUMPTIONS")
print("FY2026 net income uses Deere's $4.75B-$5.00B guidance midpoint (approximately).")
print("FY2026 segment sales use company guidance: PPA -10%, SAT +15%, and CF +20%.")
print("Large-ag margins recover gradually; FY2030 PPA margin remains below FY2024's 21.7%.")
print("Equipment operations use a 9.0% WACC and 2.5% perpetual growth rate.")
print("Financial Services is valued at 1.4x FY2025 book equity; its funding debt is not netted again.")
print("Used for educational purposes; value is highly sensitive to cycle and margin assumptions.")

print("\nMODEL VERSUS MARKET — SAME DILUTED SHARE COUNT")
print(f"Quote date: {market_quote_date}; shares: {diluted_shares:.1f} million")
print(f"{'':<15}{'Per share':>15}{'Equity value':>20}")
print(f"{'Model':<15}${valuation['per_share']:>14,.2f}${valuation['equity_value']:>19,.1f}M")
print(f"{'Market':<15}${market_price:>14,.2f}${market_price * diluted_shares:>19,.1f}M")
print(f"{'Difference':<15}${market_price - valuation['per_share']:>14,.2f}${market_price * diluted_shares - valuation['equity_value']:>19,.1f}M")
print("The $326.45 estimate reflects a 9.0% WACC, 2.5% terminal growth, a gradual equipment-margin recovery that does not regain the 2023 peak, and Financial Services valued at 1.4 times FY2025 book value, while the $697.33 market price embeds materially stronger or less risky future cash flows.")
print("The value would rise with faster sales recovery, sustained higher margins, a lower required return, higher terminal growth, or a richer Financial Services multiple, and it would fall if the agricultural cycle, tariffs, incentives, credit losses, or financing costs weaken those assumptions.")
