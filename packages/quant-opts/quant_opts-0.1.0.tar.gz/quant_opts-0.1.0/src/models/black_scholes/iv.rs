use super::BlackScholes;
use crate::{
    _E, A, B, C, D, F,
    core::{MarketData, VanillaOption},
    lets_be_rational::implied_volatility_from_a_transformed_rational_guess,
};

impl BlackScholes {
    /// Implied volatility using the Corrado–Miller style approximation + Newton–Raphson.
    ///
    /// This corresponds to the original `calc_iv` implementation.
    pub fn implied_vol(
        target_price: f64,
        option: &VanillaOption,
        market: &MarketData,
        tolerance: f64,
    ) -> Result<f64, String> {
        let s = market.spot;
        let k = option.strike;
        let r = market.rate;
        let _q = market.dividend_yield;
        let t = option.maturity;

        let p = target_price;

        let x = k * (-r * t).exp();
        let f_minus_x = s - x;
        let f_plus_x = s + x;
        let one_over_sqrt_t = 1.0 / t.sqrt();

        let x_corr = one_over_sqrt_t * (statrs::consts::SQRT_2PI / f_plus_x);
        let y = p - (s - k) / 2.0
            + ((p - f_minus_x / 2.0).powi(2) - f_minus_x.powi(2) / std::f64::consts::PI).sqrt();

        let mut sigma = one_over_sqrt_t
            * (statrs::consts::SQRT_2PI / f_plus_x)
            * (p - f_minus_x / 2.0
                + ((p - f_minus_x / 2.0).powi(2) - f_minus_x.powi(2) / std::f64::consts::PI)
                    .sqrt())
            + A
            + B / x_corr
            + C * y
            + D / x_corr.powi(2)
            + _E * y.powi(2)
            + F * y / x_corr;

        if !sigma.is_finite() {
            return Err("Failed to converge".to_string());
        }

        let mut diff: f64 = 100.0;

        while diff.abs() > tolerance {
            let price = BlackScholes::price(option, market, sigma)?;
            diff = price - p;
            let vega = BlackScholes::vega(option, market, sigma)?;
            sigma -= diff / (vega * 100.0);

            if !sigma.is_finite() {
                return Err("Failed to converge".to_string());
            }
        }

        Ok(sigma)
    }

    /// Implied volatility using the "Let's be rational" method.
    ///
    /// This corresponds to the original `calc_rational_iv` implementation.
    pub fn rational_implied_vol(
        target_price: f64,
        option: &VanillaOption,
        market: &MarketData,
    ) -> Result<f64, String> {
        let s = market.spot;
        let k = option.strike;
        let r = market.rate;
        let q = market.dividend_yield;
        let t = option.maturity;

        // Remove discount from the observed price.
        let rate_inv_discount = (r * t).exp();
        let undiscounted_price = target_price * rate_inv_discount;

        // Forward price and dividend adjustment.
        let mut f = s * rate_inv_discount;
        f *= (-q * t).exp();

        let sigma = implied_volatility_from_a_transformed_rational_guess(
            undiscounted_price,
            f,
            k,
            t,
            option.kind,
        );

        if sigma.is_nan() || sigma.is_infinite() || sigma < 0.0 {
            return Err("Implied volatility failed to converge".to_string());
        }

        Ok(sigma)
    }
}
