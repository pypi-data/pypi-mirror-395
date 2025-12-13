//! Python bindings for TETNUS NN (Neural Network) module
use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use tetnus_nn::{Linear, ReLU, Sequential, Embedding, LayerNorm, NumericalProcessor, CategoricalProcessor, Module as _};
use tetnus_nn::loss::{MSELoss, CrossEntropyLoss};
use crate::tetnus::{PyTensor, tetnus_err_to_py};

/// Embedding Layer
#[pyclass(name = "Embedding")]
#[derive(Clone)]
pub struct PyEmbedding {
    inner: Embedding,
}

#[pymethods]
impl PyEmbedding {
    #[new]
    fn new(num_embeddings: usize, embedding_dim: usize) -> PyResult<Self> {
        Embedding::new(num_embeddings, embedding_dim)
            .map(|inner| PyEmbedding { inner })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    fn forward(&self, input: &PyTensor) -> PyResult<PyTensor> {
        self.inner.forward(&input.inner)
            .map(|t| PyTensor { inner: t })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    fn parameters(&self) -> Vec<PyTensor> {
        self.inner.parameters()
            .into_iter()
            .map(|t| PyTensor { inner: t })
            .collect()
    }
}

/// Layer Normalization
#[pyclass(name = "LayerNorm")]
#[derive(Clone)]
pub struct PyLayerNorm {
    inner: LayerNorm,
}

#[pymethods]
impl PyLayerNorm {
    #[new]
    fn new(normalized_shape: Vec<usize>, eps: Option<f32>) -> PyResult<Self> {
        LayerNorm::new(normalized_shape, eps.unwrap_or(1e-5))
            .map(|inner| PyLayerNorm { inner })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    fn forward(&self, input: &PyTensor) -> PyResult<PyTensor> {
        self.inner.forward(&input.inner)
            .map(|t| PyTensor { inner: t })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    fn parameters(&self) -> Vec<PyTensor> {
        self.inner.parameters()
            .into_iter()
            .map(|t| PyTensor { inner: t })
            .collect()
    }
}

/// Numerical Processor
#[pyclass(name = "NumericalProcessor")]
#[derive(Clone)]
pub struct PyNumericalProcessor {
    inner: NumericalProcessor,
}

#[pymethods]
impl PyNumericalProcessor {
    #[new]
    fn new() -> PyResult<Self> {
        NumericalProcessor::new()
            .map(|inner| PyNumericalProcessor { inner })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    fn forward(&self, input: &PyTensor) -> PyResult<PyTensor> {
        self.inner.forward(&input.inner)
            .map(|t| PyTensor { inner: t })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    fn parameters(&self) -> Vec<PyTensor> {
        self.inner.parameters()
            .into_iter()
            .map(|t| PyTensor { inner: t })
            .collect()
    }
}

/// Categorical Processor
#[pyclass(name = "CategoricalProcessor")]
#[derive(Clone)]
pub struct PyCategoricalProcessor {
    inner: CategoricalProcessor,
}

#[pymethods]
impl PyCategoricalProcessor {
    #[new]
    fn new(num_categories: usize, embedding_dim: usize) -> PyResult<Self> {
        CategoricalProcessor::new(num_categories, embedding_dim)
            .map(|inner| PyCategoricalProcessor { inner })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    fn forward(&self, input: &PyTensor) -> PyResult<PyTensor> {
        self.inner.forward(&input.inner)
            .map(|t| PyTensor { inner: t })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    fn parameters(&self) -> Vec<PyTensor> {
        self.inner.parameters()
            .into_iter()
            .map(|t| PyTensor { inner: t })
            .collect()
    }
}

/// Linear layer (fully connected)
#[pyclass(name = "Linear")]
#[derive(Clone)]
pub struct PyLinear {
    inner: Linear,
}

#[pymethods]
impl PyLinear {
    #[new]
    #[pyo3(signature = (in_features, out_features, bias=true))]
    fn new(in_features: usize, out_features: usize, bias: bool) -> PyResult<Self> {
        Linear::new(in_features, out_features, bias)
            .map(|inner| PyLinear { inner })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    fn forward(&self, input: &PyTensor) -> PyResult<PyTensor> {
        self.inner.forward(&input.inner)
            .map(|t| PyTensor { inner: t })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    fn parameters(&self) -> Vec<PyTensor> {
        self.inner.parameters()
            .into_iter()
            .map(|t| PyTensor { inner: t })
            .collect()
    }
}

/// ReLU Activation
#[pyclass(name = "ReLU")]
#[derive(Clone)]
pub struct PyReLU {
    inner: ReLU,
}

#[pymethods]
impl PyReLU {
    #[new]
    fn new() -> Self {
        PyReLU {
            inner: ReLU::new(),
        }
    }

    fn forward(&self, input: &PyTensor) -> PyResult<PyTensor> {
        self.inner.forward(&input.inner)
            .map(|t| PyTensor { inner: t })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }
}

/// Sequential Container
#[pyclass(name = "Sequential")]
pub struct PySequential {
    inner: Sequential,
}

#[pymethods]
impl PySequential {
    #[new]
    fn new() -> Self {
        PySequential {
            inner: Sequential::new(),
        }
    }

    fn add(&mut self, module: Bound<'_, PyAny>) -> PyResult<()> {
        if let Ok(linear) = module.extract::<PyLinear>() {
            self.inner.add(Box::new(linear.inner));
        } else if let Ok(relu) = module.extract::<PyReLU>() {
            self.inner.add(Box::new(relu.inner));
        } else if let Ok(emb) = module.extract::<PyEmbedding>() {
            self.inner.add(Box::new(emb.inner));
        } else if let Ok(norm) = module.extract::<PyLayerNorm>() {
            self.inner.add(Box::new(norm.inner));
        } else if let Ok(num) = module.extract::<PyNumericalProcessor>() {
            self.inner.add(Box::new(num.inner));
        } else if let Ok(cat) = module.extract::<PyCategoricalProcessor>() {
            self.inner.add(Box::new(cat.inner));
        } else {
            return Err(PyValueError::new_err("Unsupported module type"));
        }
        Ok(())
    }

    fn forward(&self, input: &PyTensor) -> PyResult<PyTensor> {
        self.inner.forward(&input.inner)
            .map(|t| PyTensor { inner: t })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    fn parameters(&self) -> Vec<PyTensor> {
        self.inner.parameters()
            .into_iter()
            .map(|t| PyTensor { inner: t })
            .collect()
    }
}

/// Mean Squared Error Loss
#[pyclass(name = "MSELoss")]
pub struct PyMSELoss {
    inner: MSELoss,
}

#[pymethods]
impl PyMSELoss {
    #[new]
    fn new() -> Self {
        PyMSELoss { inner: MSELoss::new() }
    }

    fn forward(&self, input: &PyTensor, target: &PyTensor) -> PyResult<PyTensor> {
        self.inner.forward(&input.inner, &target.inner)
            .map(|t| PyTensor { inner: t })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }
}

/// Cross Entropy Loss
#[pyclass(name = "CrossEntropyLoss")]
pub struct PyCrossEntropyLoss {
    inner: CrossEntropyLoss,
}

#[pymethods]
impl PyCrossEntropyLoss {
    #[new]
    fn new() -> Self {
        PyCrossEntropyLoss { inner: CrossEntropyLoss::new() }
    }

    fn forward(&self, input: &PyTensor, target: &PyTensor) -> PyResult<PyTensor> {
        self.inner.forward(&input.inner, &target.inner)
            .map(|t| PyTensor { inner: t })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }
}

/// Register NN functions and classes
pub fn register_nn_module(parent: &Bound<'_, PyModule>) -> PyResult<()> {
    let m = PyModule::new(parent.py(), "nn")?;

    m.add_class::<PyLinear>()?;
    m.add_class::<PyReLU>()?;
    m.add_class::<PySequential>()?;
    m.add_class::<PyEmbedding>()?;
    m.add_class::<PyLayerNorm>()?;
    m.add_class::<PyNumericalProcessor>()?;
    m.add_class::<PyCategoricalProcessor>()?;
    m.add_class::<PyMSELoss>()?;
    m.add_class::<PyCrossEntropyLoss>()?;

    parent.add_submodule(&m)?;
    Ok(())
}
