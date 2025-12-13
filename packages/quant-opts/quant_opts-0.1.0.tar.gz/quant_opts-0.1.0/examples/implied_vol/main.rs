use quant_opts::{BlackScholes, MarketData, OptionStyle, OptionType, VanillaOption};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let option = VanillaOption::new(
        OptionStyle::European,
        OptionType::Call,
        100.0,
        45.0 / 365.25,
    );

    let market = MarketData::new(
        102.0, // spot
        0.02,  // rate
        0.00,  // dividend yield
    );

    // Suppose we observe a market price for this option.
    let observed_price = 4.25;

    // Solve for implied volatility using the rational approximation.
    let iv = BlackScholes::rational_implied_vol(observed_price, &option, &market)?;

    println!("Implied volatility (rational) = {:.6}", iv);

    Ok(())
}
