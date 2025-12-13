use pyo3::prelude::*;
use pf_workflow_core::{WorkflowRunner, WorkflowDefinition};
use std::fs::File;

#[pyfunction]
pub fn run_workflow(yaml_path: String) -> PyResult<()> {
    // 1. Parse YAML
    let file = File::open(&yaml_path).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyFileNotFoundError, _>(format!("Failed to open workflow file: {}", e))
    })?;

    let definition: WorkflowDefinition = serde_yaml::from_reader(file).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Failed to parse workflow YAML: {}", e))
    })?;

    // 2. Create Runner
    let mut runner = WorkflowRunner::new(definition);

    // 3. Register Executors
    // In a real app, we might want to register only requested ones or all available
    runner.register_executor("datafusion.sql", Box::new(pf_workflow_core::executors::datafusion::DataFusionSqlExecutor));
    runner.register_executor("parquet.read", Box::new(pf_workflow_core::executors::parquet::ParquetReadExecutor));
    runner.register_executor("parquet.write", Box::new(pf_workflow_core::executors::parquet::ParquetWriteExecutor));
    runner.register_executor("http.get", Box::new(pf_workflow_core::executors::http::HttpExecutor));
    runner.register_executor("tetnus.train", Box::new(pf_workflow_core::executors::ml::TetnusTrainExecutor));
    runner.register_executor("tetnus.predict", Box::new(pf_workflow_core::executors::ml::TetnusPredictExecutor));
    runner.register_executor("tetnus.compile", Box::new(pf_workflow_core::executors::ml::TetnusCompileExecutor));

    // 4. Run (async)
    // We need a tokio runtime
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async {
        runner.run().await
    }).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Workflow execution failed: {}", e))
    })?;

    Ok(())
}
