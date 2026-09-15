"""Asbury Automotive peer P/E valuation using the supplied FY2024 case data.

Run from the ZacharyAlvin folder with exactly:
./.python/bin/python asbury_pe.py
"""

from statistics import median


# ============================== INPUTS ======================================
# Prices: December 31, 2024 closing price, USD per share.
# EPS: FY2024 total GAAP diluted earnings per share, USD per share.
target = {"ticker": "ABG", "name": "Asbury Automotive", "price": 243.03, "eps": 21.50}

peers = [
    {"ticker": "AN", "name": "AutoNation", "price": 169.84, "eps": 16.92},
    {"ticker": "GPI", "name": "Group 1 Automotive", "price": 421.48, "eps": 36.81},
]
# ===========================================================================


def positive_number(value):
    """True only for a positive int or float; booleans are not accepted."""
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def clean_ticker(company):
    return str(company.get("ticker", "")).strip().upper()


def prepare_peers(raw_peers, target_ticker):
    """Exclude the target and deduplicate peers by ticker, keeping the first."""
    unique_peers = []
    excluded = []
    seen = set()

    for peer in raw_peers:
        ticker = clean_ticker(peer)
        if not ticker:
            excluded.append("peer with missing ticker")
        elif ticker == target_ticker:
            excluded.append(f"{ticker} (target excluded from its own peer set)")
        elif ticker in seen:
            excluded.append(f"{ticker} (duplicate peer)")
        else:
            seen.add(ticker)
            unique_peers.append(peer)

    return unique_peers, excluded


def peer_pe(peer):
    if not positive_number(peer.get("price")) or not positive_number(peer.get("eps")):
        return None
    return peer["price"] / peer["eps"]


def implied_price(multiple, target_eps):
    if multiple is None or not positive_number(target_eps):
        return None
    return multiple * target_eps


def money_or_not_meaningful(value):
    return "not meaningful" if value is None else f"${value:,.2f}"


target_ticker = clean_ticker(target)
deduplicated_peers, exclusions = prepare_peers(peers, target_ticker)
peer_results = [(peer, peer_pe(peer)) for peer in deduplicated_peers]
valid_results = [(peer, multiple) for peer, multiple in peer_results if multiple is not None]
valid_multiples = [multiple for _, multiple in valid_results]

print("ASBURY AUTOMOTIVE — FY2024 PEER P/E VALUATION")
print(
    f"Target: {target['name']} ({target_ticker}) | "
    f"12/31/2024 close: {money_or_not_meaningful(target.get('price') if positive_number(target.get('price')) else None)} | "
    f"FY2024 GAAP diluted EPS: {money_or_not_meaningful(target.get('eps') if positive_number(target.get('eps')) else None)}"
)

print("\nPEER MULTIPLES")
for peer, multiple in peer_results:
    ticker = clean_ticker(peer) or "MISSING TICKER"
    if multiple is None:
        print(
            f"{peer.get('name', 'Unnamed peer')} ({ticker}): P/E not meaningful "
            "because price or diluted EPS is missing or nonpositive"
        )
    else:
        print(
            f"{peer.get('name', 'Unnamed peer')} ({ticker}): "
            f"${peer['price']:,.2f} / ${peer['eps']:,.2f} = {multiple:.6f}x"
        )

for exclusion in exclusions:
    print(f"Excluded: {exclusion}")

print("\nTARGET IMPLIED PRICES")
if not valid_multiples:
    print("No usable peers; no peer P/E estimate.")
elif not positive_number(target.get("eps")):
    print("Target implied-price calculations are not meaningful because target EPS is missing or nonpositive.")
else:
    minimum_pe = min(valid_multiples)
    median_pe = median(valid_multiples)
    maximum_pe = max(valid_multiples)

    if len(valid_multiples) == 1:
        reference_price = implied_price(median_pe, target["eps"])
        print(f"One valid peer: reference estimate only; no range.")
        print(f"Reference P/E: {median_pe:.6f}x")
        print(f"Reference implied price: {money_or_not_meaningful(reference_price)}")
    else:
        print(f"Minimum peer P/E: {minimum_pe:.6f}x")
        print(f"Median peer P/E: {median_pe:.6f}x")
        print(f"Maximum peer P/E: {maximum_pe:.6f}x")
        print(f"Minimum implied price: {money_or_not_meaningful(implied_price(minimum_pe, target['eps']))}")
        print(f"Median implied price: {money_or_not_meaningful(implied_price(median_pe, target['eps']))}")
        print(f"Maximum implied price: {money_or_not_meaningful(implied_price(maximum_pe, target['eps']))}")

print("\nPEER-REMOVAL TEST")
if not valid_multiples:
    print("No full-peer estimate and no peers to remove.")
elif not positive_number(target.get("eps")):
    print("Removal estimates are not meaningful because target EPS is missing or nonpositive.")
else:
    full_median_price = median(valid_multiples) * target["eps"]
    for removed_peer, _ in valid_results:
        removed_ticker = clean_ticker(removed_peer)
        remaining_multiples = [
            multiple
            for peer, multiple in valid_results
            if clean_ticker(peer) != removed_ticker
        ]
        if not remaining_multiples:
            print(f"Remove {removed_ticker}: no estimate (no usable peers remain)")
        else:
            remaining_price = median(remaining_multiples) * target["eps"]
            dollar_change = remaining_price - full_median_price
            print(
                f"Remove {removed_ticker}: median-implied price "
                f"${remaining_price:,.2f}; change from full-peer estimate "
                f"{dollar_change:+,.2f}"
            )

print("\nLEAVE-ONE-OUT INTERPRETATION")
if {clean_ticker(peer) for peer, _ in valid_results} >= {"AN", "GPI"}:
    an_multiple = next(
        multiple for peer, multiple in valid_results if clean_ticker(peer) == "AN"
    )
    gpi_multiple = next(
        multiple for peer, multiple in valid_results if clean_ticker(peer) == "GPI"
    )
    if positive_number(target.get("eps")):
        full_peer_price = median(valid_multiples) * target["eps"]
        an_only_price = an_multiple * target["eps"]
        removal_change = an_only_price - full_peer_price
        direction = "lower" if removal_change < 0 else "raise"
        print(
            f"Prediction: removing GPI will {direction} Asbury's implied price "
            "because GPI has the higher P/E multiple."
        )
        print(
            f"Result: removing GPI leaves AN and changes the estimate from "
            f"${full_peer_price:,.2f} to ${an_only_price:,.2f}, a change of "
            f"{removal_change:+,.2f}, calculated with unrounded multiples."
        )
    else:
        print("The GPI-removal price effect is not meaningful because target EPS is unusable.")
else:
    print("The AN-versus-GPI prediction is unavailable because both named peers are not usable.")

print(
    "One remaining peer gives one P/E observation and therefore one reference "
    "estimate, not a minimum-to-maximum peer range."
)
print(
    "Peer decision: retain both AutoNation and Group 1 in the original peer set "
    "unless business evidence shows that either company is not economically "
    "comparable to Asbury. Numerical sensitivity alone does not justify removal."
)

print("\nMethod: peer P/E multiplied by target diluted EPS; no cash/debt bridge.")
print("Retrospective training comparison; used for educational purposes, not financial advice.")
