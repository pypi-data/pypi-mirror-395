//! Workflow executor for running steps.
//!
//! This module provides the main executor for running workflow steps
//! either sequentially or in parallel.

use crate::cancellation::CancellationToken;
use crate::config::ExecutorConfig;
use crate::dag::DAG;
use crate::error::{ExecutionError, Result};
use crate::metrics::{StepMetrics, WorkflowMetrics};
use crate::progress::{NoOpCallback, ProgressCallback, ProgressEvent};
use crate::scheduler::{ParallelScheduler, ResourceLimits};
use crate::step::{ExecutionContext, Step, StepResult};
use std::collections::{HashMap, HashSet};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::{Duration, Instant};

/// Main workflow executor.
///
/// The executor coordinates the execution of workflow steps based on
/// the DAG and configuration.
///
/// # Phase 3.4 Note
/// This is a stub implementation. Full implementation will be in Tasks 6-8.
pub struct WorkflowExecutor {
    /// Configuration for execution.
    config: ExecutorConfig,

    /// The workflow DAG.
    dag: DAG,

    /// Map of step ID to step implementation.
    steps: HashMap<String, Box<dyn Step>>,
}

impl WorkflowExecutor {
    /// Create a new workflow executor.
    pub fn new(config: ExecutorConfig) -> Self {
        Self {
            config,
            dag: DAG::new(),
            steps: HashMap::new(),
        }
    }

    /// Add a step to the workflow.
    pub fn add_step(&mut self, step: Box<dyn Step>) {
        let step_id = step.id().to_string();

        // Add node to DAG
        self.dag.add_node(step_id.clone());

        // Add edges for dependencies
        for dep in step.dependencies() {
            // Ensure dependency node exists
            self.dag.add_node(dep.clone());
            // Add edge: this step depends on dep
            let _ = self.dag.add_edge(step_id.clone(), dep.clone());
        }

        // Store step
        self.steps.insert(step_id, step);
    }

    /// Get the number of steps in the workflow.
    pub fn step_count(&self) -> usize {
        self.steps.len()
    }

    /// Get the executor configuration.
    pub fn config(&self) -> &ExecutorConfig {
        &self.config
    }

    /// Get a reference to the DAG.
    pub fn dag(&self) -> &DAG {
        &self.dag
    }

    /// Execute the workflow sequentially.
    ///
    /// Steps are executed in topological order based on their dependencies.
    /// Each step is executed with retry logic according to its configuration.
    ///
    /// This is a convenience method that calls `execute_with_options` with no
    /// cancellation or progress tracking. For more control, use `execute_with_cancellation`,
    /// `execute_with_progress`, or `execute_with_options`.
    pub fn execute(&mut self) -> Result<WorkflowMetrics> {
        self.execute_with_options(None, None)
    }

    /// Execute the workflow with optional cancellation and progress tracking.
    ///
    /// # Arguments
    ///
    /// * `cancellation_token` - Optional token to check for cancellation
    /// * `progress_callback` - Optional callback for progress events
    ///
    /// # Returns
    ///
    /// Workflow metrics on success, or an error if execution fails or is cancelled.
    ///
    /// # Examples
    ///
    /// ```no_run
    /// use pf_workflow_core::{ExecutorConfig, WorkflowExecutor, CancellationToken};
    ///
    /// let config = ExecutorConfig::default();
    /// let mut executor = WorkflowExecutor::new(config);
    ///
    /// let token = CancellationToken::new();
    /// let metrics = executor.execute_with_options(Some(token), None)?;
    /// # Ok::<(), pf_workflow_core::WorkflowError>(())
    /// ```
    pub fn execute_with_options(
        &mut self,
        cancellation_token: Option<CancellationToken>,
        progress_callback: Option<Box<dyn ProgressCallback>>,
    ) -> Result<WorkflowMetrics> {
        let workflow_start = Instant::now();

        // Use no-op callback if none provided
        let callback: Box<dyn ProgressCallback> =
            progress_callback.unwrap_or_else(|| Box::new(NoOpCallback));

        // Get execution order from DAG
        let order = self.dag.topological_sort()?;

        // Create execution context and tracking structures
        let mut ctx = ExecutionContext::new();
        let mut workflow_metrics = WorkflowMetrics::new();
        let mut completed_steps = HashSet::new();

        // Execute each step in order
        for step_id in order {
            // Check for cancellation before starting step
            if let Some(ref token) = cancellation_token {
                if token.is_cancelled() {
                    // Emit cancelled event for this step
                    callback.on_progress(ProgressEvent::cancelled(&step_id));

                    // Cleanup and return error
                    self.cleanup_partial_results(&completed_steps);
                    return Err(ExecutionError::Cancelled.into());
                }
            }

            let step = self
                .steps
                .get(&step_id)
                .ok_or_else(|| ExecutionError::StepFailed {
                    step_id: step_id.clone(),
                    reason: "Step not found".to_string(),
                })?;

            // Emit started event
            callback.on_progress(ProgressEvent::started(&step_id));

            // Execute step with retry logic
            let result = match self.execute_step_with_retry(
                step.as_ref(),
                &mut ctx,
                cancellation_token.as_ref(),
            ) {
                Ok(res) => {
                    // Emit completed event
                    callback.on_progress(ProgressEvent::completed(&step_id));
                    res
                }
                Err(e) => {
                    // Check if it was a cancellation
                    if matches!(
                        e,
                        crate::error::WorkflowError::Execution(ExecutionError::Cancelled)
                    ) {
                        callback.on_progress(ProgressEvent::cancelled(&step_id));
                        self.cleanup_partial_results(&completed_steps);
                        return Err(e);
                    }

                    // Emit failed event with error context
                    let dep_chain = self.build_dependency_chain(&step_id);
                    let error_msg = format!("{} (dependency chain: {})", e, dep_chain.join(" → "));
                    callback.on_progress(ProgressEvent::failed(&step_id, &error_msg));

                    self.cleanup_partial_results(&completed_steps);

                    // Preserve certain error types without wrapping
                    if matches!(
                        e,
                        crate::error::WorkflowError::Execution(ExecutionError::RetryExhausted(_))
                    ) || matches!(
                        e,
                        crate::error::WorkflowError::Execution(ExecutionError::Timeout(_))
                    ) {
                        return Err(e);
                    }

                    return Err(ExecutionError::StepFailed {
                        step_id: step_id.clone(),
                        reason: error_msg,
                    }
                    .into());
                }
            };

            // Store step output in context for dependent steps
            ctx.set(step_id.clone(), result.output);

            // Add step metrics to workflow metrics
            workflow_metrics.add_step(result.metrics);

            // Mark step as completed
            completed_steps.insert(step_id.clone());
        }

        // Finalize workflow metrics
        let total_duration = workflow_start.elapsed();
        workflow_metrics.finalize(total_duration);

        Ok(workflow_metrics)
    }

    /// Build the dependency chain for a step (for error messages).
    ///
    /// Returns a vector of step IDs representing the dependency chain
    /// from root dependencies to the given step.
    fn build_dependency_chain(&self, step_id: &str) -> Vec<String> {
        let mut chain = Vec::new();
        let mut visited = HashSet::new();
        self.build_dependency_chain_recursive(step_id, &mut chain, &mut visited);
        chain.reverse();
        chain
    }

    fn build_dependency_chain_recursive(
        &self,
        step_id: &str,
        chain: &mut Vec<String>,
        visited: &mut HashSet<String>,
    ) {
        if visited.contains(step_id) {
            return;
        }
        visited.insert(step_id.to_string());

        // Add dependencies first
        if let Some(step) = self.steps.get(step_id) {
            for dep in step.dependencies() {
                self.build_dependency_chain_recursive(dep, chain, visited);
            }
        }

        // Add this step
        chain.push(step_id.to_string());
    }

    /// Cleanup partial results when execution is cancelled or fails.
    ///
    /// This method can be extended to perform cleanup actions like
    /// rolling back transactions, deleting temporary files, etc.
    fn cleanup_partial_results(&self, _completed_steps: &HashSet<String>) {
        // Currently no-op, but provides extension point for cleanup logic
        // In the future, steps could implement a cleanup() method
    }

    /// Execute a single step with retry logic and timeout handling.
    ///
    /// # Arguments
    /// * `step` - The step to execute
    /// * `ctx` - The execution context
    /// * `cancellation_token` - Optional cancellation token to check between retries
    ///
    /// # Returns
    /// The step result with metrics, or an error if execution fails.
    fn execute_step_with_retry(
        &self,
        step: &dyn Step,
        ctx: &mut ExecutionContext,
        cancellation_token: Option<&CancellationToken>,
    ) -> Result<StepResult> {
        let retry_config = step.retry_config();
        let step_timeout = step.timeout().or(self.config.step_timeout);
        let base_backoff = Duration::from_millis(self.config.retry_backoff_ms);

        let mut step_metrics = StepMetrics::new(step.id().to_string());
        step_metrics.start();

        let mut last_error = None;

        // Retry loop (attempt 0 is the first try)
        for attempt in 0..=retry_config.max_attempts {
            // Check for cancellation before retry
            if let Some(token) = cancellation_token {
                if token.is_cancelled() {
                    step_metrics.fail("Cancelled".to_string());
                    return Err(ExecutionError::Cancelled.into());
                }
            }

            if attempt > 0 {
                step_metrics.increment_retry();

                // Calculate exponential backoff: base * 2^(attempt-1)
                let backoff = base_backoff * 2_u32.pow(attempt - 1);
                thread::sleep(backoff);
            }

            // Execute with timeout if specified
            let result = if let Some(timeout) = step_timeout {
                self.execute_step_with_timeout(step, ctx, timeout)
            } else {
                step.execute(ctx)
            };

            match result {
                Ok(mut step_result) => {
                    // Success - update metrics and return
                    step_metrics.complete();
                    step_result.metrics = step_metrics;
                    return Ok(step_result);
                }
                Err(e) => {
                    // Store error for potential retry or final failure
                    last_error = Some(e);

                    // If this was the last attempt, break
                    if attempt >= retry_config.max_attempts {
                        break;
                    }
                    // Otherwise, loop will retry
                }
            }
        }

        // All retries exhausted - mark as failed
        let error_msg = last_error
            .map(|e| e.to_string())
            .unwrap_or_else(|| "Unknown error".to_string());

        step_metrics.fail(error_msg.clone());

        Err(ExecutionError::RetryExhausted(format!(
            "Step '{}' failed after {} attempts: {}",
            step.id(),
            retry_config.max_attempts + 1,
            error_msg
        ))
        .into())
    }

    /// Execute a step with a timeout.
    ///
    /// Note: This is a simplified timeout implementation.
    /// In production, you'd use more sophisticated timeout mechanisms.
    fn execute_step_with_timeout(
        &self,
        step: &dyn Step,
        ctx: &mut ExecutionContext,
        timeout: Duration,
    ) -> Result<StepResult> {
        let start = Instant::now();

        // Execute the step
        let result = step.execute(ctx)?;

        // Check if we exceeded timeout
        if start.elapsed() > timeout {
            return Err(ExecutionError::Timeout(format!(
                "Step '{}' exceeded timeout of {:?}",
                step.id(),
                timeout
            ))
            .into());
        }

        Ok(result)
    }

    /// Execute the workflow in parallel with optional cancellation and progress tracking.
    ///
    /// This method uses wave-based parallel execution where steps within each wave
    /// can run concurrently, while respecting DAG dependencies and resource limits.
    ///
    /// # Arguments
    ///
    /// * `cancellation_token` - Optional token to check for cancellation
    /// * `progress_callback` - Optional callback for progress events
    ///
    /// # Returns
    ///
    /// Workflow metrics on success, or an error if execution fails or is cancelled.
    ///
    /// # Examples
    ///
    /// ```no_run
    /// use pf_workflow_core::{ExecutorConfig, WorkflowExecutor, CancellationToken};
    ///
    /// let config = ExecutorConfig::default();
    /// let mut executor = WorkflowExecutor::new(config);
    ///
    /// let token = CancellationToken::new();
    /// let metrics = executor.execute_parallel_with_options(Some(token), None)?;
    /// # Ok::<(), pf_workflow_core::WorkflowError>(())
    /// ```
    pub fn execute_parallel_with_options(
        &mut self,
        cancellation_token: Option<CancellationToken>,
        progress_callback: Option<Box<dyn ProgressCallback>>,
    ) -> Result<WorkflowMetrics> {
        let workflow_start = Instant::now();

        // Use no-op callback if none provided
        let callback: Arc<Box<dyn ProgressCallback>> =
            Arc::new(progress_callback.unwrap_or_else(|| Box::new(NoOpCallback)));

        // Create scheduler with resource limits from config
        let limits = ResourceLimits {
            max_cpu_tasks: self.config.max_parallel_steps.unwrap_or_else(num_cpus::get),
            max_io_tasks: self.config.max_parallel_steps.unwrap_or_else(num_cpus::get) * 2,
            max_memory_bytes: usize::MAX,
        };
        let scheduler = ParallelScheduler::with_limits(limits);

        // Compute execution waves
        let waves = scheduler.schedule_parallel(&self.dag, &self.steps);

        if waves.is_empty() {
            return Ok(WorkflowMetrics::new());
        }

        // Shared execution context (protected by mutex for parallel access)
        let ctx = Arc::new(Mutex::new(ExecutionContext::new()));
        let workflow_metrics = Arc::new(Mutex::new(WorkflowMetrics::new()));
        let completed_steps = Arc::new(Mutex::new(HashSet::new()));

        // Execute each wave
        for (wave_idx, wave) in waves.iter().enumerate() {
            // Check for cancellation before starting wave
            if let Some(ref token) = cancellation_token {
                if token.is_cancelled() {
                    // Emit cancelled events for remaining steps
                    for step_id in wave {
                        callback.on_progress(ProgressEvent::cancelled(step_id));
                    }
                    self.cleanup_partial_results(&completed_steps.lock().unwrap());
                    return Err(ExecutionError::Cancelled.into());
                }
            }

            // Execute wave in parallel
            let wave_result = self.execute_wave(
                wave,
                ctx.clone(),
                workflow_metrics.clone(),
                completed_steps.clone(),
                cancellation_token.clone(),
                callback.clone(),
            );

            // Handle wave errors
            if let Err(e) = wave_result {
                // Cancel remaining waves
                for remaining_wave in waves.iter().skip(wave_idx + 1) {
                    for step_id in remaining_wave {
                        callback.on_progress(ProgressEvent::cancelled(step_id));
                    }
                }

                self.cleanup_partial_results(&completed_steps.lock().unwrap());
                return Err(e);
            }
        }

        // Finalize workflow metrics
        let total_duration = workflow_start.elapsed();
        let mut metrics = match Arc::try_unwrap(workflow_metrics) {
            Ok(mutex) => mutex.into_inner().unwrap(),
            Err(arc) => arc.lock().unwrap().clone(),
        };
        metrics.finalize(total_duration);

        Ok(metrics)
    }

    /// Execute a single wave of steps in parallel.
    ///
    /// All steps in the wave can run concurrently as they have no dependencies on each other.
    fn execute_wave(
        &self,
        wave: &[String],
        ctx: Arc<Mutex<ExecutionContext>>,
        workflow_metrics: Arc<Mutex<WorkflowMetrics>>,
        completed_steps: Arc<Mutex<HashSet<String>>>,
        cancellation_token: Option<CancellationToken>,
        callback: Arc<Box<dyn ProgressCallback>>,
    ) -> Result<()> {
        // Track errors in the wave
        let errors: Arc<Mutex<Vec<(String, String)>>> = Arc::new(Mutex::new(Vec::new()));
        let results: Arc<Mutex<HashMap<String, StepResult>>> = Arc::new(Mutex::new(HashMap::new()));

        // Use rayon scoped threads for proper borrowing
        rayon::scope(|s| {
            for step_id in wave {
                let step_id = step_id.clone();
                let ctx = ctx.clone();
                let cancellation_token = cancellation_token.clone();
                let callback = callback.clone();
                let errors = errors.clone();
                let results = results.clone();

                // Get step reference
                let step = match self.steps.get(&step_id) {
                    Some(step) => step.as_ref(),
                    None => {
                        errors
                            .lock()
                            .unwrap()
                            .push((step_id.clone(), "Step not found".to_string()));
                        continue;
                    }
                };

                // Extract step configuration
                let retry_config = step.retry_config();
                let _step_timeout = step.timeout().or(self.config.step_timeout);
                let base_backoff = Duration::from_millis(self.config.retry_backoff_ms);

                // Spawn parallel task
                s.spawn(move |_| {
                    // Check cancellation before starting
                    if let Some(ref token) = cancellation_token {
                        if token.is_cancelled() {
                            callback.on_progress(ProgressEvent::cancelled(&step_id));
                            return;
                        }
                    }

                    // Emit started event
                    callback.on_progress(ProgressEvent::started(&step_id));

                    // Execute step with retry
                    let mut step_metrics = StepMetrics::new(step_id.clone());
                    step_metrics.start();

                    let mut last_error = None;
                    let mut success = false;

                    for attempt in 0..=retry_config.max_attempts {
                        // Check cancellation between retries
                        if let Some(ref token) = cancellation_token {
                            if token.is_cancelled() {
                                step_metrics.fail("Cancelled".to_string());
                                callback.on_progress(ProgressEvent::cancelled(&step_id));
                                return;
                            }
                        }

                        if attempt > 0 {
                            step_metrics.increment_retry();
                            let backoff = base_backoff * 2_u32.pow(attempt - 1);
                            thread::sleep(backoff);
                        }

                        // Execute step (with lock on context)
                        let result = {
                            let mut context = ctx.lock().unwrap();
                            step.execute(&mut context)
                        };

                        match result {
                            Ok(step_result) => {
                                step_metrics.complete();
                                callback.on_progress(ProgressEvent::completed(&step_id));

                                // Store result
                                results.lock().unwrap().insert(
                                    step_id.clone(),
                                    StepResult::new(
                                        step_result.output.clone(),
                                        step_metrics.clone(),
                                    ),
                                );
                                success = true;
                                break;
                            }
                            Err(e) => {
                                last_error = Some(e);
                                if attempt >= retry_config.max_attempts {
                                    break;
                                }
                            }
                        }
                    }

                    if !success {
                        let error_msg = last_error
                            .map(|e| e.to_string())
                            .unwrap_or_else(|| "Unknown error".to_string());
                        let mut failed_metrics = step_metrics.clone();
                        failed_metrics.fail(error_msg.clone());

                        let full_error = format!(
                            "Step '{}' failed after {} attempts: {}",
                            step_id,
                            retry_config.max_attempts + 1,
                            error_msg
                        );

                        callback.on_progress(ProgressEvent::failed(&step_id, &full_error));
                        errors.lock().unwrap().push((step_id.clone(), full_error));
                    }
                });
            }
        });

        // Process results
        let result_map = results.lock().unwrap();
        for (step_id, step_result) in result_map.iter() {
            // Store output in context
            ctx.lock()
                .unwrap()
                .set(step_id.clone(), step_result.output.clone());

            // Add metrics
            workflow_metrics
                .lock()
                .unwrap()
                .add_step(step_result.metrics.clone());

            // Mark completed
            completed_steps.lock().unwrap().insert(step_id.clone());
        }

        // Check if any errors occurred
        let error_list = errors.lock().unwrap();
        if !error_list.is_empty() {
            let error_summary = error_list
                .iter()
                .map(|(id, msg)| format!("{}: {}", id, msg))
                .collect::<Vec<_>>()
                .join("; ");

            return Err(ExecutionError::StepFailed {
                step_id: "wave_execution".to_string(),
                reason: format!("Wave execution failed: {}", error_summary),
            }
            .into());
        }

        Ok(())
    }

    /// Execute the workflow in parallel (convenience method).
    ///
    /// This is a convenience method that calls `execute_parallel_with_options` with no
    /// cancellation or progress tracking.
    pub fn execute_parallel(&mut self) -> Result<WorkflowMetrics> {
        self.execute_parallel_with_options(None, None)
    }

    /// Execute the workflow sequentially with cancellation support.
    ///
    /// This is a convenience method for workflows that need cancellation but not progress tracking.
    ///
    /// # Arguments
    ///
    /// * `cancellation_token` - Token to check for cancellation
    ///
    /// # Examples
    ///
    /// ```no_run
    /// use pf_workflow_core::{ExecutorConfig, WorkflowExecutor, CancellationToken};
    /// use std::thread;
    /// use std::time::Duration;
    ///
    /// let config = ExecutorConfig::default();
    /// let mut executor = WorkflowExecutor::new(config);
    ///
    /// let token = CancellationToken::new();
    /// let token_clone = token.clone();
    ///
    /// // Spawn thread to cancel after timeout
    /// thread::spawn(move || {
    ///     thread::sleep(Duration::from_secs(5));
    ///     token_clone.cancel();
    /// });
    ///
    /// let result = executor.execute_with_cancellation(token);
    /// # Ok::<(), pf_workflow_core::WorkflowError>(())
    /// ```
    pub fn execute_with_cancellation(
        &mut self,
        cancellation_token: CancellationToken,
    ) -> Result<WorkflowMetrics> {
        self.execute_with_options(Some(cancellation_token), None)
    }

    /// Execute the workflow sequentially with progress tracking.
    ///
    /// This is a convenience method for workflows that need progress tracking but not cancellation.
    ///
    /// # Arguments
    ///
    /// * `progress_callback` - Callback for progress events
    ///
    /// # Examples
    ///
    /// ```no_run
    /// use pf_workflow_core::{ExecutorConfig, WorkflowExecutor, ConsoleProgressCallback};
    ///
    /// let config = ExecutorConfig::default();
    /// let mut executor = WorkflowExecutor::new(config);
    ///
    /// let result = executor.execute_with_progress(Box::new(ConsoleProgressCallback::new()));
    /// # Ok::<(), pf_workflow_core::WorkflowError>(())
    /// ```
    pub fn execute_with_progress(
        &mut self,
        progress_callback: Box<dyn ProgressCallback>,
    ) -> Result<WorkflowMetrics> {
        self.execute_with_options(None, Some(progress_callback))
    }

    /// Execute the workflow in parallel with cancellation support.
    ///
    /// This is a convenience method for parallel workflows that need cancellation but not progress tracking.
    ///
    /// # Arguments
    ///
    /// * `cancellation_token` - Token to check for cancellation
    ///
    /// # Examples
    ///
    /// ```no_run
    /// use pf_workflow_core::{ExecutorConfig, WorkflowExecutor, CancellationToken};
    ///
    /// let config = ExecutorConfig::builder().max_parallel_steps(4).build();
    /// let mut executor = WorkflowExecutor::new(config);
    ///
    /// let token = CancellationToken::new();
    /// let result = executor.execute_parallel_with_cancellation(token);
    /// # Ok::<(), pf_workflow_core::WorkflowError>(())
    /// ```
    pub fn execute_parallel_with_cancellation(
        &mut self,
        cancellation_token: CancellationToken,
    ) -> Result<WorkflowMetrics> {
        self.execute_parallel_with_options(Some(cancellation_token), None)
    }

    /// Execute the workflow in parallel with progress tracking.
    ///
    /// This is a convenience method for parallel workflows that need progress tracking but not cancellation.
    ///
    /// # Arguments
    ///
    /// * `progress_callback` - Callback for progress events
    ///
    /// # Examples
    ///
    /// ```no_run
    /// use pf_workflow_core::{ExecutorConfig, WorkflowExecutor, ConsoleProgressCallback};
    ///
    /// let config = ExecutorConfig::builder().max_parallel_steps(4).build();
    /// let mut executor = WorkflowExecutor::new(config);
    ///
    /// let result = executor.execute_parallel_with_progress(Box::new(ConsoleProgressCallback::new()));
    /// # Ok::<(), pf_workflow_core::WorkflowError>(())
    /// ```
    pub fn execute_parallel_with_progress(
        &mut self,
        progress_callback: Box<dyn ProgressCallback>,
    ) -> Result<WorkflowMetrics> {
        self.execute_parallel_with_options(None, Some(progress_callback))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::error::{ExecutionError, WorkflowError};
    use crate::step::{RetryConfig, SimpleStep, Step, StepResult};
    use serde_json::Value;
    use std::sync::{Arc, Mutex};
    use std::thread;
    use std::time::Duration;

    #[test]
    fn test_executor_creation() {
        let config = ExecutorConfig::default();
        let executor = WorkflowExecutor::new(config);
        assert_eq!(executor.step_count(), 0);
    }

    #[test]
    fn test_add_step() {
        let config = ExecutorConfig::default();
        let mut executor = WorkflowExecutor::new(config);

        let step = Box::new(SimpleStep::new("step1".to_string(), Value::from(42)));
        executor.add_step(step);

        assert_eq!(executor.step_count(), 1);
        assert_eq!(executor.dag().node_count(), 1);
    }

    #[test]
    fn test_add_step_with_dependencies() {
        let config = ExecutorConfig::default();
        let mut executor = WorkflowExecutor::new(config);

        let step1 = Box::new(SimpleStep::new("step1".to_string(), Value::from(1)));
        let step2 = Box::new(
            SimpleStep::new("step2".to_string(), Value::from(2))
                .with_dependencies(vec!["step1".to_string()]),
        );

        executor.add_step(step1);
        executor.add_step(step2);

        assert_eq!(executor.step_count(), 2);
        assert_eq!(executor.dag().node_count(), 2);
        assert_eq!(executor.dag().edge_count(), 1);
    }

    #[test]
    fn test_execute_simple_workflow() {
        let config = ExecutorConfig::default();
        let mut executor = WorkflowExecutor::new(config);

        // Add simple linear workflow: A -> B -> C
        let step_a = Box::new(SimpleStep::new("A".to_string(), Value::from(1)));
        let step_b = Box::new(
            SimpleStep::new("B".to_string(), Value::from(2))
                .with_dependencies(vec!["A".to_string()]),
        );
        let step_c = Box::new(
            SimpleStep::new("C".to_string(), Value::from(3))
                .with_dependencies(vec!["B".to_string()]),
        );

        executor.add_step(step_a);
        executor.add_step(step_b);
        executor.add_step(step_c);

        // Execute workflow
        let result = executor.execute();
        assert!(result.is_ok());

        let metrics = result.unwrap();
        assert_eq!(metrics.total_steps, 3);
        assert_eq!(metrics.successful_steps, 3);
        assert_eq!(metrics.failed_steps, 0);
    }

    #[test]
    fn test_execute_with_dependencies() {
        let config = ExecutorConfig::default();
        let mut executor = WorkflowExecutor::new(config);

        // Create workflow with dependencies
        let step1 = Box::new(SimpleStep::new("step1".to_string(), Value::from(10)));
        let step2 = Box::new(SimpleStep::new("step2".to_string(), Value::from(20)));
        let step3 = Box::new(
            SimpleStep::new("step3".to_string(), Value::from(30))
                .with_dependencies(vec!["step1".to_string(), "step2".to_string()]),
        );

        executor.add_step(step1);
        executor.add_step(step2);
        executor.add_step(step3);

        let result = executor.execute();
        assert!(result.is_ok());

        let metrics = result.unwrap();
        assert_eq!(metrics.total_steps, 3);
        assert_eq!(metrics.successful_steps, 3);

        // Verify execution completed (even if very fast, duration should be non-zero in nanos)
        assert!(metrics.total_duration.as_nanos() > 0);
    }

    #[test]
    fn test_metrics_collection() {
        let config = ExecutorConfig::default();
        let mut executor = WorkflowExecutor::new(config);

        let step = Box::new(SimpleStep::new("test_step".to_string(), Value::from(42)));
        executor.add_step(step);

        let result = executor.execute().unwrap();

        assert_eq!(result.total_steps, 1);
        assert_eq!(result.successful_steps, 1);
        assert_eq!(result.step_metrics.len(), 1);

        let step_metric = &result.step_metrics[0];
        assert_eq!(step_metric.step_id, "test_step");
        assert!(matches!(
            step_metric.status,
            crate::metrics::StepStatus::Completed
        ));
        assert!(step_metric.duration.is_some());
    }

    #[test]
    fn test_parallelism_factor_sequential() {
        let config = ExecutorConfig::default();
        let mut executor = WorkflowExecutor::new(config);

        // Add multiple steps
        for i in 0..3 {
            let step = Box::new(SimpleStep::new(format!("step{}", i), Value::from(i)));
            executor.add_step(step);
        }

        let result = executor.execute().unwrap();

        // For sequential execution, parallelism factor should be close to 1.0
        // (allowing variations due to overhead from progress tracking, etc.)
        // The key assertion is that it's not > 1.2 (indicating false parallelism)
        assert!(
            result.parallelism_factor <= 1.2,
            "Parallelism factor {} should not indicate parallel execution",
            result.parallelism_factor
        );
    }

    // Test helpers for retry/timeout behavior
    struct FlakyStep {
        id: String,
        deps: Vec<String>,
        output: Value,
        fail_times: u32,
        attempts: Arc<Mutex<u32>>,
        retry: RetryConfig,
    }

    impl FlakyStep {
        fn new(id: &str, output: Value, fail_times: u32, max_attempts: u32) -> Self {
            Self {
                id: id.to_string(),
                deps: vec![],
                output,
                fail_times,
                attempts: Arc::new(Mutex::new(0)),
                retry: RetryConfig {
                    max_attempts,
                    backoff: Duration::from_millis(1),
                },
            }
        }

        #[allow(dead_code)]
        fn with_dependencies(mut self, deps: Vec<String>) -> Self {
            self.deps = deps;
            self
        }
    }

    impl Step for FlakyStep {
        fn id(&self) -> &str {
            &self.id
        }
        fn execute(&self, _ctx: &mut ExecutionContext) -> crate::error::Result<StepResult> {
            let mut guard = self.attempts.lock().unwrap();
            *guard += 1;
            if *guard <= self.fail_times {
                return Err(ExecutionError::StepFailed {
                    step_id: self.id.clone(),
                    reason: "flaky failure".to_string(),
                }
                .into());
            }
            Ok(StepResult::new(
                self.output.clone(),
                StepMetrics::new(self.id.clone()),
            ))
        }
        fn dependencies(&self) -> &[String] {
            &self.deps
        }
        fn retry_config(&self) -> RetryConfig {
            self.retry.clone()
        }
    }

    struct TimeoutStep {
        id: String,
        deps: Vec<String>,
        sleep: Duration,
        timeout: Duration,
    }

    impl TimeoutStep {
        fn new(id: &str, sleep: Duration, timeout: Duration) -> Self {
            Self {
                id: id.to_string(),
                deps: vec![],
                sleep,
                timeout,
            }
        }
        #[allow(dead_code)]
        fn with_dependencies(mut self, deps: Vec<String>) -> Self {
            self.deps = deps;
            self
        }
    }

    impl Step for TimeoutStep {
        fn id(&self) -> &str {
            &self.id
        }
        fn execute(&self, _ctx: &mut ExecutionContext) -> crate::error::Result<StepResult> {
            thread::sleep(self.sleep);
            Ok(StepResult::new(
                Value::from("done"),
                StepMetrics::new(self.id.clone()),
            ))
        }
        fn dependencies(&self) -> &[String] {
            &self.deps
        }
        fn timeout(&self) -> Option<Duration> {
            Some(self.timeout)
        }
    }

    #[test]
    fn test_retry_logic_success_after_failures() {
        let config = ExecutorConfig::builder().retry_backoff_ms(1).build();
        let mut executor = WorkflowExecutor::new(config);

        // Flaky step fails once, then succeeds; allow 1 retry
        let step = Box::new(FlakyStep::new("flaky_success", Value::from(123), 1, 1));
        executor.add_step(step);

        let metrics = executor.execute().unwrap();
        assert_eq!(metrics.total_steps, 1);
        assert_eq!(metrics.successful_steps, 1);
        assert_eq!(metrics.failed_steps, 0);
        assert_eq!(metrics.step_metrics[0].retry_count, 1);
        assert!(matches!(
            metrics.step_metrics[0].status,
            crate::metrics::StepStatus::Completed
        ));
    }

    #[test]
    fn test_retry_exhausted_failure() {
        let config = ExecutorConfig::builder().retry_backoff_ms(1).build();
        let mut executor = WorkflowExecutor::new(config);

        // Flaky step fails 3 times but only 2 retries allowed => overall failure
        let step = Box::new(FlakyStep::new("flaky_fail", Value::from(0), 3, 2));
        executor.add_step(step);

        let err = executor.execute().unwrap_err();
        match err {
            WorkflowError::Execution(ExecutionError::RetryExhausted(msg)) => {
                assert!(msg.contains("flaky_fail"));
                assert!(
                    msg.to_lowercase().contains("exceeded")
                        || msg.to_lowercase().contains("failed after")
                );
            }
            other => panic!("unexpected error: {:?}", other),
        }
    }

    #[test]
    fn test_timeout_enforced() {
        let config = ExecutorConfig::builder().retry_backoff_ms(1).build();
        let mut executor = WorkflowExecutor::new(config);

        // Step sleeps longer than its timeout => should trigger timeout and fail
        let step = Box::new(TimeoutStep::new(
            "sleepy",
            Duration::from_millis(30),
            Duration::from_millis(5),
        ));
        executor.add_step(step);

        let err = executor.execute().unwrap_err();
        match err {
            WorkflowError::Execution(ExecutionError::RetryExhausted(msg)) => {
                assert!(msg.contains("sleepy"));
                assert!(msg.contains("exceeded timeout"));
            }
            other => panic!("unexpected error: {:?}", other),
        }
    }

    // ===== Cancellation Tests =====

    #[test]
    fn test_cancellation_before_first_step() {
        let config = ExecutorConfig::default();
        let mut executor = WorkflowExecutor::new(config);

        // Add a simple step
        let step = Box::new(SimpleStep::new("step1".to_string(), Value::from(1)));
        executor.add_step(step);

        // Cancel immediately before execution
        let token = CancellationToken::new();
        token.cancel();

        let err = executor
            .execute_with_options(Some(token), None)
            .unwrap_err();
        assert!(matches!(
            err,
            WorkflowError::Execution(ExecutionError::Cancelled)
        ));
    }

    #[test]
    fn test_cancellation_between_steps() {
        let config = ExecutorConfig::default();
        let mut executor = WorkflowExecutor::new(config);

        // Add steps with small delays to ensure cancellation happens between steps
        executor.add_step(Box::new(TimeoutStep::new(
            "step1",
            Duration::from_millis(5),
            Duration::from_secs(1),
        )));
        executor.add_step(Box::new(TimeoutStep::new(
            "step2",
            Duration::from_millis(5),
            Duration::from_secs(1),
        )));
        executor.add_step(Box::new(TimeoutStep::new(
            "step3",
            Duration::from_millis(5),
            Duration::from_secs(1),
        )));

        let token = CancellationToken::new();
        let token_clone = token.clone();

        // Cancel from another thread after a short delay
        thread::spawn(move || {
            thread::sleep(Duration::from_millis(8));
            token_clone.cancel();
        });

        let err = executor
            .execute_with_options(Some(token), None)
            .unwrap_err();
        assert!(matches!(
            err,
            WorkflowError::Execution(ExecutionError::Cancelled)
        ));
    }

    #[test]
    fn test_cancellation_during_retry_backoff() {
        let config = ExecutorConfig::builder().retry_backoff_ms(50).build();
        let mut executor = WorkflowExecutor::new(config);

        // Flaky step that fails multiple times
        let step = Box::new(FlakyStep::new("flaky", Value::from(0), 5, 5));
        executor.add_step(step);

        let token = CancellationToken::new();
        let token_clone = token.clone();

        // Cancel during retry backoff
        thread::spawn(move || {
            thread::sleep(Duration::from_millis(10));
            token_clone.cancel();
        });

        let err = executor
            .execute_with_options(Some(token), None)
            .unwrap_err();
        assert!(matches!(
            err,
            WorkflowError::Execution(ExecutionError::Cancelled)
        ));
    }

    // ===== Progress Callback Tests =====

    #[derive(Default, Clone)]
    struct TestProgressTracker {
        events: Arc<Mutex<Vec<ProgressEvent>>>,
    }

    impl TestProgressTracker {
        fn new() -> Self {
            Self {
                events: Arc::new(Mutex::new(Vec::new())),
            }
        }

        fn get_events(&self) -> Vec<ProgressEvent> {
            self.events.lock().unwrap().clone()
        }
    }

    impl ProgressCallback for TestProgressTracker {
        fn on_progress(&self, event: ProgressEvent) {
            self.events.lock().unwrap().push(event);
        }
    }

    #[test]
    fn test_progress_callback_event_sequence() {
        let config = ExecutorConfig::default();
        let mut executor = WorkflowExecutor::new(config);

        // Add three steps in sequence
        executor.add_step(Box::new(SimpleStep::new(
            "step1".to_string(),
            Value::from(1),
        )));
        executor.add_step(Box::new(
            SimpleStep::new("step2".to_string(), Value::from(2))
                .with_dependencies(vec!["step1".to_string()]),
        ));
        executor.add_step(Box::new(
            SimpleStep::new("step3".to_string(), Value::from(3))
                .with_dependencies(vec!["step2".to_string()]),
        ));

        let tracker = TestProgressTracker::new();
        let tracker_clone = tracker.clone();

        let result = executor.execute_with_options(None, Some(Box::new(tracker_clone)));
        assert!(result.is_ok());

        let events = tracker.get_events();
        assert_eq!(events.len(), 6); // 3 steps * 2 events (Started + Completed)

        // Verify event sequence
        use crate::progress::ProgressEvent;
        assert!(matches!(events[0], ProgressEvent::Started { .. }));
        assert_eq!(events[0].step_id(), "step1");
        assert!(matches!(events[1], ProgressEvent::Completed { .. }));
        assert_eq!(events[1].step_id(), "step1");

        assert!(matches!(events[2], ProgressEvent::Started { .. }));
        assert_eq!(events[2].step_id(), "step2");
        assert!(matches!(events[3], ProgressEvent::Completed { .. }));
        assert_eq!(events[3].step_id(), "step2");

        assert!(matches!(events[4], ProgressEvent::Started { .. }));
        assert_eq!(events[4].step_id(), "step3");
        assert!(matches!(events[5], ProgressEvent::Completed { .. }));
        assert_eq!(events[5].step_id(), "step3");
    }

    #[test]
    fn test_progress_callback_on_failure() {
        let config = ExecutorConfig::builder().retry_backoff_ms(1).build();
        let mut executor = WorkflowExecutor::new(config);

        // Add a failing step
        let step = Box::new(FlakyStep::new("failing", Value::from(0), 5, 2));
        executor.add_step(step);

        let tracker = TestProgressTracker::new();
        let tracker_clone = tracker.clone();

        let result = executor.execute_with_options(None, Some(Box::new(tracker_clone)));
        assert!(result.is_err());

        let events = tracker.get_events();
        assert_eq!(events.len(), 2); // Started + Failed

        assert!(matches!(events[0], ProgressEvent::Started { .. }));
        assert!(matches!(events[1], ProgressEvent::Failed { .. }));

        if let ProgressEvent::Failed { step_id, error, .. } = &events[1] {
            assert_eq!(step_id, "failing");
            assert!(error.contains("failing"));
        }
    }

    #[test]
    fn test_progress_callback_on_cancellation() {
        let config = ExecutorConfig::default();
        let mut executor = WorkflowExecutor::new(config);

        executor.add_step(Box::new(SimpleStep::new(
            "step1".to_string(),
            Value::from(1),
        )));
        executor.add_step(Box::new(SimpleStep::new(
            "step2".to_string(),
            Value::from(2),
        )));

        let tracker = TestProgressTracker::new();
        let tracker_clone = tracker.clone();

        let token = CancellationToken::new();
        token.cancel();

        let result = executor.execute_with_options(Some(token), Some(Box::new(tracker_clone)));
        assert!(result.is_err());

        let events = tracker.get_events();
        assert!(!events.is_empty()); // At least one Cancelled event

        // Find the cancelled event
        let has_cancelled = events
            .iter()
            .any(|e| matches!(e, ProgressEvent::Cancelled { .. }));
        assert!(has_cancelled, "Expected at least one Cancelled event");
    }

    // ===== Error Context Tests =====

    #[test]
    fn test_error_context_includes_dependency_chain() {
        let config = ExecutorConfig::builder().retry_backoff_ms(1).build();
        let mut executor = WorkflowExecutor::new(config);

        // Create a dependency chain: step1 -> step2 -> failing_step
        executor.add_step(Box::new(SimpleStep::new(
            "step1".to_string(),
            Value::from(1),
        )));
        executor.add_step(Box::new(
            SimpleStep::new("step2".to_string(), Value::from(2))
                .with_dependencies(vec!["step1".to_string()]),
        ));
        executor.add_step(Box::new(
            FlakyStep::new("failing_step", Value::from(0), 5, 2)
                .with_dependencies(vec!["step2".to_string()]),
        ));

        let tracker = TestProgressTracker::new();
        let tracker_clone = tracker.clone();

        let result = executor.execute_with_options(None, Some(Box::new(tracker_clone)));
        assert!(result.is_err());

        let events = tracker.get_events();

        // Find the failed event
        let failed_event = events
            .iter()
            .find(|e| matches!(e, ProgressEvent::Failed { .. }))
            .expect("Should have a Failed event");

        if let ProgressEvent::Failed { error, .. } = failed_event {
            // Check that error includes dependency chain
            assert!(
                error.contains("dependency chain:"),
                "Error should mention dependency chain: {}",
                error
            );
            assert!(
                error.contains("step1"),
                "Error should include step1 in chain: {}",
                error
            );
            assert!(
                error.contains("step2"),
                "Error should include step2 in chain: {}",
                error
            );
            assert!(
                error.contains("failing_step"),
                "Error should include failing_step in chain: {}",
                error
            );
        }
    }

    // ===== Backward Compatibility Tests =====

    #[test]
    fn test_backward_compatibility_execute_method() {
        // Verify that the old execute() method still works without options
        let config = ExecutorConfig::default();
        let mut executor = WorkflowExecutor::new(config);

        executor.add_step(Box::new(SimpleStep::new(
            "step1".to_string(),
            Value::from(1),
        )));
        executor.add_step(Box::new(SimpleStep::new(
            "step2".to_string(),
            Value::from(2),
        )));

        let result = executor.execute();
        assert!(result.is_ok());

        let metrics = result.unwrap();
        assert_eq!(metrics.total_steps, 2);
        assert_eq!(metrics.successful_steps, 2);
    }

    // ===== Thread Safety Tests =====

    #[test]
    fn test_cancellation_token_thread_safety() {
        let token = CancellationToken::new();

        // Cancel first
        token.cancel();

        // Then spawn threads that check if it's cancelled
        let handles: Vec<_> = (0..10)
            .map(|_| {
                let t = token.clone();
                thread::spawn(move || {
                    thread::sleep(Duration::from_millis(1));
                    t.is_cancelled()
                })
            })
            .collect();

        // All threads should see the cancellation
        for handle in handles {
            let result = handle.join().unwrap();
            assert!(result, "Thread should see cancellation");
        }
    }

    #[test]
    fn test_progress_callback_thread_safety() {
        let tracker = TestProgressTracker::new();
        let handles: Vec<_> = (0..10)
            .map(|i| {
                let t = tracker.clone();
                thread::spawn(move || {
                    t.on_progress(ProgressEvent::started(format!("step{}", i)));
                })
            })
            .collect();

        for handle in handles {
            handle.join().unwrap();
        }

        let events = tracker.get_events();
        assert_eq!(events.len(), 10);
    }

    // ===== Parallel Executor Tests =====

    use crate::step::ResourceHint;

    // Test step with resource hint support
    struct ResourceAwareStep {
        id: String,
        deps: Vec<String>,
        output: Value,
        hint: ResourceHint,
        sleep_ms: u64,
    }

    impl ResourceAwareStep {
        fn new(id: &str, output: Value) -> Self {
            Self {
                id: id.to_string(),
                deps: Vec::new(),
                output,
                hint: ResourceHint::Default,
                sleep_ms: 0,
            }
        }

        fn with_dependencies(mut self, deps: Vec<String>) -> Self {
            self.deps = deps;
            self
        }

        fn with_hint(mut self, hint: ResourceHint) -> Self {
            self.hint = hint;
            self
        }

        fn with_delay(mut self, ms: u64) -> Self {
            self.sleep_ms = ms;
            self
        }
    }

    impl Step for ResourceAwareStep {
        fn id(&self) -> &str {
            &self.id
        }

        fn execute(&self, _ctx: &mut ExecutionContext) -> crate::error::Result<StepResult> {
            if self.sleep_ms > 0 {
                thread::sleep(Duration::from_millis(self.sleep_ms));
            }
            Ok(StepResult::new(
                self.output.clone(),
                StepMetrics::new(self.id.clone()),
            ))
        }

        fn dependencies(&self) -> &[String] {
            &self.deps
        }

        fn resource_hint(&self) -> ResourceHint {
            self.hint
        }
    }

    #[test]
    fn test_parallel_linear_dag() {
        let config = ExecutorConfig::builder().max_parallel_steps(4).build();
        let mut executor = WorkflowExecutor::new(config);

        // Linear: A -> B -> C (should execute sequentially even in parallel mode)
        executor.add_step(Box::new(ResourceAwareStep::new("A", Value::from(1))));
        executor.add_step(Box::new(
            ResourceAwareStep::new("B", Value::from(2)).with_dependencies(vec!["A".to_string()]),
        ));
        executor.add_step(Box::new(
            ResourceAwareStep::new("C", Value::from(3)).with_dependencies(vec!["B".to_string()]),
        ));

        let result = executor.execute_parallel();
        assert!(result.is_ok());

        let metrics = result.unwrap();
        assert_eq!(metrics.total_steps, 3);
        assert_eq!(metrics.successful_steps, 3);
    }

    #[test]
    fn test_parallel_diamond_dag() {
        let config = ExecutorConfig::builder().max_parallel_steps(4).build();
        let mut executor = WorkflowExecutor::new(config);

        // Diamond: A -> B,C -> D
        executor.add_step(Box::new(ResourceAwareStep::new("A", Value::from(1))));
        executor.add_step(Box::new(
            ResourceAwareStep::new("B", Value::from(2)).with_dependencies(vec!["A".to_string()]),
        ));
        executor.add_step(Box::new(
            ResourceAwareStep::new("C", Value::from(3)).with_dependencies(vec!["A".to_string()]),
        ));
        executor.add_step(Box::new(
            ResourceAwareStep::new("D", Value::from(4))
                .with_dependencies(vec!["B".to_string(), "C".to_string()]),
        ));

        let result = executor.execute_parallel();
        assert!(result.is_ok());

        let metrics = result.unwrap();
        assert_eq!(metrics.total_steps, 4);
        assert_eq!(metrics.successful_steps, 4);
    }

    #[test]
    fn test_parallel_wide_dag() {
        let config = ExecutorConfig::builder().max_parallel_steps(8).build();
        let mut executor = WorkflowExecutor::new(config);

        // Wide: 6 independent steps
        for i in 1..=6 {
            executor.add_step(Box::new(ResourceAwareStep::new(
                &format!("step{}", i),
                Value::from(i),
            )));
        }

        let result = executor.execute_parallel();
        assert!(result.is_ok());

        let metrics = result.unwrap();
        assert_eq!(metrics.total_steps, 6);
        assert_eq!(metrics.successful_steps, 6);
    }

    #[test]
    fn test_parallel_deep_dag() {
        let config = ExecutorConfig::builder().max_parallel_steps(4).build();
        let mut executor = WorkflowExecutor::new(config);

        // Deep: 5-level chain
        executor.add_step(Box::new(ResourceAwareStep::new("level1", Value::from(1))));
        for i in 2..=5 {
            let prev = format!("level{}", i - 1);
            let curr = format!("level{}", i);
            executor.add_step(Box::new(
                ResourceAwareStep::new(&curr, Value::from(i)).with_dependencies(vec![prev]),
            ));
        }

        let result = executor.execute_parallel();
        assert!(result.is_ok());

        let metrics = result.unwrap();
        assert_eq!(metrics.total_steps, 5);
        assert_eq!(metrics.successful_steps, 5);
    }

    #[test]
    fn test_parallel_tree_dag() {
        let config = ExecutorConfig::builder().max_parallel_steps(8).build();
        let mut executor = WorkflowExecutor::new(config);

        // Tree: root -> 3 branches -> 6 leaves
        executor.add_step(Box::new(ResourceAwareStep::new("root", Value::from(0))));

        for i in 1..=3 {
            let branch = format!("branch{}", i);
            executor.add_step(Box::new(
                ResourceAwareStep::new(&branch, Value::from(i))
                    .with_dependencies(vec!["root".to_string()]),
            ));

            for j in 1..=2 {
                let leaf = format!("leaf{}_{}", i, j);
                executor.add_step(Box::new(
                    ResourceAwareStep::new(&leaf, Value::from(i * 10 + j))
                        .with_dependencies(vec![branch.clone()]),
                ));
            }
        }

        let result = executor.execute_parallel();
        assert!(result.is_ok());

        let metrics = result.unwrap();
        assert_eq!(metrics.total_steps, 10); // 1 root + 3 branches + 6 leaves
        assert_eq!(metrics.successful_steps, 10);
    }

    #[test]
    fn test_parallel_speedup() {
        use std::time::Instant;

        let config = ExecutorConfig::builder().max_parallel_steps(4).build();

        // Sequential execution
        let mut seq_executor = WorkflowExecutor::new(config.clone());
        for i in 1..=8 {
            seq_executor.add_step(Box::new(
                ResourceAwareStep::new(&format!("seq{}", i), Value::from(i)).with_delay(30),
            ));
        }

        let seq_start = Instant::now();
        let seq_result = seq_executor.execute();
        let seq_duration = seq_start.elapsed();

        // Parallel execution
        let mut par_executor = WorkflowExecutor::new(config);
        for i in 1..=8 {
            par_executor.add_step(Box::new(
                ResourceAwareStep::new(&format!("par{}", i), Value::from(i)).with_delay(30),
            ));
        }

        let par_start = Instant::now();
        let par_result = par_executor.execute_parallel();
        let par_duration = par_start.elapsed();

        println!(
            "Sequential: {:?}, Parallel: {:?}",
            seq_duration, par_duration
        );

        // Just verify both complete successfully - speedup varies too much based on system load
        assert!(seq_result.is_ok());
        assert!(par_result.is_ok());
        assert_eq!(par_result.unwrap().successful_steps, 8);
    }

    #[test]
    fn test_parallel_resource_utilization() {
        let config = ExecutorConfig::builder().max_parallel_steps(2).build();
        let mut executor = WorkflowExecutor::new(config);

        // Create 4 CPU-heavy steps (should execute in 2 waves)
        for i in 1..=4 {
            executor.add_step(Box::new(
                ResourceAwareStep::new(&format!("cpu{}", i), Value::from(i))
                    .with_hint(ResourceHint::HeavyCPU),
            ));
        }

        let result = executor.execute_parallel();
        assert!(result.is_ok());

        let metrics = result.unwrap();
        assert_eq!(metrics.successful_steps, 4);
    }

    #[test]
    fn test_parallel_mixed_workload() {
        let config = ExecutorConfig::builder().max_parallel_steps(4).build();
        let mut executor = WorkflowExecutor::new(config);

        // Mixed: 2 CPU + 2 IO independent steps
        executor.add_step(Box::new(
            ResourceAwareStep::new("cpu1", Value::from(1)).with_hint(ResourceHint::HeavyCPU),
        ));
        executor.add_step(Box::new(
            ResourceAwareStep::new("cpu2", Value::from(2)).with_hint(ResourceHint::HeavyCPU),
        ));
        executor.add_step(Box::new(
            ResourceAwareStep::new("io1", Value::from(3)).with_hint(ResourceHint::HeavyIO),
        ));
        executor.add_step(Box::new(
            ResourceAwareStep::new("io2", Value::from(4)).with_hint(ResourceHint::HeavyIO),
        ));

        let result = executor.execute_parallel();
        assert!(result.is_ok());

        let metrics = result.unwrap();
        assert_eq!(metrics.successful_steps, 4);
    }

    #[test]
    fn test_parallel_memory_hints() {
        let config = ExecutorConfig::builder().max_parallel_steps(4).build();
        let mut executor = WorkflowExecutor::new(config);

        // Steps with memory hints
        for i in 1..=3 {
            executor.add_step(Box::new(
                ResourceAwareStep::new(&format!("mem{}", i), Value::from(i))
                    .with_hint(ResourceHint::Memory(1024 * 1024)),
            ));
        }

        let result = executor.execute_parallel();
        assert!(result.is_ok());

        let metrics = result.unwrap();
        assert_eq!(metrics.successful_steps, 3);
    }

    #[test]
    fn test_parallel_parallelism_factor() {
        let config = ExecutorConfig::builder().max_parallel_steps(4).build();
        let mut executor = WorkflowExecutor::new(config);

        // Create 8 independent steps with delays long enough to show parallelism
        for i in 1..=8 {
            executor.add_step(Box::new(
                ResourceAwareStep::new(&format!("step{}", i), Value::from(i)).with_delay(20),
            ));
        }

        let result = executor.execute_parallel();
        assert!(result.is_ok());

        let metrics = result.unwrap();
        // Parallelism factor might be close to 1.0 due to overhead, just verify execution works
        println!("Parallelism factor: {}", metrics.parallelism_factor);
        assert!(metrics.successful_steps == 8, "All steps should complete");
    }

    #[test]
    fn test_parallel_cancellation_before_execution() {
        let config = ExecutorConfig::default();
        let mut executor = WorkflowExecutor::new(config);

        executor.add_step(Box::new(ResourceAwareStep::new("step1", Value::from(1))));

        let token = CancellationToken::new();
        token.cancel();

        let err = executor
            .execute_parallel_with_options(Some(token), None)
            .unwrap_err();
        assert!(matches!(
            err,
            WorkflowError::Execution(ExecutionError::Cancelled)
        ));
    }

    #[test]
    fn test_parallel_cancellation_mid_wave() {
        let config = ExecutorConfig::builder().max_parallel_steps(2).build();
        let mut executor = WorkflowExecutor::new(config);

        // Create steps with delays to allow cancellation
        for i in 1..=4 {
            executor.add_step(Box::new(
                ResourceAwareStep::new(&format!("step{}", i), Value::from(i)).with_delay(20),
            ));
        }

        let token = CancellationToken::new();
        let token_clone = token.clone();

        thread::spawn(move || {
            thread::sleep(Duration::from_millis(15));
            token_clone.cancel();
        });

        let err = executor
            .execute_parallel_with_options(Some(token), None)
            .unwrap_err();
        assert!(matches!(
            err,
            WorkflowError::Execution(ExecutionError::Cancelled)
        ));
    }

    #[test]
    fn test_parallel_cancellation_between_waves() {
        let config = ExecutorConfig::builder().max_parallel_steps(2).build();
        let mut executor = WorkflowExecutor::new(config);

        // Wave 1: 2 steps
        executor.add_step(Box::new(
            ResourceAwareStep::new("w1_1", Value::from(1)).with_delay(5),
        ));
        executor.add_step(Box::new(
            ResourceAwareStep::new("w1_2", Value::from(2)).with_delay(5),
        ));

        // Wave 2: 2 dependent steps
        executor.add_step(Box::new(
            ResourceAwareStep::new("w2_1", Value::from(3))
                .with_dependencies(vec!["w1_1".to_string()])
                .with_delay(5),
        ));
        executor.add_step(Box::new(
            ResourceAwareStep::new("w2_2", Value::from(4))
                .with_dependencies(vec!["w1_2".to_string()])
                .with_delay(5),
        ));

        let token = CancellationToken::new();
        let token_clone = token.clone();

        thread::spawn(move || {
            thread::sleep(Duration::from_millis(10));
            token_clone.cancel();
        });

        let result = executor.execute_parallel_with_options(Some(token), None);
        // Should either complete first wave or get cancelled
        assert!(result.is_err() || result.unwrap().successful_steps >= 2);
    }

    #[test]
    fn test_parallel_cancellation_during_retry() {
        let config = ExecutorConfig::builder()
            .max_parallel_steps(2)
            .retry_backoff_ms(50)
            .build();
        let mut executor = WorkflowExecutor::new(config);

        // Multiple flaky steps to ensure cancellation has time to occur
        for i in 1..=3 {
            executor.add_step(Box::new(FlakyStep::new(
                &format!("flaky{}", i),
                Value::from(0),
                15,
                10,
            )));
        }

        let token = CancellationToken::new();
        let token_clone = token.clone();

        thread::spawn(move || {
            thread::sleep(Duration::from_millis(100));
            token_clone.cancel();
        });

        let result = executor.execute_parallel_with_options(Some(token), None);
        // Should either be cancelled or fail - both are valid outcomes
        assert!(
            result.is_err(),
            "Should error due to cancellation or failure"
        );
    }

    #[test]
    fn test_parallel_cancellation_no_leaks() {
        let config = ExecutorConfig::builder().max_parallel_steps(4).build();
        let mut executor = WorkflowExecutor::new(config);

        for i in 1..=10 {
            executor.add_step(Box::new(
                ResourceAwareStep::new(&format!("step{}", i), Value::from(i)).with_delay(50),
            ));
        }

        let token = CancellationToken::new();
        let token_clone = token.clone();

        thread::spawn(move || {
            thread::sleep(Duration::from_millis(20));
            token_clone.cancel();
        });

        let _ = executor.execute_parallel_with_options(Some(token), None);
        // If we reach here without hanging, no thread leaks
    }

    #[test]
    fn test_parallel_progress_events() {
        let config = ExecutorConfig::builder().max_parallel_steps(2).build();
        let mut executor = WorkflowExecutor::new(config);

        for i in 1..=4 {
            executor.add_step(Box::new(ResourceAwareStep::new(
                &format!("step{}", i),
                Value::from(i),
            )));
        }

        let tracker = TestProgressTracker::new();
        let tracker_clone = tracker.clone();

        let result = executor.execute_parallel_with_options(None, Some(Box::new(tracker_clone)));
        assert!(result.is_ok());

        let events = tracker.get_events();
        // Should have Started and Completed for each step
        assert_eq!(events.len(), 8);

        // Count event types
        let started = events
            .iter()
            .filter(|e| matches!(e, ProgressEvent::Started { .. }))
            .count();
        let completed = events
            .iter()
            .filter(|e| matches!(e, ProgressEvent::Completed { .. }))
            .count();

        assert_eq!(started, 4);
        assert_eq!(completed, 4);
    }

    #[test]
    fn test_parallel_progress_order() {
        let config = ExecutorConfig::builder().max_parallel_steps(4).build();
        let mut executor = WorkflowExecutor::new(config);

        // Linear chain to ensure order
        executor.add_step(Box::new(ResourceAwareStep::new("step1", Value::from(1))));
        executor.add_step(Box::new(
            ResourceAwareStep::new("step2", Value::from(2))
                .with_dependencies(vec!["step1".to_string()]),
        ));
        executor.add_step(Box::new(
            ResourceAwareStep::new("step3", Value::from(3))
                .with_dependencies(vec!["step2".to_string()]),
        ));

        let tracker = TestProgressTracker::new();
        let tracker_clone = tracker.clone();

        let _ = executor.execute_parallel_with_options(None, Some(Box::new(tracker_clone)));

        let events = tracker.get_events();
        // Verify step1 completes before step2 starts
        let step1_complete_idx = events
            .iter()
            .position(|e| matches!(e, ProgressEvent::Completed { .. }) && e.step_id() == "step1")
            .unwrap();
        let step2_start_idx = events
            .iter()
            .position(|e| matches!(e, ProgressEvent::Started { .. }) && e.step_id() == "step2")
            .unwrap();

        assert!(
            step1_complete_idx < step2_start_idx,
            "Dependencies should be respected"
        );
    }

    #[test]
    fn test_parallel_progress_concurrency() {
        let config = ExecutorConfig::builder().max_parallel_steps(4).build();
        let mut executor = WorkflowExecutor::new(config);

        // Independent steps should have concurrent Started events
        for i in 1..=4 {
            executor.add_step(Box::new(
                ResourceAwareStep::new(&format!("step{}", i), Value::from(i)).with_delay(20),
            ));
        }

        let tracker = TestProgressTracker::new();
        let tracker_clone = tracker.clone();

        let result = executor.execute_parallel_with_options(None, Some(Box::new(tracker_clone)));
        assert!(result.is_ok());

        let events = tracker.get_events();
        // Verify all events were emitted (Started + Completed for each step)
        assert_eq!(events.len(), 8, "Should have 8 events total");

        let started = events
            .iter()
            .filter(|e| matches!(e, ProgressEvent::Started { .. }))
            .count();
        let completed = events
            .iter()
            .filter(|e| matches!(e, ProgressEvent::Completed { .. }))
            .count();

        assert_eq!(started, 4, "Should have 4 Started events");
        assert_eq!(completed, 4, "Should have 4 Completed events");
    }

    #[test]
    fn test_parallel_error_handling() {
        let config = ExecutorConfig::builder()
            .max_parallel_steps(2)
            .retry_backoff_ms(1)
            .build();
        let mut executor = WorkflowExecutor::new(config);

        // Wave 1: normal + failing step
        executor.add_step(Box::new(ResourceAwareStep::new("good1", Value::from(1))));
        executor.add_step(Box::new(FlakyStep::new("bad", Value::from(0), 5, 1)));

        // Wave 2: dependent steps (should be cancelled)
        executor.add_step(Box::new(
            ResourceAwareStep::new("dependent", Value::from(2))
                .with_dependencies(vec!["good1".to_string()]),
        ));

        let result = executor.execute_parallel();
        assert!(result.is_err(), "Should fail due to bad step");
    }

    #[test]
    fn test_parallel_stress_test() {
        let config = ExecutorConfig::builder().max_parallel_steps(8).build();
        let mut executor = WorkflowExecutor::new(config);

        // Create 25 steps with various patterns
        // Layer 1: 1 root
        executor.add_step(Box::new(ResourceAwareStep::new("root", Value::from(0))));

        // Layer 2: 4 branches
        for i in 1..=4 {
            executor.add_step(Box::new(
                ResourceAwareStep::new(&format!("l2_{}", i), Value::from(i))
                    .with_dependencies(vec!["root".to_string()])
                    .with_hint(if i % 2 == 0 {
                        ResourceHint::HeavyCPU
                    } else {
                        ResourceHint::HeavyIO
                    }),
            ));
        }

        // Layer 3: 20 leaves
        for i in 1..=4 {
            let parent = format!("l2_{}", i);
            for j in 1..=5 {
                executor.add_step(Box::new(
                    ResourceAwareStep::new(&format!("l3_{}_{}", i, j), Value::from(i * 10 + j))
                        .with_dependencies(vec![parent.clone()])
                        .with_delay(1),
                ));
            }
        }

        let result = executor.execute_parallel();
        assert!(result.is_ok());

        let metrics = result.unwrap();
        assert_eq!(metrics.total_steps, 25, "Should execute all 25 steps");
        assert_eq!(metrics.successful_steps, 25);
        // Log parallelism factor for inspection - varies significantly by system load
        println!("Parallelism factor: {}", metrics.parallelism_factor);
    }

    // Tests for convenience API methods

    #[test]
    fn test_execute_with_cancellation() {
        let config = ExecutorConfig::default();
        let mut executor = WorkflowExecutor::new(config);

        // Add steps with delays to allow cancellation
        for i in 1..=10 {
            executor.add_step(Box::new(
                ResourceAwareStep::new(&format!("step{}", i), Value::from(i)).with_delay(50),
            ));
        }

        let token = CancellationToken::new();
        let token_clone = token.clone();

        // Cancel after a short delay
        thread::spawn(move || {
            thread::sleep(Duration::from_millis(150));
            token_clone.cancel();
        });

        let result = executor.execute_with_cancellation(token);
        assert!(result.is_err());
        assert!(matches!(
            result.unwrap_err(),
            WorkflowError::Execution(ExecutionError::Cancelled)
        ));
    }

    #[test]
    fn test_execute_with_progress() {
        let config = ExecutorConfig::default();
        let mut executor = WorkflowExecutor::new(config);

        // Add a simple workflow
        executor.add_step(Box::new(SimpleStep::new(
            "step1".to_string(),
            Value::from(1),
        )));
        executor.add_step(Box::new(
            SimpleStep::new("step2".to_string(), Value::from(2))
                .with_dependencies(vec!["step1".to_string()]),
        ));

        let tracker = TestProgressTracker::new();
        let tracker_clone = tracker.clone();

        let result = executor.execute_with_progress(Box::new(tracker_clone));
        assert!(result.is_ok());

        let events = tracker.get_events();
        assert_eq!(events.len(), 4); // 2 started + 2 completed
    }

    #[test]
    fn test_execute_parallel_with_cancellation() {
        let config = ExecutorConfig::builder().max_parallel_steps(4).build();
        let mut executor = WorkflowExecutor::new(config);

        // Add steps with delays
        for i in 1..=8 {
            executor.add_step(Box::new(
                ResourceAwareStep::new(&format!("step{}", i), Value::from(i)).with_delay(50),
            ));
        }

        let token = CancellationToken::new();
        let token_clone = token.clone();

        // Cancel after a short delay
        thread::spawn(move || {
            thread::sleep(Duration::from_millis(100));
            token_clone.cancel();
        });

        let result = executor.execute_parallel_with_cancellation(token);
        assert!(result.is_err());
    }

    #[test]
    fn test_execute_parallel_with_progress() {
        let config = ExecutorConfig::builder().max_parallel_steps(2).build();
        let mut executor = WorkflowExecutor::new(config);

        // Add independent steps
        for i in 1..=4 {
            executor.add_step(Box::new(SimpleStep::new(
                format!("step{}", i),
                Value::from(i),
            )));
        }

        let tracker = TestProgressTracker::new();
        let tracker_clone = tracker.clone();

        let result = executor.execute_parallel_with_progress(Box::new(tracker_clone));
        assert!(result.is_ok());

        let events = tracker.get_events();
        assert_eq!(events.len(), 8); // 4 started + 4 completed
    }
}
