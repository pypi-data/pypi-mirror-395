use crate::{CoralError, Result};

/// Mock implementation of Coral Context for development without hardware
pub struct CoralContext {
    model_size: usize,
}

impl CoralContext {
    /// Create a new mock Coral context
    pub fn new(model_bytes: &[u8]) -> Result<Self> {
        if model_bytes.is_empty() {
            return Err(CoralError::ModelLoadError("Empty model data".to_string()));
        }

        Ok(CoralContext {
            model_size: model_bytes.len(),
        })
    }

    /// Perform mock inference
    ///
    /// Returns dummy output data for testing purposes
    pub fn invoke(&self, input: &[u8], output: &mut [u8]) -> Result<()> {
        if input.is_empty() {
            return Err(CoralError::InvalidTensorShape);
        }

        // Fill output with mock data (zeros)
        output.fill(0);

        Ok(())
    }

    /// Get model size
    pub fn model_size(&self) -> usize {
        self.model_size
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_mock_creation() {
        let model = vec![1, 2, 3, 4];
        let ctx = CoralContext::new(&model).unwrap();
        assert_eq!(ctx.model_size(), 4);
    }

    #[test]
    fn test_mock_invoke() {
        let model = vec![1, 2, 3, 4];
        let ctx = CoralContext::new(&model).unwrap();

        let input = vec![0u8; 100];
        let mut output = vec![255u8; 100];

        ctx.invoke(&input, &mut output).unwrap();
        assert!(output.iter().all(|&x| x == 0));
    }
}
