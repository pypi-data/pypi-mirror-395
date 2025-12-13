use std::{hint::black_box, time::Duration};

use criterion::{BenchmarkId, Criterion, criterion_group, criterion_main};
use quant_opts::{BlackScholes, OptionType};

#[path = "../common/mod.rs"]
mod common;
use common::{BenchCase, Moneyness, TimeToMaturity, VolatilityLevel, generate_standard_inputs};

fn bench_implied_volatility(c: &mut Criterion) {
    let mut group = c.benchmark_group("Implied Volatility");

    // Configure the benchmark group
    group.warm_up_time(Duration::from_millis(500));
    group.measurement_time(Duration::from_secs(3)); // IV calculation takes longer

    // Different price scenarios to test IV calculation
    // We'll only use ATM options to avoid convergence issues
    let configurations = [
        ("call_atm", OptionType::Call, Moneyness::AtTheMoney),
        ("put_atm", OptionType::Put, Moneyness::AtTheMoney),
    ];

    // Generate inputs for benchmarking IV calculation
    for (name, option_type, moneyness) in configurations {
        let case: BenchCase = generate_standard_inputs(
            option_type,
            moneyness,
            TimeToMaturity::MediumTerm,
            VolatilityLevel::Medium,
        );

        let sigma = case.vol;
        let price = BlackScholes::price(&case.option, &case.market, sigma).unwrap();

        // Bench standard IV calculation with different tolerances
        for (tolerance_name, tolerance) in [
            ("high_precision", 0.00001),
            ("medium_precision", 0.0001),
            ("low_precision", 0.001),
        ] {
            group.bench_with_input(
                BenchmarkId::new(format!("calc_iv_{}", tolerance_name), name),
                &tolerance,
                |b, &tolerance: &f64| {
                    b.iter(|| {
                        let iv = black_box(
                            BlackScholes::implied_vol(price, &case.option, &case.market, tolerance)
                                .unwrap(),
                        );
                        black_box(iv);
                    })
                },
            );
        }

        // Bench rational IV calculation
        group.bench_with_input(
            BenchmarkId::new("calc_rational_iv", name),
            &price,
            |b, &price| {
                b.iter(|| {
                    let iv = black_box(
                        BlackScholes::rational_implied_vol(price, &case.option, &case.market)
                            .unwrap(),
                    );
                    black_box(iv);
                })
            },
        );

        // Compare to known result for verification
        let iv_standard =
            BlackScholes::implied_vol(price, &case.option, &case.market, 0.00001).unwrap();
        let iv_rational =
            BlackScholes::rational_implied_vol(price, &case.option, &case.market).unwrap();

        println!(
            "Verification for {}: Original sigma = {:.6}, IV standard = {:.6}, IV rational = {:.6}, Diff = {:.6}",
            name,
            sigma,
            iv_standard,
            iv_rational,
            (sigma - iv_standard).abs()
        );
    }

    group.finish();
}

criterion_group!(benches, bench_implied_volatility);
criterion_main!(benches);
