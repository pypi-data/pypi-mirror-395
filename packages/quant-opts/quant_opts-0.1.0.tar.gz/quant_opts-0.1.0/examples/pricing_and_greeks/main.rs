use quant_opts::{BlackScholes, MarketData, OptionStyle, OptionType, VanillaModel, VanillaOption};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Define a single European call option.
    let option = VanillaOption::new(
        OptionStyle::European,
        OptionType::Call,
        100.0,         // strike
        30.0 / 365.25, // maturity in years
    );

    // Market inputs.
    let market = MarketData::new(
        105.0, // spot
        0.03,  // risk-free rate
        0.01,  // dividend yield
    );

    // Volatility assumption.
    let sigma = 0.22;

    // Direct static API.
    let price = BlackScholes::price(&option, &market, sigma)?;
    let greeks = BlackScholes::greeks(&option, &market, sigma)?;

    println!("Black–Scholes pricing");
    println!("  price  : {:.6}", price);
    println!("  delta  : {:.6}", greeks.delta);
    println!("  gamma  : {:.6}", greeks.gamma);
    println!("  theta  : {:.6}", greeks.theta);
    println!("  vega   : {:.6}", greeks.vega);
    println!("  rho    : {:.6}", greeks.rho);

    // Using the trait-based API.
    let model = BlackScholes::new(sigma);
    let price_via_trait = model.price(&option, &market)?;
    println!("  (trait) price: {:.6}", price_via_trait);

    Ok(())
}
