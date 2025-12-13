use proptest::prelude::*;
use quant_opts::{BlackScholes, MarketData, OptionStyle, OptionType, VanillaOption};

proptest! {
    #[test]
    fn call_price_is_monotonic_in_vol(
        spot in 50.0f64..150.0,
        strike in 50.0f64..150.0,
        t in 0.05f64..2.0,
        r in -0.05f64..0.10,
        q in -0.05f64..0.10,
        sigma1 in 0.05f64..1.0,
        sigma2 in 0.05f64..1.0,
    ) {
        let (low_vol, high_vol) = if sigma1 <= sigma2 {
            (sigma1, sigma2)
        } else {
            (sigma2, sigma1)
        };

        let option = VanillaOption::new(OptionStyle::European, OptionType::Call, strike, t);
        let market = MarketData::new(spot, r, q);

        let p_low = BlackScholes::price(&option, &market, low_vol).unwrap();
        let p_high = BlackScholes::price(&option, &market, high_vol).unwrap();

        // Allow a tiny numerical slack.
        prop_assert!(p_high + 1e-12 >= p_low);
    }
}

proptest! {
    #[test]
    fn put_call_parity_holds_for_european_options(
        spot in 50.0f64..150.0,
        strike in 50.0f64..150.0,
        t in 0.05f64..2.0,
        r in -0.05f64..0.10,
        q in -0.05f64..0.10,
        sigma in 0.05f64..1.0,
    ) {
        let call = VanillaOption::new(OptionStyle::European, OptionType::Call, strike, t);
        let put = VanillaOption::new(OptionStyle::European, OptionType::Put, strike, t);
        let market = MarketData::new(spot, r, q);

        let c = BlackScholes::price(&call, &market, sigma).unwrap();
        let p = BlackScholes::price(&put, &market, sigma).unwrap();

        let lhs = c - p;
        let rhs = spot * (-q * t).exp() - strike * (-r * t).exp();

        let diff = lhs - rhs;
        // Relative tolerance scaled by magnitude of rhs.
        let tol = 1e-8 * (1.0 + rhs.abs());
        prop_assert!(diff.abs() < tol);
    }
}

proptest! {
    #[test]
    fn rational_implied_vol_recovers_sigma(
        spot in 50.0f64..150.0,
        strike in 50.0f64..150.0,
        t in 0.10f64..2.0,
        r in 0.0f64..0.10,   // non-negative rates to help stability
        q in 0.0f64..0.05,
        sigma in 0.10f64..0.5,
    ) {
        let option = VanillaOption::new(OptionStyle::European, OptionType::Call, strike, t);
        let market = MarketData::new(spot, r, q);

        // Avoid extremely deep ITM/OTM where numerical issues are more pronounced.
        let moneyness = spot / strike;
        prop_assume!(moneyness >= 0.8 && moneyness <= 1.2);

        let price = BlackScholes::price(&option, &market, sigma).unwrap();
        // Skip nearly worthless options where numerical noise dominates.
        prop_assume!(price > 1e-8);

        let iv = BlackScholes::rational_implied_vol(price, &option, &market).unwrap();

        let diff = iv - sigma;
        // In this “typical” range the rational IV solver should be very close.
        let tol = 1e-6 * (1.0 + sigma.abs());
        prop_assert!(diff.abs() < tol);
    }
}
