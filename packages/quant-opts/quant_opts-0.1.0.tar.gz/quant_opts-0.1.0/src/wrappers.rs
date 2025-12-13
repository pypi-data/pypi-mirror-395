//! Convenience wrappers around the core Black–Scholes API.
//!
//! These functions are intended for ergonomic use and for FFI bindings,
//! where constructing the core types manually would be noisy. They are
//! thin adapters over:
//! - `VanillaOption` / `MarketData` from `quant_opts::core`, and
//! - the `BlackScholes` model implementation.

use crate::{
    core::{Greeks, MarketData, OptionStyle, OptionType, VanillaOption},
    models::black_scholes::BlackScholes,
};

/// Price a European vanilla option under the Black–Scholes model.
///
/// This is a convenience wrapper around [`BlackScholes::price`]. For more
/// control or non-European styles, construct [`VanillaOption`] and
/// [`MarketData`] directly and call the model API.
pub fn price_eur_vanilla_bs(
    kind: OptionType,
    spot: f64,
    strike: f64,
    maturity: f64,
    rate: f64,
    dividend_yield: f64,
    vol: f64,
) -> Result<f64, String> {
    let option = VanillaOption::new(OptionStyle::European, kind, strike, maturity);
    let market = MarketData::new(spot, rate, dividend_yield);
    BlackScholes::price(&option, &market, vol)
}

/// Compute first-order Greeks for a European vanilla option under Black–Scholes.
///
/// This is a convenience wrapper around [`BlackScholes::greeks`].
pub fn greeks_eur_vanilla_bs(
    kind: OptionType,
    spot: f64,
    strike: f64,
    maturity: f64,
    rate: f64,
    dividend_yield: f64,
    vol: f64,
) -> Result<Greeks, String> {
    let option = VanillaOption::new(OptionStyle::European, kind, strike, maturity);
    let market = MarketData::new(spot, rate, dividend_yield);
    BlackScholes::greeks(&option, &market, vol)
}

/// Compute rational implied volatility for a European vanilla option under Black–Scholes.
///
/// This is a convenience wrapper around
/// [`BlackScholes::rational_implied_vol`], using the observed option
/// price as input.
pub fn rational_iv_eur_vanilla_bs(
    kind: OptionType,
    spot: f64,
    strike: f64,
    maturity: f64,
    rate: f64,
    dividend_yield: f64,
    target_price: f64,
) -> Result<f64, String> {
    let option = VanillaOption::new(OptionStyle::European, kind, strike, maturity);
    let market = MarketData::new(spot, rate, dividend_yield);
    BlackScholes::rational_implied_vol(target_price, &option, &market)
}
