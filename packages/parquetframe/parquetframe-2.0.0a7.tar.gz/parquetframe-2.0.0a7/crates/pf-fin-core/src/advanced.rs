/// Advanced technical indicators.
///
/// Implements MACD, Stochastic Oscillator, and other advanced indicators.

use arrow::array::{Array, ArrayRef, Float64Builder};
use crate::{FinError, Result};
use crate::utils::as_float64_array;
use std::sync::Arc;
use super::ema;

/// Calculate MACD (Moving Average Convergence Divergence).
///
/// # Arguments
/// * `values` - Array of price values
/// * `fast_period` - Fast EMA period (default: 12)
/// * `slow_period` - Slow EMA period (default: 26)
/// * `signal_period` - Signal line EMA period (default: 9)
///
/// # Returns
/// Tuple of (macd_line, signal_line, histogram)
pub fn macd(
    values: &ArrayRef,
    fast_period: usize,
    slow_period: usize,
    signal_period: usize,
) -> Result<(ArrayRef, ArrayRef, ArrayRef)> {
    if fast_period == 0 || slow_period == 0 || signal_period == 0 {
        return Err(FinError::InvalidParameter(
            "All periods must be > 0".to_string(),
        ));
    }

    if fast_period >= slow_period {
        return Err(FinError::InvalidParameter(
            "Fast period must be < slow period".to_string(),
        ));
    }

    // Calculate fast and slow EMAs
    let fast_ema = ema(values, fast_period)?;
    let slow_ema = ema(values, slow_period)?;

    let fast_array = as_float64_array(&fast_ema)?;
    let slow_array = as_float64_array(&slow_ema)?;
    let len = fast_array.len();

    // Calculate MACD line (fast EMA - slow EMA)
    let mut macd_builder = Float64Builder::with_capacity(len);

    for i in 0..len {
        if fast_array.is_null(i) || slow_array.is_null(i) {
            macd_builder.append_null();
        } else {
            macd_builder.append_value(fast_array.value(i) - slow_array.value(i));
        }
    }

    let macd_line = Arc::new(macd_builder.finish()) as ArrayRef;

    // Calculate signal line (EMA of MACD line)
    let signal_line = ema(&macd_line, signal_period)?;

    let macd_array = as_float64_array(&macd_line)?;
    let signal_array = as_float64_array(&signal_line)?;

    // Calculate histogram (MACD - signal)
    let mut histogram_builder = Float64Builder::with_capacity(len);

    for i in 0..len {
        if macd_array.is_null(i) || signal_array.is_null(i) {
            histogram_builder.append_null();
        } else {
            histogram_builder.append_value(macd_array.value(i) - signal_array.value(i));
        }
    }

    Ok((
        macd_line,
        signal_line,
        Arc::new(histogram_builder.finish()) as ArrayRef,
    ))
}

/// Calculate Stochastic Oscillator.
///
/// # Arguments
/// * `high` - Array of high prices
/// * `low` - Array of low prices
/// * `close` - Array of close prices
/// * `k_period` - %K period (default: 14)
/// * `d_period` - %D period (default: 3)
///
/// # Returns
/// Tuple of (%K line, %D line)
pub fn stochastic(
    high: &ArrayRef,
    low: &ArrayRef,
    close: &ArrayRef,
    k_period: usize,
    d_period: usize,
) -> Result<(ArrayRef, ArrayRef)> {
    if k_period == 0 || d_period == 0 {
        return Err(FinError::InvalidParameter("Periods must be > 0".to_string()));
    }

    let high_array = as_float64_array(high)?;
    let low_array = as_float64_array(low)?;
    let close_array = as_float64_array(close)?;

    let len = close_array.len();
    if len != high_array.len() || len != low_array.len() {
        return Err(FinError::InvalidParameter(
            "High, low, and close arrays must have same length".to_string(),
        ));
    }

    let mut k_builder = Float64Builder::with_capacity(len);

    // Calculate %K
    for i in 0..len {
        if i < k_period - 1 {
            k_builder.append_null();
        } else {
            // Find highest high and lowest low in the period
            let mut highest_high = f64::NEG_INFINITY;
            let mut lowest_low = f64::INFINITY;

            for j in (i + 1 - k_period)..=i {
                if !high_array.is_null(j) {
                    highest_high = highest_high.max(high_array.value(j));
                }
                if !low_array.is_null(j) {
                    lowest_low = lowest_low.min(low_array.value(j));
                }
            }

            if highest_high.is_finite()
                && lowest_low.is_finite()
                && !close_array.is_null(i)
                && highest_high != lowest_low
            {
                let current_close = close_array.value(i);
                let k_value = ((current_close - lowest_low) / (highest_high - lowest_low)) * 100.0;
                k_builder.append_value(k_value);
            } else {
                k_builder.append_null();
            }
        }
    }

    let k_line = Arc::new(k_builder.finish()) as ArrayRef;

    // Calculate %D (SMA of %K)
    use super::sma;
    let d_line = sma(&k_line, d_period)?;

    Ok((k_line, d_line))
}

#[cfg(test)]
mod tests {
    use super::*;
    use arrow::array::Float64Array;

    #[test]
    fn test_macd() {
        let values = Arc::new(Float64Array::from(vec![
            10.0, 11.0, 12.0, 11.5, 10.5, 11.0, 12.5, 13.0, 12.5, 11.5, 10.5, 11.0, 12.0, 13.0,
            14.0, 13.5, 12.5, 11.5, 12.0, 13.0, 14.5, 15.0, 14.5, 13.5, 12.5, 13.0, 14.0, 15.0,
            16.0, 15.5,
        ])) as ArrayRef;

        let result = macd(&values, 12, 26, 9);
        assert!(result.is_ok());

        let (macd_line, signal_line, histogram) = result.unwrap();
        assert_eq!(macd_line.len(), values.len());
        assert_eq!(signal_line.len(), values.len());
        assert_eq!(histogram.len(), values.len());
    }

    #[test]
    fn test_stochastic() {
        let high =
            Arc::new(Float64Array::from(vec![12.0, 13.0, 14.0, 13.5, 12.5, 13.5, 14.5, 15.0, 14.5, 13.5, 12.5, 13.0, 14.0, 15.0, 16.0])) as ArrayRef;
        let low = Arc::new(Float64Array::from(vec![
            10.0, 10.5, 11.0, 10.5, 9.5, 10.5, 11.5, 12.0, 11.5, 10.5, 9.5, 10.0, 11.0, 12.0, 13.0,
        ])) as ArrayRef;
        let close = Arc::new(Float64Array::from(vec![
            11.0, 12.0, 13.0, 12.0, 11.0, 12.0, 13.0, 14.0, 13.0, 12.0, 11.0, 12.0, 13.0, 14.0,
            15.0,
        ])) as ArrayRef;

        let result = stochastic(&high, &low, &close, 14, 3);
        assert!(result.is_ok());

        let (k_line, d_line) = result.unwrap();
        assert_eq!(k_line.len(), close.len());
        assert_eq!(d_line.len(), close.len());
    }
}
