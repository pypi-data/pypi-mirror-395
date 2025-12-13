use assert_approx_eq::assert_approx_eq;
use quant_opts::{BlackScholes, MarketData, OptionStyle, OptionType, VanillaOption};

const SIGMA: f64 = 0.2;

const VANILLA_CALL_OTM: VanillaOption = VanillaOption {
    style: OptionStyle::European,
    kind: OptionType::Call,
    strike: 110.0,
    maturity: 20.0 / 365.25,
};

const VANILLA_CALL_ITM: VanillaOption = VanillaOption {
    style: OptionStyle::European,
    kind: OptionType::Call,
    strike: 90.0,
    maturity: 20.0 / 365.25,
};

const VANILLA_PUT_OTM: VanillaOption = VanillaOption {
    style: OptionStyle::European,
    kind: OptionType::Put,
    strike: 90.0,
    maturity: 20.0 / 365.25,
};

const VANILLA_PUT_ITM: VanillaOption = VanillaOption {
    style: OptionStyle::European,
    kind: OptionType::Put,
    strike: 110.0,
    maturity: 20.0 / 365.25,
};

const MARKET_COMMON: MarketData = MarketData {
    spot: 100.0,
    rate: 0.05,
    dividend_yield: 0.05,
};

const VANILLA_BRANCH_CUT: VanillaOption = VanillaOption {
    style: OptionStyle::European,
    kind: OptionType::Put,
    strike: 100.0,
    maturity: 1.0,
};

const MARKET_BRANCH_CUT: MarketData = MarketData {
    spot: 100.0,
    rate: 0.0,
    dividend_yield: 0.0,
};

const SIGMA_BRANCH_CUT: f64 = 0.421;

#[test]
fn price_call_otm() {
    let price = BlackScholes::price(&VANILLA_CALL_OTM, &MARKET_COMMON, SIGMA).unwrap();
    assert_approx_eq!(price, 0.0376, 0.001);
}
#[test]
fn price_call_itm() {
    let price = BlackScholes::price(&VANILLA_CALL_ITM, &MARKET_COMMON, SIGMA).unwrap();
    assert_approx_eq!(price, 9.9913, 0.001);
}

#[test]
fn price_put_otm() {
    let price = BlackScholes::price(&VANILLA_PUT_OTM, &MARKET_COMMON, SIGMA).unwrap();
    assert_approx_eq!(price, 0.01867, 0.001);
}
#[test]
fn price_put_itm() {
    let price = BlackScholes::price(&VANILLA_PUT_ITM, &MARKET_COMMON, SIGMA).unwrap();
    assert_approx_eq!(price, 10.0103, 0.001);
}

#[test]
fn price_using_lets_be_rational() {
    // compare the results from calc_price() and calc_rational_price() for the options above
    assert_approx_eq!(
        BlackScholes::price(&VANILLA_CALL_OTM, &MARKET_COMMON, SIGMA).unwrap(),
        BlackScholes::rational_price(&VANILLA_CALL_OTM, &MARKET_COMMON, SIGMA).unwrap(),
        0.001
    );

    assert_approx_eq!(
        BlackScholes::price(&VANILLA_CALL_ITM, &MARKET_COMMON, SIGMA).unwrap(),
        BlackScholes::rational_price(&VANILLA_CALL_ITM, &MARKET_COMMON, SIGMA).unwrap(),
        0.001
    );

    assert_approx_eq!(
        BlackScholes::price(&VANILLA_PUT_OTM, &MARKET_COMMON, SIGMA).unwrap(),
        BlackScholes::rational_price(&VANILLA_PUT_OTM, &MARKET_COMMON, SIGMA).unwrap(),
        0.001
    );

    assert_approx_eq!(
        BlackScholes::price(&VANILLA_PUT_ITM, &MARKET_COMMON, SIGMA).unwrap(),
        BlackScholes::rational_price(&VANILLA_PUT_ITM, &MARKET_COMMON, SIGMA).unwrap(),
        0.001
    );
}

#[test]
fn test_rational_price_near_branch_cut() {
    assert_approx_eq!(
        BlackScholes::rational_price(&VANILLA_BRANCH_CUT, &MARKET_BRANCH_CUT, SIGMA_BRANCH_CUT)
            .unwrap(),
        16.67224,
        0.001
    );
}
