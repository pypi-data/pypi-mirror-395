use std::{hint::black_box, time::Duration};

use criterion::{BenchmarkId, Criterion, Throughput, criterion_group, criterion_main};
use quant_opts::BlackScholes;
use rand::rng;

#[path = "../common/mod.rs"]
mod common;
use common::{BatchSize, BenchCase, generate_random_inputs};

fn bench_batch_size_scaling(c: &mut Criterion) {
    let mut group = c.benchmark_group("Batch Size Scaling");

    group.measurement_time(Duration::from_secs(5));
    group.warm_up_time(Duration::from_millis(500));

    let batch_sizes = [
        10,     // Tiny
        100,    // Small
        1_000,  // Medium
        5_000,  // Medium-large
        10_000, // Large (if time permits)
    ];

    let mut rng = rng();

    for size in batch_sizes {
        let inputs: Vec<BenchCase> = generate_random_inputs(size, &mut rng);

        group.throughput(Throughput::Elements(size as u64));

        group.bench_with_input(
            BenchmarkId::new("standard_price", size),
            &inputs,
            |b, inputs: &Vec<BenchCase>| {
                b.iter(|| {
                    let mut results = Vec::with_capacity(inputs.len());
                    for input in black_box(inputs) {
                        results.push(
                            BlackScholes::price(&input.option, &input.market, input.vol).unwrap(),
                        );
                    }
                    black_box(results)
                })
            },
        );

        group.bench_with_input(
            BenchmarkId::new("rational_price", size),
            &inputs,
            |b, inputs: &Vec<BenchCase>| {
                b.iter(|| {
                    let mut results = Vec::with_capacity(inputs.len());
                    for input in black_box(inputs) {
                        results.push(
                            BlackScholes::rational_price(&input.option, &input.market, input.vol)
                                .unwrap(),
                        );
                    }
                    black_box(results)
                })
            },
        );

        group.bench_with_input(
            BenchmarkId::new("delta", size),
            &inputs,
            |b, inputs: &Vec<BenchCase>| {
                b.iter(|| {
                    let mut results = Vec::with_capacity(inputs.len());
                    for input in black_box(inputs) {
                        results.push(
                            BlackScholes::delta(&input.option, &input.market, input.vol).unwrap(),
                        );
                    }
                    black_box(results)
                })
            },
        );

        group.bench_with_input(
            BenchmarkId::new("gamma", size),
            &inputs,
            |b, inputs: &Vec<BenchCase>| {
                b.iter(|| {
                    let mut results = Vec::with_capacity(inputs.len());
                    for input in black_box(inputs) {
                        results.push(
                            BlackScholes::gamma(&input.option, &input.market, input.vol).unwrap(),
                        );
                    }
                    black_box(results)
                })
            },
        );

        group.bench_with_input(
            BenchmarkId::new("all_greeks", size),
            &inputs,
            |b, inputs: &Vec<BenchCase>| {
                b.iter(|| {
                    let mut results = Vec::with_capacity(inputs.len());
                    for input in black_box(inputs) {
                        results.push(
                            BlackScholes::greeks(&input.option, &input.market, input.vol).unwrap(),
                        );
                    }
                    black_box(results)
                })
            },
        );
    }

    group.finish();
}

criterion_group!(benches, bench_batch_size_scaling);
criterion_main!(benches);
