use super::{
    BlackScholes,
    math::{nd1_nd2, nprimed1},
};
use crate::{
    DAYS_PER_YEAR, OptionType,
    core::{Greeks, MarketData, VanillaOption},
};

impl BlackScholes {
    /// Compute the Black–Scholes delta.
    pub fn delta(option: &VanillaOption, market: &MarketData, vol: f64) -> Result<f64, String> {
        let (nd1, _) = nd1_nd2(option, market, vol)?;
        let q = market.dividend_yield;
        let t = option.maturity;

        let sign = match option.kind {
            OptionType::Call => 1.0,
            OptionType::Put => -1.0,
        };

        let delta = sign * (-q * t).exp() * nd1;
        Ok(delta)
    }

    /// Compute the Black–Scholes gamma.
    pub fn gamma(option: &VanillaOption, market: &MarketData, vol: f64) -> Result<f64, String> {
        let sigma = vol;
        let nprimed1 = nprimed1(option, market, sigma)?;

        let s = market.spot;
        let q = market.dividend_yield;
        let t = option.maturity;

        let gamma = (-q * t).exp() * nprimed1 / (s * sigma * t.sqrt());
        Ok(gamma)
    }

    /// Compute the Black–Scholes theta (per day).
    pub fn theta(option: &VanillaOption, market: &MarketData, vol: f64) -> Result<f64, String> {
        let sigma = vol;
        let nprimed1 = nprimed1(option, market, sigma)?;
        let (nd1, nd2) = nd1_nd2(option, market, sigma)?;

        let s = market.spot;
        let k = option.strike;
        let r = market.rate;
        let q = market.dividend_yield;
        let t = option.maturity;

        let sign = match option.kind {
            OptionType::Call => 1.0,
            OptionType::Put => -1.0,
        };

        let term1 = -(s * sigma * (-q * t).exp() * nprimed1 / (2.0 * t.sqrt()));
        let term2 = -r * k * (-r * t).exp() * nd2 * sign;
        let term3 = q * s * (-q * t).exp() * nd1 * sign;

        let theta = (term1 + term2 + term3) / DAYS_PER_YEAR;
        Ok(theta)
    }

    /// Compute the Black–Scholes vega.
    pub fn vega(option: &VanillaOption, market: &MarketData, vol: f64) -> Result<f64, String> {
        let nprimed1 = nprimed1(option, market, vol)?;

        let s = market.spot;
        let q = market.dividend_yield;
        let t = option.maturity;

        let vega = 0.01 * s * (-q * t).exp() * t.sqrt() * nprimed1;
        Ok(vega)
    }

    /// Compute the Black–Scholes rho.
    pub fn rho(option: &VanillaOption, market: &MarketData, vol: f64) -> Result<f64, String> {
        let (_, nd2) = nd1_nd2(option, market, vol)?;

        let k = option.strike;
        let r = market.rate;
        let t = option.maturity;

        let sign = match option.kind {
            OptionType::Call => 1.0,
            OptionType::Put => -1.0,
        };

        let rho = sign * k * t * (-r * t).exp() * nd2 / 100.0;
        Ok(rho)
    }

    /// Compute a full set of Greeks using the core `Greeks` struct.
    ///
    /// This mirrors the existing Greeks implementation but returns a structured
    /// value instead of a map.
    pub fn greeks(option: &VanillaOption, market: &MarketData, vol: f64) -> Result<Greeks, String> {
        let delta = Self::delta(option, market, vol)?;
        let gamma = Self::gamma(option, market, vol)?;
        let theta = Self::theta(option, market, vol)?;
        let vega = Self::vega(option, market, vol)?;
        let rho = Self::rho(option, market, vol)?;

        // Higher-order Greeks are not yet re-expressed here; they can
        // be added as needed by porting the formulas from the original
        // implementation.
        Ok(Greeks {
            delta,
            gamma,
            theta,
            vega,
            rho,
            ..Greeks::default()
        })
    }
}
