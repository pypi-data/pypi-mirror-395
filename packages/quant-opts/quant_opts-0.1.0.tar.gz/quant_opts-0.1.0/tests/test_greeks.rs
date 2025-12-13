#[cfg(test)]
mod tests {
    use quant_opts::{BlackScholes, MarketData, OptionStyle, OptionType, VanillaOption};

    #[test]
    fn test_calc_delta_zero_stock_price() {
        // arrange
        let option = VanillaOption::new(
            OptionStyle::European,
            OptionType::Call,
            100.0,
            20.0 / 365.25,
        );
        let market = MarketData::new(0.0, 0.05, 0.0); // extreme value: spot = 0
        let sigma = 0.2;

        // act
        let result = BlackScholes::delta(&option, &market, sigma);

        // assert
        assert!(result.is_err());
    }

    #[test]
    fn test_calc_delta_zero_strike_price() {
        // arrange
        let option = VanillaOption::new(
            OptionStyle::European,
            OptionType::Call,
            0.0, // extreme value: strike = 0
            20.0 / 365.25,
        );
        let market = MarketData::new(100.0, 0.05, 0.0);
        let sigma = 0.2;

        // act
        let result = BlackScholes::delta(&option, &market, sigma);

        // assert
        assert!(result.is_err());
    }

    #[test]
    fn test_calc_delta_zero_risk_free_rate() {
        // arrange
        let option = VanillaOption::new(
            OptionStyle::European,
            OptionType::Call,
            100.0,
            20.0 / 365.25,
        );
        let market = MarketData::new(100.0, 0.0, 0.0); // extreme value: r = 0
        let sigma = 0.2;

        // act
        let result = BlackScholes::delta(&option, &market, sigma);

        // assert
        assert!(result.is_ok());
    }

    #[test]
    fn test_calc_delta_none_volatility() {
        // arrange
        let option = VanillaOption::new(
            OptionStyle::European,
            OptionType::Call,
            100.0,
            20.0 / 365.25,
        );
        let market = MarketData::new(100.0, 0.05, 0.0);
        let sigma = f64::NAN; // extreme value

        // act
        let result = BlackScholes::delta(&option, &market, sigma);

        // assert
        assert!(result.is_err());
    }

    #[test]
    fn test_calc_delta_zero_time_to_maturity() {
        // arrange
        let option = VanillaOption::new(
            OptionStyle::European,
            OptionType::Call,
            100.0,
            0.0, // extreme value
        );
        let market = MarketData::new(100.0, 0.05, 0.0);
        let sigma = 0.2;

        // act
        let result = BlackScholes::delta(&option, &market, sigma);

        // assert
        assert!(result.is_err());
    }
}
