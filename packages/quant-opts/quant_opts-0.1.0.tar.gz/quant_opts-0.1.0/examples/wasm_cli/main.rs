//! Minimal CLI compiled to WebAssembly (WASI preview1) for pricing/IV.
//! Build: `cargo build --target wasm32-wasip1 --example wasm_cli`
//! Run (wasmtime): `wasmtime target/wasm32-wasip1/debug/examples/wasm_cli.wasm price --spot 105 --strike 100 --mat 0.25 --rate 0.03 --div 0.01 --vol 0.22`

use quant_opts::{BlackScholes, MarketData, OptionStyle, OptionType, VanillaOption};

fn parse_flag(args: &[String], name: &str, default: f64) -> f64 {
    let key = format!("--{name}");
    args.windows(2)
        .find_map(|w| (w[0] == key).then(|| w[1].parse::<f64>().ok()).flatten())
        .unwrap_or(default)
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.is_empty() {
        print_usage();
        std::process::exit(1);
    }

    let cmd = &args[0];
    let flags = &args[1..];

    match cmd.as_str() {
        "price" => do_price(flags),
        "iv" => do_iv(flags),
        _ => {
            print_usage();
            std::process::exit(1);
        }
    }
}

fn do_price(flags: &[String]) {
    let spot = parse_flag(flags, "spot", 105.0);
    let strike = parse_flag(flags, "strike", 100.0);
    let mat = parse_flag(flags, "mat", 0.25);
    let rate = parse_flag(flags, "rate", 0.03);
    let div = parse_flag(flags, "div", 0.01);
    let vol = parse_flag(flags, "vol", 0.22);

    let opt = VanillaOption::new(OptionStyle::European, OptionType::Call, strike, mat);
    let mkt = MarketData::new(spot, rate, div);

    match BlackScholes::price(&opt, &mkt, vol) {
        Ok(p) => println!("price={:.6}", p),
        Err(e) => {
            eprintln!("error: {e}");
            std::process::exit(2);
        }
    }
}

fn do_iv(flags: &[String]) {
    let observed = parse_flag(flags, "price", 4.25);
    let spot = parse_flag(flags, "spot", 102.0);
    let strike = parse_flag(flags, "strike", 100.0);
    let mat = parse_flag(flags, "mat", 0.25);
    let rate = parse_flag(flags, "rate", 0.02);
    let div = parse_flag(flags, "div", 0.00);

    let opt = VanillaOption::new(OptionStyle::European, OptionType::Call, strike, mat);
    let mkt = MarketData::new(spot, rate, div);

    match BlackScholes::rational_implied_vol(observed, &opt, &mkt) {
        Ok(iv) => println!("iv={:.6}", iv),
        Err(e) => {
            eprintln!("error: {e}");
            std::process::exit(2);
        }
    }
}

fn print_usage() {
    eprintln!(
        "Usage:\n  price: wasm_cli price --spot 105 --strike 100 --mat 0.25 --rate 0.03 --div 0.01 --vol 0.22\n  iv   : wasm_cli iv --price 4.25 --spot 102 --strike 100 --mat 0.25 --rate 0.02 --div 0.0"
    );
}
