//! Progress tracking for workflow execution.
//!
//! This module provides a trait-based system for tracking workflow progress
//! through callback events. The progress system is zero-cost when unused and
//! thread-safe when enabled.
//!
//! # Examples
//!
//! ```
//! use pf_workflow_core::{ProgressCallback, ProgressEvent};
//! use std::sync::{Arc, Mutex};
//!
//! // Create a custom callback that collects events
//! #[derive(Clone)]
//! struct CollectorCallback {
//!     events: Arc<Mutex<Vec<ProgressEvent>>>,
//! }
//!
//! impl ProgressCallback for CollectorCallback {
//!     fn on_progress(&self, event: ProgressEvent) {
//!         self.events.lock().unwrap().push(event);
//!     }
//! }
//! ```

use serde::{Deserialize, Serialize};
use std::fmt;
use std::fs::{File, OpenOptions};
use std::io::Write;
use std::path::{Path, PathBuf};
use std::sync::{Arc, Mutex};
use std::time::SystemTime;

/// Progress event types during workflow execution.
///
/// These events represent the lifecycle of individual workflow steps,
/// allowing external observers to track execution progress, handle failures,
/// and respond to cancellations.
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", rename_all = "lowercase")]
pub enum ProgressEvent {
    /// A workflow step has started executing.
    Started {
        /// The identifier of the step that started.
        step_id: String,

        /// Timestamp when the step started.
        #[serde(with = "systemtime_serde")]
        timestamp: SystemTime,

        /// Optional message providing additional context.
        message: Option<String>,
    },

    /// A workflow step has completed successfully.
    Completed {
        /// The identifier of the step that completed.
        step_id: String,

        /// Timestamp when the step completed.
        #[serde(with = "systemtime_serde")]
        timestamp: SystemTime,

        /// Optional message providing additional context.
        message: Option<String>,
    },

    /// A workflow step has failed.
    Failed {
        /// The identifier of the step that failed.
        step_id: String,

        /// Timestamp when the failure occurred.
        #[serde(with = "systemtime_serde")]
        timestamp: SystemTime,

        /// Error message describing the failure.
        error: String,

        /// Optional additional context about the failure.
        message: Option<String>,
    },

    /// A workflow step was cancelled.
    Cancelled {
        /// The identifier of the step that was cancelled.
        step_id: String,

        /// Timestamp when the cancellation occurred.
        #[serde(with = "systemtime_serde")]
        timestamp: SystemTime,

        /// Optional message providing additional context.
        message: Option<String>,
    },
}

impl ProgressEvent {
    /// Create a new Started event.
    pub fn started(step_id: impl Into<String>) -> Self {
        Self::Started {
            step_id: step_id.into(),
            timestamp: SystemTime::now(),
            message: None,
        }
    }

    /// Create a new Started event with a message.
    pub fn started_with_message(step_id: impl Into<String>, message: impl Into<String>) -> Self {
        Self::Started {
            step_id: step_id.into(),
            timestamp: SystemTime::now(),
            message: Some(message.into()),
        }
    }

    /// Create a new Completed event.
    pub fn completed(step_id: impl Into<String>) -> Self {
        Self::Completed {
            step_id: step_id.into(),
            timestamp: SystemTime::now(),
            message: None,
        }
    }

    /// Create a new Completed event with a message.
    pub fn completed_with_message(step_id: impl Into<String>, message: impl Into<String>) -> Self {
        Self::Completed {
            step_id: step_id.into(),
            timestamp: SystemTime::now(),
            message: Some(message.into()),
        }
    }

    /// Create a new Failed event.
    pub fn failed(step_id: impl Into<String>, error: impl Into<String>) -> Self {
        Self::Failed {
            step_id: step_id.into(),
            timestamp: SystemTime::now(),
            error: error.into(),
            message: None,
        }
    }

    /// Create a new Failed event with additional context.
    pub fn failed_with_message(
        step_id: impl Into<String>,
        error: impl Into<String>,
        message: impl Into<String>,
    ) -> Self {
        Self::Failed {
            step_id: step_id.into(),
            timestamp: SystemTime::now(),
            error: error.into(),
            message: Some(message.into()),
        }
    }

    /// Create a new Cancelled event.
    pub fn cancelled(step_id: impl Into<String>) -> Self {
        Self::Cancelled {
            step_id: step_id.into(),
            timestamp: SystemTime::now(),
            message: None,
        }
    }

    /// Create a new Cancelled event with a message.
    pub fn cancelled_with_message(step_id: impl Into<String>, message: impl Into<String>) -> Self {
        Self::Cancelled {
            step_id: step_id.into(),
            timestamp: SystemTime::now(),
            message: Some(message.into()),
        }
    }

    /// Get the step ID from the event.
    pub fn step_id(&self) -> &str {
        match self {
            Self::Started { step_id, .. }
            | Self::Completed { step_id, .. }
            | Self::Failed { step_id, .. }
            | Self::Cancelled { step_id, .. } => step_id,
        }
    }

    /// Get the timestamp from the event.
    pub fn timestamp(&self) -> SystemTime {
        match self {
            Self::Started { timestamp, .. }
            | Self::Completed { timestamp, .. }
            | Self::Failed { timestamp, .. }
            | Self::Cancelled { timestamp, .. } => *timestamp,
        }
    }
}

impl fmt::Display for ProgressEvent {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Started {
                step_id, message, ..
            } => {
                if let Some(msg) = message {
                    write!(f, "Started: {} - {}", step_id, msg)
                } else {
                    write!(f, "Started: {}", step_id)
                }
            }
            Self::Completed {
                step_id, message, ..
            } => {
                if let Some(msg) = message {
                    write!(f, "Completed: {} - {}", step_id, msg)
                } else {
                    write!(f, "Completed: {}", step_id)
                }
            }
            Self::Failed {
                step_id,
                error,
                message,
                ..
            } => {
                if let Some(msg) = message {
                    write!(f, "Failed: {} - {} ({})", step_id, error, msg)
                } else {
                    write!(f, "Failed: {} - {}", step_id, error)
                }
            }
            Self::Cancelled {
                step_id, message, ..
            } => {
                if let Some(msg) = message {
                    write!(f, "Cancelled: {} - {}", step_id, msg)
                } else {
                    write!(f, "Cancelled: {}", step_id)
                }
            }
        }
    }
}

/// Trait for receiving progress notifications during workflow execution.
///
/// Implementations of this trait receive callbacks for each significant event
/// during workflow execution (step start, completion, failure, cancellation).
///
/// # Thread Safety
///
/// Implementations must be `Send + Sync` as callbacks may be invoked from
/// multiple threads during parallel execution. Use appropriate synchronization
/// primitives (Arc, Mutex, etc.) if your callback needs to maintain state.
///
/// # Performance
///
/// Callback implementations should be fast (<1μs) to avoid impacting workflow
/// performance. For expensive operations (logging to disk, network calls, etc.),
/// consider buffering events and processing them asynchronously.
///
/// # Examples
///
/// ```
/// use pf_workflow_core::{ProgressCallback, ProgressEvent};
///
/// struct ConsoleLogger;
///
/// impl ProgressCallback for ConsoleLogger {
///     fn on_progress(&self, event: ProgressEvent) {
///         println!("[WORKFLOW] {}", event);
///     }
/// }
/// ```
pub trait ProgressCallback: Send + Sync {
    /// Called when a progress event occurs.
    ///
    /// This method is invoked for each significant event during workflow execution.
    /// Implementations should be fast and non-blocking.
    ///
    /// # Arguments
    ///
    /// * `event` - The progress event that occurred.
    fn on_progress(&self, event: ProgressEvent);
}

/// A no-op progress callback that discards all events.
///
/// This is useful as a default callback when progress tracking is not needed,
/// providing zero runtime overhead.
#[derive(Debug, Clone, Copy, Default)]
pub struct NoOpCallback;

impl ProgressCallback for NoOpCallback {
    #[inline]
    fn on_progress(&self, _event: ProgressEvent) {
        // Intentionally empty - no-op
    }
}

/// A console logger callback that prints events to stdout.
///
/// This is a simple implementation useful for debugging and development.
/// For production use, consider implementing a custom callback that integrates
/// with your logging framework.
///
/// # Examples
///
/// ```
/// use pf_workflow_core::ConsoleProgressCallback;
///
/// let callback = ConsoleProgressCallback::new();
/// // Use with executor: executor.execute_with_progress(Box::new(callback))
/// ```
#[derive(Debug, Clone, Copy, Default)]
pub struct ConsoleProgressCallback;

impl ConsoleProgressCallback {
    /// Create a new console progress callback.
    pub fn new() -> Self {
        Self
    }
}

impl ProgressCallback for ConsoleProgressCallback {
    fn on_progress(&self, event: ProgressEvent) {
        println!("[WORKFLOW] {}", event);
    }
}

/// A callback-based progress tracker that wraps a closure.
///
/// This allows you to easily create custom progress tracking behavior
/// using closures or function pointers without implementing the full trait.
///
/// # Examples
///
/// ```
/// use pf_workflow_core::{CallbackProgressTracker, ProgressEvent};
/// use std::sync::{Arc, Mutex};
///
/// let events = Arc::new(Mutex::new(Vec::new()));
/// let events_clone = Arc::clone(&events);
///
/// let tracker = CallbackProgressTracker::new(move |event: ProgressEvent| {
///     events_clone.lock().unwrap().push(event);
/// });
///
/// // Use with executor:
/// // executor.execute_with_progress(Box::new(tracker))
/// ```
pub struct CallbackProgressTracker<F>
where
    F: Fn(ProgressEvent) + Send + Sync,
{
    callback: F,
}

impl<F> CallbackProgressTracker<F>
where
    F: Fn(ProgressEvent) + Send + Sync,
{
    /// Create a new callback-based progress tracker.
    ///
    /// # Arguments
    ///
    /// * `callback` - A function or closure that will be called for each progress event
    ///
    /// # Examples
    ///
    /// ```
    /// use pf_workflow_core::CallbackProgressTracker;
    ///
    /// let tracker = CallbackProgressTracker::new(|event| {
    ///     println!("Event: {}", event);
    /// });
    /// ```
    pub fn new(callback: F) -> Self {
        Self { callback }
    }
}

impl<F> ProgressCallback for CallbackProgressTracker<F>
where
    F: Fn(ProgressEvent) + Send + Sync,
{
    fn on_progress(&self, event: ProgressEvent) {
        (self.callback)(event);
    }
}

/// A file-based progress tracker that logs events to a file.
///
/// Events are written as JSON lines (one JSON object per line) for easy parsing.
/// The file is created if it doesn't exist and appended to if it does.
///
/// # Thread Safety
///
/// This tracker is thread-safe and can be used with parallel execution.
/// Events from different threads are serialized through a mutex.
///
/// # Examples
///
/// ```no_run
/// use pf_workflow_core::FileProgressTracker;
///
/// let tracker = FileProgressTracker::new("workflow_progress.jsonl")
///     .expect("Failed to create progress tracker");
///
/// // Use with executor:
/// // executor.execute_with_progress(Box::new(tracker))
/// ```
pub struct FileProgressTracker {
    file: Arc<Mutex<File>>,
    path: PathBuf,
}

impl FileProgressTracker {
    /// Create a new file-based progress tracker.
    ///
    /// The file will be created if it doesn't exist, or appended to if it does.
    ///
    /// # Arguments
    ///
    /// * `path` - Path to the log file
    ///
    /// # Errors
    ///
    /// Returns an error if the file cannot be created or opened.
    ///
    /// # Examples
    ///
    /// ```no_run
    /// use pf_workflow_core::FileProgressTracker;
    ///
    /// let tracker = FileProgressTracker::new("progress.log")?;
    /// # Ok::<(), std::io::Error>(())
    /// ```
    pub fn new<P: AsRef<Path>>(path: P) -> std::io::Result<Self> {
        let path_buf = path.as_ref().to_path_buf();
        let file = OpenOptions::new()
            .create(true)
            .append(true)
            .open(&path_buf)?;

        Ok(Self {
            file: Arc::new(Mutex::new(file)),
            path: path_buf,
        })
    }

    /// Get the path to the log file.
    pub fn path(&self) -> &Path {
        &self.path
    }
}

impl ProgressCallback for FileProgressTracker {
    fn on_progress(&self, event: ProgressEvent) {
        // Serialize event to JSON and write to file
        if let Ok(json) = serde_json::to_string(&event) {
            if let Ok(mut file) = self.file.lock() {
                let _ = writeln!(file, "{}", json);
                let _ = file.flush(); // Ensure it's written immediately
            }
        }
    }
}

impl std::fmt::Debug for FileProgressTracker {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("FileProgressTracker")
            .field("path", &self.path)
            .finish()
    }
}

/// Helper module for SystemTime serialization/deserialization.
mod systemtime_serde {
    use serde::{Deserialize, Deserializer, Serializer};
    use std::time::{Duration, SystemTime, UNIX_EPOCH};

    pub fn serialize<S>(time: &SystemTime, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let duration = time
            .duration_since(UNIX_EPOCH)
            .unwrap_or_else(|_| Duration::from_secs(0));
        serializer.serialize_f64(duration.as_secs_f64())
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<SystemTime, D::Error>
    where
        D: Deserializer<'de>,
    {
        let secs = f64::deserialize(deserializer)?;
        Ok(UNIX_EPOCH + Duration::from_secs_f64(secs))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::BufRead;
    use std::sync::{Arc, Mutex};
    use std::thread;
    use std::time::Duration;

    #[test]
    fn test_progress_event_started() {
        let event = ProgressEvent::started("test_step");
        assert_eq!(event.step_id(), "test_step");

        match event {
            ProgressEvent::Started { .. } => {}
            _ => panic!("Expected Started event"),
        }
    }

    #[test]
    fn test_progress_event_completed() {
        let event = ProgressEvent::completed("test_step");
        assert_eq!(event.step_id(), "test_step");

        match event {
            ProgressEvent::Completed { .. } => {}
            _ => panic!("Expected Completed event"),
        }
    }

    #[test]
    fn test_progress_event_failed() {
        let event = ProgressEvent::failed("test_step", "error message");

        match &event {
            ProgressEvent::Failed { step_id, error, .. } => {
                assert_eq!(step_id, "test_step");
                assert_eq!(error, "error message");
            }
            _ => panic!("Expected Failed event"),
        }
    }

    #[test]
    fn test_progress_event_cancelled() {
        let event = ProgressEvent::cancelled("test_step");
        assert_eq!(event.step_id(), "test_step");

        match event {
            ProgressEvent::Cancelled { .. } => {}
            _ => panic!("Expected Cancelled event"),
        }
    }

    #[test]
    fn test_progress_event_with_message() {
        let event = ProgressEvent::started_with_message("test_step", "custom message");

        match &event {
            ProgressEvent::Started { message, .. } => {
                assert_eq!(message.as_ref().unwrap(), "custom message");
            }
            _ => panic!("Expected Started event"),
        }
    }

    #[test]
    fn test_progress_event_display() {
        let started = ProgressEvent::started("step1");
        assert!(started.to_string().contains("Started"));
        assert!(started.to_string().contains("step1"));

        let completed = ProgressEvent::completed("step2");
        assert!(completed.to_string().contains("Completed"));

        let failed = ProgressEvent::failed("step3", "test error");
        assert!(failed.to_string().contains("Failed"));
        assert!(failed.to_string().contains("test error"));

        let cancelled = ProgressEvent::cancelled("step4");
        assert!(cancelled.to_string().contains("Cancelled"));
    }

    #[test]
    fn test_no_op_callback() {
        let callback = NoOpCallback;
        let event = ProgressEvent::started("test");

        // Should not panic or do anything
        callback.on_progress(event);
    }

    #[test]
    fn test_console_callback() {
        let callback = ConsoleProgressCallback::new();
        let event = ProgressEvent::started("test");

        // Should print to console (we can't capture this in test, but verify it doesn't panic)
        callback.on_progress(event);
    }

    // Custom collector callback for testing
    #[derive(Clone)]
    struct CollectorCallback {
        events: Arc<Mutex<Vec<ProgressEvent>>>,
    }

    impl CollectorCallback {
        fn new() -> Self {
            Self {
                events: Arc::new(Mutex::new(Vec::new())),
            }
        }

        fn get_events(&self) -> Vec<ProgressEvent> {
            self.events.lock().unwrap().clone()
        }
    }

    impl ProgressCallback for CollectorCallback {
        fn on_progress(&self, event: ProgressEvent) {
            self.events.lock().unwrap().push(event);
        }
    }

    #[test]
    fn test_custom_callback_collects_events() {
        let callback = CollectorCallback::new();

        callback.on_progress(ProgressEvent::started("step1"));
        callback.on_progress(ProgressEvent::completed("step1"));
        callback.on_progress(ProgressEvent::started("step2"));
        callback.on_progress(ProgressEvent::failed("step2", "error"));

        let events = callback.get_events();
        assert_eq!(events.len(), 4);

        assert!(matches!(events[0], ProgressEvent::Started { .. }));
        assert!(matches!(events[1], ProgressEvent::Completed { .. }));
        assert!(matches!(events[2], ProgressEvent::Started { .. }));
        assert!(matches!(events[3], ProgressEvent::Failed { .. }));
    }

    #[test]
    fn test_callback_thread_safety() {
        let callback = Arc::new(CollectorCallback::new());
        let mut handles = vec![];

        // Spawn multiple threads that emit events
        for i in 0..10 {
            let callback_clone = Arc::clone(&callback);
            let handle = thread::spawn(move || {
                callback_clone.on_progress(ProgressEvent::started(format!("step{}", i)));
                thread::sleep(Duration::from_millis(5));
                callback_clone.on_progress(ProgressEvent::completed(format!("step{}", i)));
            });
            handles.push(handle);
        }

        // Wait for all threads
        for handle in handles {
            handle.join().unwrap();
        }

        let events = callback.get_events();
        assert_eq!(events.len(), 20); // 10 started + 10 completed

        // Count each event type
        let started_count = events
            .iter()
            .filter(|e| matches!(e, ProgressEvent::Started { .. }))
            .count();
        let completed_count = events
            .iter()
            .filter(|e| matches!(e, ProgressEvent::Completed { .. }))
            .count();

        assert_eq!(started_count, 10);
        assert_eq!(completed_count, 10);
    }

    #[test]
    fn test_event_serialization() {
        let event = ProgressEvent::started("test_step");
        let json = serde_json::to_string(&event).unwrap();
        assert!(json.contains("test_step"));
        assert!(json.contains("started"));

        let deserialized: ProgressEvent = serde_json::from_str(&json).unwrap();
        assert_eq!(deserialized.step_id(), "test_step");
    }

    #[test]
    fn test_failed_event_serialization() {
        let event = ProgressEvent::failed("step1", "test error");
        let json = serde_json::to_string(&event).unwrap();

        let deserialized: ProgressEvent = serde_json::from_str(&json).unwrap();
        match deserialized {
            ProgressEvent::Failed { step_id, error, .. } => {
                assert_eq!(step_id, "step1");
                assert_eq!(error, "test error");
            }
            _ => panic!("Expected Failed event"),
        }
    }

    #[test]
    fn test_trait_object_usage() {
        let callback: Box<dyn ProgressCallback> = Box::new(NoOpCallback);
        callback.on_progress(ProgressEvent::started("test"));

        let callback: Box<dyn ProgressCallback> = Box::new(ConsoleProgressCallback::new());
        callback.on_progress(ProgressEvent::completed("test"));

        let callback: Box<dyn ProgressCallback> = Box::new(CollectorCallback::new());
        callback.on_progress(ProgressEvent::failed("test", "error"));
    }

    #[test]
    fn test_callback_progress_tracker() {
        let events = Arc::new(Mutex::new(Vec::new()));
        let events_clone = Arc::clone(&events);

        let tracker = CallbackProgressTracker::new(move |event: ProgressEvent| {
            events_clone.lock().unwrap().push(event);
        });

        tracker.on_progress(ProgressEvent::started("step1"));
        tracker.on_progress(ProgressEvent::completed("step1"));

        let collected = events.lock().unwrap();
        assert_eq!(collected.len(), 2);
        assert!(matches!(collected[0], ProgressEvent::Started { .. }));
        assert!(matches!(collected[1], ProgressEvent::Completed { .. }));
    }

    #[test]
    fn test_file_progress_tracker() {
        let temp_dir = std::env::temp_dir();
        let log_path = temp_dir.join("test_progress.jsonl");

        // Clean up any existing file
        let _ = std::fs::remove_file(&log_path);

        let tracker = FileProgressTracker::new(&log_path).expect("Failed to create file tracker");

        assert_eq!(tracker.path(), log_path.as_path());

        // Log some events
        tracker.on_progress(ProgressEvent::started("step1"));
        tracker.on_progress(ProgressEvent::completed("step1"));
        tracker.on_progress(ProgressEvent::started("step2"));
        tracker.on_progress(ProgressEvent::failed("step2", "test error"));

        // Drop tracker to ensure file is flushed
        drop(tracker);

        // Read back and verify
        let file = std::fs::File::open(&log_path).expect("Failed to open log file");
        let reader = std::io::BufReader::new(file);
        let lines: Vec<String> = reader.lines().map(|l| l.unwrap()).collect();

        assert_eq!(lines.len(), 4);

        // Verify each line is valid JSON
        for line in &lines {
            let _event: ProgressEvent = serde_json::from_str(line).expect("Failed to parse JSON");
        }

        // Clean up
        let _ = std::fs::remove_file(&log_path);
    }

    #[test]
    fn test_file_tracker_thread_safety() {
        let temp_dir = std::env::temp_dir();
        let log_path = temp_dir.join("test_progress_concurrent.jsonl");

        let _ = std::fs::remove_file(&log_path);

        let tracker =
            Arc::new(FileProgressTracker::new(&log_path).expect("Failed to create tracker"));

        let mut handles = vec![];

        // Spawn multiple threads writing events
        for i in 0..5 {
            let tracker_clone = Arc::clone(&tracker);
            let handle = thread::spawn(move || {
                tracker_clone.on_progress(ProgressEvent::started(format!("step{}", i)));
                tracker_clone.on_progress(ProgressEvent::completed(format!("step{}", i)));
            });
            handles.push(handle);
        }

        for handle in handles {
            handle.join().unwrap();
        }

        drop(tracker);

        // Verify all events were written
        let file = std::fs::File::open(&log_path).expect("Failed to open log file");
        let reader = std::io::BufReader::new(file);
        let lines: Vec<String> = reader.lines().map(|l| l.unwrap()).collect();

        assert_eq!(lines.len(), 10); // 5 threads * 2 events each

        let _ = std::fs::remove_file(&log_path);
    }
}
