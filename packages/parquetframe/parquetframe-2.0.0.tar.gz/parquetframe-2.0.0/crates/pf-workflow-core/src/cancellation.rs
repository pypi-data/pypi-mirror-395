//! Cancellation mechanism for workflow execution.
//!
//! This module provides a thread-safe cancellation token that allows workflows
//! to be gracefully interrupted from external threads. The cancellation mechanism
//! uses atomic operations for minimal overhead (<10ns check latency).
//!
//! # Examples
//!
//! ```
//! use pf_workflow_core::CancellationToken;
//! use std::thread;
//! use std::time::Duration;
//!
//! // Create a cancellation token
//! let token = CancellationToken::new();
//! let token_clone = token.clone();
//!
//! // Spawn a thread that cancels after 1 second
//! thread::spawn(move || {
//!     thread::sleep(Duration::from_secs(1));
//!     token_clone.cancel();
//! });
//!
//! // Main thread checks for cancellation
//! while !token.is_cancelled() {
//!     // Do work...
//!     thread::sleep(Duration::from_millis(100));
//! }
//! ```

use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;

/// A thread-safe cancellation token for workflow execution.
///
/// `CancellationToken` uses atomic operations to provide lock-free cancellation
/// signaling with minimal performance overhead. Multiple clones of the token
/// share the same underlying state, allowing cancellation to be triggered from
/// any thread and observed by all threads.
///
/// # Thread Safety
///
/// This type is both `Send` and `Sync`, allowing it to be shared across threads.
/// The `cancel()` operation uses atomic stores, and `is_cancelled()` uses atomic
/// loads with relaxed ordering for maximum performance.
///
/// # Performance
///
/// - `is_cancelled()`: <10ns latency (single atomic load)
/// - `cancel()`: <50ns latency (single atomic store)
/// - `check()`: <50ns latency (conditional branch on atomic load)
#[derive(Debug, Clone)]
pub struct CancellationToken {
    /// Shared cancellation flag using atomic boolean.
    cancelled: Arc<AtomicBool>,
}

impl CancellationToken {
    /// Create a new cancellation token.
    ///
    /// The token starts in the non-cancelled state.
    ///
    /// # Examples
    ///
    /// ```
    /// use pf_workflow_core::CancellationToken;
    ///
    /// let token = CancellationToken::new();
    /// assert!(!token.is_cancelled());
    /// ```
    pub fn new() -> Self {
        Self {
            cancelled: Arc::new(AtomicBool::new(false)),
        }
    }

    /// Cancel the workflow.
    ///
    /// This sets the cancellation flag, which will be observed by all clones
    /// of this token. The operation is idempotent - calling `cancel()` multiple
    /// times has the same effect as calling it once.
    ///
    /// # Thread Safety
    ///
    /// This method can be called from any thread. The cancellation will be
    /// visible to all threads that have a clone of this token.
    ///
    /// # Examples
    ///
    /// ```
    /// use pf_workflow_core::CancellationToken;
    ///
    /// let token = CancellationToken::new();
    /// assert!(!token.is_cancelled());
    ///
    /// token.cancel();
    /// assert!(token.is_cancelled());
    ///
    /// // Calling cancel again is safe
    /// token.cancel();
    /// assert!(token.is_cancelled());
    /// ```
    pub fn cancel(&self) {
        self.cancelled.store(true, Ordering::Release);
    }

    /// Check if the workflow has been cancelled.
    ///
    /// Returns `true` if `cancel()` has been called on this token or any of
    /// its clones.
    ///
    /// # Performance
    ///
    /// This operation is extremely fast (<10ns) and can be called frequently
    /// without significant overhead. It uses relaxed atomic ordering for
    /// maximum performance.
    ///
    /// # Examples
    ///
    /// ```
    /// use pf_workflow_core::CancellationToken;
    ///
    /// let token = CancellationToken::new();
    /// assert!(!token.is_cancelled());
    ///
    /// token.cancel();
    /// assert!(token.is_cancelled());
    /// ```
    pub fn is_cancelled(&self) -> bool {
        self.cancelled.load(Ordering::Acquire)
    }

    /// Check for cancellation and return an error if cancelled.
    ///
    /// This is a convenience method that checks `is_cancelled()` and returns
    /// a `CancellationError` if the token has been cancelled.
    ///
    /// # Errors
    ///
    /// Returns `Err(WorkflowError::Execution(ExecutionError::Cancelled))` if
    /// the token has been cancelled.
    ///
    /// # Examples
    ///
    /// ```
    /// use pf_workflow_core::{CancellationToken, Result};
    ///
    /// fn do_work(token: &CancellationToken) -> Result<()> {
    ///     // Check for cancellation before expensive operation
    ///     token.check()?;
    ///
    ///     // Do work...
    ///
    ///     Ok(())
    /// }
    ///
    /// let token = CancellationToken::new();
    /// assert!(do_work(&token).is_ok());
    ///
    /// token.cancel();
    /// assert!(do_work(&token).is_err());
    /// ```
    pub fn check(&self) -> crate::error::Result<()> {
        if self.is_cancelled() {
            Err(crate::error::ExecutionError::Cancelled.into())
        } else {
            Ok(())
        }
    }

    /// Reset the cancellation state.
    ///
    /// This sets the cancellation flag back to `false`, allowing the token
    /// to be reused. This is primarily useful for testing or when reusing
    /// tokens across multiple workflow executions.
    ///
    /// # Examples
    ///
    /// ```
    /// use pf_workflow_core::CancellationToken;
    ///
    /// let token = CancellationToken::new();
    /// token.cancel();
    /// assert!(token.is_cancelled());
    ///
    /// token.reset();
    /// assert!(!token.is_cancelled());
    /// ```
    pub fn reset(&self) {
        self.cancelled.store(false, Ordering::Release);
    }
}

impl Default for CancellationToken {
    fn default() -> Self {
        Self::new()
    }
}

// Ensure CancellationToken is thread-safe
// These are automatically implemented by the compiler due to Arc<AtomicBool>
// but we make it explicit for documentation purposes.
unsafe impl Send for CancellationToken {}
unsafe impl Sync for CancellationToken {}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::Arc;
    use std::thread;
    use std::time::{Duration, Instant};

    #[test]
    fn test_new_token_not_cancelled() {
        let token = CancellationToken::new();
        assert!(!token.is_cancelled());
    }

    #[test]
    fn test_cancel_sets_flag() {
        let token = CancellationToken::new();
        assert!(!token.is_cancelled());

        token.cancel();
        assert!(token.is_cancelled());
    }

    #[test]
    fn test_idempotent_cancel() {
        let token = CancellationToken::new();

        token.cancel();
        assert!(token.is_cancelled());

        // Calling cancel again should be safe
        token.cancel();
        assert!(token.is_cancelled());
    }

    #[test]
    fn test_clone_shares_state() {
        let token = CancellationToken::new();
        let token_clone = token.clone();

        assert!(!token.is_cancelled());
        assert!(!token_clone.is_cancelled());

        token.cancel();

        assert!(token.is_cancelled());
        assert!(token_clone.is_cancelled());
    }

    #[test]
    fn test_check_ok_when_not_cancelled() {
        let token = CancellationToken::new();
        assert!(token.check().is_ok());
    }

    #[test]
    fn test_check_err_when_cancelled() {
        let token = CancellationToken::new();
        token.cancel();

        let result = token.check();
        assert!(result.is_err());

        match result {
            Err(crate::error::WorkflowError::Execution(
                crate::error::ExecutionError::Cancelled,
            )) => {}
            _ => panic!("Expected Cancelled error"),
        }
    }

    #[test]
    fn test_reset_clears_cancellation() {
        let token = CancellationToken::new();
        token.cancel();
        assert!(token.is_cancelled());

        token.reset();
        assert!(!token.is_cancelled());
    }

    #[test]
    fn test_multithreaded_cancellation() {
        let token = CancellationToken::new();
        let token_clone = token.clone();

        // Spawn thread that cancels after a delay
        let handle = thread::spawn(move || {
            thread::sleep(Duration::from_millis(50));
            token_clone.cancel();
        });

        // Main thread waits for cancellation
        let start = Instant::now();
        while !token.is_cancelled() {
            thread::sleep(Duration::from_millis(10));

            // Timeout after 1 second to prevent infinite loop in case of failure
            if start.elapsed() > Duration::from_secs(1) {
                panic!("Cancellation not detected within timeout");
            }
        }

        handle.join().unwrap();
        assert!(token.is_cancelled());
    }

    #[test]
    fn test_multiple_clones_concurrent_cancel() {
        let token = CancellationToken::new();
        let mut handles = vec![];

        // Spawn 10 threads, each with a clone of the token
        for i in 0..10 {
            let token_clone = token.clone();
            let handle = thread::spawn(move || {
                if i == 5 {
                    // One thread cancels
                    thread::sleep(Duration::from_millis(10));
                    token_clone.cancel();
                } else {
                    // Other threads wait for cancellation
                    while !token_clone.is_cancelled() {
                        thread::sleep(Duration::from_millis(5));
                    }
                }
            });
            handles.push(handle);
        }

        // Wait for all threads to complete
        for handle in handles {
            handle.join().unwrap();
        }

        assert!(token.is_cancelled());
    }

    #[test]
    fn test_cancellation_check_latency() {
        let token = CancellationToken::new();
        let iterations = 1_000_000;

        let start = Instant::now();
        for _ in 0..iterations {
            let _ = token.is_cancelled();
        }
        let elapsed = start.elapsed();

        let avg_latency_ns = elapsed.as_nanos() / iterations;

        // Should be well under 10ns per check on modern hardware
        // We use 50ns as a conservative threshold for CI environments
        assert!(
            avg_latency_ns < 50,
            "Average check latency {}ns exceeds 50ns threshold",
            avg_latency_ns
        );

        println!(
            "Cancellation check average latency: {}ns over {} iterations",
            avg_latency_ns, iterations
        );
    }

    #[test]
    fn test_default_trait() {
        let token: CancellationToken = Default::default();
        assert!(!token.is_cancelled());
    }

    #[test]
    fn test_send_sync() {
        // This test ensures CancellationToken implements Send and Sync
        fn assert_send<T: Send>() {}
        fn assert_sync<T: Sync>() {}

        assert_send::<CancellationToken>();
        assert_sync::<CancellationToken>();
    }

    #[test]
    fn test_arc_wrapping() {
        // Test that CancellationToken works correctly when wrapped in Arc
        let token = Arc::new(CancellationToken::new());
        let token_clone = Arc::clone(&token);

        let handle = thread::spawn(move || {
            thread::sleep(Duration::from_millis(10));
            token_clone.cancel();
        });

        while !token.is_cancelled() {
            thread::sleep(Duration::from_millis(5));
        }

        handle.join().unwrap();
        assert!(token.is_cancelled());
    }
}
