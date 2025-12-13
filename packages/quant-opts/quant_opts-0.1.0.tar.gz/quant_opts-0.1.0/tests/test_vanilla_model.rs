use assert_approx_eq::assert_approx_eq;
use quant_opts::{BlackScholes, MarketData, OptionStyle, OptionType, VanillaModel, VanillaOption};

const SIGMA: f64 = 0.2;

fn vanilla_model_contract<M: VanillaModel>(model: &M, sigma: f64) {
    let option = VanillaOption::new(
        OptionStyle::European,
        OptionType::Call,
        100.0,
        20.0 / 365.25,
    );
    let market = MarketData::new(100.0, 0.05, 0.05);

    // price: trait vs. static API
    let price_trait = model.price(&option, &market).unwrap();
    let price_static = BlackScholes::price(&option, &market, sigma).unwrap();
    assert_approx_eq!(price_trait, price_static, 1e-12);

    // greeks: trait vs. static API (delta as representative)
    let greeks_trait = model.greeks(&option, &market).unwrap();
    let delta_static = BlackScholes::delta(&option, &market, sigma).unwrap();
    assert_approx_eq!(greeks_trait.delta, delta_static, 1e-12);

    // implied vol: recover sigma from price
    let iv_trait = model.implied_vol(price_static, &option, &market).unwrap();
    assert_approx_eq!(iv_trait, sigma, 1e-8);
}

#[test]
fn vanilla_model_price_matches_static_bs() {
    let model = BlackScholes::new(SIGMA);
    vanilla_model_contract(&model, SIGMA);
}

#[test]
fn vanilla_model_reports_errors_for_invalid_inputs() {
    // Non-finite volatility in the model should produce an error.
    let model_bad_vol = BlackScholes::new(f64::NAN);
    let option = VanillaOption::new(
        OptionStyle::European,
        OptionType::Call,
        100.0,
        20.0 / 365.25,
    );
    let market = MarketData::new(100.0, 0.05, 0.0);
    assert!(model_bad_vol.price(&option, &market).is_err());
    assert!(model_bad_vol.greeks(&option, &market).is_err());

    // Zero time to maturity should also surface as an error via the trait.
    let model = BlackScholes::new(SIGMA);
    let option_zero_t = VanillaOption::new(OptionStyle::European, OptionType::Call, 100.0, 0.0);
    let market = MarketData::new(100.0, 0.05, 0.0);
    assert!(model.price(&option_zero_t, &market).is_err());
    assert!(model.greeks(&option_zero_t, &market).is_err());
}
