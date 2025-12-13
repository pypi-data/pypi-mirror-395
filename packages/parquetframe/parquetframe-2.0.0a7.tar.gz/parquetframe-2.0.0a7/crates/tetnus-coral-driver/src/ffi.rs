use std::ffi::{CStr, c_char};
use crate::{CoralError, Result};

// Opaque type representing Edge TPU context
#[repr(C)]
pub struct EdgeTpuContext {
    _private: [u8; 0],
}

// FFI declarations for libedgetpu.so
// These are only compiled when coral-hardware feature is enabled
#[link(name = "edgetpu")]
extern "C" {
    fn edgetpu_version() -> *const c_char;
    fn edgetpu_create_context(
        model_data: *const u8,
        model_size: usize,
    ) -> *mut EdgeTpuContext;
    fn edgetpu_invoke(
        context: *mut EdgeTpuContext,
        input: *const u8,
        output: *mut u8,
    );
    fn edgetpu_destroy_context(context: *mut EdgeTpuContext);
}

/// Get Edge TPU library version
pub fn edgetpu_version() -> String {
    unsafe {
        let ver_ptr = edgetpu_version();
        if ver_ptr.is_null() {
            return "unknown".to_string();
        }
        CStr::from_ptr(ver_ptr)
            .to_string_lossy()
            .into_owned()
    }
}

/// Safe wrapper around Edge TPU context
pub struct CoralContext {
    internal: *mut EdgeTpuContext,
}

impl CoralContext {
    /// Create a new Coral context from model data
    pub fn new(model_bytes: &[u8]) -> Result<Self> {
        if model_bytes.is_empty() {
            return Err(CoralError::ModelLoadError("Empty model data".to_string()));
        }

        let ctx = unsafe {
            edgetpu_create_context(model_bytes.as_ptr(), model_bytes.len())
        };

        if ctx.is_null() {
            return Err(CoralError::InitFailed);
        }

        Ok(CoralContext { internal: ctx })
    }

    /// Perform inference on the Edge TPU
    pub fn invoke(&self, input: &[u8], output: &mut [u8]) -> Result<()> {
        if input.is_empty() || output.is_empty() {
            return Err(CoralError::InvalidTensorShape);
        }

        unsafe {
            edgetpu_invoke(self.internal, input.as_ptr(), output.as_mut_ptr());
        }

        Ok(())
    }
}

impl Drop for CoralContext {
    fn drop(&mut self) {
        unsafe {
            edgetpu_destroy_context(self.internal);
        }
    }
}

// Safety: CoralContext ownership is exclusive
unsafe impl Send for CoralContext {}
