"""
Minimal usage check for the quant_opts Python bindings.

Run after installing via `maturin develop --release -m bindings/python/pyproject.toml`.
"""

from quant_opts import greeks, price, rational_implied_vol, rational_price


def main() -> None:
    p = price("call", 105, 100, 0.25, 0.03, 0.01, 0.22)
    rp = rational_price("put", 100, 95, 0.5, 0.02, 0.01, 0.3)
    g = greeks("call", 105, 100, 0.25, 0.03, 0.01, 0.22)
    iv = rational_implied_vol(4.25, "call", 102, 100, 0.25, 0.02, 0.0)

    print(f"price={p:.6f}")
    print(f"rational_price={rp:.6f}")
    print(f"delta={g['delta']:.6f}")
    print(f"iv={iv:.6f}")


if __name__ == "__main__":
    main()
