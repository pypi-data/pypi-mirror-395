#![cfg(feature = "wrappers")]

use assert_approx_eq::assert_approx_eq;
use quant_opts::{OptionType, wrappers};

#[test]
fn price_eur_call_bs_matches_core_api() {
    let spot = 100.0;
    let strike = 110.0;
    let maturity = 20.0 / 365.25;
    let rate = 0.05;
    let dividend_yield = 0.05;
    let sigma = 0.2;

    let price = wrappers::price_eur_vanilla_bs(
        OptionType::Call,
        spot,
        strike,
        maturity,
        rate,
        dividend_yield,
        sigma,
    )
    .unwrap();

    // Same expected value as in `tests/test_pricing.rs`
    assert_approx_eq!(price, 0.0376, 0.001);
}
