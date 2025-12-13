//! Error types for workflow execution.
//!
//! This module defines all error types that can occur during workflow
//! execution, including DAG validation, step execution, and resource errors.

use thiserror::Error;

/// Top-level workflow error type.
#[derive(Error, Debug)]
pub enum WorkflowError {
    /// Error during DAG construction or validation.
    #[error("DAG error: {0}")]
    DAG(#[from] DAGError),

    /// Error during workflow execution.
    #[error("Execution error: {0}")]
    Execution(#[from] ExecutionError),

    /// Error related to resource management.
    #[error("Resource error: {0}")]
    Resource(#[from] ResourceError),
}

/// Errors related to DAG structure and validation.
#[derive(Error, Debug)]
pub enum DAGError {
    /// A cycle was detected in the workflow DAG.
    #[error("Cycle detected in workflow DAG")]
    CycleDetected,

    /// A dependency references a non-existent node.
    #[error("Invalid dependency: {0}")]
    InvalidDependency(String),

    /// A node was not found in the DAG.
    #[error("Node not found: {0}")]
    NodeNotFound(String),

    /// The DAG is empty (no nodes).
    #[error("Empty DAG")]
    EmptyDAG,
}

/// Errors that occur during step execution.
#[derive(Error, Debug)]
pub enum ExecutionError {
    /// A step failed during execution.
    #[error("Step failed: {step_id}, reason: {reason}")]
    StepFailed { step_id: String, reason: String },

    /// A step exceeded its timeout.
    #[error("Step timeout: {0}")]
    Timeout(String),

    /// A step exhausted all retry attempts.
    #[error("Retry exhausted for step: {0}")]
    RetryExhausted(String),

    /// The workflow was cancelled.
    #[error("Workflow cancelled")]
    Cancelled,

    /// Serialization/deserialization error.
    #[error("Serialization error: {0}")]
    Serialization(String),
}

/// Errors related to resource management.
#[derive(Error, Debug)]
pub enum ResourceError {
    /// The thread pool is exhausted.
    #[error("Thread pool exhausted")]
    ThreadPoolExhausted,

    /// Memory limit was exceeded.
    #[error("Memory limit exceeded")]
    MemoryLimitExceeded,

    /// Invalid resource configuration.
    #[error("Invalid resource configuration: {0}")]
    InvalidConfiguration(String),
}

/// Result type for workflow operations.
pub type Result<T> = std::result::Result<T, WorkflowError>;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_error_conversion() {
        let dag_error = DAGError::CycleDetected;
        let workflow_error: WorkflowError = dag_error.into();
        assert!(matches!(workflow_error, WorkflowError::DAG(_)));
    }

    #[test]
    fn test_error_display() {
        let error = ExecutionError::StepFailed {
            step_id: "step1".to_string(),
            reason: "test error".to_string(),
        };
        assert!(error.to_string().contains("step1"));
        assert!(error.to_string().contains("test error"));
    }
}
