use std::hint::black_box;

use criterion::{Criterion, criterion_group, criterion_main};
use quant_opts::{BlackScholes, MarketData, OptionStyle, OptionType, VanillaOption};

const OPTION: VanillaOption = VanillaOption {
    style: OptionStyle::European,
    kind: OptionType::Call,
    strike: 55.0,
    maturity: 30.0 / 365.25,
};

const MARKET: MarketData = MarketData {
    spot: 51.03,
    rate: 0.05,
    dividend_yield: 0.02,
};

const SIGMA: f64 = 0.3;

fn criterion_benchmark(c: &mut Criterion) {
    let mut group = c.benchmark_group("Greeks");

    group.bench_function("delta", |b| {
        b.iter(|| black_box(BlackScholes::delta(&OPTION, &MARKET, SIGMA).unwrap()))
    });
    group.bench_function("gamma", |b| {
        b.iter(|| black_box(BlackScholes::gamma(&OPTION, &MARKET, SIGMA).unwrap()))
    });
    group.bench_function("theta", |b| {
        b.iter(|| black_box(BlackScholes::theta(&OPTION, &MARKET, SIGMA).unwrap()))
    });
    group.bench_function("vega", |b| {
        b.iter(|| black_box(BlackScholes::vega(&OPTION, &MARKET, SIGMA).unwrap()))
    });
    group.bench_function("rho", |b| {
        b.iter(|| black_box(BlackScholes::rho(&OPTION, &MARKET, SIGMA).unwrap()))
    });
    group.bench_function("all_greeks", |b| {
        b.iter(|| black_box(BlackScholes::greeks(&OPTION, &MARKET, SIGMA).unwrap()))
    });

    group.finish();
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
