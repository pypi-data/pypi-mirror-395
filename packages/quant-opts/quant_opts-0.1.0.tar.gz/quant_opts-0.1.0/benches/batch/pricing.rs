use std::{hint::black_box, time::Duration};

use criterion::{BenchmarkId, Criterion, criterion_group, criterion_main, measurement::WallTime};
use quant_opts::BlackScholes;
use rand::rng;

#[path = "../common/mod.rs"]
mod common;
use common::{BatchSize, BenchCase, InputsSoA, generate_random_inputs, get_sample_config};

// Batch pricing benchmark - this is a placeholder for now
// Later we'll implement optimized batch methods in the library
fn bench_batch_pricing(c: &mut Criterion) {
    let mut group = c.benchmark_group("Batch Option Pricing");

    // Configure the benchmark group
    group.warm_up_time(Duration::from_millis(500));

    let batch_sizes = [
        (BatchSize::Tiny as usize, "tiny"),
        (BatchSize::Small as usize, "small"),
        (BatchSize::Medium as usize, "medium"),
    ];

    let mut rng = rng();

    for &(size, size_name) in batch_sizes.iter() {
        // Adjust sample count and measurement time based on batch size
        let (sample_count, measurement_time) = get_sample_config(size);
        group.sample_size(sample_count);
        group.measurement_time(measurement_time);

        // Generate random inputs for batch processing
        let inputs: Vec<BenchCase> = generate_random_inputs(size, &mut rng);

        // Benchmark naive batch processing (just a loop over inputs)
        group.bench_function(BenchmarkId::new("sequential", size_name), |b| {
            b.iter(|| {
                let mut results = Vec::with_capacity(inputs.len());
                for input in black_box(&inputs) {
                    results.push(
                        BlackScholes::price(&input.option, &input.market, input.vol).unwrap(),
                    );
                }
                black_box(results)
            })
        });

        // Convert to SoA format (will be used for SIMD optimization later)
        let inputs_soa = InputsSoA::from_cases(&inputs);

        // Just a placeholder to show how we'll benchmark SoA version
        // The actual optimized implementation will come in a future task
        group.bench_function(BenchmarkId::new("soa_format", size_name), |b| {
            b.iter(|| {
                let mut results = Vec::with_capacity(inputs_soa.len());
                for i in 0..inputs_soa.len() {
                    let option = quant_opts::VanillaOption {
                        style: quant_opts::OptionStyle::European,
                        kind: inputs_soa.option_types[i],
                        strike: inputs_soa.strikes[i],
                        maturity: inputs_soa.times[i],
                    };
                    let market = quant_opts::MarketData {
                        spot: inputs_soa.spots[i],
                        rate: inputs_soa.rates[i],
                        dividend_yield: inputs_soa.dividends[i],
                    };
                    results.push(
                        BlackScholes::price(&option, &market, inputs_soa.volatilities[i]).unwrap(),
                    );
                }
                black_box(results)
            })
        });
    }

    group.finish();
}

criterion_group!(
    name = benches;
    config = Criterion::default().measurement_time(Duration::from_secs(10));
    targets = bench_batch_pricing
);
criterion_main!(benches);
