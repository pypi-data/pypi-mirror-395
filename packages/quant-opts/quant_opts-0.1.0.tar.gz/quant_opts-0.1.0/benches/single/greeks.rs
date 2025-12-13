use std::{hint::black_box, time::Duration};

use criterion::{BenchmarkId, Criterion, criterion_group, criterion_main};
use quant_opts::{BlackScholes, OptionType};

#[path = "../common/mod.rs"]
mod common;
use common::{BenchCase, Moneyness, TimeToMaturity, VolatilityLevel, generate_standard_inputs};

fn bench_greeks(c: &mut Criterion) {
    let mut group = c.benchmark_group("Single Option Greeks");

    // Configure the benchmark group
    group.warm_up_time(Duration::from_millis(500));
    group.measurement_time(Duration::from_secs(2));

    // We'll test ATM call options with medium volatility at different maturities
    let configurations = [
        ("short_term", TimeToMaturity::ShortTerm),
        ("medium_term", TimeToMaturity::MediumTerm),
        ("long_term", TimeToMaturity::LongTerm),
    ];

    // First-order Greeks (most frequently used)
    for (name, maturity) in configurations.iter() {
        let case: BenchCase = generate_standard_inputs(
            OptionType::Call,
            Moneyness::AtTheMoney,
            *maturity,
            VolatilityLevel::Medium,
        );

        // Delta
        group.bench_with_input(
            BenchmarkId::new("delta", name),
            &case,
            |b, case: &BenchCase| {
                b.iter(|| {
                    black_box(BlackScholes::delta(&case.option, &case.market, case.vol).unwrap())
                })
            },
        );

        // Gamma
        group.bench_with_input(
            BenchmarkId::new("gamma", name),
            &case,
            |b, case: &BenchCase| {
                b.iter(|| {
                    black_box(BlackScholes::gamma(&case.option, &case.market, case.vol).unwrap())
                })
            },
        );

        // Theta
        group.bench_with_input(
            BenchmarkId::new("theta", name),
            &case,
            |b, case: &BenchCase| {
                b.iter(|| {
                    black_box(BlackScholes::theta(&case.option, &case.market, case.vol).unwrap())
                })
            },
        );

        // Vega
        group.bench_with_input(
            BenchmarkId::new("vega", name),
            &case,
            |b, case: &BenchCase| {
                b.iter(|| {
                    black_box(BlackScholes::vega(&case.option, &case.market, case.vol).unwrap())
                })
            },
        );

        // Rho
        group.bench_with_input(
            BenchmarkId::new("rho", name),
            &case,
            |b, case: &BenchCase| {
                b.iter(|| {
                    black_box(BlackScholes::rho(&case.option, &case.market, case.vol).unwrap())
                })
            },
        );
    }

    group.finish();
}

fn bench_all_greeks(c: &mut Criterion) {
    let mut group = c.benchmark_group("All Greeks Calculation");

    // Configure the benchmark group
    group.warm_up_time(Duration::from_millis(500));
    group.measurement_time(Duration::from_secs(2));

    // Compare individual vs. all_greeks calculation for different option types
    let call_atm: BenchCase = generate_standard_inputs(
        OptionType::Call,
        Moneyness::AtTheMoney,
        TimeToMaturity::MediumTerm,
        VolatilityLevel::Medium,
    );

    let put_atm: BenchCase = generate_standard_inputs(
        OptionType::Put,
        Moneyness::AtTheMoney,
        TimeToMaturity::MediumTerm,
        VolatilityLevel::Medium,
    );

    // Benchmark each individual Greek calculation separately (sum of times)
    for (name, case) in [("call", call_atm), ("put", put_atm)] {
        group.bench_with_input(
            BenchmarkId::new("individual", name),
            &case,
            |b, case: &BenchCase| {
                b.iter(|| {
                    let delta = black_box(
                        BlackScholes::delta(&case.option, &case.market, case.vol).unwrap(),
                    );
                    let gamma = black_box(
                        BlackScholes::gamma(&case.option, &case.market, case.vol).unwrap(),
                    );
                    let theta = black_box(
                        BlackScholes::theta(&case.option, &case.market, case.vol).unwrap(),
                    );
                    let vega = black_box(
                        BlackScholes::vega(&case.option, &case.market, case.vol).unwrap(),
                    );
                    let rho =
                        black_box(BlackScholes::rho(&case.option, &case.market, case.vol).unwrap());
                    black_box((delta, gamma, theta, vega, rho))
                })
            },
        );

        // Benchmark all_greeks calculation (calculates all at once)
        group.bench_with_input(
            BenchmarkId::new("all_greeks", name),
            &case,
            |b, case: &BenchCase| {
                b.iter(|| {
                    let all = black_box(
                        BlackScholes::greeks(&case.option, &case.market, case.vol).unwrap(),
                    );
                    black_box(all)
                })
            },
        );
    }

    group.finish();
}

// Second-order Greeks benchmark
fn bench_second_order_greeks(c: &mut Criterion) {
    let mut group = c.benchmark_group("Second Order Greeks");

    // Configure the benchmark group
    group.warm_up_time(Duration::from_millis(500));
    group.measurement_time(Duration::from_secs(2));

    let case: BenchCase = generate_standard_inputs(
        OptionType::Call,
        Moneyness::AtTheMoney,
        TimeToMaturity::MediumTerm,
        VolatilityLevel::Medium,
    );

    group.bench_function("vanna", |b| {
        b.iter(|| black_box(BlackScholes::vanna(&case.option, &case.market, case.vol).unwrap()))
    });

    group.bench_function("charm", |b| {
        b.iter(|| black_box(BlackScholes::charm(&case.option, &case.market, case.vol).unwrap()))
    });

    group.bench_function("vomma", |b| {
        b.iter(|| black_box(BlackScholes::vomma(&case.option, &case.market, case.vol).unwrap()))
    });

    group.bench_function("speed", |b| {
        b.iter(|| black_box(BlackScholes::speed(&case.option, &case.market, case.vol).unwrap()))
    });

    group.bench_function("zomma", |b| {
        b.iter(|| black_box(BlackScholes::zomma(&case.option, &case.market, case.vol).unwrap()))
    });

    group.finish();
}

criterion_group!(
    benches,
    bench_greeks,
    bench_all_greeks,
    bench_second_order_greeks
);
criterion_main!(benches);
