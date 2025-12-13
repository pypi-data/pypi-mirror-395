//! PyO3 bindings for time-series operations.

use pyo3::prelude::*;
use pyo3::types::PyBytes;
use pyo3::exceptions::PyValueError;

/// Resample time-series data using Rust backend.
///
/// Args:
///     timestamps (list[int]): Timestamps in nanoseconds
///     values (list[float]): Values
///     freq (str): Target frequency (e.g., "1H", "30s")
///     method (str): Aggregation method ("mean", "sum", "first", "last", "min", "max", "count")
///
/// Returns:
///     tuple: (new_timestamps, new_values)
#[pyfunction]
#[pyo3(signature = (timestamps, values, freq, method="mean"))]
fn resample_ts(
    timestamps: Vec<i64>,
    values: Vec<f64>,
    freq: String,
    method: &str,
) -> PyResult<(Vec<i64>, Vec<f64>)> {
    use pf_time_core::resample::{resample, AggMethod};

    let agg_method = match method {
        "mean" => AggMethod::Mean,
        "sum" => AggMethod::Sum,
        "first" => AggMethod::First,
        "last" => AggMethod::Last,
        "min" => AggMethod::Min,
        "max" => AggMethod::Max,
        "count" => AggMethod::Count,
        _ => return Err(PyValueError::new_err(format!("Unknown aggregation method: {}", method))),
    };

    resample(&timestamps, &values, &freq, agg_method)
        .map_err(|e| PyValueError::new_err(e.to_string()))
}

/// Apply rolling window mean.
///
/// Args:
///     values (list[float]): Input values
///     window (int): Window size
///
/// Returns:
///     list[float]: Rolling means
#[pyfunction]
fn rolling_mean_ts(values: Vec<f64>, window: usize) -> PyResult<Vec<f64>> {
    use pf_time_core::rolling::rolling_mean;

    rolling_mean(&values, window)
        .map_err(|e| PyValueError::new_err(e.to_string()))
}

/// Apply rolling window standard deviation.
#[pyfunction]
fn rolling_std_ts(values: Vec<f64>, window: usize) -> PyResult<Vec<f64>> {
    use pf_time_core::rolling::rolling_std;

    rolling_std(&values, window)
        .map_err(|e| PyValueError::new_err(e.to_string()))
}

/// Apply rolling window minimum.
#[pyfunction]
fn rolling_min_ts(values: Vec<f64>, window: usize) -> PyResult<Vec<f64>> {
    use pf_time_core::rolling::rolling_min;

    rolling_min(&values, window)
        .map_err(|e| PyValueError::new_err(e.to_string()))
}

/// Apply rolling window maximum.
#[pyfunction]
fn rolling_max_ts(values: Vec<f64>, window: usize) -> PyResult<Vec<f64>> {
    use pf_time_core::rolling::rolling_max;

    rolling_max(&values, window)
        .map_err(|e| PyValueError::new_err(e.to_string()))
}

/// Perform as-of join.
///
/// Args:
///     left_times (list[int]): Query timestamps
///     right_times (list[int]): Reference timestamps (must be sorted)
///     right_values (list[float]): Values for reference timestamps
///     strategy (str): Join strategy ("backward", "forward", "nearest")
///     tolerance_ns (int | None): Maximum time difference in nanoseconds
///
/// Returns:
///     list[float]: Matched values (NaN if no match)
#[pyfunction]
#[pyo3(signature = (left_times, right_times, right_values, strategy="backward", tolerance_ns=None))]
fn asof_join_ts(
    left_times: Vec<i64>,
    right_times: Vec<i64>,
    right_values: Vec<f64>,
    strategy: &str,
    tolerance_ns: Option<i64>,
) -> PyResult<Vec<f64>> {
    use pf_time_core::asof::{asof_join, AsofStrategy};

    let join_strategy = match strategy {
        "backward" => AsofStrategy::Backward,
        "forward" => AsofStrategy::Forward,
        "nearest" => AsofStrategy::Nearest,
        _ => return Err(PyValueError::new_err(format!("Unknown strategy: {}", strategy))),
    };

    asof_join(&left_times, &right_times, &right_values, join_strategy, tolerance_ns)
        .map_err(|e| PyValueError::new_err(e.to_string()))
}

/// Register time-series functions with the Python module.
pub fn register_time_functions(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(resample_ts, m)?)?;
    m.add_function(wrap_pyfunction!(rolling_mean_ts, m)?)?;
    m.add_function(wrap_pyfunction!(rolling_std_ts, m)?)?;
    m.add_function(wrap_pyfunction!(rolling_min_ts, m)?)?;
    m.add_function(wrap_pyfunction!(rolling_max_ts, m)?)?;
    m.add_function(wrap_pyfunction!(asof_join_ts, m)?)?;
    Ok(())
}
