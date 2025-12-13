//! Python bindings for ParquetFrame Rust backend.
//!
//! This module provides PyO3 bindings that expose Rust functionality to Python.
//! It serves as the bridge between Python and Rust components.
//!
//! Phase 1: Graph Core - CSR/CSC, BFS, DFS implementations
//! Phase 2: I/O Fast-Paths - Parquet metadata and statistics
//! Phase 3.5: Workflow Engine - Parallel DAG execution

mod graph;
mod io;
mod time;
mod workflow;
mod fin;
mod geo;
mod mob;
mod tetnus;
mod tetnus_nn;
mod tetnus_optim;
mod tetnus_graph;
mod tetnus_llm;
mod tetnus_edge;

use pyo3::prelude::*;

/// Check if Rust backend is available.
///
/// This function is called by Python to detect if the Rust backend
/// was successfully compiled and loaded.
///
/// # Returns
/// Always returns `true` when the Rust module is loaded.
#[pyfunction]
fn rust_available() -> bool {
    true
}

/// Check if Rust workflow engine is available.
///
/// # Returns
/// Always returns `true` when the Rust module is loaded.
#[pyfunction]
fn workflow_rust_available() -> bool {
    true
}

/// Get the version of the Rust backend.
///
/// # Returns
/// Version string matching the workspace version
#[pyfunction]
fn rust_version() -> String {
    env!("CARGO_PKG_VERSION").to_string()
}

/// ParquetFrame Rust backend module.
///
/// This module is imported by Python as `parquetframe._rustic`.
/// It provides high-performance implementations of performance-critical operations.
#[pymodule]
fn _rustic(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Core detection functions
    m.add_function(wrap_pyfunction!(rust_available, m)?)?;
    m.add_function(wrap_pyfunction!(rust_version, m)?)?;
    m.add_function(wrap_pyfunction!(workflow_rust_available, m)?)?;

    // Graph algorithm functions
    match graph::register_graph_functions(m) {
        Ok(_) => {}
        Err(e) => eprintln!("Error registering graph functions: {:?}", e),
    }

    // I/O functions
    match io::register_io_functions(m) {
        Ok(_) => {}
        Err(e) => eprintln!("Error registering I/O functions: {:?}", e),
    }

    // Workflow engine functions
    // workflow::run_workflow is registered via #[pyfn] below

    // Time-series functions
    time::register_time_functions(m)?;

    // Financial analytics functions
    fin::register_fin_functions(m)?;
    geo::register_geo_functions(&m)?;
    // Register MOB functions
    mob::register_mob_functions(&m)?;

    // Register TETNUS functions
    tetnus::register_tetnus_functions(&m)?;

    #[pyfn(m)]
    #[pyo3(name = "run_workflow")]
    fn run_workflow_py(yaml_path: String) -> PyResult<()> {
        workflow::run_workflow(yaml_path)
    }

    Ok(())
}
