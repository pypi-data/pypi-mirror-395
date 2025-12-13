use std::hint::black_box;

use criterion::{Criterion, criterion_group, criterion_main};
use quant_opts::{BlackScholes, MarketData, OptionStyle, OptionType, VanillaOption};

const OPTION: VanillaOption = VanillaOption {
    style: OptionStyle::European,
    kind: OptionType::Call,
    strike: 55.0,
    maturity: 45.0 / 360.0,
};

const MARKET: MarketData = MarketData {
    spot: 51.03,
    rate: 0.0,
    dividend_yield: 0.0,
};

const MARKET_PRICE: f64 = 1.24;

fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("calc_rational_iv", |b| {
        b.iter(|| {
            black_box(BlackScholes::rational_implied_vol(MARKET_PRICE, &OPTION, &MARKET).unwrap())
        })
    });
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
