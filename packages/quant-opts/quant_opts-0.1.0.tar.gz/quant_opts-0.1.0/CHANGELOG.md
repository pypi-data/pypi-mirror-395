# Changelog

## [0.1.0] - 2025-01-13

- Initial crate release after migration from the original `blackscholes` codebase
- Upgraded dependencies (criterion 0.8, rand 0.9, statrs 0.18, getrandom 0.3/0.2 with wasm support)
- Adopted Rust 2024 edition and declared MSRV 1.81+
- Stabilised core Black–Scholes API for European vanilla options, Greeks, and implied volatility
- Benchmark suite refreshed; baseline numbers remain in `docs/baseline.md`

[0.1.0]: https://github.com/day01/quant-opts/releases/tag/v0.1.0
