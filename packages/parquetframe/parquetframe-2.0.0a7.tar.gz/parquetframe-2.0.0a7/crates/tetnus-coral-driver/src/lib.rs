pub mod error;

pub use error::{CoralError, Result};

#[cfg(feature = "coral-hardware")]
mod ffi;

#[cfg(feature = "coral-hardware")]
pub use ffi::CoralContext;

#[cfg(not(feature = "coral-hardware"))]
mod mock;

#[cfg(not(feature = "coral-hardware"))]
pub use mock::CoralContext;

/// Get the Edge TPU library version
pub fn version() -> String {
    #[cfg(feature = "coral-hardware")]
    {
        ffi::edgetpu_version()
    }

    #[cfg(not(feature = "coral-hardware"))]
    {
        "mock-0.1.0".to_string()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_version() {
        let ver = version();
        assert!(!ver.is_empty());
    }

    #[test]
    fn test_mock_context() {
        let model_data = vec![0u8; 1024];
        let ctx = CoralContext::new(&model_data);
        assert!(ctx.is_ok());
    }
}
