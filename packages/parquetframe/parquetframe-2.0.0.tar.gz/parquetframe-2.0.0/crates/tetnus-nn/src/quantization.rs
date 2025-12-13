use tetnus_core::Tensor;
use crate::{Result, TetnusNnError};

/// Quantization parameters for int8 quantization
#[derive(Debug, Clone, Copy)]
pub struct QuantizationParams {
    /// Scale factor: q = round(x / scale) + zero_point
    pub scale: f32,
    /// Zero point offset
    pub zero_point: i32,
}

impl QuantizationParams {
    /// Calculate quantization parameters from tensor data
    ///
    /// Uses asymmetric quantization:
    /// - Maps [min, max] to [-128, 127]
    /// - Scale: (max - min) / 255
    /// - Zero point: maps 0.0 to an int8 value
    pub fn from_tensor(tensor: &Tensor) -> Self {
        let data = tensor.data();

        if data.is_empty() {
            return Self {
                scale: 1.0,
                zero_point: 0,
            };
        }

        let min = data.iter().copied().fold(f32::INFINITY, f32::min);
        let max = data.iter().copied().fold(f32::NEG_INFINITY, f32::max);

        // Avoid division by zero
        let range = if (max - min).abs() < 1e-8 {
            1.0
        } else {
            max - min
        };

        // Scale for 8-bit range: map [min, max] to [-128, 127]
        let scale = range / 255.0;

        // Zero point: what int8 value represents 0.0?
        // 0.0 = (zero_point - offset) * scale
        // zero_point = 0.0/scale + offset = offset
        // offset = -min/scale
        let zero_point = if scale > 0.0 {
            (-min / scale - 128.0).round() as i32
        } else {
            0
        };

        Self { scale, zero_point }
    }
}

/// Quantize a tensor to int8
///
/// Formula: q = round(x / scale - zero_point) clamped to [-128, 127]
pub fn quantize_tensor(tensor: &Tensor, params: &QuantizationParams) -> Vec<i8> {
    let data = tensor.data();

    data.iter()
        .map(|&x| {
            let q = (x / params.scale - params.zero_point as f32).round();
            // Clamp to int8 range
            q.clamp(-128.0, 127.0) as i8
        })
        .collect()
}

/// Dequantize int8 data back to float
///
/// Formula: x = (q + zero_point) * scale
pub fn dequantize_tensor(
    quantized: &[i8],
    shape: Vec<usize>,
    params: &QuantizationParams,
) -> Result<Tensor> {
    let data: Vec<f32> = quantized
        .iter()
        .map(|&q| (q as f32 + params.zero_point as f32) * params.scale)
        .collect();

    Tensor::new(data, shape).map_err(|e| {
        TetnusNnError::InvalidInput(format!("Failed to create tensor: {}", e))
    })
}

/// Quantize model weights
///
/// Returns quantization parameters for each layer/weight
pub fn quantize_model_weights(weights: &[&Tensor]) -> Vec<(Vec<i8>, QuantizationParams)> {
    weights
        .iter()
        .map(|tensor| {
            let params = QuantizationParams::from_tensor(tensor);
            let quantized = quantize_tensor(tensor, &params);
            (quantized, params)
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_quantization_params() {
        let tensor = Tensor::new(vec![-1.0, 0.0, 1.0, 2.0], vec![4]).unwrap();
        let params = QuantizationParams::from_tensor(&tensor);

        assert!(params.scale > 0.0);
        assert!(params.zero_point.abs() < 256);
    }

    #[test]
    fn test_quantize_dequantize_roundtrip() {
        // Use a wider range for more realistic quantization
        let original = Tensor::new(vec![-10.0, -5.0, 0.0, 5.0, 10.0], vec![5]).unwrap();
        let params = QuantizationParams::from_tensor(&original);

        let quantized = quantize_tensor(&original, &params);
        let dequantized = dequantize_tensor(&quantized, vec![5], &params).unwrap();

        let original_data = original.data();
        let dequant_data = dequantized.data();

        // Check that error is small (within 2x quantization step size)
        // For reasonable data ranges, this should give ~1% accuracy
        let max_error = params.scale * 2.0;
        for (o, d) in original_data.iter().zip(dequant_data.iter()) {
            assert!((o - d).abs() <= max_error,
                "Original: {}, Dequantized: {}, Max Error: {}, Actual Error: {}",
                o, d, max_error, (o - d).abs());
        }
    }

    #[test]
    fn test_quantize_zero_range() {
        let tensor = Tensor::new(vec![1.0, 1.0, 1.0], vec![3]).unwrap();
        let params = QuantizationParams::from_tensor(&tensor);

        // Should handle zero range gracefully
        let quantized = quantize_tensor(&tensor, &params);
        assert_eq!(quantized.len(), 3);
    }

    #[test]
    fn test_quantize_model_weights() {
        let w1 = Tensor::randn(vec![10, 10]).unwrap();
        let w2 = Tensor::randn(vec![10, 5]).unwrap();

        let weights = vec![&w1, &w2];
        let quantized = quantize_model_weights(&weights);

        assert_eq!(quantized.len(), 2);
        assert_eq!(quantized[0].0.len(), 100);  // 10x10
        assert_eq!(quantized[1].0.len(), 50);   // 10x5
    }
}
