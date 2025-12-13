//! Micro-benchmarks for internal "Let's Be Rational" Black expansions.
//!
//! This uses Criterion to measure the performance of:
//! - `asymptotic_expansion_of_normalised_black_call`,
//! - `small_t_expansion_of_normalised_black_call`,
//! for a handful of representative (h, t) pairs.

use std::hint::black_box;

use criterion::{Criterion, criterion_group, criterion_main};
use quant_opts::lets_be_rational::{
    asymptotic_expansion_of_normalised_black_call, small_t_expansion_of_normalised_black_call,
};

fn benchmark_asymptotic_expansion_of_normalised_black_call(c: &mut Criterion) {
    let test_values = vec![
        (-12.0, 0.1),
        (-20.0, 0.05),
        (-15.0, 0.2),
        (-10.0, 0.05),
        (-30.0, 0.01),
    ];

    for (h, t) in test_values {
        c.bench_function(
            &format!("asymptotic_expansion_of_normalised_black_call h={h}, t={t}"),
            |b| {
                b.iter(|| {
                    // Ignore the error; benchmark the happy path where inputs
                    // satisfy the asymptotic expansion conditions.
                    let _ =
                        asymptotic_expansion_of_normalised_black_call(black_box(h), black_box(t));
                })
            },
        );
    }
}

fn benchmark_small_t_expansion(c: &mut Criterion) {
    let test_values = vec![
        (0.1, 0.1),
        (0.05, 0.05),
        (0.15, 0.15),
        (0.2, 0.2),
        (0.0, 0.0),
    ];

    for (h, t) in test_values {
        c.bench_function(
            &format!("small_t_expansion_of_normalised_black_call h={h}, t={t}"),
            |b| {
                b.iter(|| {
                    let _ = small_t_expansion_of_normalised_black_call(black_box(h), black_box(t));
                })
            },
        );
    }
}

criterion_group!(
    benches,
    benchmark_asymptotic_expansion_of_normalised_black_call,
    benchmark_small_t_expansion
);
criterion_main!(benches);
