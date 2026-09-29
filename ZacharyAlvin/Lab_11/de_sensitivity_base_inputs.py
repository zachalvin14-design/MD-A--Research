"""Separate base-input snapshot for Deere one-at-a-time sensitivities.

Amounts are USD millions except per-share values, ratios, and percentages.
These values mirror the base inputs in de_proforma.py on 2026-09-29.
"""

YEARS = [2026, 2027, 2028, 2029, 2030]
SEGMENT_SALES_2025 = {"ppa": 17_311.0, "sat": 10_224.0, "cf": 11_382.0}
SEGMENT_GROWTH = {
    "ppa": [-0.10, 0.12, 0.09, 0.06, 0.04],
    "sat": [0.15, 0.06, 0.05, 0.04, 0.035],
    "cf": [0.20, 0.05, 0.04, 0.04, 0.035],
}
SEGMENT_MARGIN = {
    "ppa": [0.115, 0.140, 0.160, 0.172, 0.180],
    "sat": [0.165, 0.160, 0.155, 0.152, 0.150],
    "cf": [0.110, 0.120, 0.130, 0.137, 0.140],
}
FINANCE_INCOME = [5_400.0, 5_550.0, 5_750.0, 5_950.0, 6_150.0]
OTHER_INCOME_PERCENT_SALES = 0.025
EQUIPMENT_DA_PERCENT_SALES = 0.031
CAPEX_PERCENT_SALES = [0.034, 0.033, 0.032, 0.031, 0.030]
EQUIPMENT_NWC_PERCENT_SALES = 0.105
TAX_RATE = 0.235
FS_NET_INCOME = [870.0, 900.0, 930.0, 960.0, 990.0]
CORPORATE_AND_NET_INTEREST = [-150.0, -170.0, -190.0, -210.0, -230.0]
ANNUAL_DIVIDEND_PER_SHARE = [6.48, 6.65, 6.85, 7.05, 7.25]
ANNUAL_BUYBACKS = [900.0, 1_000.0, 1_100.0, 1_200.0, 1_300.0]
WACC = 0.090
TERMINAL_GROWTH = 0.025
EQUIPMENT_NET_DEBT = 2_613.0
FS_BOOK_EQUITY = 7_069.0
FS_PRICE_TO_BOOK = 1.40
DILUTED_SHARES = 270.8
MINIMUM_CASH = 5_000.0
OPENING = {
    "sales": 38_917.0,
    "equipment_nwc": 38_917.0 * EQUIPMENT_NWC_PERCENT_SALES,
    "ppe": 8_079.0,
    "cash_securities": 9_687.0,
    "finance_assets": 59_006.0,
    "other_assets": 29_224.0,
    "borrowings": 63_936.0,
    "other_liabilities": 16_053.0,
    "equity": 25_956.0,
}

# Previously specified paths: base plus/minus 2 percentage points in each year.
PPA_GROWTH_PATHS = {
    "Lower": [-0.12, 0.10, 0.07, 0.04, 0.02],
    "Base": [-0.10, 0.12, 0.09, 0.06, 0.04],
    "Higher": [-0.08, 0.14, 0.11, 0.08, 0.06],
}
PPA_MARGIN_PATHS = {
    "Lower": [0.095, 0.120, 0.140, 0.152, 0.160],
    "Base": [0.115, 0.140, 0.160, 0.172, 0.180],
    "Higher": [0.135, 0.160, 0.180, 0.192, 0.200],
}
