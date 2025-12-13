/// Financial analytics core library for ParquetFrame.
///
/// Provides high-performance technical indicators, risk metrics,
/// and financial calculations built on top of pf-time-core.

pub mod error;
pub mod indicators;
pub mod advanced;
pub mod portfolio;
pub mod ohlcv;
pub mod indicators_extended;
pub mod backtest;
pub mod utils;

pub use error::FinError;
pub type Result<T> = std::result::Result<T, FinError>;

// Re-export commonly used functions
pub use indicators::{sma, ema, rsi, bollinger_bands};
pub use advanced::{macd, stochastic};
pub use portfolio::{
    returns, volatility, sharpe_ratio, sortino_ratio,
    value_at_risk, conditional_value_at_risk
};
pub use ohlcv::resample_ohlcv;
pub use indicators_extended::{atr, adx};
pub use backtest::{backtest, BacktestResult};
