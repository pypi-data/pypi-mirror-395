use super::{BlackScholes, math::nd1_nd2};
use crate::{
    OptionType,
    core::{MarketData, VanillaOption},
    lets_be_rational::black as black_price,
};

impl BlackScholes {
    /// Calculate the Black–Scholes price of a vanilla option.
    pub fn price(option: &VanillaOption, market: &MarketData, vol: f64) -> Result<f64, String> {
        let (nd1, nd2) = nd1_nd2(option, market, vol)?;

        let s = market.spot;
        let k = option.strike;
        let r = market.rate;
        let q = market.dividend_yield;
        let t = option.maturity;

        let discount_r = (-r * t).exp();
        let discount_q = (-q * t).exp();

        let price = match option.kind {
            OptionType::Call => f64::max(0.0, discount_q * s * nd1 - discount_r * k * nd2),
            OptionType::Put => f64::max(0.0, discount_r * k * nd2 - discount_q * s * nd1),
        };

        Ok(price)
    }

    /// Calculate the Black–Scholes price using the "Let's be rational" implementation.
    pub fn rational_price(
        option: &VanillaOption,
        market: &MarketData,
        vol: f64,
    ) -> Result<f64, String> {
        let s = market.spot;
        let k = option.strike;
        let r = market.rate;
        let q = market.dividend_yield;
        let t = option.maturity;

        // Forward price under Black–Scholes with carry q.
        let forward = s * ((r - q) * t).exp();

        // Price using `black` on the forward and then discount back.
        let undiscounted_price = black_price(forward, k, vol, t, option.kind);

        let price = undiscounted_price * (-r * t).exp();
        Ok(price)
    }
}
