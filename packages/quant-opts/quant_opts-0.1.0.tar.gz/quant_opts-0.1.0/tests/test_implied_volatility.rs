mod tests {
    use assert_approx_eq::assert_approx_eq;
    use quant_opts::{BlackScholes, MarketData, OptionStyle, OptionType, VanillaOption};

    // Tolerance is a bit higher due to IV being an approximation
    const TOLERANCE: f64 = 1e-8;

    #[test]
    fn test_put_otm_rational_iv() {
        let sigma = 0.25;
        let option =
            VanillaOption::new(OptionStyle::European, OptionType::Put, 100.0, 45.0 / 365.25);
        let market = MarketData::new(90.0, 0.03, 0.02);

        let price = BlackScholes::price(&option, &market, sigma).unwrap();
        let iv = BlackScholes::rational_implied_vol(price, &option, &market).unwrap();

        println!("Put OTM: {}", iv);
        assert_approx_eq!(iv, sigma, TOLERANCE);
    }

    #[test]
    fn test_call_itm_rational_iv() {
        let sigma = 0.15;
        let option = VanillaOption::new(
            OptionStyle::European,
            OptionType::Call,
            100.0,
            60.0 / 365.25,
        );
        let market = MarketData::new(120.0, 0.01, 0.0);

        let price = BlackScholes::price(&option, &market, sigma).unwrap();
        let iv = BlackScholes::rational_implied_vol(price, &option, &market).unwrap();

        println!("Call ITM: {}", iv);
        assert_approx_eq!(iv, sigma, TOLERANCE);
    }

    #[test]
    fn test_put_itm_rational_iv() {
        let sigma = 0.18;
        let option =
            VanillaOption::new(OptionStyle::European, OptionType::Put, 100.0, 60.0 / 365.25);
        let market = MarketData::new(80.0, 0.04, 0.03);

        let price = BlackScholes::price(&option, &market, sigma).unwrap();
        let iv = BlackScholes::rational_implied_vol(price, &option, &market).unwrap();

        println!("Put ITM: {}", iv);
        assert_approx_eq!(iv, sigma, TOLERANCE);
    }

    #[test]
    fn test_call_atm_rational_iv() {
        let sigma = 0.2;
        let option = VanillaOption::new(
            OptionStyle::European,
            OptionType::Call,
            100.0,
            90.0 / 365.25,
        );
        let market = MarketData::new(100.0, 0.05, 0.04);

        let price = BlackScholes::price(&option, &market, sigma).unwrap();
        let iv = BlackScholes::rational_implied_vol(price, &option, &market).unwrap();

        println!("Call ATM: {}", iv);
        assert_approx_eq!(iv, sigma, TOLERANCE);
    }

    #[test]
    fn test_put_atm_rational_iv() {
        let sigma = 0.22;
        let option = VanillaOption::new(
            OptionStyle::European,
            OptionType::Put,
            100.0,
            120.0 / 365.25,
        );
        let market = MarketData::new(100.0, 0.06, 0.01);

        let price = BlackScholes::price(&option, &market, sigma).unwrap();
        let iv = BlackScholes::rational_implied_vol(price, &option, &market).unwrap();

        println!("Put ATM: {}", iv);
        assert_approx_eq!(iv, sigma, TOLERANCE);
    }
}
