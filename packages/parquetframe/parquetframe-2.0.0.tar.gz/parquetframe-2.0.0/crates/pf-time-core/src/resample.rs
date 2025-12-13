//! Resampling operations for time-series data.

use crate::error::{Result, TimeError};
use crate::index::Frequency;

/// Aggregation method for resampling.
#[derive(Debug, Clone)]
pub enum AggMethod {
    Mean,
    Sum,
    First,
    Last,
    Min,
    Max,
    Count,
}

/// Resample time-series data to a new frequency.
///
/// # Arguments
/// * `timestamps` - Original timestamps (nanoseconds since epoch)
/// * `values` - Original values
/// * `freq` - Target frequency (e.g., "1H", "30s")
/// * `method` - Aggregation method
///
/// # Returns
/// Tuple of (new_timestamps, new_values)
pub fn resample(
    timestamps: &[i64],
    values: &[f64],
    freq: &str,
    method: AggMethod,
) -> Result<(Vec<i64>, Vec<f64>)> {
    if timestamps.len() != values.len() {
        return Err(TimeError::ResampleError(
            "Timestamps and values must have same length".to_string(),
        ));
    }

    if timestamps.is_empty() {
        return Ok((vec![], vec![]));
    }

    // Parse frequency
    let frequency = Frequency::from_str(freq)
        .map_err(|e| TimeError::ResampleError(e))?;

    let freq_ns = frequency.to_nanoseconds();

    // Determine time range
    let min_time = *timestamps.iter().min().unwrap();
    let max_time = *timestamps.iter().max().unwrap();

    // Generate new time bins
    let mut new_timestamps = Vec::new();
    let mut current = min_time - (min_time % freq_ns); // Align to frequency

    while current <= max_time {
        new_timestamps.push(current);
        current += freq_ns;
    }

    // Aggregate values into bins
    let mut new_values = Vec::new();

    for &bin_start in &new_timestamps {
        let bin_end = bin_start + freq_ns;

        // Collect values in this bin
        let bin_values: Vec<f64> = timestamps
            .iter()
            .zip(values.iter())
            .filter(|(t, _)| **t >= bin_start && **t < bin_end)
            .map(|(_, v)| *v)
            .collect();

        // Apply aggregation
        let aggregated = match method {
            AggMethod::Mean => {
                if bin_values.is_empty() {
                    f64::NAN
                } else {
                    bin_values.iter().sum::<f64>() / bin_values.len() as f64
                }
            }
            AggMethod::Sum => bin_values.iter().sum(),
            AggMethod::First => bin_values.first().copied().unwrap_or(f64::NAN),
            AggMethod::Last => bin_values.last().copied().unwrap_or(f64::NAN),
            AggMethod::Min => {
                bin_values
                    .iter()
                    .copied()
                    .min_by(|a, b| a.partial_cmp(b).unwrap())
                    .unwrap_or(f64::NAN)
            }
            AggMethod::Max => {
                bin_values
                    .iter()
                    .copied()
                    .max_by(|a, b| a.partial_cmp(b).unwrap())
                    .unwrap_or(f64::NAN)
            }
            AggMethod::Count => bin_values.len() as f64,
        };

        new_values.push(aggregated);
    }

    Ok((new_timestamps, new_values))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_resample_mean() {
        let timestamps = vec![
            0,
            1_000_000_000, // 1 second
            2_000_000_000, // 2 seconds
            3_000_000_000, // 3 seconds
        ];
        let values = vec![1.0, 2.0, 3.0, 4.0];

        let (new_ts, new_vals) = resample(&timestamps, &values, "2s", AggMethod::Mean).unwrap();

        assert_eq!(new_ts.len(), 2);
        assert_eq!(new_vals[0], 1.5); // Mean of 1.0, 2.0
        assert_eq!(new_vals[1], 3.5); // Mean of 3.0, 4.0
    }

    #[test]
    fn test_resample_sum() {
        let timestamps = vec![0, 1_000_000_000, 2_000_000_000];
        let values = vec![1.0, 2.0, 3.0];

        let (_, new_vals) = resample(&timestamps, &values, "3s", AggMethod::Sum).unwrap();

        assert_eq!(new_vals[0], 6.0); // Sum of all values
    }
}
