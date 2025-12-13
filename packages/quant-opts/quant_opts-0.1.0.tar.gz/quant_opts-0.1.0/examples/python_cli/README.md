# Python CLI sanity check

Minimal example that uses the Python bindings (`quant_opts` built via maturin) to print price, rational price, delta, and implied volatility.

## Run

```bash
# from repo root, after building the extension:
maturin develop --release -m bindings/python/pyproject.toml
python examples/python_cli/main.py
```

Expected output includes values for `price`, `rational_price`, `delta`, and `iv`.
