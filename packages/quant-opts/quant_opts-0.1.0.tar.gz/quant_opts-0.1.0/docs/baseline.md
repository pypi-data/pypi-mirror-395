# quant-opts – Baseline

## Numerical baselines

All values below are computed with the current `BlackScholes` model and
the parameters shown. They serve as fixed numerical references when
validating future changes.

### Pricing (`BlackScholes::price` / `BlackScholes::rational_price`)

- `call_otm`  
  - `price` = `0.0376589547`  
  - `rational_price` = `0.0376589547`
- `call_itm`  
  - `price` = `9.9913356994`  
  - `rational_price` = `9.9913356994`
- `put_otm`  
  - `price` = `0.0186767623`  
  - `rational_price` = `0.0186767623`
- `put_itm`  
  - `price` = `10.0103178918`  
  - `rational_price` = `10.0103178918`
- `branch_cut` (`calc_rational_price`)  
  - `rational_price` = `16.6722548339`

### Implied volatility (`BlackScholes::rational_implied_vol`)

- `put_otm`  
  - `true_sigma` = `0.25`  
  - `rational_iv` = `0.25`
- `call_itm`  
  - `true_sigma` = `0.15`  
  - `rational_iv` = `0.15`
- `put_itm`  
  - `true_sigma` = `0.18`  
  - `rational_iv` = `0.18`
- `call_atm`  
  - `true_sigma` = `0.20`  
  - `rational_iv` = `0.20`
- `put_atm`  
  - `true_sigma` = `0.22`  
  - `rational_iv` = `0.22`

## Performance baselines

The values below were measured in `release` mode on 1,000,000 iterations
(single-threaded), using the current API at the time of writing. They
serve as the starting baseline for future performance work.

- `BlackScholes::price`  
  - ~`31.9 ns/op`
- `BlackScholes::rational_price`  
  - ~`40.6 ns/op`
- `BlackScholes::rational_implied_vol`  
  - ~`280.4 ns/op`

These numbers are approximate and hardware/compiler dependent, but
serve as a sanity check when comparing future changes to the model-based API
(`BlackScholes::price`, `BlackScholes::rational_price`,
`BlackScholes::rational_implied_vol`).

### Greeks (current Black–Scholes API)

Measured with:

```bash
cargo bench --no-default-features --bench greeks
```

On the refactored `BlackScholes` model (single-threaded):

- `BlackScholes::delta`  
  - ~`0.35 ns/op`
- `BlackScholes::gamma`  
  - ~`0.40 ns/op`
- `BlackScholes::theta`  
  - ~`15.55 ns/op`
- `BlackScholes::vega`  
  - ~`0.40 ns/op`
- `BlackScholes::rho`  
  - ~`0.35 ns/op`
- `BlackScholes::greeks` (all first-order greeks at once)  
  - ~`18.65 ns/op`

### Current Black–Scholes API (quant-opts)

Measured with the refactored model-based API (`BlackScholes` +
`VanillaOption`/`MarketData`).

#### Single-option pricing

Micro-benchmark (Criterion):

```bash
cargo bench --no-default-features --bench pricing
```

- `BlackScholes::price`  
  - ~`0.32 ns/op` (single European option, fixed parameters)

Single-option sweeps across several moneyness/maturity configurations
(`cargo bench --no-default-features --bench single_option`) give:

- `BlackScholes::price`  
  - ~`8.3–16.5 ns/op` depending on scenario
- `BlackScholes::rational_price`  
  - ~`37.4–41.2 ns/op`

#### Implied volatility

Criterion benchmark:

```bash
cargo bench --no-default-features --bench implied_volatility
```

- `BlackScholes::rational_implied_vol`  
  - ~`95.5 ns/op` for a representative call option

Single-option IV sweeps (`cargo bench --no-default-features --bench single_iv`),
ATM call/put, show:

- `BlackScholes::implied_vol` (high precision, `tolerance = 1e-5`)  
  - ~`182–187 ns/op`
- `BlackScholes::implied_vol` (low precision, `tolerance = 1e-3`)  
  - ~`121–123 ns/op`
- `BlackScholes::rational_implied_vol`  
  - ~`279–285 ns/op`

The exact numbers depend on the specific inputs and hardware, but both
paths show consistent behaviour with the numerical baselines above and
the tests in `tests/`.

#### Single-option Greeks

Single-option Greeks sweeps (`cargo bench --no-default-features --bench single_greeks`)
for ATM calls (short/medium/long maturities) give approximate ranges:

- `BlackScholes::delta`  
  - ~`22–39 ns/op`
- `BlackScholes::gamma`  
  - ~`11–13 ns/op`
- `BlackScholes::theta`  
  - ~`48–77 ns/op`
- `BlackScholes::vega`  
  - ~`11–15 ns/op`
- `BlackScholes::rho`  
  - ~`27–42 ns/op`

Second-order Greeks:

- `BlackScholes::vanna`  
  - ~`21–24 ns/op`
- `BlackScholes::charm`  
  - ~`50 ns/op`
- `BlackScholes::vomma`  
  - ~`23 ns/op`
- `BlackScholes::speed`  
  - ~`24 ns/op`
- `BlackScholes::zomma`  
  - ~`23–24 ns/op`

### Batch and throughput baselines

These benchmarks use synthetic batches of options (see `benches/common`)
and are meant to characterise throughput, not precise per-option timing.

#### Batch pricing

`cargo bench --no-default-features --bench batch_pricing`

For sequential pricing (`BlackScholes::price`):

- batch size 10 (tiny)  
  - ~`0.38 µs` total per batch
- batch size 100 (small)  
  - ~`3.53 µs` total per batch
- batch size 1,000 (medium)  
  - ~`42.5 µs` total per batch

SoA placeholder variant is currently slightly slower (e.g. ~`46.1 µs`
for 1,000 options).

#### Batch Greeks

`cargo bench --no-default-features --bench batch_greeks`

For batch size 10 (tiny):

- `delta`  
  - ~`337 ns` per batch
- `gamma` / `vega`  
  - ~`165–186 ns` per batch
- `all_greeks`  
  - ~`1.45 µs` per batch

For batch size 100 (small):

- `delta`  
  - ~`2.99 µs` per batch
- `gamma`  
  - ~`1.41 µs` per batch
- `vega`  
  - ~`1.37–1.50 µs` per batch
- `all_greeks`  
  - ~`14.2 µs` per batch

#### Throughput (option pricing)

`cargo bench --no-default-features --bench throughput`

For medium batch size:

- `price`  
  - ~`44.4 µs` per batch  
  - throughput ~`22.5 M options/s`
- `rational_price`  
  - ~`55.8 µs` per batch  
  - throughput ~`17.9 M options/s`
- `delta`  
  - ~`42.4 µs` per batch  
  - throughput ~`23.6 M options/s`

For large batch size:

- `price`  
  - ~`643 µs` per batch (~`15.6 M options/s`)
- `rational_price`  
  - ~`704 µs` per batch (~`14.2 M options/s`)
- `delta`  
  - ~`617 µs` per batch (~`16.2 M options/s`)

#### Batch size scaling

`cargo bench --no-default-features --bench scaling`

For `BlackScholes::price`, throughput vs batch size:

- batch size 10  
  - ~`0.40 µs` per batch, ~`25.1 M options/s`
- batch size 100  
  - ~`3.50 µs` per batch, ~`28.5 M options/s`
- batch size 1,000  
  - ~`40.0 µs` per batch, ~`25.0 M options/s`
- batch size 10,000  
  - ~`624 µs` per batch, ~`16.0 M options/s`
- batch size 100,000  
  - ~`6.37 ms` per batch, ~`15.7 M options/s`

`cargo bench --no-default-features --bench batch_size_study` provides
similar scaling data for pricing and Greeks across batch sizes 10–10,000
and serves as a secondary reference for throughput behaviour.
