/// OHLCV (Open, High, Low, Close, Volume) operations for candlestick data.
///
/// Provides resampling and aggregation functions for financial time-series data.

use arrow::array::{Array, ArrayRef, Float64Array, Float64Builder, TimestampMillisecondArray};
use arrow::datatypes::TimeUnit;
use crate::{FinError, Result};
use crate::utils::as_float64_array;
use std::sync::Arc;
use std::collections::HashMap;

/// OHLCV data structure for candlestick aggregation.
#[derive(Debug, Clone)]
pub struct OHLCVBar {
    pub timestamp: i64,
    pub open: f64,
    pub high: f64,
    pub low: f64,
    pub close: f64,
    pub volume: f64,
}

/// Resample OHLCV data to a new timeframe.
///
/// # Arguments
/// * `timestamps` - Array of timestamps in milliseconds
/// * `open` - Array of open prices
/// * `high` - Array of high prices
/// * `low` - Array of low prices
/// * `close` - Array of close prices
/// * `volume` - Array of volumes
/// * `interval_ms` - Resampling interval in milliseconds
///
/// # Returns
/// Tuple of (timestamps, open, high, low, close, volume) arrays
pub fn resample_ohlcv(
    timestamps: &ArrayRef,
    open: &ArrayRef,
    high: &ArrayRef,
    low: &ArrayRef,
    close: &ArrayRef,
    volume: &ArrayRef,
    interval_ms: i64,
) -> Result<(ArrayRef, ArrayRef, ArrayRef, ArrayRef, ArrayRef, ArrayRef)> {
    if interval_ms <= 0 {
        return Err(FinError::InvalidParameter("Interval must be > 0".to_string()));
    }

    // Get timestamp array
    let ts_array = timestamps
        .as_any()
        .downcast_ref::<TimestampMillisecondArray>()
        .ok_or_else(|| FinError::InvalidParameter("Expected TimestampMillisecondArray".to_string()))?;

    let open_array = as_float64_array(open)?;
    let high_array = as_float64_array(high)?;
    let low_array = as_float64_array(low)?;
    let close_array = as_float64_array(close)?;
    let volume_array = as_float64_array(volume)?;

    let len = ts_array.len();

    // Group data into intervals
    let mut bars: HashMap<i64, Vec<usize>> = HashMap::new();

    for i in 0..len {
        if ts_array.is_null(i) {
            continue;
        }

        let ts = ts_array.value(i);
        let interval_key = (ts / interval_ms) * interval_ms;
        bars.entry(interval_key).or_insert_with(Vec::new).push(i);
    }

    // Sort intervals
    let mut interval_keys: Vec<i64> = bars.keys().copied().collect();
    interval_keys.sort_unstable();

    // Build output arrays
    let mut ts_builder = Vec::with_capacity(interval_keys.len());
    let mut open_builder = Float64Builder::with_capacity(interval_keys.len());
    let mut high_builder = Float64Builder::with_capacity(interval_keys.len());
    let mut low_builder = Float64Builder::with_capacity(interval_keys.len());
    let mut close_builder = Float64Builder::with_capacity(interval_keys.len());
    let mut volume_builder = Float64Builder::with_capacity(interval_keys.len());

    for interval_key in interval_keys {
        let indices = &bars[&interval_key];

        if indices.is_empty() {
            continue;
        }

        // Open: first value
        let first_idx = indices[0];
        let open_val = if !open_array.is_null(first_idx) {
            open_array.value(first_idx)
        } else {
            continue;
        };

        // Close: last value
        let last_idx = indices[indices.len() - 1];
        let close_val = if !close_array.is_null(last_idx) {
            close_array.value(last_idx)
        } else {
            continue;
        };

        // High: max value
        let mut high_val = f64::NEG_INFINITY;
        for &idx in indices {
            if !high_array.is_null(idx) {
                high_val = high_val.max(high_array.value(idx));
            }
        }

        // Low: min value
        let mut low_val = f64::INFINITY;
        for &idx in indices {
            if !low_array.is_null(idx) {
                low_val = low_val.min(low_array.value(idx));
            }
        }

        // Volume: sum
        let mut volume_val = 0.0;
        for &idx in indices {
            if !volume_array.is_null(idx) {
                volume_val += volume_array.value(idx);
            }
        }

        if high_val.is_finite() && low_val.is_finite() {
            ts_builder.push(interval_key);
            open_builder.append_value(open_val);
            high_builder.append_value(high_val);
            low_builder.append_value(low_val);
            close_builder.append_value(close_val);
            volume_builder.append_value(volume_val);
        }
    }

    Ok((
        Arc::new(TimestampMillisecondArray::from(ts_builder)) as ArrayRef,
        Arc::new(open_builder.finish()) as ArrayRef,
        Arc::new(high_builder.finish()) as ArrayRef,
        Arc::new(low_builder.finish()) as ArrayRef,
        Arc::new(close_builder.finish()) as ArrayRef,
        Arc::new(volume_builder.finish()) as ArrayRef,
    ))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ohlcv_resample() {
        // Create 1-second data
        let timestamps = Arc::new(TimestampMillisecondArray::from(vec![
            1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
        ])) as ArrayRef;

        let open = Arc::new(Float64Array::from(vec![
            100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0,
        ])) as ArrayRef;

        let high = Arc::new(Float64Array::from(vec![
            102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0, 110.0, 111.0,
        ])) as ArrayRef;

        let low = Arc::new(Float64Array::from(vec![
            99.0, 100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0,
        ])) as ArrayRef;

        let close = Arc::new(Float64Array::from(vec![
            101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0, 110.0,
        ])) as ArrayRef;

        let volume = Arc::new(Float64Array::from(vec![
            1000.0, 1100.0, 1200.0, 1300.0, 1400.0, 1500.0, 1600.0, 1700.0, 1800.0, 1900.0,
        ])) as ArrayRef;

        // Resample to 5-second intervals
        let result = resample_ohlcv(&timestamps, &open, &high, &low, &close, &volume, 5000);
        assert!(result.is_ok());

        let (ts_out, open_out, _high_out, _low_out, _close_out, _volume_out) = result.unwrap();

        // Should have at least 1 bar
        assert!(ts_out.len() >= 1, "Expected at least 1 bar, got {}", ts_out.len());
        assert_eq!(open_out.len(), ts_out.len());

        let open_out_array = as_float64_array(&open_out).unwrap();
        assert_eq!(open_out_array.value(0), 100.0); // First bar opens at 100
    }
}
