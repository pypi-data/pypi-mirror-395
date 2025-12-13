//! Metrics collection for workflow execution.
//!
//! This module provides structures for tracking workflow and step execution
//! metrics including timing, memory usage, and parallelism factors.

use serde::{Deserialize, Serialize};
use std::time::{Duration, Instant};

/// Status of a workflow step.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "lowercase")]
pub enum StepStatus {
    /// Step is pending execution.
    Pending,

    /// Step is currently running.
    Running,

    /// Step completed successfully.
    Completed,

    /// Step failed with an error.
    Failed(String),

    /// Step timed out.
    Timeout,

    /// Step was cancelled.
    Cancelled,
}

/// Metrics for a single workflow step.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StepMetrics {
    /// Unique identifier for the step.
    pub step_id: String,

    /// Start time (duration since workflow start).
    #[serde(skip, default = "Instant::now")]
    pub start_time: Instant,

    /// End time (duration since workflow start).
    #[serde(skip, default)]
    pub end_time: Option<Instant>,

    /// Duration of step execution.
    #[serde(serialize_with = "serialize_duration_opt")]
    pub duration: Option<Duration>,

    /// Current status of the step.
    pub status: StepStatus,

    /// Number of retry attempts made.
    pub retry_count: u32,

    /// Memory usage in bytes (if available).
    pub memory_usage: Option<u64>,

    /// CPU usage percentage (if available).
    pub cpu_usage: Option<f64>,
}

impl StepMetrics {
    /// Create a new StepMetrics for a step that's about to start.
    pub fn new(step_id: String) -> Self {
        Self {
            step_id,
            start_time: Instant::now(),
            end_time: None,
            duration: None,
            status: StepStatus::Pending,
            retry_count: 0,
            memory_usage: None,
            cpu_usage: None,
        }
    }

    /// Mark the step as started.
    pub fn start(&mut self) {
        self.start_time = Instant::now();
        self.status = StepStatus::Running;
    }

    /// Mark the step as completed.
    pub fn complete(&mut self) {
        let now = Instant::now();
        self.end_time = Some(now);
        self.duration = Some(now.duration_since(self.start_time));
        self.status = StepStatus::Completed;
    }

    /// Mark the step as failed.
    pub fn fail(&mut self, reason: String) {
        let now = Instant::now();
        self.end_time = Some(now);
        self.duration = Some(now.duration_since(self.start_time));
        self.status = StepStatus::Failed(reason);
    }

    /// Mark the step as timed out.
    pub fn timeout(&mut self) {
        let now = Instant::now();
        self.end_time = Some(now);
        self.duration = Some(now.duration_since(self.start_time));
        self.status = StepStatus::Timeout;
    }

    /// Increment the retry count.
    pub fn increment_retry(&mut self) {
        self.retry_count += 1;
    }
}

/// Metrics for the entire workflow execution.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WorkflowMetrics {
    /// Total duration of workflow execution.
    #[serde(serialize_with = "serialize_duration")]
    pub total_duration: Duration,

    /// Peak memory usage in bytes.
    pub peak_memory: u64,

    /// Parallelism factor (average concurrent steps / total steps).
    pub parallelism_factor: f64,

    /// Resource utilization (0.0 to 1.0).
    pub resource_utilization: f64,

    /// Metrics for individual steps.
    pub step_metrics: Vec<StepMetrics>,

    /// Total number of steps.
    pub total_steps: usize,

    /// Number of successful steps.
    pub successful_steps: usize,

    /// Number of failed steps.
    pub failed_steps: usize,
}

impl WorkflowMetrics {
    /// Create a new WorkflowMetrics.
    pub fn new() -> Self {
        Self {
            total_duration: Duration::from_secs(0),
            peak_memory: 0,
            parallelism_factor: 1.0,
            resource_utilization: 0.0,
            step_metrics: Vec::new(),
            total_steps: 0,
            successful_steps: 0,
            failed_steps: 0,
        }
    }

    /// Add step metrics.
    pub fn add_step(&mut self, metrics: StepMetrics) {
        self.total_steps += 1;

        match &metrics.status {
            StepStatus::Completed => self.successful_steps += 1,
            StepStatus::Failed(_) | StepStatus::Timeout => self.failed_steps += 1,
            _ => {}
        }

        if let Some(mem) = metrics.memory_usage {
            if mem > self.peak_memory {
                self.peak_memory = mem;
            }
        }

        self.step_metrics.push(metrics);
    }

    /// Finalize metrics after workflow completion.
    pub fn finalize(&mut self, total_duration: Duration) {
        self.total_duration = total_duration;
        self.compute_parallelism_factor();
    }

    /// Compute the parallelism factor based on step timings.
    fn compute_parallelism_factor(&mut self) {
        if self.step_metrics.is_empty() {
            self.parallelism_factor = 1.0;
            return;
        }

        let total_step_time: f64 = self
            .step_metrics
            .iter()
            .filter_map(|m| m.duration.map(|d| d.as_secs_f64()))
            .sum();

        let workflow_time = self.total_duration.as_secs_f64();

        // Handle edge cases for very fast execution
        const MIN_TIME: f64 = 0.000001; // 1 microsecond

        // If steps execute too fast to measure accurately, assume reasonable parallelism
        // For sequential execution, this should be close to 1.0
        if total_step_time < MIN_TIME || workflow_time < MIN_TIME {
            self.parallelism_factor = 1.0;
            return;
        }

        self.parallelism_factor = total_step_time / workflow_time;
    }
}

impl Default for WorkflowMetrics {
    fn default() -> Self {
        Self::new()
    }
}

/// Custom serializer for Duration.
fn serialize_duration<S>(duration: &Duration, serializer: S) -> Result<S::Ok, S::Error>
where
    S: serde::Serializer,
{
    serializer.serialize_f64(duration.as_secs_f64())
}

/// Custom serializer for Option<Duration>.
fn serialize_duration_opt<S>(duration: &Option<Duration>, serializer: S) -> Result<S::Ok, S::Error>
where
    S: serde::Serializer,
{
    match duration {
        Some(d) => serializer.serialize_some(&d.as_secs_f64()),
        None => serializer.serialize_none(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::thread;

    #[test]
    fn test_step_metrics_lifecycle() {
        let mut metrics = StepMetrics::new("test_step".to_string());
        assert_eq!(metrics.status, StepStatus::Pending);

        metrics.start();
        assert_eq!(metrics.status, StepStatus::Running);

        thread::sleep(Duration::from_millis(10));

        metrics.complete();
        assert_eq!(metrics.status, StepStatus::Completed);
        assert!(metrics.duration.unwrap() >= Duration::from_millis(10));
    }

    #[test]
    fn test_step_metrics_failure() {
        let mut metrics = StepMetrics::new("test_step".to_string());
        metrics.start();
        metrics.fail("test error".to_string());

        assert!(matches!(metrics.status, StepStatus::Failed(_)));
        assert!(metrics.duration.is_some());
    }

    #[test]
    fn test_workflow_metrics() {
        let mut workflow_metrics = WorkflowMetrics::new();

        let mut step1 = StepMetrics::new("step1".to_string());
        step1.complete();

        let mut step2 = StepMetrics::new("step2".to_string());
        step2.fail("error".to_string());

        workflow_metrics.add_step(step1);
        workflow_metrics.add_step(step2);

        assert_eq!(workflow_metrics.total_steps, 2);
        assert_eq!(workflow_metrics.successful_steps, 1);
        assert_eq!(workflow_metrics.failed_steps, 1);
    }

    #[test]
    fn test_parallelism_factor() {
        let mut workflow_metrics = WorkflowMetrics::new();

        // Simulate 2 steps that ran in parallel (each took 1s, total time 1s)
        let mut step1 = StepMetrics::new("step1".to_string());
        step1.duration = Some(Duration::from_secs(1));
        step1.status = StepStatus::Completed;

        let mut step2 = StepMetrics::new("step2".to_string());
        step2.duration = Some(Duration::from_secs(1));
        step2.status = StepStatus::Completed;

        workflow_metrics.add_step(step1);
        workflow_metrics.add_step(step2);
        workflow_metrics.finalize(Duration::from_secs(1));

        // Parallelism factor should be ~2.0 (2 seconds of work in 1 second)
        assert!((workflow_metrics.parallelism_factor - 2.0).abs() < 0.1);
    }
}
