# quant-opts Benchmarking

This document describes how performance benchmarks are organised and run for
`quant-opts` (Black–Scholes + vanilla model API).

## Overview

Benchmarks are implemented with **Criterion.rs** and cover:

- single‑option pricing, Greeks and implied volatility,
- batch workloads (arrays of options / SoA layouts),
- throughput and scaling studies,
- micro‑benchmarks for internal “Let’s Be Rational” helpers.

Baseline numbers for key operations are recorded in `docs/baseline.md`.

## Benchmark suites

The main suites are defined as `[[bench]]` entries in `Cargo.toml`:

- `pricing` – single option pricing via `BlackScholes::price` and `::rational_price`.
- `implied_volatility` – implied vol, in particular
  `BlackScholes::rational_implied_vol`.
- `greeks` – first‑order Greeks for a representative option.
- `single_option`, `single_greeks`, `single_iv` – more detailed grids over
  moneyness, maturity and volatility.
- `batch_pricing`, `batch_greeks` – Vec/SoA batch workloads (placeholders for
  future SIMD/parallel implementations).
- `throughput`, `scaling`, `batch_size_study` – focus on ops/sec and scaling
  with batch size.
- `black` – micro‑benchmarks of internal `lets_be_rational::black` expansions,
  enabled only with a dedicated feature (see below).

Some suites are feature‑gated:

- `visualize` (in `benches/throughput/visualize.rs`) requires
  the `visualize-bench` feature and `plotters` dependency.
- `black` (in `validation/black.rs`) requires
  the `lets-be-rational-validation` feature.

## Running benchmarks locally

Run all core benchmarks (without optional features):

```bash
cargo bench --no-default-features
```

Run a specific suite, for example implied volatility:

```bash
cargo bench --no-default-features --bench implied_volatility
```

Run the “Let’s Be Rational” micro‑benchmarks:

```bash
cargo bench --no-default-features \
  --features lets-be-rational-validation \
  --bench black
```

Criterion reports are written to `target/criterion/`. Open
`target/criterion/report/index.html` in a browser for detailed charts.

## CI integration

The workflow `.github/workflows/benchmark.yml` runs a subset of benchmarks on:

- pushes to `main` touching:
  - `src/**`, `benches/**`, `Cargo.*`,
  - `.github/workflows/benchmark.yml`,
- pull requests to `main` with the same path filters.

It uses `boa-dev/criterion-compare-action@v3` on `ubuntu-22.04` to:

- execute the configured `cargo bench` command,
- compare current results with the base branch,
- post a summary comment on the PR showing relative changes.

The workflow is intentionally conservative: it does not publish GitHub Pages
or manipulate branches, and runs with minimal permissions (`pull-requests: write`).

## Adding new benchmarks

To add a new benchmark:

1. Create a file under `benches/`:

   ```rust
   // benches/my_feature.rs
   use criterion::{criterion_group, criterion_main, Criterion};

   fn benchmark_my_feature(c: &mut Criterion) {
       c.bench_function("my_feature", |b| {
           b.iter(|| {
               // benchmarked code here
           })
       });
   }

   criterion_group!(benches, benchmark_my_feature);
   criterion_main!(benches);
   ```

2. Register it in `Cargo.toml`:

   ```toml
   [[bench]]
   name = "my_feature"
   path = "benches/my_feature.rs"
   harness = false
   ```

3. Optionally update `.github/workflows/benchmark.yml` if you want CI to
   include or highlight the new suite.

Keep benchmarks deterministic where possible (fixed seeds or static grids of
inputs) so that comparisons across commits are meaningful. Baseline values for
important paths (pricing, Greeks, IV) should be recorded or updated in
`docs/baseline.md` when making deliberate performance changes.
