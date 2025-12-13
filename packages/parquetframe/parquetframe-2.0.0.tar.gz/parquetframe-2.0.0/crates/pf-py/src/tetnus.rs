/// Python bindings for TETNUS tensor operations
use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use pyo3::types::PyList;
use numpy::{PyArrayDyn, PyArrayMethods, PyUntypedArrayMethods, IntoPyArray};
use tetnus_core::Tensor;

/// Convert TetnusError to PyErr
pub fn tetnus_err_to_py(err: tetnus_core::TetnusError) -> PyErr {
    PyValueError::new_err(format!("{}", err))
}

/// Python wrapper for Tensor
#[pyclass(name = "Tensor")]
#[derive(Clone)]
pub struct PyTensor {
    pub inner: Tensor,
}

#[pymethods]
impl PyTensor {
    /// Get tensor shape
    #[getter]
    fn shape(&self) -> Vec<usize> {
        self.inner.shape().to_vec()
    }

    /// Get number of dimensions
    #[getter]
    fn ndim(&self) -> usize {
        self.inner.ndim()
    }

    /// Get total number of elements
    #[getter]
    fn numel(&self) -> usize {
        self.inner.numel()
    }

    /// Get tensor data as Python list
    fn data(&self) -> Vec<f32> {
        self.inner.data()
    }

    /// Get gradient tensor (if computed)
    #[getter]
    fn grad(&self) -> Option<PyTensor> {
        self.inner.grad().map(|t| PyTensor { inner: t })
    }

    /// Check if tensor requires gradient
    #[getter]
    fn requires_grad(&self) -> bool {
        self.inner.0.requires_grad
    }

    /// Enable gradient tracking (returns new tensor)
    fn requires_grad_(&self) -> PyTensor {
        PyTensor {
            inner: self.inner.clone().requires_grad_(),
        }
    }

    /// String representation
    fn __repr__(&self) -> String {
        format!(
            "Tensor(shape={:?}, requires_grad={})",
            self.shape(),
            self.requires_grad()
        )
    }

    /// Convert tensor to NumPy array
    fn to_numpy<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyArrayDyn<f32>>> {
        let data = self.inner.data();
        let shape = self.shape();
        // Convert to 1D array first, then reshape
        let arr = data.into_pyarray(py);
        arr.reshape(shape)
    }

    /// Create tensor from NumPy array
    #[staticmethod]
    fn from_numpy(array: &Bound<'_, PyArrayDyn<f32>>) -> PyResult<PyTensor> {
        let shape: Vec<usize> = array.shape().to_vec();
        let data: Vec<f32> = array.to_vec()?;

        Tensor::new(data, shape)
            .map(|t| PyTensor { inner: t })
            .map_err(tetnus_err_to_py)
    }
}

/// Create tensor filled with zeros
#[pyfunction]
fn zeros(shape: Vec<usize>) -> PyResult<PyTensor> {
    Tensor::zeros(shape)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Create tensor filled with ones
#[pyfunction]
fn ones(shape: Vec<usize>) -> PyResult<PyTensor> {
    Tensor::ones(shape)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Create tensor with evenly spaced values
#[pyfunction]
fn arange(start: f32, stop: f32, step: f32) -> PyResult<PyTensor> {
    Tensor::arange(start, stop, step)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Create tensor with linearly spaced values
#[pyfunction]
fn linspace(start: f32, stop: f32, num: usize) -> PyResult<PyTensor> {
    Tensor::linspace(start, stop, num)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Create identity matrix
#[pyfunction]
fn eye(n: usize, m: Option<usize>) -> PyResult<PyTensor> {
    Tensor::eye(n, m)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Create tensor filled with random values [0, 1)
#[pyfunction]
fn rand(shape: Vec<usize>) -> PyResult<PyTensor> {
    Tensor::rand(shape)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Create tensor with random values from standard normal distribution
#[pyfunction]
fn randn(shape: Vec<usize>) -> PyResult<PyTensor> {
    Tensor::randn(shape)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Create tensor filled with a constant value
#[pyfunction]
fn full(shape: Vec<usize>, value: f32) -> PyResult<PyTensor> {
    Tensor::full(shape, value)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Element-wise sine
#[pyfunction]
fn sin(tensor: &PyTensor) -> PyResult<PyTensor> {
    tetnus_core::ops::elementwise::sin(&tensor.inner)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Element-wise cosine
#[pyfunction]
fn cos(tensor: &PyTensor) -> PyResult<PyTensor> {
    tetnus_core::ops::elementwise::cos(&tensor.inner)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Element-wise tangent
#[pyfunction]
fn tan(tensor: &PyTensor) -> PyResult<PyTensor> {
    tetnus_core::ops::elementwise::tan(&tensor.inner)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Element-wise exponential
#[pyfunction]
fn exp(tensor: &PyTensor) -> PyResult<PyTensor> {
    tetnus_core::ops::elementwise::exp(&tensor.inner)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Element-wise natural logarithm
#[pyfunction]
fn log(tensor: &PyTensor) -> PyResult<PyTensor> {
    tetnus_core::ops::elementwise::log(&tensor.inner)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Element-wise square root
#[pyfunction]
fn sqrt(tensor: &PyTensor) -> PyResult<PyTensor> {
    tetnus_core::ops::elementwise::sqrt(&tensor.inner)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Rectified Linear Unit
#[pyfunction]
fn relu(tensor: &PyTensor) -> PyResult<PyTensor> {
    tetnus_core::ops::elementwise::relu(&tensor.inner)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Create tensor from Python list
#[pyfunction]
fn from_list(_py: Python, data: &Bound<'_, PyList>, shape: Vec<usize>) -> PyResult<PyTensor> {
    // Extract f32 values from Python list
    let mut flat_data = Vec::new();

    fn extract_nested(list: &Bound<'_, PyList>, output: &mut Vec<f32>) -> PyResult<()> {
        for item in list.iter() {
            if let Ok(nested) = item.downcast::<PyList>() {
                extract_nested(&nested, output)?;
            } else if let Ok(val) = item.extract::<f32>() {
                output.push(val);
            } else {
                return Err(PyValueError::new_err("List must contain only numbers"));
            }
        }
        Ok(())
    }

    extract_nested(data, &mut flat_data)?;

    Tensor::new(flat_data, shape)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Matrix multiplication
#[pyfunction]
fn matmul(a: &PyTensor, b: &PyTensor) -> PyResult<PyTensor> {
    tetnus_core::ops::matmul::matmul(&a.inner, &b.inner)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Element-wise addition
#[pyfunction]
fn add(a: &PyTensor, b: &PyTensor) -> PyResult<PyTensor> {
    tetnus_core::ops::elementwise::add(&a.inner, &b.inner)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Element-wise subtraction
#[pyfunction]
fn sub(a: &PyTensor, b: &PyTensor) -> PyResult<PyTensor> {
    tetnus_core::ops::elementwise::sub(&a.inner, &b.inner)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Element-wise division
#[pyfunction]
fn div(a: &PyTensor, b: &PyTensor) -> PyResult<PyTensor> {
    tetnus_core::ops::elementwise::div(&a.inner, &b.inner)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Element-wise multiplication
#[pyfunction]
fn mul(a: &PyTensor, b: &PyTensor) -> PyResult<PyTensor> {
    tetnus_core::ops::elementwise::mul(&a.inner, &b.inner)
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Reshape tensor
#[pyfunction]
fn reshape(tensor: &PyTensor, new_shape: Vec<usize>) -> PyResult<PyTensor> {
    use tetnus_core::ops::Op;

    let op = tetnus_core::ops::view::ReshapeOp::new(
        tensor.inner.shape().to_vec(),
        new_shape
    );

    op.forward(&[&tensor.inner])
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Transpose 2D tensor
#[pyfunction]
fn transpose(tensor: &PyTensor) -> PyResult<PyTensor> {
    use tetnus_core::ops::Op;

    let op = tetnus_core::ops::view::TransposeOp::new(tensor.inner.shape().to_vec());

    op.forward(&[&tensor.inner])
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Sum all elements
#[pyfunction]
fn sum(tensor: &PyTensor) -> PyResult<PyTensor> {
    use tetnus_core::ops::Op;

    let op = tetnus_core::ops::reduce::SumOp::new(tensor.inner.shape().to_vec());

    op.forward(&[&tensor.inner])
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Mean of all elements
#[pyfunction]
fn mean(tensor: &PyTensor) -> PyResult<PyTensor> {
    use tetnus_core::ops::Op;

    let op = tetnus_core::ops::reduce::MeanOp::new(tensor.inner.shape().to_vec());

    op.forward(&[&tensor.inner])
        .map(|t| PyTensor { inner: t })
        .map_err(tetnus_err_to_py)
}

/// Compute gradients via backpropagation
#[pyfunction]
fn backward(tensor: &PyTensor) -> PyResult<()> {
    tetnus_core::backward(&tensor.inner)
        .map_err(tetnus_err_to_py)
}

/// Register TETNUS functions in the _rustic module
pub fn register_tetnus_functions(parent: &Bound<'_, PyModule>) -> PyResult<()> {
    let m = PyModule::new(parent.py(), "tetnus")?;

    // Register class
    m.add_class::<PyTensor>()?;

    // Register functions
    m.add_function(wrap_pyfunction!(zeros, &m)?)?;
    m.add_function(wrap_pyfunction!(ones, &m)?)?;
    m.add_function(wrap_pyfunction!(arange, &m)?)?;
    m.add_function(wrap_pyfunction!(linspace, &m)?)?;
    m.add_function(wrap_pyfunction!(eye, &m)?)?;
    m.add_function(wrap_pyfunction!(rand, &m)?)?;
    m.add_function(wrap_pyfunction!(randn, &m)?)?;
    m.add_function(wrap_pyfunction!(full, &m)?)?;
    m.add_function(wrap_pyfunction!(from_list, &m)?)?;
    m.add_function(wrap_pyfunction!(matmul, &m)?)?;
    m.add_function(wrap_pyfunction!(add, &m)?)?;
    m.add_function(wrap_pyfunction!(sub, &m)?)?;
    m.add_function(wrap_pyfunction!(mul, &m)?)?;
    m.add_function(wrap_pyfunction!(div, &m)?)?;
    m.add_function(wrap_pyfunction!(reshape, &m)?)?;
    m.add_function(wrap_pyfunction!(transpose, &m)?)?;
    m.add_function(wrap_pyfunction!(sum, &m)?)?;
    m.add_function(wrap_pyfunction!(mean, &m)?)?;
    m.add_function(wrap_pyfunction!(backward, &m)?)?;
    m.add_function(wrap_pyfunction!(sin, &m)?)?;
    m.add_function(wrap_pyfunction!(cos, &m)?)?;
    m.add_function(wrap_pyfunction!(tan, &m)?)?;
    m.add_function(wrap_pyfunction!(exp, &m)?)?;
    m.add_function(wrap_pyfunction!(log, &m)?)?;
    m.add_function(wrap_pyfunction!(sqrt, &m)?)?;
    m.add_function(wrap_pyfunction!(relu, &m)?)?;

    // Register NN submodule
    crate::tetnus_nn::register_nn_module(&m)?;

    // Register Optim submodule
    crate::tetnus_optim::register_optim_module(&m)?;

    // Register Graph submodule
    crate::tetnus_graph::register_tetnus_graph_module(parent.py(), &m)?;

    // Register LLM submodule
    crate::tetnus_llm::register_tetnus_llm_module(parent.py(), &m)?;

    // Register Edge submodule
    crate::tetnus_edge::register_tetnus_edge_module(parent.py(), &m)?;

    parent.add_submodule(&m)?;
    Ok(())
}
