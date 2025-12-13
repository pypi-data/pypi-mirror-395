//! Step trait and execution context for workflow steps.
//!
//! This module defines the trait that all workflow steps must implement,
//! as well as the execution context that steps receive.

use crate::error::Result;
use crate::metrics::StepMetrics;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;
use std::time::Duration;

/// Resource hint for step execution scheduling.
///
/// Resource hints inform the parallel scheduler about the expected resource
/// requirements of a step, enabling intelligent scheduling decisions and
/// preventing resource oversubscription.
///
/// # Examples
///
/// ```
/// use pf_workflow_core::ResourceHint;
///
/// let light_cpu = ResourceHint::LightCPU;
/// let heavy_io = ResourceHint::HeavyIO;
/// let memory_intensive = ResourceHint::Memory(1024 * 1024 * 1024); // 1GB
/// ```
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ResourceHint {
    /// Light CPU-bound task (default).
    ///
    /// Suitable for quick computations, string operations, simple transformations.
    /// Expected duration: <100ms, CPU usage: <50%.
    LightCPU,

    /// Heavy CPU-bound task.
    ///
    /// Suitable for intensive computations, data processing, algorithms.
    /// Expected duration: >100ms, CPU usage: >50%.
    /// The scheduler may limit concurrent heavy CPU tasks.
    HeavyCPU,

    /// Light I/O-bound task.
    ///
    /// Suitable for file reads, HTTP requests, database queries.
    /// Expected duration: <500ms, mostly waiting on I/O.
    LightIO,

    /// Heavy I/O-bound task.
    ///
    /// Suitable for large file transfers, bulk database operations.
    /// Expected duration: >500ms, significant I/O operations.
    HeavyIO,

    /// Memory-intensive task.
    ///
    /// The value indicates estimated peak memory usage in bytes.
    /// The scheduler may limit concurrent memory-intensive tasks
    /// to prevent OOM conditions.
    Memory(usize),

    /// Default resource hint.
    ///
    /// Equivalent to `LightCPU`. Used when no specific hint is provided.
    Default,
}

impl Default for ResourceHint {
    fn default() -> Self {
        Self::Default
    }
}

impl ResourceHint {
    /// Check if this is a CPU-bound task.
    pub fn is_cpu_bound(&self) -> bool {
        matches!(self, Self::LightCPU | Self::HeavyCPU | Self::Default)
    }

    /// Check if this is an I/O-bound task.
    pub fn is_io_bound(&self) -> bool {
        matches!(self, Self::LightIO | Self::HeavyIO)
    }

    /// Check if this is a heavy task (CPU or I/O).
    pub fn is_heavy(&self) -> bool {
        matches!(self, Self::HeavyCPU | Self::HeavyIO)
    }

    /// Get the estimated memory requirement in bytes.
    pub fn memory_requirement(&self) -> Option<usize> {
        match self {
            Self::Memory(bytes) => Some(*bytes),
            _ => None,
        }
    }
}

/// Trait for workflow steps.
pub trait Step: Send + Sync {
    /// Get the step's unique identifier.
    fn id(&self) -> &str;

    /// Execute the step.
    fn execute(&self, ctx: &mut ExecutionContext) -> Result<StepResult>;

    /// Get the IDs of steps this step depends on.
    fn dependencies(&self) -> &[String];

    /// Get the timeout for this step, if any.
    fn timeout(&self) -> Option<Duration> {
        None
    }

    /// Get the retry configuration for this step.
    fn retry_config(&self) -> RetryConfig {
        RetryConfig::default()
    }

    /// Get the resource hint for this step.
    ///
    /// Returns a hint about the expected resource usage of this step,
    /// which the parallel scheduler uses to make intelligent scheduling decisions.
    ///
    /// The default implementation returns `ResourceHint::Default` (equivalent to `LightCPU`).
    fn resource_hint(&self) -> ResourceHint {
        ResourceHint::Default
    }
}

/// Configuration for retry behavior.
#[derive(Debug, Clone)]
pub struct RetryConfig {
    /// Maximum number of retry attempts.
    pub max_attempts: u32,

    /// Backoff duration between retries.
    pub backoff: Duration,
}

impl Default for RetryConfig {
    fn default() -> Self {
        Self {
            max_attempts: 0,
            backoff: Duration::from_millis(100),
        }
    }
}

/// Execution context shared across workflow steps.
#[derive(Debug)]
pub struct ExecutionContext {
    /// Data storage for step outputs.
    /// Maps step ID to its output value.
    pub data: HashMap<String, Value>,

    /// Accumulated metrics (for internal use).
    #[allow(dead_code)]
    pub(crate) metrics: Vec<StepMetrics>,
}

impl ExecutionContext {
    /// Create a new execution context.
    pub fn new() -> Self {
        Self {
            data: HashMap::new(),
            metrics: Vec::new(),
        }
    }

    /// Store a value with the given key.
    pub fn set(&mut self, key: String, value: Value) {
        self.data.insert(key, value);
    }

    /// Get a value by key.
    pub fn get(&self, key: &str) -> Option<&Value> {
        self.data.get(key)
    }

    /// Check if a key exists.
    pub fn contains_key(&self, key: &str) -> bool {
        self.data.contains_key(key)
    }
}

impl Default for ExecutionContext {
    fn default() -> Self {
        Self::new()
    }
}

/// Result of a step execution.
#[derive(Debug)]
pub struct StepResult {
    /// Output value from the step.
    pub output: Value,

    /// Metrics collected during step execution.
    pub metrics: StepMetrics,
}

impl StepResult {
    /// Create a new step result.
    pub fn new(output: Value, metrics: StepMetrics) -> Self {
        Self { output, metrics }
    }
}

/// A simple step implementation for testing.
#[cfg(test)]
pub struct SimpleStep {
    id: String,
    dependencies: Vec<String>,
    output: Value,
}

#[cfg(test)]
impl SimpleStep {
    pub fn new(id: String, output: Value) -> Self {
        Self {
            id,
            dependencies: Vec::new(),
            output,
        }
    }

    pub fn with_dependencies(mut self, deps: Vec<String>) -> Self {
        self.dependencies = deps;
        self
    }
}

#[cfg(test)]
impl Step for SimpleStep {
    fn id(&self) -> &str {
        &self.id
    }

    fn execute(&self, _ctx: &mut ExecutionContext) -> Result<StepResult> {
        let metrics = StepMetrics::new(self.id.clone());
        Ok(StepResult::new(self.output.clone(), metrics))
    }

    fn dependencies(&self) -> &[String] {
        &self.dependencies
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_execution_context() {
        let mut ctx = ExecutionContext::new();

        ctx.set("key1".to_string(), Value::from("value1"));
        assert!(ctx.contains_key("key1"));
        assert_eq!(ctx.get("key1").unwrap(), &Value::from("value1"));

        assert!(!ctx.contains_key("nonexistent"));
    }

    #[test]
    fn test_simple_step() {
        let step = SimpleStep::new("test".to_string(), Value::from(42));
        assert_eq!(step.id(), "test");
        assert_eq!(step.dependencies().len(), 0);

        let mut ctx = ExecutionContext::new();
        let result = step.execute(&mut ctx).unwrap();
        assert_eq!(result.output, Value::from(42));
    }

    #[test]
    fn test_step_with_dependencies() {
        let step = SimpleStep::new("test".to_string(), Value::from(42))
            .with_dependencies(vec!["dep1".to_string(), "dep2".to_string()]);

        assert_eq!(step.dependencies().len(), 2);
        assert_eq!(step.dependencies()[0], "dep1");
    }

    #[test]
    fn test_resource_hint_default() {
        let hint = ResourceHint::default();
        assert_eq!(hint, ResourceHint::Default);
    }

    #[test]
    fn test_resource_hint_cpu_bound() {
        assert!(ResourceHint::LightCPU.is_cpu_bound());
        assert!(ResourceHint::HeavyCPU.is_cpu_bound());
        assert!(ResourceHint::Default.is_cpu_bound());
        assert!(!ResourceHint::LightIO.is_cpu_bound());
        assert!(!ResourceHint::HeavyIO.is_cpu_bound());
    }

    #[test]
    fn test_resource_hint_io_bound() {
        assert!(ResourceHint::LightIO.is_io_bound());
        assert!(ResourceHint::HeavyIO.is_io_bound());
        assert!(!ResourceHint::LightCPU.is_io_bound());
        assert!(!ResourceHint::HeavyCPU.is_io_bound());
        assert!(!ResourceHint::Default.is_io_bound());
    }

    #[test]
    fn test_resource_hint_heavy() {
        assert!(ResourceHint::HeavyCPU.is_heavy());
        assert!(ResourceHint::HeavyIO.is_heavy());
        assert!(!ResourceHint::LightCPU.is_heavy());
        assert!(!ResourceHint::LightIO.is_heavy());
        assert!(!ResourceHint::Default.is_heavy());
    }

    #[test]
    fn test_resource_hint_memory_requirement() {
        let memory_hint = ResourceHint::Memory(1024 * 1024 * 1024); // 1GB
        assert_eq!(memory_hint.memory_requirement(), Some(1024 * 1024 * 1024));

        assert_eq!(ResourceHint::LightCPU.memory_requirement(), None);
        assert_eq!(ResourceHint::Default.memory_requirement(), None);
    }

    #[test]
    fn test_resource_hint_serialization() {
        let hint = ResourceHint::HeavyCPU;
        let json = serde_json::to_string(&hint).unwrap();
        println!("Serialized JSON: {}", json);

        // Just check that it can be deserialized correctly
        let deserialized: ResourceHint = serde_json::from_str(&json).unwrap();
        assert_eq!(deserialized, ResourceHint::HeavyCPU);

        // Test Memory variant
        let memory_hint = ResourceHint::Memory(1024);
        let json = serde_json::to_string(&memory_hint).unwrap();
        let deserialized: ResourceHint = serde_json::from_str(&json).unwrap();
        assert_eq!(deserialized, ResourceHint::Memory(1024));

        // Test all variants round-trip correctly
        let variants = vec![
            ResourceHint::LightCPU,
            ResourceHint::HeavyCPU,
            ResourceHint::LightIO,
            ResourceHint::HeavyIO,
            ResourceHint::Memory(1024),
            ResourceHint::Default,
        ];

        for variant in variants {
            let json = serde_json::to_string(&variant).unwrap();
            let deserialized: ResourceHint = serde_json::from_str(&json).unwrap();
            assert_eq!(deserialized, variant);
        }
    }

    #[test]
    fn test_step_default_resource_hint() {
        let step = SimpleStep::new("test".to_string(), Value::from(42));
        assert_eq!(step.resource_hint(), ResourceHint::Default);
    }
}
