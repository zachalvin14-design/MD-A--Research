# Monthly adjusted closing prices

`prices.csv` contains Date first, followed by SPY, VXUS, BND, and SGOV, ordered oldest month first. Prices are in USD per share, adjusted for distributions and splits by Yahoo Finance.

There are 61 monthly observations from September 30, 2021 through September 30, 2026. The September 2021 starting observation supports 60 monthly returns for October 2021 through September 2026 (five years).

| Ticker | Fund | Source | Download date (America/Indiana/Indianapolis) |
| --- | --- | --- | --- |
| SPY | SPDR S&P 500 ETF Trust | [Yahoo Finance historical prices](https://finance.yahoo.com/quote/SPY/history/) via yfinance | 2026-10-22 |
| VXUS | Vanguard Total International Stock ETF | [Yahoo Finance historical prices](https://finance.yahoo.com/quote/VXUS/history/) via yfinance | 2026-10-22 |
| BND | Vanguard Total Bond Market ETF | [Yahoo Finance historical prices](https://finance.yahoo.com/quote/BND/history/) via yfinance | 2026-10-22 |
| SGOV | iShares 0-3 Month Treasury Bond ETF | [Yahoo Finance historical prices](https://finance.yahoo.com/quote/SGOV/history/) via yfinance | 2026-10-22 |

Method: `meridian_portfolio.py` downloaded daily prices using `yfinance.download` with `auto_adjust=True`, start `2021-09-01`, and exclusive end `2026-10-01`. The adjusted `Close` returned with this setting is used as the adjusted closing price. Each monthly value is the last available daily adjusted close, labeled with calendar month-end (which can be a non-trading day). Values were copied without rounding from `portfolio_results/monthly_adjusted_prices.csv`.

Validation: date column first; one column per ticker; ascending unique dates; consecutive months; 61 rows; all 244 price values finite and positive; no missing prices. The download date is taken from the source file's last modification time from the successful download in this session. Historical adjusted prices can change when the provider revises its data or adjustment factors.

## Project 2 use and timing

The price snapshot's SHA-256 is `1ee8f53b6e38b98311e2d01fdb810188f48681ac6237f6c7a4a7659a26a723c4`. The strategy fits its target weights using monthly returns through September 30, 2024. Returns ending October 31, 2024 through September 30, 2026 are reserved for scoring. The frozen download contains retrospectively adjusted prices. It supports reproducing the split, while exact historical adjustment vintages and trade execution remain unverified.
