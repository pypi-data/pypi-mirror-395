/// Technical indicators for financial time-series analysis.
///
/// Implements common indicators like SMA, EMA, RSI, and Bollinger Bands.

use arrow::array::{Array, ArrayRef, Float64Builder};
use crate::{FinError, Result};
use crate::utils::as_float64_array;
use std::sync::Arc;

/// Calculate Simple Moving Average (SMA).
///
/// # Arguments
/// * `values` - Array of price values
/// * `window` - Window size for averaging
///
/// # Returns
/// Array with NaN for initial values until window is filled
pub fn sma(values: &ArrayRef, window: usize) -> Result<ArrayRef> {
    if window == 0 {
        return Err(FinError::InvalidParameter("Window must be > 0".to_string()));
    }

    let array = as_float64_array(values)?;
    let len = array.len();
    let mut builder = Float64Builder::with_capacity(len);

    for i in 0..len {
        if i < window - 1 {
            builder.append_null();
        } else {
            let mut sum = 0.0;
            let mut count = 0;

            for j in (i + 1 - window)..=i {
                if !array.is_null(j) {
                    sum += array.value(j);
                    count += 1;
                }
            }

            if count > 0 {
                builder.append_value(sum / count as f64);
            } else {
                builder.append_null();
            }
        }
    }

    Ok(Arc::new(builder.finish()) as ArrayRef)
}

/// Calculate Exponential Moving Average (EMA).
///
/// # Arguments
/// * `values` - Array of price values
/// * `span` - Span (number of periods) for EMA calculation
///
/// # Returns
/// Array with EMA values
pub fn ema(values: &ArrayRef, span: usize) -> Result<ArrayRef> {
    if span == 0 {
        return Err(FinError::InvalidParameter("Span must be > 0".to_string()));
    }

    let array = as_float64_array(values)?;
    let len = array.len();
    let mut builder = Float64Builder::with_capacity(len);

    // EMA multiplier: 2 / (span + 1)
    let alpha = 2.0 / (span as f64 + 1.0);
    let mut ema_value: Option<f64> = None;

    for i in 0..len {
        if array.is_null(i) {
            builder.append_null();
            continue;
        }

        let current = array.value(i);

        ema_value = match ema_value {
            None => Some(current), // First value
            Some(prev_ema) => Some(alpha * current + (1.0 - alpha) * prev_ema),
        };

        builder.append_value(ema_value.unwrap());
    }

    Ok(Arc::new(builder.finish()) as ArrayRef)
}

/// Calculate Relative Strength Index (RSI).
///
/// # Arguments
/// * `values` - Array of price values
/// * `window` - Window size for RSI calculation (typically 14)
///
/// # Returns
/// Array with RSI values (0-100)
pub fn rsi(values: &ArrayRef, window: usize) -> Result<ArrayRef> {
    if window == 0 {
        return Err(FinError::InvalidParameter("Window must be > 0".to_string()));
    }

    let array = as_float64_array(values)?;
    let len = array.len();
    let mut builder = Float64Builder::with_capacity(len);

    // Calculate price changes
    let mut gains = Vec::with_capacity(len);
    let mut losses = Vec::with_capacity(len);

    builder.append_null(); // First value has no change

    for i in 1..len {
        if array.is_null(i) || array.is_null(i - 1) {
            gains.push(0.0);
            losses.push(0.0);
            builder.append_null();
            continue;
        }

        let change = array.value(i) - array.value(i - 1);
        gains.push(if change > 0.0 { change } else { 0.0 });
        losses.push(if change < 0.0 { -change } else { 0.0 });

        if i < window {
            builder.append_null();
        } else {
            // Calculate average gains and losses
            let avg_gain: f64 = gains[(i - window)..i].iter().sum::<f64>() / window as f64;
            let avg_loss: f64 = losses[(i - window)..i].iter().sum::<f64>() / window as f64;

            let rsi_value = if avg_loss == 0.0 {
                100.0
            } else {
                let rs = avg_gain / avg_loss;
                100.0 - (100.0 / (1.0 + rs))
            };

            builder.append_value(rsi_value);
        }
    }

    Ok(Arc::new(builder.finish()) as ArrayRef)
}

/// Calculate Bollinger Bands.
///
/// # Arguments
/// * `values` - Array of price values
/// * `window` - Window size for calculation
/// * `num_std` - Number of standard deviations for bands
///
/// # Returns
/// Tuple of (upper_band, middle_band, lower_band)
pub fn bollinger_bands(
    values: &ArrayRef,
    window: usize,
    num_std: f64,
) -> Result<(ArrayRef, ArrayRef, ArrayRef)> {
    if window == 0 {
        return Err(FinError::InvalidParameter("Window must be > 0".to_string()));
    }

    let array = as_float64_array(values)?;
    let len = array.len();

    let mut upper_builder = Float64Builder::with_capacity(len);
    let mut middle_builder = Float64Builder::with_capacity(len);
    let mut lower_builder = Float64Builder::with_capacity(len);

    for i in 0..len {
        if i < window - 1 {
            upper_builder.append_null();
            middle_builder.append_null();
            lower_builder.append_null();
        } else {
            // Calculate mean and std
            let window_data: Vec<f64> = (i + 1 - window..=i)
                .filter_map(|j| if !array.is_null(j) { Some(array.value(j)) } else { None })
                .collect();

            if window_data.is_empty() {
                upper_builder.append_null();
                middle_builder.append_null();
                lower_builder.append_null();
                continue;
            }

            let mean = window_data.iter().sum::<f64>() / window_data.len() as f64;
            let variance = window_data
                .iter()
                .map(|x| (x - mean).powi(2))
                .sum::<f64>()
                / window_data.len() as f64;
            let std_dev = variance.sqrt();

            middle_builder.append_value(mean);
            upper_builder.append_value(mean + num_std * std_dev);
            lower_builder.append_value(mean - num_std * std_dev);
        }
    }

    Ok((
        Arc::new(upper_builder.finish()) as ArrayRef,
        Arc::new(middle_builder.finish()) as ArrayRef,
        Arc::new(lower_builder.finish()) as ArrayRef,
    ))
}

#[cfg(test)]
mod tests {
    use super::*;
    use arrow::array::Float64Array;

    #[test]
    fn test_sma() {
        let values = Arc::new(Float64Array::from(vec![1.0, 2.0, 3.0, 4.0, 5.0])) as ArrayRef;
        let result = sma(&values, 3).unwrap();
        let result_array = as_float64_array(&result).unwrap();

        assert!(result_array.is_null(0));
        assert!(result_array.is_null(1));
        assert_eq!(result_array.value(2), 2.0); // (1+2+3)/3
        assert_eq!(result_array.value(3), 3.0); // (2+3+4)/3
        assert_eq!(result_array.value(4), 4.0); // (3+4+5)/3
    }

    #[test]
    fn test_ema() {
        let values = Arc::new(Float64Array::from(vec![1.0, 2.0, 3.0, 4.0, 5.0])) as ArrayRef;
        let result = ema(&values, 3).unwrap();
        let result_array = as_float64_array(&result).unwrap();

        assert_eq!(result_array.value(0), 1.0); // First value
        assert!(result_array.value(1) > 1.0 && result_array.value(1) < 2.0);
    }
}
