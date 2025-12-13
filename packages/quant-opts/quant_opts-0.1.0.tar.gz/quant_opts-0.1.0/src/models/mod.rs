//! Pricing models available in `quant-opts`.
//!
//! For now this module provides a Black–Scholes–Merton implementation
//! for vanilla options. Additional models (e.g. SABR) can be added
//! alongside it while reusing the core domain types.
//!
//! The [`VanillaModel`] trait defines a generic interface for
//! vanilla option models. Concrete models like [`black_scholes::BlackScholes`]
//! implement this trait so callers can write code generic over the model.

use crate::core::{Greeks, MarketData, VanillaOption};

/// Core abstraction for a model that can price vanilla options.
///
/// This trait is intentionally conservative in scope for now:
/// - it operates only on the core domain types,
/// - it does not prescribe any particular volatility parametrisation,
/// - it exposes fallible operations via `Result` so callers can
///   handle invalid inputs explicitly.
pub trait VanillaModel {
    /// Price a vanilla option under this model.
    fn price(&self, opt: &VanillaOption, mkt: &MarketData) -> Result<f64, String>;

    /// Compute a set of Greeks for a vanilla option.
    fn greeks(&self, opt: &VanillaOption, mkt: &MarketData) -> Result<Greeks, String>;

    /// Compute implied volatility such that the model price matches `target_price`.
    fn implied_vol(
        &self,
        target_price: f64,
        opt: &VanillaOption,
        mkt: &MarketData,
    ) -> Result<f64, String>;
}

pub mod black_scholes;
