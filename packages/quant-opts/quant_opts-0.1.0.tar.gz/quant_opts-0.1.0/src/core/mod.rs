//! Core domain types for `quant-opts`.
//!
//! These types describe *what* is being priced (vanilla options) and the
//! surrounding market data, independently of any particular pricing model
//! (Black–Scholes, SABR, etc.).

use std::{
    fmt::{Display, Formatter, Result as FmtResult},
    ops::Neg,
};

use num_traits::ConstZero;

/// The type of option to be priced (call or put).
#[derive(Debug, Clone, Eq, PartialEq, Copy)]
#[repr(i8)]
pub enum OptionType {
    Call = 1,
    Put = -1,
}

impl Neg for OptionType {
    type Output = Self;

    #[inline]
    fn neg(self) -> Self::Output {
        match self {
            OptionType::Call => OptionType::Put,
            OptionType::Put => OptionType::Call,
        }
    }
}

impl Display for OptionType {
    fn fmt(&self, f: &mut Formatter<'_>) -> FmtResult {
        match self {
            OptionType::Call => write!(f, "Call"),
            OptionType::Put => write!(f, "Put"),
        }
    }
}

macro_rules! impl_option_type {
    ($type:ty) => {
        impl From<OptionType> for $type {
            #[inline]
            fn from(val: OptionType) -> Self {
                <$type>::from(val as i8)
            }
        }

        impl From<$type> for OptionType {
            #[inline]
            fn from(value: $type) -> Self {
                if value >= <$type>::ZERO {
                    OptionType::Call
                } else {
                    OptionType::Put
                }
            }
        }

        impl std::ops::Mul<OptionType> for $type {
            type Output = $type;

            #[inline]
            fn mul(self, rhs: OptionType) -> Self::Output {
                match rhs {
                    OptionType::Call => self,
                    OptionType::Put => -self,
                }
            }
        }

        impl std::ops::Mul<$type> for OptionType {
            type Output = $type;

            #[inline]
            fn mul(self, rhs: $type) -> Self::Output {
                match self {
                    OptionType::Call => rhs,
                    OptionType::Put => -rhs,
                }
            }
        }
    };
}

impl_option_type!(f32);
impl_option_type!(f64);
impl_option_type!(i8);
impl_option_type!(i16);
impl_option_type!(i32);
impl_option_type!(i64);
impl_option_type!(i128);
impl_option_type!(isize);

/// Exercise style of a vanilla option.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OptionStyle {
    /// European-style option (exercise only at maturity).
    European,
    /// American-style option (exercise any time up to maturity).
    American,
}

/// Specification of a single vanilla option contract.
///
/// This struct is model-agnostic; pricing models interpret the fields
/// according to their own assumptions.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct VanillaOption {
    /// Exercise style (European or American).
    pub style: OptionStyle,
    /// Payoff direction (call or put).
    pub kind: OptionType,
    /// Strike price of the option.
    pub strike: f64,
    /// Time to maturity in years.
    ///
    /// The exact day-count convention (e.g. ACT/365 or ACT/365.25) is
    /// determined by how `t` is computed by the caller. The current
    /// library typically uses 365.25 days per year.
    pub maturity: f64,
}

impl VanillaOption {
    /// Creates a new vanilla option from its components.
    #[inline]
    pub fn new(style: OptionStyle, kind: OptionType, strike: f64, maturity: f64) -> Self {
        Self {
            style,
            kind,
            strike,
            maturity,
        }
    }

    /// Convenience constructor for a European call.
    #[inline]
    pub fn european_call(strike: f64, maturity: f64) -> Self {
        Self::new(OptionStyle::European, OptionType::Call, strike, maturity)
    }

    /// Convenience constructor for a European put.
    #[inline]
    pub fn european_put(strike: f64, maturity: f64) -> Self {
        Self::new(OptionStyle::European, OptionType::Put, strike, maturity)
    }

    /// Convenience constructor for an American call.
    #[inline]
    pub fn american_call(strike: f64, maturity: f64) -> Self {
        Self::new(OptionStyle::American, OptionType::Call, strike, maturity)
    }

    /// Convenience constructor for an American put.
    #[inline]
    pub fn american_put(strike: f64, maturity: f64) -> Self {
        Self::new(OptionStyle::American, OptionType::Put, strike, maturity)
    }
}

/// Market data required for pricing a single underlying.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct MarketData {
    /// Current spot price of the underlying.
    pub spot: f64,
    /// Continuously-compounded risk-free interest rate.
    pub rate: f64,
    /// Continuously-compounded dividend yield (or cost of carry).
    pub dividend_yield: f64,
}

impl MarketData {
    /// Creates a new `MarketData` instance.
    #[inline]
    pub fn new(spot: f64, rate: f64, dividend_yield: f64) -> Self {
        Self {
            spot,
            rate,
            dividend_yield,
        }
    }
}

/// Collection of Greeks for a vanilla option.
///
/// All fields are optional from a modeling perspective; a particular model
/// may choose to populate only a subset. By default they are initialized
/// to zero.
#[allow(clippy::struct_excessive_bools)]
#[derive(Debug, Clone, Copy, Default, PartialEq)]
pub struct Greeks {
    pub delta: f64,
    pub gamma: f64,
    pub theta: f64,
    pub vega: f64,
    pub rho: f64,
    pub epsilon: f64,
    pub lambda: f64,
    pub vanna: f64,
    pub charm: f64,
    pub veta: f64,
    pub vomma: f64,
    pub speed: f64,
    pub zomma: f64,
    pub color: f64,
    pub ultima: f64,
    pub dual_delta: f64,
    pub dual_gamma: f64,
}
