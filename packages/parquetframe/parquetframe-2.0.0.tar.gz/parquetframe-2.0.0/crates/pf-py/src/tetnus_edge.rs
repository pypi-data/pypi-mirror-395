use pyo3::prelude::*;
use tetnus_coral_driver::{CoralContext, CoralError};

#[pyclass(name = "EdgeModel")]
pub struct PyEdgeModel {
    context: CoralContext,
}

#[pymethods]
impl PyEdgeModel {
    #[staticmethod]
    fn load(model_path: &str) -> PyResult<Self> {
        // Read model file
        let model_data = std::fs::read(model_path)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("Failed to read model: {}", e)))?;

        // Create Coral context
        let context = CoralContext::new(&model_data)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Failed to load model: {}", e)))?;

        Ok(PyEdgeModel { context })
    }

    fn invoke(&self, input: Vec<u8>, output_size: usize) -> PyResult<Vec<u8>> {
        let mut output = vec![0u8; output_size];

        self.context.invoke(&input, &mut output)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Inference failed: {}", e)))?;

        Ok(output)
    }
}

pub fn register_tetnus_edge_module(py: Python, parent_module: &Bound<'_, PyModule>) -> PyResult<()> {
    let m = PyModule::new(py, "edge")?;
    m.add_class::<PyEdgeModel>()?;
    parent_module.add_submodule(&m)?;
    Ok(())
}
