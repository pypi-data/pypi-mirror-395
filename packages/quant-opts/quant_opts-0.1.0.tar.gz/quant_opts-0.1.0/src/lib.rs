//! High-performance Black–Scholes–Merton primitives for pricing European vanilla options,
//! computing Greeks, and implied volatility.
//!
//! ## Quick start
//! ```
//! use quant_opts::{BlackScholes, MarketData, OptionStyle, OptionType, VanillaModel, VanillaOption};
//!
//! // Define an option and market snapshot
//! let option = VanillaOption::new(OptionStyle::European, OptionType::Call, 100.0, 30.0 / 365.25);
//! let market = MarketData::new(105.0, 0.03, 0.01);
//! let sigma = 0.22;
//!
//! // Static API
//! let price = BlackScholes::price(&option, &market, sigma).unwrap();
//! let greeks = BlackScholes::greeks(&option, &market, sigma).unwrap();
//!
//! // Trait-based API
//! let model = BlackScholes::new(sigma);
//! let price_via_trait = model.price(&option, &market).unwrap();
//! assert!((price - price_via_trait).abs() < 1e-12);
//! ```
//!
//! More runnable examples live under `examples/`:
//! - `cargo run --example pricing_and_greeks`
//! - `cargo run --example implied_vol`
//!
//! Benchmark commands are documented in `README.md` and `docs/BENCHMARKING.md`.

pub mod core;
pub mod models;

pub mod lets_be_rational;

pub use core::{MarketData, OptionStyle, OptionType, VanillaOption};

pub use models::{VanillaModel, black_scholes::BlackScholes};

#[cfg(feature = "wrappers")]
pub mod wrappers;

#[cfg(target_arch = "wasm32")]
mod wasm_api {
    use wasm_bindgen::prelude::*;

    use crate::{BlackScholes, MarketData, OptionStyle, OptionType, VanillaOption};

    /// Price a European call via Black–Scholes (WASM binding).
    #[wasm_bindgen]
    pub fn price_call_bs(
        spot: f64,
        strike: f64,
        maturity_years: f64,
        rate: f64,
        dividend_yield: f64,
        vol: f64,
    ) -> Result<f64, JsValue> {
        let opt = VanillaOption::new(
            OptionStyle::European,
            OptionType::Call,
            strike,
            maturity_years,
        );
        let mkt = MarketData::new(spot, rate, dividend_yield);
        BlackScholes::price(&opt, &mkt, vol).map_err(|e| JsValue::from_str(&e))
    }

    /// Dividend-adjusted rational implied volatility for a call.
    #[wasm_bindgen]
    pub fn rational_iv_bs(
        observed_price: f64,
        spot: f64,
        strike: f64,
        maturity_years: f64,
        rate: f64,
        dividend_yield: f64,
    ) -> Result<f64, JsValue> {
        let opt = VanillaOption::new(
            OptionStyle::European,
            OptionType::Call,
            strike,
            maturity_years,
        );
        let mkt = MarketData::new(spot, rate, dividend_yield);
        BlackScholes::rational_implied_vol(observed_price, &opt, &mkt)
            .map_err(|e| JsValue::from_str(&e))
    }
}

pub(crate) const DAYS_PER_YEAR: f64 = 365.25;

pub(crate) const A: f64 = 4.626_275_3e-1;
pub(crate) const B: f64 = -1.168_519_2e-2;
pub(crate) const C: f64 = 9.635_418_5e-4;
pub(crate) const D: f64 = 7.535_022_5e-5;
pub(crate) const _E: f64 = 1.424_516_45e-5;
pub(crate) const F: f64 = -2.102_376_9e-5;
