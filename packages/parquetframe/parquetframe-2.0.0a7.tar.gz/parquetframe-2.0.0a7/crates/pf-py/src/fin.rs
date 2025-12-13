/// PyO3 bindings for financial analytics (pf-fin-core).

use pyo3::prelude::*;
use pyo3::types::PyList;
use numpy::{PyArray1, PyReadonlyArray1};
use pf_fin_core::indicators;
use arrow_array::{Float64Array, ArrayRef, Array};
use std::sync::Arc;

/// Convert numpy array to Arrow Float64Array.
fn numpy_to_arrow_f64(arr: PyReadonlyArray1<f64>) -> ArrayRef {
    let slice = arr.as_slice().unwrap();
    Arc::new(Float64Array::from(slice.to_vec())) as ArrayRef
}

/// Convert Arrow ArrayRef to numpy array.
fn arrow_to_numpy<'py>(py: Python<'py>, arr: &ArrayRef) -> PyResult<Bound<'py, PyArray1<f64>>> {
    let float_array = arr
        .as_any()
        .downcast_ref::<Float64Array>()
        .ok_or_else(|| pyo3::exceptions::PyTypeError::new_err("Expected Float64Array"))?;

    let mut values = Vec::with_capacity(float_array.len());
    for i in 0..float_array.len() {
        if float_array.is_null(i) {
            values.push(f64::NAN);
        } else {
            values.push(float_array.value(i));
        }
    }

    Ok(PyArray1::from_vec(py, values))
}

/// Calculate Simple Moving Average.
#[pyfunction]
fn fin_sma<'py>(
    py: Python<'py>,
    values: PyReadonlyArray1<f64>,
    window: usize,
) -> PyResult<Bound<'py, PyArray1<f64>>> {
    let arrow_values = numpy_to_arrow_f64(values);
    let result = indicators::sma(&arrow_values, window)
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{}", e)))?;
    arrow_to_numpy(py, &result)
}

/// Calculate Exponential Moving Average.
#[pyfunction]
fn fin_ema<'py>(
    py: Python<'py>,
    values: PyReadonlyArray1<f64>,
    span: usize,
) -> PyResult<Bound<'py, PyArray1<f64>>> {
    let arrow_values = numpy_to_arrow_f64(values);
    let result = indicators::ema(&arrow_values, span)
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{}", e)))?;
    arrow_to_numpy(py, &result)
}

/// Calculate Relative Strength Index.
#[pyfunction]
fn fin_rsi<'py>(
    py: Python<'py>,
    values: PyReadonlyArray1<f64>,
    window: usize,
) -> PyResult<Bound<'py, PyArray1<f64>>> {
    let arrow_values = numpy_to_arrow_f64(values);
    let result = indicators::rsi(&arrow_values, window)
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{}", e)))?;
    arrow_to_numpy(py, &result)
}

/// Calculate Bollinger Bands.
#[pyfunction]
fn fin_bollinger_bands<'py>(
    py: Python<'py>,
    values: PyReadonlyArray1<f64>,
    window: usize,
    num_std: f64,
) -> PyResult<(Bound<'py, PyArray1<f64>>, Bound<'py, PyArray1<f64>>, Bound<'py, PyArray1<f64>>)> {
    let arrow_values = numpy_to_arrow_f64(values);
    let (upper, middle, lower) = indicators::bollinger_bands(&arrow_values, window, num_std)
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{}", e)))?;

    Ok((
        arrow_to_numpy(py, &upper)?,
        arrow_to_numpy(py, &middle)?,
        arrow_to_numpy(py, &lower)?,
    ))
}

/// Register financial functions with Python module.
pub fn register_fin_functions(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fin_sma, m)?)?;
    m.add_function(wrap_pyfunction!(fin_ema, m)?)?;
    m.add_function(wrap_pyfunction!(fin_rsi, m)?)?;
    m.add_function(wrap_pyfunction!(fin_bollinger_bands, m)?)?;
    Ok(())
}
