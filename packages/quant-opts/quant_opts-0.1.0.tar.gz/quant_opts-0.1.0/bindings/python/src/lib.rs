use pyo3::prelude::*;
use pyo3::types::{PyDict, PyModule};

use quant_opts::{BlackScholes, MarketData, OptionStyle, OptionType, VanillaOption};

fn parse_kind(kind: &str) -> PyResult<OptionType> {
    match kind.to_lowercase().as_str() {
        "call" | "c" => Ok(OptionType::Call),
        "put" | "p" => Ok(OptionType::Put),
        _ => Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            "kind must be 'call' or 'put'",
        )),
    }
}

fn build_inputs(
    kind: OptionType,
    spot: f64,
    strike: f64,
    maturity: f64,
    rate: f64,
    dividend_yield: f64,
) -> (VanillaOption, MarketData) {
    let opt = VanillaOption::new(OptionStyle::European, kind, strike, maturity);
    let mkt = MarketData::new(spot, rate, dividend_yield);
    (opt, mkt)
}

#[pyfunction]
#[pyo3(
    text_signature = "(kind, spot, strike, maturity, rate, dividend_yield, vol)",
    signature = (
        kind,
        spot,
        strike,
        maturity,
        rate,
        dividend_yield,
        vol
    )
)]
/// Black–Scholes price for a European option.
///
/// kind: "call"/"put" (or c/p)
/// spot: spot price
/// strike: strike price
/// maturity: time in years
/// rate: risk-free rate
/// dividend_yield: continuous dividend yield
/// vol: volatility
///
/// Example:
/// ```python
/// >>> from quant_opts import price
/// >>> round(price("call", 105, 100, 0.25, 0.03, 0.01, 0.22), 6)
/// 7.238559
/// ```
fn price(
    kind: &str,
    spot: f64,
    strike: f64,
    maturity: f64,
    rate: f64,
    dividend_yield: f64,
    vol: f64,
) -> PyResult<f64> {
    let kind = parse_kind(kind)?;
    let (opt, mkt) = build_inputs(kind, spot, strike, maturity, rate, dividend_yield);
    BlackScholes::price(&opt, &mkt, vol).map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e))
}

#[pyfunction]
#[pyo3(
    text_signature = "(kind, spot, strike, maturity, rate, dividend_yield, vol)",
    signature = (
        kind,
        spot,
        strike,
        maturity,
        rate,
        dividend_yield,
        vol
    )
)]
/// Rational (dividend-adjusted) price for a European option.
///
/// Same parameters as price().
///
/// Example:
/// ```python
/// >>> from quant_opts import rational_price
/// >>> round(rational_price("put", 100, 95, 0.5, 0.02, 0.01, 0.3), 6)
/// 4.592931
/// ```
fn rational_price(
    kind: &str,
    spot: f64,
    strike: f64,
    maturity: f64,
    rate: f64,
    dividend_yield: f64,
    vol: f64,
) -> PyResult<f64> {
    let kind = parse_kind(kind)?;
    let (opt, mkt) = build_inputs(kind, spot, strike, maturity, rate, dividend_yield);
    BlackScholes::rational_price(&opt, &mkt, vol)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e))
}

#[pyfunction]
#[pyo3(
    text_signature = "(kind, spot, strike, maturity, rate, dividend_yield, vol)",
    signature = (
        kind,
        spot,
        strike,
        maturity,
        rate,
        dividend_yield,
        vol
    )
)]
/// Return Black–Scholes Greeks as a dict.
///
/// Keys: delta, gamma, theta, vega, rho, epsilon, vanna, charm, vomma, speed, zomma.
///
/// Example:
/// ```python
/// >>> from quant_opts import greeks
/// >>> g = greeks("call", 105, 100, 0.25, 0.03, 0.01, 0.22)
/// >>> round(g["delta"], 6)
/// 0.63793
/// ```
fn greeks(
    kind: &str,
    spot: f64,
    strike: f64,
    maturity: f64,
    rate: f64,
    dividend_yield: f64,
    vol: f64,
) -> PyResult<Py<PyDict>> {
    let kind = parse_kind(kind)?;
    let (opt, mkt) = build_inputs(kind, spot, strike, maturity, rate, dividend_yield);
    let g = BlackScholes::greeks(&opt, &mkt, vol)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e))?;

    Python::attach(|py| {
        let dict = PyDict::new(py);
        dict.set_item("delta", g.delta)?;
        dict.set_item("gamma", g.gamma)?;
        dict.set_item("theta", g.theta)?;
        dict.set_item("vega", g.vega)?;
        dict.set_item("rho", g.rho)?;
        dict.set_item("epsilon", g.epsilon)?;
        dict.set_item("vanna", g.vanna)?;
        dict.set_item("charm", g.charm)?;
        dict.set_item("vomma", g.vomma)?;
        dict.set_item("speed", g.speed)?;
        dict.set_item("zomma", g.zomma)?;
        Ok(dict.unbind())
    })
}

#[pyfunction]
#[pyo3(
    text_signature = "(target_price, kind, spot, strike, maturity, rate, dividend_yield)",
    signature = (
        target_price,
        kind,
        spot,
        strike,
        maturity,
        rate,
        dividend_yield
    )
)]
/// Solve implied volatility using the rational (dividend-adjusted) model.
///
/// target_price: observed option price
/// Other parameters match price().
///
/// Example:
/// ```python
/// >>> from quant_opts import rational_implied_vol
/// >>> round(rational_implied_vol(4.25, "call", 102, 100, 0.25, 0.02, 0.0), 6)
/// 0.197251
/// ```
fn rational_implied_vol(
    target_price: f64,
    kind: &str,
    spot: f64,
    strike: f64,
    maturity: f64,
    rate: f64,
    dividend_yield: f64,
) -> PyResult<f64> {
    let kind = parse_kind(kind)?;
    let (opt, mkt) = build_inputs(kind, spot, strike, maturity, rate, dividend_yield);
    BlackScholes::rational_implied_vol(target_price, &opt, &mkt)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e))
}

#[pymodule]
fn core(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add(
        "__doc__",
        "Black–Scholes pricing, Greeks, and rational IV for Python (docstrings include Python examples).",
    )?;
    m.add_function(wrap_pyfunction!(price, m)?)?;
    m.add_function(wrap_pyfunction!(rational_price, m)?)?;
    m.add_function(wrap_pyfunction!(greeks, m)?)?;
    m.add_function(wrap_pyfunction!(rational_implied_vol, m)?)?;
    Ok(())
}
