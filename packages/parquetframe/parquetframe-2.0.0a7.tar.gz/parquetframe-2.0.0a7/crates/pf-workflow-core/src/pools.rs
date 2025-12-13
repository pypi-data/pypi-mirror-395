//! Thread pool management for workflow execution.
//!
//! This module provides a hybrid thread pool manager that handles both CPU-bound
//! and I/O-bound tasks efficiently. It uses Rayon for CPU parallelism and optionally
//! Tokio for async I/O operations.

use crate::config::ExecutorConfig;
use crate::error::{ResourceError, Result};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;

/// Manager for hybrid thread pools supporting CPU and I/O workloads.
///
/// The `ThreadPoolManager` coordinates execution across different types of tasks:
/// - CPU-bound tasks run on the Rayon global thread pool
/// - I/O-bound tasks run on an optional Tokio runtime (feature-gated)
///
/// Resource tracking ensures that concurrency limits are respected to prevent
/// over-subscription and resource exhaustion.
///
/// # Examples
///
/// ```
/// use pf_workflow_core::{ExecutorConfig, ThreadPoolManager};
///
/// let config = ExecutorConfig::builder()
///     .max_parallel_steps(4)
///     .build();
///
/// let pool_manager = ThreadPoolManager::new(&config);
/// assert!(pool_manager.has_cpu_capacity());
/// ```
#[derive(Debug)]
pub struct ThreadPoolManager {
    /// Maximum number of concurrent CPU tasks.
    max_cpu_tasks: usize,

    /// Maximum number of concurrent I/O tasks.
    #[allow(dead_code)]
    max_io_tasks: usize,

    /// Current number of in-flight CPU tasks.
    in_flight_cpu: Arc<AtomicUsize>,

    /// Current number of in-flight I/O tasks.
    #[allow(dead_code)]
    in_flight_io: Arc<AtomicUsize>,

    /// Optional Tokio runtime for async I/O (feature-gated).
    #[cfg(feature = "async")]
    tokio_runtime: Option<tokio::runtime::Runtime>,
}

impl ThreadPoolManager {
    /// Create a new thread pool manager from executor configuration.
    ///
    /// # Arguments
    ///
    /// * `config` - Executor configuration specifying resource limits
    ///
    /// # Examples
    ///
    /// ```
    /// use pf_workflow_core::{ExecutorConfig, ThreadPoolManager};
    ///
    /// let config = ExecutorConfig::builder()
    ///     .max_parallel_steps(8)
    ///     .build();
    ///
    /// let manager = ThreadPoolManager::new(&config);
    /// ```
    pub fn new(config: &ExecutorConfig) -> Self {
        let max_parallel = config.get_max_parallel_steps();

        // For CPU tasks, use the configured max parallel steps
        let max_cpu_tasks = max_parallel;

        // For I/O tasks, allow more concurrency since they're waiting on I/O
        // Default to 2x CPU limit for I/O tasks
        let max_io_tasks = max_parallel * 2;

        #[cfg(feature = "async")]
        let tokio_runtime = Self::create_tokio_runtime(max_io_tasks);

        Self {
            max_cpu_tasks,
            max_io_tasks,
            in_flight_cpu: Arc::new(AtomicUsize::new(0)),
            in_flight_io: Arc::new(AtomicUsize::new(0)),
            #[cfg(feature = "async")]
            tokio_runtime,
        }
    }

    /// Create a Tokio runtime for I/O tasks.
    #[cfg(feature = "async")]
    fn create_tokio_runtime(worker_threads: usize) -> Option<tokio::runtime::Runtime> {
        tokio::runtime::Builder::new_multi_thread()
            .worker_threads(worker_threads)
            .thread_name("pf-workflow-io")
            .enable_all()
            .build()
            .ok()
    }

    /// Check if there is capacity for more CPU tasks.
    ///
    /// Returns `true` if the number of in-flight CPU tasks is below the limit.
    pub fn has_cpu_capacity(&self) -> bool {
        self.in_flight_cpu.load(Ordering::Acquire) < self.max_cpu_tasks
    }

    /// Check if there is capacity for more I/O tasks.
    ///
    /// Returns `true` if the number of in-flight I/O tasks is below the limit.
    #[allow(dead_code)]
    pub fn has_io_capacity(&self) -> bool {
        self.in_flight_io.load(Ordering::Acquire) < self.max_io_tasks
    }

    /// Reserve a slot for a CPU task.
    ///
    /// Increments the in-flight CPU task counter. Returns an error if
    /// no capacity is available.
    ///
    /// # Errors
    ///
    /// Returns `ResourceError::ThreadPoolExhausted` if the CPU pool is at capacity.
    pub fn reserve_cpu_slot(&self) -> Result<CpuSlot> {
        let current = self.in_flight_cpu.fetch_add(1, Ordering::AcqRel);
        if current >= self.max_cpu_tasks {
            // Rollback the increment
            self.in_flight_cpu.fetch_sub(1, Ordering::AcqRel);
            return Err(ResourceError::ThreadPoolExhausted.into());
        }
        Ok(CpuSlot {
            counter: Arc::clone(&self.in_flight_cpu),
        })
    }

    /// Reserve a slot for an I/O task.
    ///
    /// Increments the in-flight I/O task counter. Returns an error if
    /// no capacity is available.
    ///
    /// # Errors
    ///
    /// Returns `ResourceError::ThreadPoolExhausted` if the I/O pool is at capacity.
    #[allow(dead_code)]
    pub fn reserve_io_slot(&self) -> Result<IoSlot> {
        let current = self.in_flight_io.fetch_add(1, Ordering::AcqRel);
        if current >= self.max_io_tasks {
            // Rollback the increment
            self.in_flight_io.fetch_sub(1, Ordering::AcqRel);
            return Err(ResourceError::ThreadPoolExhausted.into());
        }
        Ok(IoSlot {
            counter: Arc::clone(&self.in_flight_io),
        })
    }

    /// Execute a CPU-bound task on the Rayon thread pool.
    ///
    /// The task runs in parallel with other CPU tasks up to the configured limit.
    /// The slot is automatically released when the task completes.
    ///
    /// # Arguments
    ///
    /// * `f` - Closure to execute on the thread pool
    ///
    /// # Examples
    ///
    /// ```no_run
    /// use pf_workflow_core::{ExecutorConfig, ThreadPoolManager};
    ///
    /// let config = ExecutorConfig::default();
    /// let manager = ThreadPoolManager::new(&config);
    ///
    /// let result = manager.execute_cpu(|| {
    ///     // CPU-intensive work
    ///     42
    /// });
    /// ```
    pub fn execute_cpu<F, R>(&self, f: F) -> Result<R>
    where
        F: FnOnce() -> R + Send,
        R: Send,
    {
        let _slot = self.reserve_cpu_slot()?;

        // Execute on Rayon's global thread pool
        let result = rayon::scope(|_s| f());

        // Slot is automatically released when _slot is dropped
        Ok(result)
    }

    /// Get the number of currently in-flight CPU tasks.
    pub fn in_flight_cpu_count(&self) -> usize {
        self.in_flight_cpu.load(Ordering::Acquire)
    }

    /// Get the number of currently in-flight I/O tasks.
    #[allow(dead_code)]
    pub fn in_flight_io_count(&self) -> usize {
        self.in_flight_io.load(Ordering::Acquire)
    }

    /// Get the maximum number of concurrent CPU tasks allowed.
    pub fn max_cpu_tasks(&self) -> usize {
        self.max_cpu_tasks
    }

    /// Get the maximum number of concurrent I/O tasks allowed.
    #[allow(dead_code)]
    pub fn max_io_tasks(&self) -> usize {
        self.max_io_tasks
    }

    /// Check if the Tokio runtime is available for I/O tasks.
    #[cfg(feature = "async")]
    pub fn has_tokio_runtime(&self) -> bool {
        self.tokio_runtime.is_some()
    }

    /// Check if the Tokio runtime is available for I/O tasks.
    #[cfg(not(feature = "async"))]
    pub fn has_tokio_runtime(&self) -> bool {
        false
    }
}

/// RAII guard for a CPU task slot.
///
/// When dropped, automatically decrements the in-flight CPU task counter.
#[derive(Debug)]
pub struct CpuSlot {
    counter: Arc<AtomicUsize>,
}

impl Drop for CpuSlot {
    fn drop(&mut self) {
        self.counter.fetch_sub(1, Ordering::AcqRel);
    }
}

/// RAII guard for an I/O task slot.
///
/// When dropped, automatically decrements the in-flight I/O task counter.
#[derive(Debug)]
#[allow(dead_code)]
pub struct IoSlot {
    counter: Arc<AtomicUsize>,
}

impl Drop for IoSlot {
    fn drop(&mut self) {
        self.counter.fetch_sub(1, Ordering::AcqRel);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::Barrier;
    use std::thread;
    use std::time::Duration;

    #[test]
    fn test_pool_manager_creation() {
        let config = ExecutorConfig::default();
        let manager = ThreadPoolManager::new(&config);

        assert!(manager.max_cpu_tasks() > 0);
        assert!(manager.max_io_tasks() > 0);
        assert_eq!(manager.in_flight_cpu_count(), 0);
        assert_eq!(manager.in_flight_io_count(), 0);
    }

    #[test]
    fn test_cpu_capacity_check() {
        let config = ExecutorConfig::builder().max_parallel_steps(2).build();
        let manager = ThreadPoolManager::new(&config);

        assert!(manager.has_cpu_capacity());
        assert_eq!(manager.max_cpu_tasks(), 2);
    }

    #[test]
    fn test_reserve_cpu_slot() {
        let config = ExecutorConfig::builder().max_parallel_steps(2).build();
        let manager = ThreadPoolManager::new(&config);

        let slot1 = manager.reserve_cpu_slot();
        assert!(slot1.is_ok());
        assert_eq!(manager.in_flight_cpu_count(), 1);

        let slot2 = manager.reserve_cpu_slot();
        assert!(slot2.is_ok());
        assert_eq!(manager.in_flight_cpu_count(), 2);

        // Should fail - at capacity
        let slot3 = manager.reserve_cpu_slot();
        assert!(slot3.is_err());
        assert_eq!(manager.in_flight_cpu_count(), 2);

        // Drop slot1, should free capacity
        drop(slot1);
        assert_eq!(manager.in_flight_cpu_count(), 1);

        // Should succeed now
        let slot4 = manager.reserve_cpu_slot();
        assert!(slot4.is_ok());
        assert_eq!(manager.in_flight_cpu_count(), 2);
    }

    #[test]
    fn test_cpu_slot_auto_release() {
        let config = ExecutorConfig::builder().max_parallel_steps(4).build();
        let manager = ThreadPoolManager::new(&config);

        {
            let _slot = manager.reserve_cpu_slot().unwrap();
            assert_eq!(manager.in_flight_cpu_count(), 1);
        } // slot dropped here

        assert_eq!(manager.in_flight_cpu_count(), 0);
    }

    #[test]
    fn test_execute_cpu_task() {
        let config = ExecutorConfig::default();
        let manager = ThreadPoolManager::new(&config);

        let result = manager.execute_cpu(|| 42);
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), 42);

        // Should be released after execution
        assert_eq!(manager.in_flight_cpu_count(), 0);
    }

    #[test]
    fn test_execute_cpu_respects_limits() {
        let config = ExecutorConfig::builder().max_parallel_steps(2).build();
        let manager = Arc::new(ThreadPoolManager::new(&config));

        // Reserve all slots
        let _slot1 = manager.reserve_cpu_slot().unwrap();
        let _slot2 = manager.reserve_cpu_slot().unwrap();

        // Try to execute - should fail
        let result = manager.execute_cpu(|| 42);
        assert!(result.is_err());
    }

    #[test]
    fn test_concurrent_cpu_execution() {
        let config = ExecutorConfig::builder().max_parallel_steps(4).build();
        let manager = Arc::new(ThreadPoolManager::new(&config));

        let barrier = Arc::new(Barrier::new(4));
        let mut handles = vec![];

        for i in 0..4 {
            let manager_clone = Arc::clone(&manager);
            let barrier_clone = Arc::clone(&barrier);

            let handle = thread::spawn(move || {
                manager_clone.execute_cpu(move || {
                    barrier_clone.wait();
                    i * 2
                })
            });
            handles.push(handle);
        }

        let results: Vec<_> = handles.into_iter().map(|h| h.join().unwrap()).collect();

        assert_eq!(results.len(), 4);
        for result in results {
            assert!(result.is_ok());
        }

        // All slots should be released
        assert_eq!(manager.in_flight_cpu_count(), 0);
    }

    #[test]
    fn test_io_capacity_check() {
        let config = ExecutorConfig::builder().max_parallel_steps(2).build();
        let manager = ThreadPoolManager::new(&config);

        assert!(manager.has_io_capacity());
        // I/O pool should be 2x CPU pool
        assert_eq!(manager.max_io_tasks(), 4);
    }

    #[test]
    fn test_reserve_io_slot() {
        let config = ExecutorConfig::builder().max_parallel_steps(1).build();
        let manager = ThreadPoolManager::new(&config);

        // I/O pool is 2x CPU pool (2 slots)
        let slot1 = manager.reserve_io_slot();
        assert!(slot1.is_ok());
        assert_eq!(manager.in_flight_io_count(), 1);

        let slot2 = manager.reserve_io_slot();
        assert!(slot2.is_ok());
        assert_eq!(manager.in_flight_io_count(), 2);

        // Should fail - at capacity
        let slot3 = manager.reserve_io_slot();
        assert!(slot3.is_err());
    }

    #[test]
    fn test_tokio_runtime_availability() {
        let config = ExecutorConfig::default();
        let manager = ThreadPoolManager::new(&config);

        // Tokio runtime availability depends on the async feature
        #[cfg(feature = "async")]
        assert!(manager.has_tokio_runtime());

        #[cfg(not(feature = "async"))]
        assert!(!manager.has_tokio_runtime());
    }

    #[test]
    fn test_resource_tracking_accuracy() {
        let config = ExecutorConfig::builder().max_parallel_steps(3).build();
        let manager = ThreadPoolManager::new(&config);

        let slot1 = manager.reserve_cpu_slot().unwrap();
        let slot2 = manager.reserve_cpu_slot().unwrap();
        assert_eq!(manager.in_flight_cpu_count(), 2);
        assert!(manager.has_cpu_capacity());

        let slot3 = manager.reserve_cpu_slot().unwrap();
        assert_eq!(manager.in_flight_cpu_count(), 3);
        assert!(!manager.has_cpu_capacity());

        drop(slot2);
        assert_eq!(manager.in_flight_cpu_count(), 2);
        assert!(manager.has_cpu_capacity());

        drop(slot1);
        drop(slot3);
        assert_eq!(manager.in_flight_cpu_count(), 0);
    }

    #[test]
    fn test_execute_cpu_with_panic_recovery() {
        let config = ExecutorConfig::default();
        let manager = ThreadPoolManager::new(&config);

        // Execute task that panics
        let result = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            manager.execute_cpu(|| panic!("test panic"))
        }));

        assert!(result.is_err());

        // Slot should still be released even after panic
        // Give a small delay for cleanup
        thread::sleep(Duration::from_millis(10));
        assert_eq!(manager.in_flight_cpu_count(), 0);
    }
}
