//! Rolling window operations for time-series data.

use crate::error::{Result, TimeError};

/// Apply rolling window mean.
///
/// # Arguments
/// * `values` - Input values
/// * `window` - Window size
///
/// # Returns
/// Vector of rolling means
pub fn rolling_mean(values: &[f64], window: usize) -> Result<Vec<f64>> {
    if window == 0 {
        return Err(TimeError::RollingError("Window size must be > 0".to_string()));
    }

    if values.is_empty() {
        return Ok(vec![]);
    }

    let mut result = Vec::with_capacity(values.len());

    for i in 0..values.len() {
        let start = if i + 1 < window { 0 } else { i + 1 - window };
        let window_values = &values[start..=i];
        let mean = window_values.iter().sum::<f64>() / window_values.len() as f64;
        result.push(mean);
    }

    Ok(result)
}

/// Apply rolling window standard deviation.
pub fn rolling_std(values: &[f64], window: usize) -> Result<Vec<f64>> {
    if window == 0 {
        return Err(TimeError::RollingError("Window size must be > 0".to_string()));
    }

    if values.is_empty() {
        return Ok(vec![]);
    }

    let mut result = Vec::with_capacity(values.len());

    for i in 0..values.len() {
        let start = if i + 1 < window { 0 } else { i + 1 - window };
        let window_values = &values[start..=i];

        let mean = window_values.iter().sum::<f64>() / window_values.len() as f64;
        let variance = window_values
            .iter()
            .map(|v| (v - mean).powi(2))
            .sum::<f64>()
            / window_values.len() as f64;
        let std = variance.sqrt();

        result.push(std);
    }

    Ok(result)
}

/// Apply rolling window minimum.
pub fn rolling_min(values: &[f64], window: usize) -> Result<Vec<f64>> {
    if window == 0 {
        return Err(TimeError::RollingError("Window size must be > 0".to_string()));
    }

    if values.is_empty() {
        return Ok(vec![]);
    }

    let mut result = Vec::with_capacity(values.len());

    for i in 0..values.len() {
        let start = if i + 1 < window { 0 } else { i + 1 - window };
        let window_values = &values[start..=i];
        let min = window_values
            .iter()
            .copied()
            .min_by(|a, b| a.partial_cmp(b).unwrap())
            .unwrap();
        result.push(min);
    }

    Ok(result)
}

/// Apply rolling window maximum.
pub fn rolling_max(values: &[f64], window: usize) -> Result<Vec<f64>> {
    if window == 0 {
        return Err(TimeError::RollingError("Window size must be > 0".to_string()));
    }

    if values.is_empty() {
        return Ok(vec![]);
    }

    let mut result = Vec::with_capacity(values.len());

    for i in 0..values.len() {
        let start = if i + 1 < window { 0 } else { i + 1 - window };
        let window_values = &values[start..=i];
        let max = window_values
            .iter()
            .copied()
            .max_by(|a, b| a.partial_cmp(b).unwrap())
            .unwrap();
        result.push(max);
    }

    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rolling_mean() {
        let values = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let result = rolling_mean(&values, 3).unwrap();

        assert_eq!(result.len(), 5);
        assert_eq!(result[0], 1.0); // [1]
        assert_eq!(result[1], 1.5); // [1, 2]
        assert_eq!(result[2], 2.0); // [1, 2, 3]
        assert_eq!(result[3], 3.0); // [2, 3, 4]
        assert_eq!(result[4], 4.0); // [3, 4, 5]
    }

    #[test]
    fn test_rolling_min_max() {
        let values = vec![3.0, 1.0, 4.0, 1.0, 5.0];

        let mins = rolling_min(&values, 2).unwrap();
        let maxs = rolling_max(&values, 2).unwrap();

        assert_eq!(mins[2], 1.0); // min of [1, 4]
        assert_eq!(maxs[2], 4.0); // max of [1, 4]
    }
}
