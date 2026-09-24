"""Run the Deere five-year model built from the ABG pro-forma assignment.

The ABG floor-plan block is replaced by Deere's equipment operations and
Financial Services blocks. All amounts are USD millions.
"""


history = {
    2023: {"revenue": 61_251.0, "gross_profit": 17_850.0, "sga": 4_595.0,
           "net_income": 10_166.0, "inventory": 8_160.0, "ppe": 6_879.0,
           "equity": 21_785.0},
    2024: {"revenue": 51_716.0, "gross_profit": 13_984.0, "sga": 4_840.0,
           "net_income": 7_100.0, "inventory": 7_093.0, "ppe": 7_580.0,
           "equity": 22_836.0},
    2025: {"revenue": 45_684.0, "gross_profit": 10_758.0, "sga": 4_663.0,
           "net_income": 5_027.0, "inventory": 7_406.0, "ppe": 8_079.0,
           "equity": 25_950.0},
}

opening_balance_sheet = {
    "cash_and_marketables": 9_687.0,
    "trade_receivables": 5_317.0,
    "financing_receivables": 51_406.0,
    "equipment_on_operating_leases": 7_600.0,
    "inventory": 7_406.0,
    "ppe": 8_079.0,
    "other_assets": 16_501.0,
    "total_assets": 105_996.0,
    "short_term_borrowings": 13_796.0,
    "securitization_borrowings": 6_596.0,
    "long_term_borrowings": 43_544.0,
    "other_liabilities": 16_060.0,
    "stockholders_equity": 25_950.0,
    "noncontrolling_interest": 50.0,
    "total_liabilities_and_equity": 105_996.0,
}


def print_history():
    print("DEERE HISTORICAL INPUT TABLE")
    print("USD millions".ljust(25) + "".join(f"{year:>13}" for year in history))
    print("-" * 64)
    for label, key in [
        ("Revenue", "revenue"),
        ("Equipment gross profit", "gross_profit"),
        ("SG&A", "sga"),
        ("Net income", "net_income"),
        ("Inventory", "inventory"),
        ("Net PP&E", "ppe"),
        ("Stockholders' equity", "equity"),
    ]:
        print(label.ljust(25) + "".join(f"{history[y][key]:13,.1f}" for y in history))


def print_opening_balance_sheet():
    print("\nOPENING BALANCE SHEET — FY2025")
    print("USD millions")
    for label, key in [
        ("Cash + marketable securities", "cash_and_marketables"),
        ("Trade receivables", "trade_receivables"),
        ("Financing receivables", "financing_receivables"),
        ("Equipment on operating leases", "equipment_on_operating_leases"),
        ("Inventory", "inventory"),
        ("Net PP&E", "ppe"),
        ("Other assets", "other_assets"),
        ("Total assets", "total_assets"),
        ("Short-term borrowings", "short_term_borrowings"),
        ("Securitization borrowings", "securitization_borrowings"),
        ("Long-term borrowings", "long_term_borrowings"),
        ("Other liabilities", "other_liabilities"),
        ("Stockholders' equity", "stockholders_equity"),
        ("Noncontrolling interest", "noncontrolling_interest"),
        ("Liabilities + equity", "total_liabilities_and_equity"),
    ]:
        print(f"{label:<38}{opening_balance_sheet[key]:>13,.1f}")

    gap = (
        opening_balance_sheet["total_assets"]
        - opening_balance_sheet["total_liabilities_and_equity"]
    )
    if abs(gap) > 0.01:
        raise ValueError(f"2025: opening balance sheet gap is {gap:.6f}")
    print(f"Opening balance check: {gap:.1f}")


print_history()
print_opening_balance_sheet()

# Importing executes the full five-year forecast, hard balance checks, FCFE
# checks, sum-of-parts valuation, and sensitivity table.
import de_proforma  # noqa: E402,F401

market_price = 697.33
quote_date = "September 24, 2026 at 2:30 p.m. EDT"
model_price = de_proforma.valuation["per_share"]
shares = de_proforma.diluted_shares

print("\nMODEL VERSUS MARKET — SAME DILUTED SHARE COUNT")
print(f"Quote date: {quote_date}; shares: {shares:.1f} million")
print(f"{'':<15}{'Per share':>15}{'Equity value':>20}")
print(f"{'Model':<15}${model_price:>14,.2f}${model_price * shares:>19,.1f}M")
print(f"{'Market':<15}${market_price:>14,.2f}${market_price * shares:>19,.1f}M")
print(f"{'Difference':<15}${market_price - model_price:>14,.2f}${(market_price - model_price) * shares:>19,.1f}M")
print(
    "The $326.45 estimate reflects a 9.0% WACC, 2.5% terminal growth, a gradual "
    "equipment-margin recovery that does not regain the 2023 peak, and Financial "
    "Services valued at 1.4 times FY2025 book value, while the $697.33 market price "
    "embeds materially stronger or less risky future cash flows."
)
print(
    "The value would rise with faster sales recovery, sustained higher margins, a "
    "lower required return, higher terminal growth, or a richer Financial Services "
    "multiple, and it would fall if the agricultural cycle, tariffs, incentives, "
    "credit losses, or financing costs weaken those assumptions."
)
