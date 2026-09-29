"""One-at-a-time operating sensitivities for the Deere pro-forma."""

import contextlib
import copy
import importlib.util
import io
from pathlib import Path

import de_sensitivity_base_inputs as base


MODEL_PATH = Path(__file__).with_name("de_proforma.py")


def fresh_base_model():
    """Load an independent model and explicitly restore every saved base input."""
    spec = importlib.util.spec_from_file_location("de_proforma_fresh", MODEL_PATH)
    model = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(model)

    model.years = copy.deepcopy(base.YEARS)
    model.segment_sales_2025 = copy.deepcopy(base.SEGMENT_SALES_2025)
    model.segment_growth = copy.deepcopy(base.SEGMENT_GROWTH)
    model.segment_margin = copy.deepcopy(base.SEGMENT_MARGIN)
    model.finance_income = copy.deepcopy(base.FINANCE_INCOME)
    model.other_income_percent_sales = base.OTHER_INCOME_PERCENT_SALES
    model.equipment_da_percent_sales = base.EQUIPMENT_DA_PERCENT_SALES
    model.capex_percent_sales = copy.deepcopy(base.CAPEX_PERCENT_SALES)
    model.equipment_nwc_percent_sales = base.EQUIPMENT_NWC_PERCENT_SALES
    model.tax_rate = base.TAX_RATE
    model.fs_net_income = copy.deepcopy(base.FS_NET_INCOME)
    model.corporate_and_net_interest = copy.deepcopy(base.CORPORATE_AND_NET_INTEREST)
    model.annual_dividend_per_share = copy.deepcopy(base.ANNUAL_DIVIDEND_PER_SHARE)
    model.annual_buybacks = copy.deepcopy(base.ANNUAL_BUYBACKS)
    model.wacc = base.WACC
    model.terminal_growth = base.TERMINAL_GROWTH
    model.equipment_net_debt = base.EQUIPMENT_NET_DEBT
    model.fs_book_equity = base.FS_BOOK_EQUITY
    model.fs_price_to_book = base.FS_PRICE_TO_BOOK
    model.diluted_shares = base.DILUTED_SHARES
    model.minimum_cash = base.MINIMUM_CASH
    model.opening = copy.deepcopy(base.OPENING)
    return model


def run_case(driver, level, path):
    model = fresh_base_model()
    if driver == "PPA sales growth":
        model.segment_growth["ppa"] = copy.deepcopy(path)
    elif driver == "PPA operating margin":
        model.segment_margin["ppa"] = copy.deepcopy(path)
    else:
        raise ValueError(f"Unknown driver: {driver}")

    try:
        forecast = model.build_forecast()
        balance_valid = all(abs(row["balance_check"]) <= 0.01 for row in forecast)
        cash_valid = all(row["cash_floor_met"] for row in forecast)
        accounting_valid = balance_valid and cash_valid
        valuation = None
        valuation_note = "Available"
        if not accounting_valid:
            valuation_note = "Unavailable: accounting or cash-floor check failed."
        elif forecast[-1]["equipment_fcff"] <= 0:
            valuation_note = "Unavailable: final-year FCFF is not positive; no terminal value used."
        elif model.terminal_growth >= model.wacc:
            valuation_note = "Unavailable: terminal growth is not below WACC."
        else:
            valuation = model.value_business(forecast)
        return {
            "driver": driver,
            "level": level,
            "path": copy.deepcopy(path),
            "status": "VALID" if accounting_valid else "INVALID",
            "forecast": forecast,
            "operating_profit": forecast[-1]["segment_profit"],
            "fcff": forecast[-1]["equipment_fcff"],
            "value_per_share": None if valuation is None else valuation["per_share"],
            "valuation_note": valuation_note,
        }
    except Exception as error:
        return {
            "driver": driver,
            "level": level,
            "path": copy.deepcopy(path),
            "status": "INVALID",
            "forecast": [],
            "operating_profit": None,
            "fcff": None,
            "value_per_share": None,
            "valuation_note": f"Unavailable: {type(error).__name__}: {error}",
        }


def signed(value):
    return f"{value:+,.1f}"


def signed_share(value):
    return f"{value:+,.2f}"


def path_text(path):
    return ", ".join(f"{year} {value:.1%}" for year, value in zip(base.YEARS, path))


def print_case(case, base_case):
    print(f"\nRUN: {case['driver']} — {case['level']}")
    print(f"Input path (annual percentage): {path_text(case['path'])}")
    print(f"Run status: {case['status']}")
    if not case["forecast"]:
        print(case["valuation_note"])
        return

    print("Accounting checks:")
    for row in case["forecast"]:
        print(
            f"  {row['year']}: balance gap {row['balance_check']:+.1f} USD million; "
            f"cash {row['cash_securities']:,.1f} >= {base.MINIMUM_CASH:,.1f} USD million = "
            f"{row['cash_floor_met']}"
        )

    op_delta = case["operating_profit"] - base_case["operating_profit"]
    fcff_delta = case["fcff"] - base_case["fcff"]
    print(
        f"FY2030 operating profit: {case['operating_profit']:,.1f} USD million "
        f"(change from base {signed(op_delta)} USD million)"
    )
    print(
        f"FY2030 equipment operations FCFF: {case['fcff']:,.1f} USD million "
        f"(change from base {signed(fcff_delta)} USD million)"
    )
    if case["value_per_share"] is None:
        print(f"Value per share: unavailable. {case['valuation_note']}")
    else:
        value_delta = case["value_per_share"] - base_case["value_per_share"]
        print(
            f"Value per share: ${case['value_per_share']:,.2f} "
            f"(change from base {signed_share(value_delta)} USD/share)"
        )

    print("Trace detail (USD millions except percentages and balance check):")
    print(
        f"{'Year':<6}{'PPA growth':>12}{'PPA sales':>14}{'PPA margin':>13}"
        f"{'PPA op profit':>16}{'Total op profit':>18}{'D&A':>11}{'Capex':>11}"
        f"{'Change NWC':>13}{'Equipment FCFF':>16}{'Balance':>11}"
    )
    for index, row in enumerate(case["forecast"]):
        ppa_margin = (case["path"][index] if case["driver"] == "PPA operating margin"
                      else base.SEGMENT_MARGIN["ppa"][index])
        ppa_growth = (case["path"][index] if case["driver"] == "PPA sales growth"
                      else base.SEGMENT_GROWTH["ppa"][index])
        ppa_profit = row["ppa_sales"] * ppa_margin
        print(
            f"{row['year']:<6}{ppa_growth:>11.1%}{row['ppa_sales']:>14,.1f}{ppa_margin:>12.1%}"
            f"{ppa_profit:>16,.1f}{row['segment_profit']:>18,.1f}{row['depreciation']:>11,.1f}"
            f"{row['capex']:>11,.1f}{row['change_nwc']:>13,.1f}{row['equipment_fcff']:>16,.1f}"
            f"{row['balance_check']:>11.1f}"
        )


def print_span(driver, cases):
    valid = [case for case in cases if case["status"] == "VALID"]
    print(f"\nOUTPUT SPANS — {driver}")
    if not valid:
        print("No valid lower/base/higher runs; spans unavailable.")
        return
    for label, key, unit in [
        ("FY2030 operating profit", "operating_profit", "USD million"),
        ("FY2030 equipment operations FCFF", "fcff", "USD million"),
    ]:
        values = [case[key] for case in valid if case[key] is not None]
        print(f"{label}: {max(values) - min(values):,.1f} {unit}")
    values = [case["value_per_share"] for case in valid if case["value_per_share"] is not None]
    if len(values) == len(valid):
        print(f"Value per share: ${max(values) - min(values):,.2f}")
    else:
        print("Value per share span: unavailable because a valid accounting run lacks a valid valuation.")


base_reference = run_case("PPA sales growth", "Base", base.PPA_GROWTH_PATHS["Base"])

print("DEERE ONE-AT-A-TIME OPERATING SENSITIVITY")
print("Inputs: annual percentages. Outputs: USD millions and USD/share as labelled.")
print("Every run starts from a fresh independent copy of de_sensitivity_base_inputs.py.")

groups = [
    ("PPA sales growth", base.PPA_GROWTH_PATHS),
    ("PPA operating margin", base.PPA_MARGIN_PATHS),
]
for driver, paths in groups:
    cases = [run_case(driver, level, path) for level, path in paths.items()]
    for case in cases:
        print_case(case, base_reference)
    print_span(driver, cases)

print("\nFINAL RESTORED-BASE RERUN")
final_base = run_case("PPA sales growth", "Base", base.PPA_GROWTH_PATHS["Base"])
print_case(final_base, base_reference)
same_outputs = all(
    abs(final_base[key] - base_reference[key]) < 0.000001
    for key in ("operating_profit", "fcff", "value_per_share")
)
print(f"Final base matches initial base outputs: {same_outputs}")
