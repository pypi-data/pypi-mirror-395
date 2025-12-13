//! Configuration for workflow execution.
//!
//! This module defines the configuration options for the workflow executor,
//! including parallelism settings, retry behavior, and timeouts.

use std::time::Duration;

/// Configuration for the workflow executor.
#[derive(Debug, Clone)]
pub struct ExecutorConfig {
    /// Maximum number of steps to run in parallel.
    /// If `None`, uses the number of CPU cores.
    pub max_parallel_steps: Option<usize>,

    /// Number of retry attempts for failed steps.
    pub retry_attempts: u32,

    /// Timeout for individual steps.
    /// If `None`, steps have no timeout.
    pub step_timeout: Option<Duration>,

    /// Whether to collect detailed metrics.
    pub enable_metrics: bool,

    /// Initial backoff duration for retries (in milliseconds).
    pub retry_backoff_ms: u64,
}

impl Default for ExecutorConfig {
    fn default() -> Self {
        Self {
            max_parallel_steps: None, // Auto-detect from CPU cores
            retry_attempts: 0,        // No retries by default
            step_timeout: None,       // No timeout by default
            enable_metrics: true,     // Metrics enabled by default
            retry_backoff_ms: 100,    // 100ms initial backoff
        }
    }
}

impl ExecutorConfig {
    /// Create a new configuration builder.
    pub fn builder() -> ExecutorConfigBuilder {
        ExecutorConfigBuilder::default()
    }

    /// Get the actual max parallel steps, accounting for auto-detection.
    pub fn get_max_parallel_steps(&self) -> usize {
        self.max_parallel_steps.unwrap_or_else(num_cpus::get)
    }

    /// Validate the configuration.
    pub fn validate(&self) -> Result<(), String> {
        if let Some(max_parallel) = self.max_parallel_steps {
            if max_parallel == 0 {
                return Err("max_parallel_steps must be greater than 0".to_string());
            }
        }

        if self.retry_backoff_ms == 0 {
            return Err("retry_backoff_ms must be greater than 0".to_string());
        }

        Ok(())
    }
}

/// Builder for ExecutorConfig.
#[derive(Default)]
pub struct ExecutorConfigBuilder {
    max_parallel_steps: Option<usize>,
    retry_attempts: u32,
    step_timeout: Option<Duration>,
    enable_metrics: bool,
    retry_backoff_ms: u64,
}

impl ExecutorConfigBuilder {
    /// Set the maximum number of parallel steps.
    pub fn max_parallel_steps(mut self, max: usize) -> Self {
        self.max_parallel_steps = Some(max);
        self
    }

    /// Set the number of retry attempts.
    pub fn retry_attempts(mut self, attempts: u32) -> Self {
        self.retry_attempts = attempts;
        self
    }

    /// Set the step timeout.
    pub fn step_timeout(mut self, timeout: Duration) -> Self {
        self.step_timeout = Some(timeout);
        self
    }

    /// Set whether to enable metrics.
    pub fn enable_metrics(mut self, enable: bool) -> Self {
        self.enable_metrics = enable;
        self
    }

    /// Set the retry backoff duration.
    pub fn retry_backoff_ms(mut self, ms: u64) -> Self {
        self.retry_backoff_ms = ms;
        self
    }

    /// Build the configuration.
    pub fn build(self) -> ExecutorConfig {
        ExecutorConfig {
            max_parallel_steps: self.max_parallel_steps,
            retry_attempts: self.retry_attempts,
            step_timeout: self.step_timeout,
            enable_metrics: self.enable_metrics,
            retry_backoff_ms: self.retry_backoff_ms,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_default_config() {
        let config = ExecutorConfig::default();
        assert_eq!(config.retry_attempts, 0);
        assert!(config.enable_metrics);
        assert!(config.max_parallel_steps.is_none());
    }

    #[test]
    fn test_config_builder() {
        let config = ExecutorConfig::builder()
            .max_parallel_steps(4)
            .retry_attempts(3)
            .enable_metrics(false)
            .build();

        assert_eq!(config.max_parallel_steps, Some(4));
        assert_eq!(config.retry_attempts, 3);
        assert!(!config.enable_metrics);
    }

    #[test]
    fn test_config_validation() {
        let config = ExecutorConfig::default();
        assert!(config.validate().is_ok());

        let bad_config = ExecutorConfig {
            max_parallel_steps: Some(0),
            ..Default::default()
        };
        assert!(bad_config.validate().is_err());
    }

    #[test]
    fn test_get_max_parallel_steps() {
        let config = ExecutorConfig::default();
        let max = config.get_max_parallel_steps();
        assert!(max > 0);

        let config_explicit = ExecutorConfig::builder().max_parallel_steps(8).build();
        assert_eq!(config_explicit.get_max_parallel_steps(), 8);
    }
}
