//! Black–Scholes–Merton model implementation for vanilla options.
//!
//! This module provides pricing, Greeks, and implied-volatility solvers
//! expressed in terms of the core domain types:
//! - `VanillaOption` (contract),
//! - `MarketData` (spot, rate, dividend yield).
//!
//! The implementation is split across several submodules to keep files small:
//! - `pricing` – price and rational price,
//! - `greeks_impl` – Greeks calculations,
//! - `iv` – implied volatility solvers,
//! - `math` – internal helpers (d1/d2 and related quantities).

mod greeks_higher;
mod greeks_impl;
mod iv;
mod math;
mod pricing;

use crate::{
    core::{Greeks, MarketData, VanillaOption},
    models::VanillaModel,
};

/// Black–Scholes–Merton model for vanilla options.
///
/// The struct form is used with the [`VanillaModel`] trait, where the
/// volatility is stored in `vol`. For convenience, the existing
/// associated functions such as [`BlackScholes::price`] continue to
/// take volatility explicitly and can be used in a “namespace” style.
#[derive(Debug, Clone, Copy, Default)]
pub struct BlackScholes {
    /// Volatility parameter used by the [`VanillaModel`] interface.
    pub vol: f64,
}

impl BlackScholes {
    /// Construct a Black–Scholes model with the given volatility.
    pub fn new(vol: f64) -> Self {
        Self { vol }
    }
}

impl VanillaModel for BlackScholes {
    fn price(&self, opt: &VanillaOption, mkt: &MarketData) -> Result<f64, String> {
        // Delegate to the existing associated function which already
        // encodes the error semantics for invalid inputs.
        BlackScholes::price(opt, mkt, self.vol)
    }

    fn greeks(&self, opt: &VanillaOption, mkt: &MarketData) -> Result<Greeks, String> {
        BlackScholes::greeks(opt, mkt, self.vol)
    }

    fn implied_vol(
        &self,
        target_price: f64,
        opt: &VanillaOption,
        mkt: &MarketData,
    ) -> Result<f64, String> {
        // Use the rational implied-volatility solver as the default
        // implementation for the trait.
        BlackScholes::rational_implied_vol(target_price, opt, mkt)
    }
}
