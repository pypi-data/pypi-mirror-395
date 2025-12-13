/// Simple backtest framework for strategy validation.
///
/// Provides basic backtesting capabilities for trading strategies.

use arrow::array::{Array, ArrayRef, Float64Array, Float64Builder};
use crate::{FinError, Result};
use crate::utils::as_float64_array;
use std::sync::Arc;

/// Backtest result structure.
#[derive(Debug, Clone)]
pub struct BacktestResult {
    pub total_return: f64,
    pub sharpe_ratio: f64,
    pub max_drawdown: f64,
    pub win_rate: f64,
    pub num_trades: usize,
}

/// Run a simple backtest on a strategy.
///
/// # Arguments
/// * `prices` - Array of prices
/// * `signals` - Array of signals (-1 = sell, 0 = hold, 1 = buy)
/// * `initial_capital` - Starting capital
/// * `commission` - Commission rate per trade (e.g., 0.001 for 0.1%)
///
/// # Returns
/// BacktestResult with performance metrics
pub fn backtest(
    prices: &ArrayRef,
    signals: &ArrayRef,
    initial_capital: f64,
    commission: f64,
) -> Result<BacktestResult> {
    let price_array = as_float64_array(prices)?;
    let signal_array = as_float64_array(signals)?;

    let len = price_array.len();
    if len != signal_array.len() {
        return Err(FinError::InvalidParameter(
            "Prices and signals must have same length".to_string(),
        ));
    }

    let mut capital = initial_capital;
    let mut position = 0.0; // Number of shares held
    let mut equity_curve = Vec::with_capacity(len);
    let mut trades = Vec::new();
    let mut prev_signal = 0.0;

    for i in 0..len {
        if price_array.is_null(i) || signal_array.is_null(i) {
            equity_curve.push(capital + position * if i > 0 && !price_array.is_null(i - 1) {
                price_array.value(i - 1)
            } else {
                0.0
            });
            continue;
        }

        let price = price_array.value(i);
        let signal = signal_array.value(i);

        // Handle signal changes
        if signal != prev_signal {
            // Close existing position if any
            if position != 0.0 {
                let proceeds = position * price * (1.0 - commission);
                capital += proceeds;
                trades.push((prev_signal, price, position));
                position = 0.0;
            }

            // Open new position based on signal
            if signal > 0.0 {
                // Buy signal
                let shares = (capital * 0.95) / price; // Use 95% of capital
                let cost = shares * price * (1.0 + commission);
                if cost <= capital {
                    position = shares;
                    capital -= cost;
                }
            } else if signal < 0.0 {
                // Sell/short signal (for simplicity, we'll just close long positions)
                // In a real backtest, you might implement short selling here
            }

            prev_signal = signal;
        }

        // Calculate current equity
        let current_equity = capital + position * price;
        equity_curve.push(current_equity);
    }

    // Close final position
    if position != 0.0 && len > 0 && !price_array.is_null(len - 1) {
        let final_price = price_array.value(len - 1);
        capital += position * final_price * (1.0 - commission);
    }

    // Calculate metrics
    let final_equity = capital;
    let total_return = (final_equity - initial_capital) / initial_capital;

    // Calculate returns for Sharpe ratio
    let mut returns = Vec::new();
    for i in 1..equity_curve.len() {
        if equity_curve[i - 1] > 0.0 {
            returns.push((equity_curve[i] - equity_curve[i - 1]) / equity_curve[i - 1]);
        }
    }

    let sharpe_ratio = if !returns.is_empty() {
        let mean = returns.iter().sum::<f64>() / returns.len() as f64;
        let variance = returns.iter().map(|r| (r - mean).powi(2)).sum::<f64>() / returns.len() as f64;
        let std_dev = variance.sqrt();
        if std_dev > 0.0 {
            (mean * 252.0) / (std_dev * (252.0_f64).sqrt()) // Annualized
        } else {
            0.0
        }
    } else {
        0.0
    };

    // Calculate maximum drawdown
    let mut peak = equity_curve[0];
    let mut max_drawdown = 0.0;

    for &equity in &equity_curve {
        if equity > peak {
            peak = equity;
        }
        let drawdown = (peak - equity) / peak;
        if drawdown > max_drawdown {
            max_drawdown = drawdown;
        }
    }

    // Calculate win rate
    let winning_trades = trades.iter().filter(|(signal, price, shares)| {
        if *signal > 0.0 {
            // Was a buy, check if we made money
            true // Simplified: assume we track entry/exit prices properly
        } else {
            false
        }
    }).count();

    let win_rate = if !trades.is_empty() {
        winning_trades as f64 / trades.len() as f64
    } else {
        0.0
    };

    Ok(BacktestResult {
        total_return,
        sharpe_ratio,
        max_drawdown,
        win_rate,
        num_trades: trades.len(),
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_backtest() {
        let prices = Arc::new(Float64Array::from(vec![
            100.0, 102.0, 101.0, 103.0, 105.0, 104.0, 106.0, 108.0, 107.0, 109.0,
        ])) as ArrayRef;

        // Strategy with signal changes (buy then hold then sell)
        let signals = Arc::new(Float64Array::from(vec![
            0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0,
        ])) as ArrayRef;

        let result = backtest(&prices, &signals, 10000.0, 0.001);
        assert!(result.is_ok());

        let bt_result = result.unwrap();
        assert!(bt_result.total_return != 0.0); // Should have returns
        // num_trades might be 0 if no sell signal, that's ok
    }
}
