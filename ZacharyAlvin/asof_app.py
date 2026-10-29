"""FRED-style rate charts. Run: .venv/bin/python -m streamlit run asof_app.py"""
from datetime import date
from io import BytesIO
from pathlib import Path
import re
from urllib.parse import urlencode
from urllib.request import urlopen

import pandas as pd
import streamlit as st


SERIES = {
    'BAA': "Moody's Baa corporate bond yield",
    'FEDFUNDS': 'Federal funds rate',
    'DGS10': '10-year Treasury yield',
    'MORTGAGE30US': '30-year mortgage rate',
    'CPIAUCSL': 'Consumer Price Index — your prework series',
}
RATE_IDS = ['BAA', 'FEDFUNDS', 'DGS10', 'MORTGAGE30US']


def parse_csv(content, series_id):
    """Both sources have a date column and one value column (vintage suffix varies)."""
    frame = pd.read_csv(BytesIO(content), na_values=['.'])
    if len(frame.columns) != 2:
        raise ValueError('Expected a date column and one series column.')
    dates = pd.to_datetime(frame.iloc[:, 0], errors='raise')
    values = pd.to_numeric(frame.iloc[:, 1], errors='raise')
    result = pd.Series(values.to_numpy(), index=dates, name=series_id).sort_index()
    result.index.name = 'Date'
    if result.index.has_duplicates:
        raise ValueError('The download contains duplicate observation dates.')
    return result


@st.cache_data(show_spinner=False)
def download_today(series_id, downloaded_on):
    """One FRED request per series, cached separately for each download day."""
    url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?' + urlencode({'id': series_id})
    with urlopen(url, timeout=30) as response:
        return parse_csv(response.read(), series_id)


@st.cache_data(show_spinner=False)
def download_asof(series_id, vintage_date, downloaded_on):
    """One ALFRED request per series/vintage, cached for the download day."""
    url = 'https://alfred.stlouisfed.org/graph/alfredgraph.csv?' + urlencode(
        {'id': series_id, 'vintage_date': str(vintage_date)})
    with urlopen(url, timeout=30) as response:
        return parse_csv(response.read(), series_id)


def comparison(series_id, current, vintage):
    """Count numeric observations, not missing-day placeholders; use full downloads."""
    row = {'Series': f'https://fred.stlouisfed.org/series/{series_id}'}
    for label, data in [('As known then', vintage), ('Today', current)]:
        valid = data.dropna() if data is not None else pd.Series(dtype=float)
        row[f'{label}: last measured'] = valid.index[-1].date().isoformat() if len(valid) else None
        row[f'{label}: value'] = float(valid.iloc[-1]) if len(valid) else None
    row['New values after last known date'] = None
    row['Revised values on shared dates'] = None
    if current is not None and vintage is not None:
        now, then = current.dropna(), vintage.dropna()
        if len(then):
            row['New values after last known date'] = int((now.index > then.index[-1]).sum())
        shared = pd.concat([now.rename('now'), then.rename('then')], axis=1, join='inner')
        row['Revised values on shared dates'] = int((shared['now'] != shared['then']).sum())
    return row


def main():
    today = date.today()
    st.set_page_config(page_title='Interest rates | As-of FRED lab', layout='wide')
    st.title('Interest rates · As-of FRED lab')
    st.caption(f'Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today ({today}); built with AI help, a learning demonstration, not investment advice.')
    with st.sidebar:
        selected = st.multiselect('Series', list(SERIES), default=RATE_IDS,
                                  format_func=lambda key: f'{key} — {SERIES[key]}')
        extra = st.text_input('Add another FRED series ID', placeholder='CPIAUCSL').strip().upper()
        start = st.date_input('Start date', date(2020, 1, 1))
        vintage_date = st.date_input('As known on', today, max_value=today)
    if extra:
        if re.fullmatch(r'[A-Z0-9_]+', extra):
            selected = list(dict.fromkeys(selected + [extra]))
        else:
            st.error('Additional series ID must contain only letters, numbers, or underscores.')
    if not selected:
        st.info('Select a series or enter another FRED series ID.')
        return

    rows = []
    for series_id in selected:
        st.subheader(f'{series_id} — {SERIES.get(series_id, "Additional FRED series")}')
        current = vintage = None
        # Independent error handling keeps a working chart if only ALFRED fails.
        with st.spinner(f'Loading {series_id}…'):
            try:
                current = download_today(series_id, today)
            except Exception as error:
                st.error(f'{series_id}: FRED download failed ({type(error).__name__}). Check the ID and connection.')
            try:
                vintage = download_asof(series_id, vintage_date, today)
            except Exception as error:
                st.error(f'{series_id}: ALFRED download failed ({type(error).__name__}). Check the ID, vintage coverage, and connection.')
        if current is not None:
            chart = current.loc[current.index >= pd.Timestamp(start)]
            if chart.dropna().empty:
                st.info('No numeric observations on or after the start date.')
            else:
                units = 'Percent' if series_id in RATE_IDS else (
                    'Index, 1982–1984 = 100' if series_id == 'CPIAUCSL' else 'Series value')
                st.line_chart(chart, x_label='Date measured', y_label=units)
        known = vintage.dropna() if vintage is not None else pd.Series(dtype=float)
        last = known.index[-1].date().isoformat() if len(known) else 'Unavailable'
        st.caption(f'Last measured date with a numeric value known on {vintage_date}: {last}')
        rows.append(comparison(series_id, current, vintage))

    st.subheader('Then and today')
    st.caption('Table uses full histories; the start date limits charts only. Counts exclude missing values (including “.”). Revisions compare numeric values on identical observation dates. A missing vintage has no last known date, so its new-value count is unavailable. Dates establish day-level availability, not intraday trade timing.')
    table = pd.DataFrame(rows)
    for column in ['New values after last known date', 'Revised values on shared dates']:
        table[column] = table[column].astype('Int64')
    st.dataframe(table, hide_index=True, width='stretch', column_config={
        'Series': st.column_config.LinkColumn('Series', display_text=r'https://fred\.stlouisfed\.org/series/(.*)'),
    })
    if 'CPIAUCSL' in selected:
        with st.expander('CPIAUCSL data card and Project 2 decision', expanded=True):
            st.markdown(Path(__file__).with_name('asof_app_data_card.md').read_text())


if __name__ == '__main__':
    main()
