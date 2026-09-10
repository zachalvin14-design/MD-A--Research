"""Costco Wholesale DCF and reverse DCF.

Used for educational purposes, not financial advice.
All dollar amounts are USD millions except per-share values and the share price.
"""

# ============================== INPUTS ======================================
# Edit the values in this block, then run: python dcf.py

# Costco FY2025 10-K facts (52 weeks ended / balance sheet at August 31, 2025)
operating_cash_flow = 13_335.0
cash_interest_paid = 106.0
effective_tax_rate = 0.251
capital_expenditures = 5_498.0
cash = 14_161.0
short_term_investments = 1_123.0
debt = 5_788.0
diluted_shares = 444.803

# Forecasts / estimates (not reported by Costco)
growth_rates = [0.08, 0.07, 0.06, 0.05, 0.04]
wacc = 0.10  # Placeholder: unresolved company-specific WACC; training value retained
terminal_growth = 0.03

# Editable sensitivity lists
wacc_values = [0.09, 0.10, 0.11]
terminal_growth_values = [0.02, 0.03, 0.04]

# Editable reverse-DCF inputs
target_share_price = 902.60
target_share_price_as_of = "September 9, 2026 market close (latest completed session)"
reverse_lower_bound = -0.05
reverse_upper_bound = 0.10
# ===========================================================================


def value_dcf(starting_fcff, annual_growth_rates, discount_rate, perpetual_growth):
    """Return the main DCF values; all cash flows occur at each year-end."""
    if perpetual_growth >= discount_rate:
        raise ValueError("Terminal growth must be below WACC.")

    projected_fcff = []
    fcff = starting_fcff
    for growth_rate in annual_growth_rates:
        if growth_rate <= -1.0:
            raise ValueError("An annual growth rate cannot be -100% or below.")
        fcff *= 1.0 + growth_rate
        projected_fcff.append(fcff)

    pv_explicit = sum(
        cash_flow / (1.0 + discount_rate) ** year
        for year, cash_flow in enumerate(projected_fcff, start=1)
    )
    terminal_value = (
        projected_fcff[-1]
        * (1.0 + perpetual_growth)
        / (discount_rate - perpetual_growth)
    )
    pv_terminal = terminal_value / (1.0 + discount_rate) ** len(projected_fcff)
    enterprise_value = pv_explicit + pv_terminal
    equity_value = enterprise_value + cash + short_term_investments - debt
    value_per_share = equity_value / diluted_shares

    return {
        "projected_fcff": projected_fcff,
        "pv_explicit": pv_explicit,
        "terminal_value": terminal_value,
        "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "value_per_share": value_per_share,
    }


def shifted_value_per_share(starting_fcff, shift):
    shifted_growth_rates = [rate + shift for rate in growth_rates]
    return value_dcf(starting_fcff, shifted_growth_rates, wacc, terminal_growth)[
        "value_per_share"
    ]


def solve_reverse_dcf(starting_fcff, target, lower, upper, tolerance=0.000001):
    """Solve for a uniform explicit-growth shift using a valid bisection bracket."""
    if lower >= upper:
        return None, "lower bound must be less than upper bound"

    for bound_name, bound in (("lower", lower), ("upper", upper)):
        if any(rate + bound <= -1.0 for rate in growth_rates):
            return None, (
                f"{bound_name} bound is refused because it pushes an annual "
                "growth rate to -100% or below"
            )

    lower_difference = shifted_value_per_share(starting_fcff, lower) - target
    upper_difference = shifted_value_per_share(starting_fcff, upper) - target

    if abs(lower_difference) <= tolerance:
        return lower, None
    if abs(upper_difference) <= tolerance:
        return upper, None
    if lower_difference * upper_difference > 0.0:
        return None, "target price cannot be reached inside this bracket"

    left, right = lower, upper
    left_difference = lower_difference
    for _ in range(200):
        midpoint = (left + right) / 2.0
        midpoint_difference = shifted_value_per_share(starting_fcff, midpoint) - target

        if abs(midpoint_difference) <= tolerance or (right - left) <= 1e-12:
            return midpoint, None
        if left_difference * midpoint_difference <= 0.0:
            right = midpoint
        else:
            left = midpoint
            left_difference = midpoint_difference

    return None, "bisection did not converge"


starting_fcff = (
    operating_cash_flow
    + cash_interest_paid * (1.0 - effective_tax_rate)
    - capital_expenditures
)
base = value_dcf(starting_fcff, growth_rates, wacc, terminal_growth)

# Twelve-line base-case output block. Keep these twelve print statements intact.
print("COSTCO WHOLESALE DCF — BASE CASE")
print(f"1. Starting FCFF: ${starting_fcff:,.3f} million")
print("2. Growth, Years 1-5: " + ", ".join(f"{rate:.1%}" for rate in growth_rates))
print("3. Projected FCFF: " + ", ".join(f"${value:,.3f}" for value in base["projected_fcff"]) + " million")
print(f"4. WACC: {wacc:.1%}")
print(f"5. Terminal growth: {terminal_growth:.1%}")
print(f"6. PV of explicit FCFF: ${base['pv_explicit']:,.3f} million")
print(f"7. Terminal value: ${base['terminal_value']:,.3f} million")
print(f"8. PV of terminal value: ${base['pv_terminal']:,.3f} million")
print(f"9. Enterprise value: ${base['enterprise_value']:,.3f} million")
print(f"10. Equity bridge: +${cash:,.3f} cash +${short_term_investments:,.3f} short-term investments -${debt:,.3f} debt (millions)")
print(f"11. Equity value: ${base['equity_value']:,.3f} million")
print(f"12. Value per diluted share: ${base['value_per_share']:,.2f}")

print("\nSENSITIVITY — VALUE PER DILUTED SHARE ($)")
first_column_width = 18
cell_width = 12
header = "WACC \\ terminal".ljust(first_column_width)
header += "".join(f"{rate:.1%}".rjust(cell_width) for rate in terminal_growth_values)
print(header)
print("-" * len(header))
for sensitivity_wacc in wacc_values:
    row = f"{sensitivity_wacc:.1%}".ljust(first_column_width)
    for sensitivity_terminal_growth in terminal_growth_values:
        if sensitivity_terminal_growth >= sensitivity_wacc:
            cell = "INVALID"
        else:
            cell = f"${value_dcf(starting_fcff, growth_rates, sensitivity_wacc, sensitivity_terminal_growth)['value_per_share']:,.2f}"
        row += cell.rjust(cell_width)
    print(row)

print("\nREVERSE DCF — UNIFORM SHIFT TO ALL FIVE EXPLICIT GROWTH RATES")
solved_shift, reverse_error = solve_reverse_dcf(
    starting_fcff,
    target_share_price,
    reverse_lower_bound,
    reverse_upper_bound,
)
print(f"Target share price: ${target_share_price:,.2f}")
print(f"Target price as of: {target_share_price_as_of}")
print(f"Search bracket: {reverse_lower_bound:+.2%} to {reverse_upper_bound:+.2%}")
if solved_shift is None:
    print(f"Solved shift: NO SOLUTION ({reverse_error})")
else:
    print(f"Solved shift: {solved_shift:+.4%} ({solved_shift * 100:+.4f} percentage points)")
    print(f"Value per share at solved shift: ${shifted_value_per_share(starting_fcff, solved_shift):,.2f}")
print(
    "Held fixed: starting FCFF; WACC; terminal growth; cash; short-term "
    "investments; debt; diluted shares; and the five-year forecast structure."
)
print(
    "Interpretation: this is one set of assumptions consistent with the target "
    "price, not proof of mispricing."
)

print("\nCONDITIONAL CALL — AND THE FLOOR")
price_to_value = target_share_price / base["value_per_share"]
lower_comparison_bound = 0.5 * base["value_per_share"]
upper_comparison_bound = 2.0 * base["value_per_share"]
print(
    f"Company value per share: ${base['value_per_share']:,.2f} | "
    f"Recorded market price: ${target_share_price:,.2f} "
    f"({target_share_price_as_of})"
)
print(f"Price / modeled value: {price_to_value:.2f}x")
if lower_comparison_bound <= target_share_price <= upper_comparison_bound:
    print(
        "Range check: inside 0.5x to 2.0x modeled value "
        f"(${lower_comparison_bound:,.2f} to ${upper_comparison_bound:,.2f})."
    )
else:
    print(
        "Range check: outside 0.5x to 2.0x modeled value "
        f"(${lower_comparison_bound:,.2f} to ${upper_comparison_bound:,.2f}); "
        "no input was adjusted."
    )
    print(
        "Input distrusted most: WACC, because 10.0% is an unresolved training "
        "placeholder rather than a sourced, company-specific cost-of-capital estimate."
    )
if solved_shift is None:
    print(
        "Growth the price assumes: not solved inside the allowed -5.00% to "
        "+10.00% bracket; the target requires a shift above +10.00 percentage "
        "points under the held-fixed inputs."
    )
else:
    print(
        f"Growth the price assumes: {solved_shift * 100:+.4f} percentage points "
        "added uniformly to each explicit annual growth rate."
    )
print(
    f"Watch-defer. Initiate if the recorded market price falls to or below "
    f"the ${base['value_per_share']:,.2f} base-case value, or if sourced evidence "
    "supports assumptions that raise modeled value to the market price; otherwise, "
    "continue watching."
)
print("Monitor: Costco's operating margin in its next quarterly filing.")
print(
    "Floor present: sourced inputs; company value; sensitivity grid; growth "
    "implied by price (or an explicit no-solution bracket); and conditional call."
)
print("Used for educational purposes, not financial advice.")

# Sources / exact locators:
# SEC Form 10-K, FY ended August 31, 2025, filed October 8, 2025:
# https://www.sec.gov/Archives/edgar/data/909832/000090983225000101/cost-20250831.htm
# - Consolidated Statements of Cash Flows: CFO $13,335m; capex $5,498m;
#   cash interest paid $106m; cash and equivalents $14,161m.
# - Item 7, Provision for Income Taxes: FY2025 effective tax rate 25.1%.
# - Consolidated Balance Sheets / Notes 2 and 4: short-term investments
#   $1,123m and debt at net carrying value $5,788m ($75m current + $5,713m long term).
# - Note 9, Net Income per Common and Common Equivalent Share: FY2025 weighted-
#   average diluted shares 444.803m (443.985m basic + 0.818m RSUs).
# Target price placeholder: $902.60 closing price on September 9, 2026, shown by
# StockAnalysis historical data (S&P Global Market Intelligence); update at top.
