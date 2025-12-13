//! As-of join operations for point-in-time correctness.

use crate::error::{Result, TimeError};

/// As-of join strategy.
#[derive(Debug, Clone, Copy)]
pub enum AsofStrategy {
    /// Use the most recent value before or at the timestamp
    Backward,
    /// Use the next value after or at the timestamp
    Forward,
    /// Use the nearest value (before or after)
    Nearest,
}

/// Perform as-of join.
///
/// For each timestamp in `left_times`, find the corresponding value from `right_times`
/// based on the specified strategy.
///
/// # Arguments
/// * `left_times` - Query timestamps
/// * `right_times` - Reference timestamps
/// * `right_values` - Values associated with reference timestamps
/// * `strategy` - Join strategy (backward, forward, nearest)
/// * `tolerance_ns` - Maximum time difference (in nanoseconds), None for no limit
///
/// # Returns
/// Vector of matched values (NaN if no match within tolerance)
pub fn asof_join(
    left_times: &[i64],
    right_times: &[i64],
    right_values: &[f64],
    strategy: AsofStrategy,
    tolerance_ns: Option<i64>,
) -> Result<Vec<f64>> {
    if right_times.len() != right_values.len() {
        return Err(TimeError::AsofError(
            "Right times and values must have same length".to_string(),
        ));
    }

    // Check if right times are sorted
    if !right_times.windows(2).all(|w| w[0] <= w[1]) {
        return Err(TimeError::AsofError(
            "Right timestamps must be sorted".to_string(),
        ));
    }

    let mut result = Vec::with_capacity(left_times.len());

    for &left_time in left_times {
        let matched_value = match strategy {
            AsofStrategy::Backward => find_backward(left_time, right_times, right_values, tolerance_ns),
            AsofStrategy::Forward => find_forward(left_time, right_times, right_values, tolerance_ns),
            AsofStrategy::Nearest => find_nearest(left_time, right_times, right_values, tolerance_ns),
        };

        result.push(matched_value);
    }

    Ok(result)
}

fn find_backward(
    target: i64,
    times: &[i64],
    values: &[f64],
    tolerance: Option<i64>,
) -> f64 {
    // Binary search for the position
    let pos = match times.binary_search(&target) {
        Ok(i) => i, // Exact match
        Err(i) => {
            if i == 0 {
                return f64::NAN; // No earlier value
            }
            i - 1 // Use the previous index
        }
    };

    let time_diff = (target - times[pos]).abs();

    if let Some(tol) = tolerance {
        if time_diff > tol {
            return f64::NAN;
        }
    }

    values[pos]
}

fn find_forward(
    target: i64,
    times: &[i64],
    values: &[f64],
    tolerance: Option<i64>,
) -> f64 {
    let pos = match times.binary_search(&target) {
        Ok(i) => i, // Exact match
        Err(i) => {
            if i >= times.len() {
                return f64::NAN; // No later value
            }
            i
        }
    };

    let time_diff = (times[pos] - target).abs();

    if let Some(tol) = tolerance {
        if time_diff > tol {
            return f64::NAN;
        }
    }

    values[pos]
}

fn find_nearest(
    target: i64,
    times: &[i64],
    values: &[f64],
    tolerance: Option<i64>,
) -> f64 {
    let backward = find_backward(target, times, values, None);
    let forward = find_forward(target, times, values, None);

    if backward.is_nan() && forward.is_nan() {
        return f64::NAN;
    }

    if backward.is_nan() {
        let pos = times.binary_search(&target).unwrap_or_else(|i| i);
        let diff = (times[pos] - target).abs();
        return if tolerance.map_or(true, |tol| diff <= tol) {
            forward
        } else {
            f64::NAN
        };
    }

    if forward.is_nan() {
        let pos = match times.binary_search(&target) {
            Ok(i) => i,
            Err(i) => i - 1,
        };
        let diff = (target - times[pos]).abs();
        return if tolerance.map_or(true, |tol| diff <= tol) {
            backward
        } else {
            f64::NAN
        };
    }

    // Both exist, find nearest
    let back_pos = match times.binary_search(&target) {
        Ok(i) => i,
        Err(i) => i - 1,
    };
    let fwd_pos = match times.binary_search(&target) {
        Ok(i) => i,
        Err(i) => i,
    };

    let back_diff = (target - times[back_pos]).abs();
    let fwd_diff = (times[fwd_pos] - target).abs();

    let nearest_val = if back_diff <= fwd_diff { backward } else { forward };
    let nearest_diff = back_diff.min(fwd_diff);

    if tolerance.map_or(true, |tol| nearest_diff <= tol) {
        nearest_val
    } else {
        f64::NAN
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_asof_backward() {
        let left = vec![150, 250, 350];
        let right = vec![100, 200, 300, 400];
        let values = vec![1.0, 2.0, 3.0, 4.0];

        let result = asof_join(&left, &right, &values, AsofStrategy::Backward, None).unwrap();

        assert_eq!(result[0], 1.0); // 150 -> 100
        assert_eq!(result[1], 2.0); // 250 -> 200
        assert_eq!(result[2], 3.0); // 350 -> 300
    }

    #[test]
    fn test_asof_forward() {
        let left = vec![150, 250, 350];
        let right = vec![100, 200, 300, 400];
        let values = vec![1.0, 2.0, 3.0, 4.0];

        let result = asof_join(&left, &right, &values, AsofStrategy::Forward, None).unwrap();

        assert_eq!(result[0], 2.0); // 150 -> 200
        assert_eq!(result[1], 3.0); // 250 -> 300
        assert_eq!(result[2], 4.0); // 350 -> 400
    }

    #[test]
    fn test_asof_with_tolerance() {
        let left = vec![150];
        let right = vec![100];
        let values = vec![1.0];

        // Within tolerance (50 diff, backward lookup should work)
        let result = asof_join(&left, &right, &values, AsofStrategy::Backward, Some(100)).unwrap();
        assert_eq!(result[0], 1.0); // Should match since diff is within tolerance

        // Outside tolerance
        let result = asof_join(&left, &right, &values, AsofStrategy::Backward, Some(25)).unwrap();
        assert!(result[0].is_nan()); // Should be NaN since diff > tolerance
    }
}
