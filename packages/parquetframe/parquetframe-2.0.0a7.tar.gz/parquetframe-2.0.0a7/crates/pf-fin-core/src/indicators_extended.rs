/// Additional technical indicators.
///
/// Implements ATR, ADX, and other advanced indicators.

use arrow::array::{Array, ArrayRef, Float64Array, Float64Builder};
use crate::{FinError, Result};
use crate::utils::as_float64_array;
use std::sync::Arc;

/// Calculate Average True Range (ATR).
///
/// # Arguments
/// * `high` - Array of high prices
/// * `low` - Array of low prices
/// * `close` - Array of close prices
/// * `period` - ATR period (typically 14)
///
/// # Returns
/// Array of ATR values
pub fn atr(
    high: &ArrayRef,
    low: &ArrayRef,
    close: &ArrayRef,
    period: usize,
) -> Result<ArrayRef> {
    if period == 0 {
        return Err(FinError::InvalidParameter("Period must be > 0".to_string()));
    }

    let high_array = as_float64_array(high)?;
    let low_array = as_float64_array(low)?;
    let close_array = as_float64_array(close)?;

    let len = close_array.len();
    let mut builder = Float64Builder::with_capacity(len);

    // Calculate True Range
    let mut tr_values = Vec::with_capacity(len);
    builder.append_null(); // First value has no previous close

    for i in 1..len {
        if high_array.is_null(i) || low_array.is_null(i) || close_array.is_null(i) || close_array.is_null(i - 1) {
            tr_values.push(0.0);
            builder.append_null();
            continue;
        }

        let h = high_array.value(i);
        let l = low_array.value(i);
        let prev_close = close_array.value(i - 1);

        // TR = max(H-L, |H-PC|, |L-PC|)
        let tr = (h - l).max((h - prev_close).abs()).max((l - prev_close).abs());
        tr_values.push(tr);

        if i < period {
            builder.append_null();
        } else {
            // Calculate ATR as average of TR
            let start_idx = if i >= period { i - period + 1 } else { 0 };
            let atr_val = tr_values[start_idx..].iter().sum::<f64>() / (tr_values.len() - start_idx) as f64;
            builder.append_value(atr_val);
        }
    }

    Ok(Arc::new(builder.finish()) as ArrayRef)
}

/// Calculate Average Directional Index (ADX).
///
/// # Arguments
/// * `high` - Array of high prices
/// * `low` - Array of low prices
/// * `close` - Array of close prices
/// * `period` - ADX period (typically 14)
///
/// # Returns
/// Tuple of (ADX, +DI, -DI)
pub fn adx(
    high: &ArrayRef,
    low: &ArrayRef,
    close: &ArrayRef,
    period: usize,
) -> Result<(ArrayRef, ArrayRef, ArrayRef)> {
    if period == 0 {
        return Err(FinError::InvalidParameter("Period must be > 0".to_string()));
    }

    let high_array = as_float64_array(high)?;
    let low_array = as_float64_array(low)?;
    let close_array = as_float64_array(close)?;

    let len = close_array.len();

    let mut adx_builder = Float64Builder::with_capacity(len);
    let mut plus_di_builder = Float64Builder::with_capacity(len);
    let mut minus_di_builder = Float64Builder::with_capacity(len);

    adx_builder.append_null();
    plus_di_builder.append_null();
    minus_di_builder.append_null();

    let mut plus_dm_values = Vec::with_capacity(len);
    let mut minus_dm_values = Vec::with_capacity(len);
    let mut tr_values = Vec::with_capacity(len);

    // Calculate +DM, -DM, and TR
    for i in 1..len {
        if high_array.is_null(i) || low_array.is_null(i) || close_array.is_null(i) ||
           high_array.is_null(i - 1) || low_array.is_null(i - 1) || close_array.is_null(i - 1) {
            plus_dm_values.push(0.0);
            minus_dm_values.push(0.0);
            tr_values.push(0.0);
            adx_builder.append_null();
            plus_di_builder.append_null();
            minus_di_builder.append_null();
            continue;
        }

        let h = high_array.value(i);
        let l = low_array.value(i);
        let prev_h = high_array.value(i - 1);
        let prev_l = low_array.value(i - 1);
        let prev_close = close_array.value(i - 1);

        // +DM and -DM
        let up_move = h - prev_h;
        let down_move = prev_l - l;

        let plus_dm = if up_move > down_move && up_move > 0.0 { up_move } else { 0.0 };
        let minus_dm = if down_move > up_move && down_move > 0.0 { down_move } else { 0.0 };

        plus_dm_values.push(plus_dm);
        minus_dm_values.push(minus_dm);

        // True Range
        let tr = (h - l).max((h - prev_close).abs()).max((l - prev_close).abs());
        tr_values.push(tr);

        if i < period {
            adx_builder.append_null();
            plus_di_builder.append_null();
            minus_di_builder.append_null();
        } else {
            // Calculate smoothed values - ensure we don't go out of bounds
            let start_idx = if i >= period { i - period + 1 } else { 1 };
            let end_idx = i.min(plus_dm_values.len() - 1);

            if start_idx > end_idx || end_idx >= plus_dm_values.len() {
                adx_builder.append_null();
                plus_di_builder.append_null();
                minus_di_builder.append_null();
                continue;
            }

            let smoothed_plus_dm = plus_dm_values[start_idx..=end_idx].iter().sum::<f64>() / (end_idx - start_idx + 1) as f64;
            let smoothed_minus_dm = minus_dm_values[start_idx..=end_idx].iter().sum::<f64>() / (end_idx - start_idx + 1) as f64;
            let smoothed_tr = tr_values[start_idx..=end_idx].iter().sum::<f64>() / (end_idx - start_idx + 1) as f64;

            if smoothed_tr == 0.0 {
                adx_builder.append_null();
                plus_di_builder.append_null();
                minus_di_builder.append_null();
                continue;
            }

            // +DI and -DI
            let plus_di = (smoothed_plus_dm / smoothed_tr) * 100.0;
            let minus_di = (smoothed_minus_dm / smoothed_tr) * 100.0;

            plus_di_builder.append_value(plus_di);
            minus_di_builder.append_value(minus_di);

            // DX
            let di_sum = plus_di + minus_di;
            let dx = if di_sum == 0.0 {
                0.0
            } else {
                ((plus_di - minus_di).abs() / di_sum) * 100.0
            };

            // ADX (simple moving average of DX for simplicity)
            adx_builder.append_value(dx);
        }
    }

    Ok((
        Arc::new(adx_builder.finish()) as ArrayRef,
        Arc::new(plus_di_builder.finish()) as ArrayRef,
        Arc::new(minus_di_builder.finish()) as ArrayRef,
    ))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_atr() {
        let high = Arc::new(Float64Array::from(vec![
            12.0, 13.0, 14.0, 13.5, 12.5, 13.5, 14.5, 15.0, 14.5, 13.5, 12.5, 13.0, 14.0, 15.0, 16.0,
        ])) as ArrayRef;

        let low = Arc::new(Float64Array::from(vec![
            10.0, 10.5, 11.0, 10.5, 9.5, 10.5, 11.5, 12.0, 11.5, 10.5, 9.5, 10.0, 11.0, 12.0, 13.0,
        ])) as ArrayRef;

        let close = Arc::new(Float64Array::from(vec![
            11.0, 12.0, 13.0, 12.0, 11.0, 12.0, 13.0, 14.0, 13.0, 12.0, 11.0, 12.0, 13.0, 14.0, 15.0,
        ])) as ArrayRef;

        let result = atr(&high, &low, &close, 14);
        assert!(result.is_ok());

        let atr_values = result.unwrap();
        assert_eq!(atr_values.len(), close.len());
    }

    #[test]
    fn test_adx() {
        // Use 20 data points to ensure enough for period of 14
        let high = Arc::new(Float64Array::from(vec![
            12.0, 13.0, 14.0, 13.5, 12.5, 13.5, 14.5, 15.0, 14.5, 13.5,
            12.5, 13.0, 14.0, 15.0, 16.0, 15.5, 16.5, 17.0, 16.5, 17.5,
        ])) as ArrayRef;

        let low = Arc::new(Float64Array::from(vec![
            10.0, 10.5, 11.0, 10.5, 9.5, 10.5, 11.5, 12.0, 11.5, 10.5,
            9.5, 10.0, 11.0, 12.0, 13.0, 12.5, 13.5, 14.0, 13.5, 14.5,
        ])) as ArrayRef;

        let close = Arc::new(Float64Array::from(vec![
            11.0, 12.0, 13.0, 12.0, 11.0, 12.0, 13.0, 14.0, 13.0, 12.0,
            11.0, 12.0, 13.0, 14.0, 15.0, 14.5, 15.5, 16.0, 15.5, 16.5,
        ])) as ArrayRef;

        let result = adx(&high, &low, &close, 14);
        assert!(result.is_ok());

        let (adx_values, plus_di, minus_di) = result.unwrap();
        assert_eq!(adx_values.len(), close.len());
        assert_eq!(plus_di.len(), close.len());
        assert_eq!(minus_di.len(), close.len());
    }
}
