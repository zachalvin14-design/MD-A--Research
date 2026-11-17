"""Run with: .venv/bin/python -m streamlit run app.py"""

from copy import deepcopy
from hashlib import sha256
from io import BytesIO, StringIO

import streamlit as st

from project2_holdout import run_report

from portfolio import (
    SLEEVES, CORRELATION, OBJECTIVE_RETURN,
    estimate_from_prices, search_lowest_volatility,
)


st.set_page_config(page_title="Meridian portfolio pilot", layout="wide")
st.caption("AI assisted with building and checking this project. For education, not investment advice.")
st.title("Meridian portfolio pilot")
st.subheader("Holdout decision")
haircut = st.number_input("Reduce the SPY training return assumption by (percentage points)",
                          min_value=0.0, value=2.0, step=1.0)
report = StringIO()
run_report(haircut / 100, output=report)
st.code(report.getvalue(), language=None)
st.divider()
st.subheader("Portfolio lab sandbox")
st.caption("The sidebar and sandbox controls only affect the exploratory results below.")

with st.sidebar:
    objective = st.number_input("Objective annual return (%)", value=OBJECTIVE_RETURN * 100,
                                step=0.1, format="%.2f") / 100
    reserve_minimum = st.number_input("Reserve minimum (%)", min_value=0.0,
                                      max_value=100.0, value=3.0, step=1.0) / 100
    upload = st.file_uploader("Upload prices.csv", type=["csv"])
    last_36 = st.toggle("Use only the last 36 months", value=False,
                        disabled=upload is None)
    st.caption("CSV: date first, oldest first, then one price column per ticker. "
               "One row per consecutive month; at least 37 rows for the 36-month window.")

try:
    if upload is None:
        loaded = deepcopy(SLEEVES)
        active = deepcopy(SLEEVES)
        loaded_correlation = active_correlation = CORRELATION
        source_key = "meridian"
        st.write("Source: Meridian course-authored annual inputs.")
    else:
        content = upload.getvalue()
        source_key = sha256(content).hexdigest()
        loaded, loaded_correlation = estimate_from_prices(BytesIO(content))
        active, active_correlation = estimate_from_prices(BytesIO(content), last_36)
        st.write(f"Source: {upload.name}; "
                 + ("last 36 monthly returns." if last_36 else "all monthly returns."))
        st.caption("Historical annualized arithmetic return estimate: monthly mean × 12, "
                   "not a forecast. Risk estimates: sample standard deviation × √12 and "
                   "correlations from the same monthly returns. Select reserve eligibility below.")

    st.subheader("Edit annual return assumptions and reserve eligibility")
    st.caption("Meridian returns are course-authored assumptions. CSV defaults are historical "
               "averages for the selected window; using them in the search does not make them forecasts.")
    for index, sleeve in enumerate(active):
        left, right = st.columns([2, 1])
        with left:
            sleeve["return"] = st.number_input(
                f"{sleeve['name']} annual return assumption (%)",
                value=sleeve["return"] * 100, step=0.1, format="%.2f",
                key=f"return-{source_key}-{last_36}-{index}",
            ) / 100
        with right:
            sleeve["reserve_eligible"] = st.checkbox(
                f"{sleeve['name']} reserve-eligible",
                value=sleeve["reserve_eligible"], key=f"reserve-{source_key}-{index}",
            )

    current = search_lowest_volatility(active, active_correlation, objective, reserve_minimum)
    baseline = search_lowest_volatility(loaded, loaded_correlation, objective, reserve_minimum)

    def show_result(title, result, sleeves):
        st.subheader(title)
        if result is None:
            st.write("no mix meets the objective")
            return
        st.table({"Asset": [s["name"] for s in sleeves],
                  "Weight": [f"{w:.2%}" for w in result["weights"]]})
        st.metric("Annual return under input assumptions", f"{result['return']:.2%}")
        st.metric("Annual volatility", f"{result['volatility']:.2%}")
        st.metric("Reserve-eligible weight", f"{result['reserve_weight']:.2%}")

    st.caption("Every fully invested, long-only mix in 5 percentage point steps. "
               "Both answers use the sidebar objective and reserve minimum.")
    left, right = st.columns(2)
    with left:
        show_result("Lowest-risk mix: current inputs", current, active)
    with right:
        show_result("Lowest-risk mix: inputs as loaded", baseline, loaded)
        st.caption("Original returns and reserve flags; CSV comparison always uses all months. "
                   "CSV tickers start with no reserve eligibility assigned.")
    if current is not None and baseline is not None:
        changes = [100 * (a - b) for a, b in zip(current["weights"], baseline["weights"])]
        largest = max(range(len(changes)), key=lambda i: abs(changes[i]))
        st.write(f"Largest weight change: {active[largest]['name']} "
                 f"{changes[largest]:+.2f} percentage points "
                 "(current minus loaded).")
    else:
        st.write("Largest weight change: unavailable because one or both mixes are infeasible.")
except (ValueError, TypeError, KeyError) as error:
    st.error(str(error))
