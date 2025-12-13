use std::hint::black_box;

use criterion::{Criterion, criterion_group, criterion_main};
use quant_opts::{BlackScholes, MarketData, OptionStyle, OptionType, VanillaOption};

const OPTION: VanillaOption = VanillaOption {
    style: OptionStyle::European,
    kind: OptionType::Call,
    strike: 55.0,
    maturity: 25.0 / 360.0,
};

const MARKET: MarketData = MarketData {
    spot: 51.03,
    rate: 0.0,
    dividend_yield: 0.0,
};

const SIGMA: f64 = 0.5;

fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("calc_price", |b| {
        b.iter(|| {
            let result = BlackScholes::price(&OPTION, &MARKET, SIGMA)
                .map_err(|e| black_box(e))
                .unwrap();
            black_box(result + 1.0);
        })
    });
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
