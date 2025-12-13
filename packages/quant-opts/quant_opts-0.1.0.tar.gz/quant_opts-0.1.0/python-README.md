# quant-opts Python bindings

Built with pyo3 + maturin. Provides Black–Scholes pricing, rational pricing, Greeks, and rational implied volatility.

## Quick usage (dev install)

```bash
cd bindings/python
# optional: create venv
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install maturin
maturin develop --release
python - <<'PY'
from quant_opts import price, greeks, rational_implied_vol

print('price', price('call', 105, 100, 0.25, 0.03, 0.01, 0.22))
print('iv', rational_implied_vol(4.25, 'call', 102, 100, 0.25, 0.02, 0.0))
print('greeks', greeks('call', 105, 100, 0.25, 0.03, 0.01, 0.22))
PY
```

## Build wheels

```bash
cd bindings/python
maturin build --release
# or maturin publish (requires PyPI creds/Trusted Publisher)
```

## Example script

After `maturin develop --release -m bindings/python/pyproject.toml` you can run:

```bash
python examples/python_cli/main.py
```

This prints price, rational price, delta, and implied vol to sanity-check the build.

## Notes
- Module name: `quant_opts.core` (re-exported from `quant_opts/__init__.py` for a flat import surface).
- Type hints included (PEP 561): `.pyi` stubs + `py.typed` shipped with the wheel.
- Requires Python >=3.9, Rust toolchain, and `maturin`.
