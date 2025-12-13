from typing import Dict, Literal

Kind = Literal["call", "put", "c", "p"]

def price(
    kind: Kind,
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    dividend_yield: float,
    vol: float,
) -> float:
    """Black–Scholes price for a European option.

    Example:
        >>> round(price("call", 105, 100, 0.25, 0.03, 0.01, 0.22), 6)
        7.238559
    """

def rational_price(
    kind: Kind,
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    dividend_yield: float,
    vol: float,
) -> float:
    """Dividend-adjusted (rational) price for a European option.

    Example:
        >>> round(rational_price("put", 100, 95, 0.5, 0.02, 0.01, 0.3), 6)
        4.592931
    """

def greeks(
    kind: Kind,
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    dividend_yield: float,
    vol: float,
) -> Dict[str, float]:
    """Black–Scholes Greeks dict with delta, gamma, theta, vega, rho, epsilon, vanna, charm, vomma, speed, zomma.

    Example:
        >>> g = greeks("call", 105, 100, 0.25, 0.03, 0.01, 0.22)
        >>> round(g["delta"], 6)
        0.63793
    """

def rational_implied_vol(
    target_price: float,
    kind: Kind,
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    dividend_yield: float,
) -> float:
    """Implied volatility from the rational model for a target price.

    Example:
        >>> round(rational_implied_vol(4.25, "call", 102, 100, 0.25, 0.02, 0.0), 6)
        0.197251
    """
