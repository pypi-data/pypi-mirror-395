use serde::{Deserialize, Serialize};

/// Configuration for a simple transformer model
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ModelConfig {
    /// Vocabulary size
    pub vocab_size: usize,
    /// Hidden dimension size
    pub hidden_size: usize,
    /// Number of transformer layers
    pub num_layers: usize,
    /// Number of attention heads
    pub num_heads: usize,
    /// Intermediate feed-forward dimension
    pub intermediate_size: usize,
    /// Maximum sequence length
    pub max_seq_len: usize,
}

impl Default for ModelConfig {
    fn default() -> Self {
        Self {
            vocab_size: 50257,      // GPT-2 vocab size
            hidden_size: 768,
            num_layers: 12,
            num_heads: 12,
            intermediate_size: 3072,
            max_seq_len: 1024,
        }
    }
}

impl ModelConfig {
    /// Create a small model configuration for testing
    pub fn small() -> Self {
        Self {
            vocab_size: 1000,
            hidden_size: 128,
            num_layers: 2,
            num_heads: 4,
            intermediate_size: 512,
            max_seq_len: 256,
        }
    }
}
