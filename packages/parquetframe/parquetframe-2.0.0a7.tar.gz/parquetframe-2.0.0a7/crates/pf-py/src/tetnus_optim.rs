//! Python bindings for TETNUS Optimizers
use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use tetnus_nn::optim::{SGD, Adam};
use crate::tetnus::{PyTensor, tetnus_err_to_py};

/// Stochastic Gradient Descent optimizer
#[pyclass(name = "SGD")]
pub struct PySGD {
    inner: SGD,
}

#[pymethods]
impl PySGD {
    #[new]
    #[pyo3(signature = (params, lr, momentum=0.0))]
    fn new(params: Vec<PyTensor>, lr: f32, momentum: f32) -> PyResult<Self> {
        let tensors: Vec<_> = params.into_iter().map(|p| p.inner).collect();
        Ok(PySGD {
            inner: SGD::new(tensors, lr).with_momentum(momentum)
        })
    }

    fn step(&mut self) -> PyResult<()> {
        self.inner.step().map_err(|e| PyValueError::new_err(e.to_string()))
    }

    fn zero_grad(&self) -> PyResult<()> {
        self.inner.zero_grad().map_err(|e| PyValueError::new_err(e.to_string()))
    }
}

/// Adam optimizer
#[pyclass(name = "Adam")]
pub struct PyAdam {
    inner: Adam,
}

#[pymethods]
impl PyAdam {
    #[new]
    fn new(params: Vec<PyTensor>, lr: f32) -> PyResult<Self> {
        let tensors: Vec<_> = params.into_iter().map(|p| p.inner).collect();
        Ok(PyAdam {
            inner: Adam::new(tensors, lr)
        })
    }

    fn step(&mut self) -> PyResult<()> {
        self.inner.step().map_err(|e| PyValueError::new_err(e.to_string()))
    }

    fn zero_grad(&self) -> PyResult<()> {
        self.inner.zero_grad().map_err(|e| PyValueError::new_err(e.to_string()))
    }
}

/// Register optim module
pub fn register_optim_module(parent: &Bound<'_, PyModule>) -> PyResult<()> {
    let m = PyModule::new(parent.py(), "optim")?;

    m.add_class::<PySGD>()?;
    m.add_class::<PyAdam>()?;

    parent.add_submodule(&m)?;
    Ok(())
}
