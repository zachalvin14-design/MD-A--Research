"""Apply the assignment's provenance gates as of 31 March 2026."""
from datetime import date

DECISION_DATE = date(2026, 3, 31)
# Original row number, ticker, month measured, published on, price.
DATA = [
    (1, 'AAA', '2026-01', '2026-02-10', 101.0),
    (2, 'AAA', '2026-02', '2026-03-10', 104.0),
    (3, 'AAA', '2026-03', '2026-04-10', 109.0),
    (4, 'AAA', '2026-02', '2026-03-25', 103.0),
    (5, 'BBB', '2026-01', '2026-02-10', 98.0),
    (6, 'BBB', '2026-02', '2026-03-10', 97.0),
    (7, 'BBB', '2026-02', '2026-03-10', 97.0),
    (8, 'BBB', '2026-03', '2026-04-10', 92.0),
    (9, 'CCC', '2026-01', '2026-02-10', 110.0),
    (10, 'CCC', '2026-02', '2026-04-05', 112.0),
    (11, '', '2026-02', '2026-03-10', 99.0),
    (12, 'CCC', '2026-02', '2026-03-10', 111.0),
]


def select_latest(rows):
    latest = {}
    for row in rows:
        key = row[1:3]
        if key not in latest or row[3] > latest[key][3]:
            latest[key] = row
    return sorted(latest.values())


def signals(admitted):
    ranked = []
    for ticker in sorted({row[1] for row in admitted}):
        history = sorted((r for r in admitted if r[1] == ticker), key=lambda r: r[2])
        current = history[-1]
        year, month = map(int, current[2].split('-'))
        previous_month = f'{year - 1}-12' if month == 1 else f'{year}-{month - 1:02d}'
        previous = next((r for r in history if r[2] == previous_month), None)
        if previous is None:
            print(f'{ticker}: unavailable; missing previous calendar month')
            continue
        result = current[4] / previous[4] - 1
        ranked.append((result, ticker))
        print(f'{ticker}: {current[4]:.1f} / {previous[4]:.1f} - 1 = {result:+.2%}'
              f' (rows {previous[0]}, {current[0]})')
    print('Ranking: ' + ' > '.join(ticker for _, ticker in sorted(ranked, reverse=True)))


def validity_flags(admitted):
    print('\nV: economic validity flags (separate from the four gates)')
    for number, ticker, month, published, price in admitted:
        if price > 100:
            print(f'Row {number}: {ticker} {month}, price {price:.1f} > 100; '
                  f'one-year zero yield = {100 / price - 1:+.2%}')
    for month in sorted({r[2] for r in admitted}):
        by_ticker = {r[1]: r for r in admitted if r[2] == month}
        for safer, riskier in [('AAA', 'BBB'), ('BBB', 'CCC')]:
            if safer in by_ticker and riskier in by_ticker:
                a, b = by_ticker[safer], by_ticker[riskier]
                if a[4] <= b[4]:
                    print(f'{month}: rows {a[0]} and {b[0]} violate '
                          f'{safer} price > {riskier} price ({a[4]:.1f} <= {b[4]:.1f})')
    print('Negative yields are possible in real markets; flagged here under the exercise assumptions.')


def main():
    cutoff = DECISION_DATE
    rows = list(DATA)
    funnel = []
    quarantined = []

    def apply_rule(label, keep):
        nonlocal rows
        decisions = [(r, keep(r)) for r in rows]
        removed = [r[0] for r, retained in decisions if not retained]
        rows = [r for r, retained in decisions if retained]
        funnel.append((label, removed))

    quarantined = [r for r in rows if not r[1]]
    apply_rule('1. Missing ticker (quarantine)', lambda r: bool(r[1]))
    seen = set()

    def unique(r):
        key = r[1:]  # Exact content duplicate, excluding original row number.
        if key in seen:
            return False
        seen.add(key)
        return True

    apply_rule('2. Exact duplicate', unique)
    apply_rule('3. Published after decision date',
               lambda r: date.fromisoformat(r[3]) <= cutoff)
    chosen = select_latest(rows)
    retained_ids = {r[0] for r in chosen}
    apply_rule('4. Superseded publication (revision)',
               lambda r: r[0] in retained_ids)

    print(f'Decision date: {cutoff}')
    print('\nRow funnel:')
    for label, removed in funnel:
        action = 'quarantined' if label.startswith('1.') else 'removed'
        print(f'  {label}: {action} {len(removed)}; rows {removed if removed else "none"}')
    print(f'  Remaining: {len(rows)}')
    print(f'  Quarantine retains original rows: {[r[0] for r in quarantined]}')
    print('\nAs-of panel:')
    print(f'  {"Row":>3}  {"Ticker":<6} {"Month":<7} {"Published":<10} {"Price":>8}')
    for number, ticker, month, published, price in chosen:
        print(f'  {number:>3}  {ticker:<6} {month:<7} {published:<10} {price:>8.2f}')
    print('\nAs-of signals:')
    signals(chosen)
    print('\nNaive signals (latest publication per ticker/month, ignoring cutoff):')
    signals(select_latest([r for r in DATA if r[1].strip()]))
    print('Naive signals may compare different months across funds and use future publications.')
    validity_flags(chosen)


if __name__ == '__main__':
    main()
