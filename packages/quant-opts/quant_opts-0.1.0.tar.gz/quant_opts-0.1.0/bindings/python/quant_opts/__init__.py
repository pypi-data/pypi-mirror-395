"""Python bindings for quant-opts (Black–Scholes).

Functions accept primitive floats and `kind` as "call" or "put".
"""

from __future__ import annotations

from typing import Dict

from .core import greeks, price, rational_implied_vol, rational_price

__all__ = ["price", "rational_price", "greeks", "rational_implied_vol"]


def _greeks_dict(kind: str, spot: float, strike: float, maturity: float, rate: float, div: float, vol: float) -> Dict[str, float]:
    return greeks(kind, spot, strike, maturity, rate, div, vol)
