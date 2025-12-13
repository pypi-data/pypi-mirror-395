## quant-opts (0.1.0)

[![Build](https://github.com/day01/quant-opts/actions/workflows/build.yml/badge.svg)](https://github.com/day01/quant-opts/actions/workflows/build.yml)
[![Coverage](https://codecov.io/gh/day01/quant-opts/branch/main/graph/badge.svg)](https://codecov.io/gh/day01/quant-opts)

A high-performance Rust library for option pricing and risk, starting from a fast Black–Scholes–Merton implementation and evolving towards a more general framework (e.g. SABR and other models).

The current codebase is focused on Black–Scholes for European vanilla options. Over time, `quant-opts` will extend this to a broader set of models and instruments while keeping the API ergonomic and performance-oriented.

## Current scope

- Black–Scholes–Merton model
- European vanilla options (calls and puts) expressed via core types
  (`VanillaOption`, `MarketData`, `OptionStyle`, `OptionType`)
- Pricing and Greeks for vanilla options
- Implied-volatility solvers (including a rational approximation based on
  Peter Jäckel’s *“Let’s Be Rational”* method)
- Batch-friendly API and Criterion benchmarks for throughput studies

## Roadmap (high level)

- Additional models such as SABR and other stochastic-volatility / local-volatility models
- Extended product coverage beyond plain-vanilla options
- Unified abstractions for models, products, and numerical methods
- First-class batch / vectorized pricing workflows

## Core Rust API

The primary way to use `quant-opts` today is via the core types and the
Black–Scholes model:

```rust
use quant_opts::{
    BlackScholes, MarketData, OptionStyle, OptionType, VanillaModel, VanillaOption,
};

let option = VanillaOption::new(
    OptionStyle::European,
    OptionType::Call,
    100.0,             // strike
    20.0 / 365.25,     // time to maturity (years)
);

let market = MarketData::new(
    100.0,  // spot
    0.05,   // risk-free rate
    0.01,   // dividend yield
);

// Direct static API with explicit volatility
let price = BlackScholes::price(&option, &market, 0.2)?;

// Or via the generic `VanillaModel` trait
let model = BlackScholes::new(0.2);
let price_via_trait = model.price(&option, &market)?;
```

Error handling uses `Result<_, String>` to propagate issues such as
non-finite volatility or zero time to maturity.

## Optional wrappers feature

For FFI and quick scripting use cases, you can enable the `wrappers`
feature to get simple function-style helpers:

```toml
[dependencies]
quant-opts = { version = "0.1.0", features = ["wrappers"] }
```

```rust
use quant_opts::{wrappers, OptionType};

let price = wrappers::price_eur_vanilla_bs(
    OptionType::Call,
    100.0,           // spot
    110.0,           // strike
    20.0 / 365.25,   // maturity (years)
    0.05,            // risk-free rate
    0.05,            // dividend yield
    0.2,             // volatility
)?;
```

## Language bindings

Rust is the primary API, but the library is being designed with FFI in mind. Planned bindings include:

- Python
- WebAssembly (WASM)
- Other FFI targets where low-latency option pricing is needed

These bindings are part of the roadmap and will be added as the core library stabilizes.

## Performance

This library is written with performance in mind, both for single-option pricing and large batch workloads. The repository already includes Criterion-based benchmarks and throughput studies.

Up-to-date baseline numbers for pricing, Greeks and implied volatility are
documented in `docs/baseline.md`. The CI and benchmarking setup is described
in `docs/BENCHMARKING.md`.

### Benchmark commands (no default features)

- Micro pricing: `cargo bench --no-default-features --bench pricing`
- Micro IV: `cargo bench --no-default-features --bench implied_volatility`
- Micro Greeks: `cargo bench --no-default-features --bench greeks`
- Single option sweeps: `cargo bench --no-default-features --bench single_option`
- Single IV sweeps: `cargo bench --no-default-features --bench single_iv`
- Single Greeks sweeps: `cargo bench --no-default-features --bench single_greeks`
- Batch pricing: `cargo bench --no-default-features --bench batch_pricing`
- Batch Greeks: `cargo bench --no-default-features --bench batch_greeks`
- Throughput: `cargo bench --no-default-features --bench throughput`
- Scaling study: `cargo bench --no-default-features --bench scaling`
- Batch size study: `cargo bench --no-default-features --bench batch_size_study`

## Examples

Run the included examples with:

- Pricing and Greeks: `cargo run --example pricing_and_greeks`
- Implied volatility (rational solver): `cargo run --example implied_vol`
- WASM bindings demo: install the target (`rustup target add wasm32-unknown-unknown`) and `wasm-bindgen-cli`, then build with `--features wasm-example --target wasm32-unknown-unknown --example wasm_api`; run `wasm-bindgen --target web --out-dir examples/wasm/pkg target/wasm32-unknown-unknown/debug/examples/wasm_api.wasm` and open `examples/wasm/index.html` via a local server. See `examples/wasm/README.md`.
- WASM CLI (WASI): `rustup target add wasm32-wasip1` then `cargo build --target wasm32-wasip1 --example wasm_cli`; run with `wasmtime target/wasm32-wasip1/debug/examples/wasm_cli.wasm price --spot ...` (see `examples/wasm/README.md`).

Make targets for wasm bindings (requires `wasm-pack`):
- `make wasm-bindings` → builds web (`target/wasm/pkg-web`) and bundler (`target/wasm/pkg-react`) bindings

## Origin and credits

This project started as a fork of the excellent [`blackscholes`](https://crates.io/crates/blackscholes) crate by [Hayden Rose](https://github.com/hayden4r4). Many thanks for the original implementation and design. The goal of `quant-opts` is to build on that foundation, extending model coverage and abstractions while preserving and further improving performance.

## Metadata

- Edition: 2024
- MSRV: 1.91.1 (Rust toolchain pinned in `rust-toolchain.toml`)
- License: MIT (see `LICENSE.md`)
- Changelog: see `CHANGELOG.md`
