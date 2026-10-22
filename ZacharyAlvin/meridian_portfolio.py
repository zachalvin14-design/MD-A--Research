"""FIN 439: historical estimates and illustrative portfolio optimization."""
from pathlib import Path
import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize

TICKERS = ['SPY', 'VXUS', 'BND', 'SGOV']
START = '2021-09-01'  # Include September month-end for 60 monthly returns.
END = '2026-10-01'  # Exclusive: last full month September 2026.
TARGET_RETURN = 0.065  # Illustrative; replace with mandate objective.
MIN_SGOV = 0.10  # Illustrative; replace with actual reserve requirement.
OUT = Path(__file__).resolve().parent / 'portfolio_results'


def get_prices():
    raw = yf.download(TICKERS, start=START, end=END, auto_adjust=True,
                      progress=False, threads=False)
    if raw.empty:
        raise RuntimeError('Yahoo Finance returned no data. Check internet connection.')
    if isinstance(raw.columns, pd.MultiIndex):
        prices = raw['Close']
    else:
        prices = raw[['Close']].rename(columns={'Close': TICKERS[0]})
    monthly = prices.reindex(columns=TICKERS).resample('ME').last()
    if monthly.isna().any().any():
        raise RuntimeError(f'Missing monthly price data:\n{monthly.isna().sum()}')
    if len(monthly) != 61:
        raise RuntimeError(f'Need 61 month-end prices for 60 returns; got {len(monthly)}.')
    return monthly


def main():
    monthly = get_prices()
    returns = monthly.pct_change(fill_method=None).dropna()
    mu = returns.mean() * 12
    cov = returns.cov() * 12
    corr = returns.corr()
    summary = pd.DataFrame({'Annualized arithmetic return': mu,
                            'Annualized volatility': np.sqrt(np.diag(cov))}, index=TICKERS)
    OUT.mkdir(exist_ok=True)
    for frame, name in [(monthly, 'monthly_adjusted_prices'), (returns, 'monthly_returns'),
                        (summary, 'fund_statistics'), (corr, 'correlations'),
                        (cov, 'annualized_covariance')]:
        frame.to_csv(OUT / f'{name}.csv')
    mu_vec = mu.to_numpy()
    cov_mat = cov.to_numpy()
    sg = TICKERS.index('SGOV')
    constraints = [
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
        {'type': 'ineq', 'fun': lambda w: w[sg] - MIN_SGOV},
        {'type': 'ineq', 'fun': lambda w: float(w @ mu_vec) - TARGET_RETURN},
    ]
    solution = minimize(lambda w: float(w @ cov_mat @ w),
                        np.full(len(TICKERS), 1 / len(TICKERS)), method='SLSQP',
                        bounds=[(0, 1)] * len(TICKERS), constraints=constraints,
                        options={'ftol': 1e-12, 'maxiter': 3000})
    w = solution.x
    feasible = (solution.success and np.isfinite(w).all()
                and np.all(w >= -1e-6) and np.all(w <= 1 + 1e-6)
                and abs(w.sum() - 1) < 1e-6 and w[sg] >= MIN_SGOV - 1e-6
                and w @ mu_vec >= TARGET_RETURN - 1e-6)
    print('\nFIVE-YEAR HISTORICAL FUND STATISTICS\n')
    print(summary.to_string(float_format=lambda x: f'{x:.2%}'))
    print('\nCORRELATION MATRIX\n', corr.round(3).to_string())
    print(f'\nObjective: >= {TARGET_RETURN:.2%} annual expected return')
    print(f'Hard constraint: SGOV >= {MIN_SGOV:.2%}; long-only; weights sum to 100%')
    if feasible:
        weights = pd.Series(w, index=TICKERS, name='Weight')
        weights.to_csv(OUT / 'optimized_weights.csv')
        print('\nOPTIMIZED WEIGHTS\n', weights.to_string(float_format=lambda x: f'{x:.2%}'))
        print(f'Expected return: {w @ mu_vec:.2%}')
        print(f'Annualized volatility: {np.sqrt(w @ cov_mat @ w):.2%}')
        print('Illustrative numerical constraints: PASS')
    else:
        print('\nNO VERIFIED FEASIBLE PORTFOLIO for the specified return and reserve requirements.')
        print('Optimizer message:', solution.message)
        print('Do not report candidate weights as mandate-compliant.')
    print('\nFiles saved to:', OUT)
    print('Note: Historical estimates are not forecasts; this is not full mandate compliance.')


if __name__ == '__main__':
    main()
