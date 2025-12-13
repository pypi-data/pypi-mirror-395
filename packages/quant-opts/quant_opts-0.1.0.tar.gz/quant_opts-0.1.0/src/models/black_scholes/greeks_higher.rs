use super::{
    BlackScholes,
    math::{d1_d2, nd1_nd2, nprimed1},
};
use crate::{
    OptionType,
    core::{MarketData, VanillaOption},
};

impl BlackScholes {
    /// Vanna: sensitivity of delta with respect to volatility.
    pub fn vanna(option: &VanillaOption, market: &MarketData, vol: f64) -> Result<f64, String> {
        let sigma = vol;
        let nprimed1 = nprimed1(option, market, sigma)?;
        let (_, d2) = d1_d2(option, market, sigma)?;
        let t = option.maturity;
        let q = market.dividend_yield;

        let vanna = d2 * (-q * t).exp() * nprimed1 * -0.01 / sigma;
        Ok(vanna)
    }

    /// Charm: sensitivity of delta with respect to time.
    pub fn charm(option: &VanillaOption, market: &MarketData, vol: f64) -> Result<f64, String> {
        let sigma = vol;
        let nprimed1 = nprimed1(option, market, sigma)?;
        let (nd1, _) = nd1_nd2(option, market, sigma)?;
        let (_, d2) = d1_d2(option, market, sigma)?;

        let t = option.maturity;
        let r = market.rate;
        let q = market.dividend_yield;

        let sign = match option.kind {
            OptionType::Call => 1.0,
            OptionType::Put => -1.0,
        };

        let e_negqt = (-q * t).exp();

        let charm = sign * q * e_negqt * nd1
            - e_negqt * nprimed1 * (2.0 * (r - q) * t - d2 * sigma * t.sqrt())
                / (2.0 * t * sigma * t.sqrt());

        Ok(charm)
    }

    /// Vomma (volga): sensitivity of vega with respect to volatility.
    pub fn vomma(option: &VanillaOption, market: &MarketData, vol: f64) -> Result<f64, String> {
        let sigma = vol;
        let (d1, d2) = d1_d2(option, market, sigma)?;
        let vega = Self::vega(option, market, sigma)?;

        let vomma = vega * (d1 * d2) / sigma;
        Ok(vomma)
    }

    /// Speed: third derivative of price with respect to spot.
    pub fn speed(option: &VanillaOption, market: &MarketData, vol: f64) -> Result<f64, String> {
        let sigma = vol;
        let (d1, _) = d1_d2(option, market, sigma)?;
        let gamma = Self::gamma(option, market, sigma)?;

        let s = market.spot;
        let t = option.maturity;

        let speed = -gamma / s * (d1 / (sigma * t.sqrt()) + 1.0);
        Ok(speed)
    }

    /// Zomma: sensitivity of gamma with respect to volatility.
    pub fn zomma(option: &VanillaOption, market: &MarketData, vol: f64) -> Result<f64, String> {
        let sigma = vol;
        let (d1, d2) = d1_d2(option, market, sigma)?;
        let gamma = Self::gamma(option, market, sigma)?;

        let zomma = gamma * ((d1 * d2 - 1.0) / sigma);
        Ok(zomma)
    }
}
