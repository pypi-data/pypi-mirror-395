use std::{hint::black_box, time::Duration};

use criterion::{BenchmarkId, Criterion, Throughput, criterion_group, criterion_main};
use quant_opts::BlackScholes;
use rand::rng;

#[path = "../common/mod.rs"]
mod common;
use common::{BatchSize, BenchCase, generate_random_inputs, get_sample_config};

fn bench_throughput(c: &mut Criterion) {
    let mut group = c.benchmark_group("Option Pricing Throughput");

    group.warm_up_time(Duration::from_millis(500));

    let batch_sizes = [
        (BatchSize::Medium as usize, "medium"),
        (BatchSize::Large as usize, "large"),
    ];

    let mut rng = rng();

    for &(size, size_name) in batch_sizes.iter() {
        let (sample_count, measurement_time) = get_sample_config(size);
        group.sample_size(sample_count);
        group.measurement_time(measurement_time);

        let inputs: Vec<BenchCase> = generate_random_inputs(size, &mut rng);

        group.throughput(Throughput::Elements(size as u64));

        group.bench_function(BenchmarkId::new("price", size_name), |b| {
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

        group.bench_function(BenchmarkId::new("rational_price", size_name), |b| {
            b.iter(|| {
                let mut results = Vec::with_capacity(inputs.len());
                for input in black_box(&inputs) {
                    results.push(
                        BlackScholes::rational_price(&input.option, &input.market, input.vol)
                            .unwrap(),
                    );
                }
                black_box(results)
            })
        });

        group.bench_function(BenchmarkId::new("delta", size_name), |b| {
            b.iter(|| {
                let mut results = Vec::with_capacity(inputs.len());
                for input in black_box(&inputs) {
                    results.push(
                        BlackScholes::delta(&input.option, &input.market, input.vol).unwrap(),
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
    targets = bench_throughput
);
criterion_main!(benches);
