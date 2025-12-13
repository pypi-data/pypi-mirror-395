use crate::{
    OptionType,
    core::{MarketData, VanillaOption},
    lets_be_rational::normal_distribution::{standard_normal_cdf, standard_normal_pdf},
};

pub(super) fn d1_d2(
    option: &VanillaOption,
    market: &MarketData,
    sigma: f64,
) -> Result<(f64, f64), String> {
    if !sigma.is_finite() {
        return Err("Volatility must be finite".to_string());
    }

    let s = market.spot;
    let k = option.strike;
    let r = market.rate;
    let q = market.dividend_yield;
    let t = option.maturity;

    let part1 = (s / k).ln();
    if part1.is_infinite() {
        return Err("Log from s/k is infinity".to_string());
    }

    if t == 0.0 {
        return Err("Time to maturity is 0".to_string());
    }

    let part2 = (r - q + sigma.powi(2) / 2.0) * t;
    let num_d1 = part1 + part2;
    let den = sigma * t.sqrt();

    let d1 = num_d1 / den;
    let d2 = d1 - den;

    Ok((d1, d2))
}

pub(super) fn nd1_nd2(
    option: &VanillaOption,
    market: &MarketData,
    sigma: f64,
) -> Result<(f64, f64), String> {
    let (d1, d2) = d1_d2(option, market, sigma)?;

    let (nd1, nd2) = match option.kind {
        OptionType::Call => (standard_normal_cdf(d1), standard_normal_cdf(d2)),
        OptionType::Put => (standard_normal_cdf(-d1), standard_normal_cdf(-d2)),
    };

    Ok((nd1, nd2))
}

pub(super) fn nprimed1(
    option: &VanillaOption,
    market: &MarketData,
    sigma: f64,
) -> Result<f64, String> {
    let (d1, _) = d1_d2(option, market, sigma)?;
    Ok(standard_normal_pdf(d1))
}
