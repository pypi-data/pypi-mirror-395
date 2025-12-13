/// Core tensor structure with Arrow integration
use arrow::buffer::Buffer;
use std::sync::Arc;
use crate::{Result, TetnusError};
use crate::ops::Op;

/// Device where tensor data resides
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Device {
    /// CPU device
    CPU,
    // Future: CUDA(usize), // GPU device with ID
}

/// Internal tensor data (ref-counted, immutable)
pub struct TensorInternal {
    /// Arrow buffer holding the data (zero-copy when from Arrow arrays)
    pub data: Arc<parking_lot::RwLock<Buffer>>,

    /// Shape of the tensor (e.g., [2, 3] for 2x3 matrix)
    pub shape: Vec<usize>,

    /// Strides for each dimension (for zero-copy views)
    pub strides: Vec<usize>,

    /// Byte offset into the buffer
    pub offset: usize,

    /// Device location
    pub device: Device,

    /// Whether this tensor requires gradient computation
    pub requires_grad: bool,

    /// Gradient tensor (None until backward is called)
    pub grad: parking_lot::Mutex<Option<Tensor>>,

    /// Operation that created this tensor (for autograd)
    pub op: Option<Arc<dyn Op>>,

    /// Input tensors to the operation (for autograd)
    pub inputs: Vec<Tensor>,
}

/// Public tensor handle (cheaply cloneable via Arc)
#[derive(Clone)]
pub struct Tensor(pub Arc<TensorInternal>);

impl Tensor {
    /// Create a new tensor from raw f32 data
    pub fn new(data: Vec<f32>, shape: Vec<usize>) -> Result<Self> {
        Self::validate_shape(&data, &shape)?;

        // Convert Vec<f32> to Arrow buffer
        let byte_data: Vec<u8> = data
            .iter()
            .flat_map(|f| f.to_le_bytes())
            .collect();
        let buffer = Buffer::from(byte_data);

        // Compute strides (row-major / C-contiguous)
        let strides = Self::compute_strides(&shape);

        Ok(Tensor(Arc::new(TensorInternal {
            data: Arc::new(parking_lot::RwLock::new(buffer)),
            shape,
            strides,
            offset: 0,
            device: Device::CPU,
            requires_grad: false,
            grad: parking_lot::Mutex::new(None),
            op: None,
            inputs: Vec::new(),
        })))
    }

    /// Create tensor filled with zeros
    pub fn zeros(shape: Vec<usize>) -> Result<Self> {
        let numel = shape.iter().product();
        let data = vec![0.0f32; numel];
        Self::new(data, shape)
    }

    /// Create tensor filled with ones
    pub fn ones(shape: Vec<usize>) -> Result<Self> {
        let numel = shape.iter().product();
        let data = vec![1.0f32; numel];
        Self::new(data, shape)
    }

    /// Create tensor with evenly spaced values (like numpy.arange)
    pub fn arange(start: f32, stop: f32, step: f32) -> Result<Self> {
        if step == 0.0 {
            return Err(TetnusError::InvalidInput("step cannot be zero".to_string()));
        }
        if (stop - start) / step < 0.0 {
            return Err(TetnusError::InvalidInput("invalid start/stop/step combination".to_string()));
        }

        let mut values = Vec::new();
        let mut current = start;

        if step > 0.0 {
            while current < stop {
                values.push(current);
                current += step;
            }
        } else {
            while current > stop {
                values.push(current);
                current += step;
            }
        }

        let len = values.len();
        Self::new(values, vec![len])
    }

    /// Create tensor with linearly spaced values (like numpy.linspace)
    pub fn linspace(start: f32, stop: f32, num: usize) -> Result<Self> {
        if num == 0 {
            return Err(TetnusError::InvalidInput("num must be positive".to_string()));
        }

        if num == 1 {
            return Self::new(vec![start], vec![1]);
        }

        let step = (stop - start) / ((num - 1) as f32);
        let values: Vec<f32> = (0..num)
            .map(|i| start + (i as f32) * step)
            .collect();

        Self::new(values, vec![num])
    }

    /// Create identity matrix (like numpy.eye)
    pub fn eye(n: usize, m: Option<usize>) -> Result<Self> {
        let m = m.unwrap_or(n);
        let mut data = vec![0.0f32; n * m];

        let min_dim = n.min(m);
        for i in 0..min_dim {
            data[i * m + i] = 1.0;
        }

        Self::new(data, vec![n, m])
    }

    /// Create tensor filled with random values [0, 1) (like numpy.random.rand)
    pub fn rand(shape: Vec<usize>) -> Result<Self> {
        use std::cell::RefCell;
        thread_local! {
            static RNG: RefCell<fastrand::Rng> = RefCell::new(fastrand::Rng::new());
        }

        let numel: usize = shape.iter().product();
        let data: Vec<f32> = RNG.with(|rng| {
            (0..numel).map(|_| rng.borrow_mut().f32()).collect()
        });

        Self::new(data, shape)
    }

    /// Create tensor with random values from standard normal distribution (like numpy.random.randn)
    pub fn randn(shape: Vec<usize>) -> Result<Self> {
        use std::cell::RefCell;
        thread_local! {
            static RNG: RefCell<fastrand::Rng> = RefCell::new(fastrand::Rng::new());
        }

        let numel: usize = shape.iter().product();
        let data: Vec<f32> = RNG.with(|rng| {
            (0..numel).map(|_| {
                // Box-Muller transform for normal distribution
                let u1 = rng.borrow_mut().f32();
                let u2 = rng.borrow_mut().f32();
                (-2.0 * u1.ln()).sqrt() * (2.0 * std::f32::consts::PI * u2).cos()
            }).collect()
        });

        Self::new(data, shape)
    }

    /// Create tensor filled with a constant value (like numpy.full)
    pub fn full(shape: Vec<usize>, value: f32) -> Result<Self> {
        let numel: usize = shape.iter().product();
        let data = vec![value; numel];
        Self::new(data, shape)
    }

    /// Get the shape of the tensor
    pub fn shape(&self) -> &[usize] {
        &self.0.shape
    }

    /// Get the number of dimensions
    pub fn ndim(&self) -> usize {
        self.0.shape.len()
    }

    /// Get the total number of elements
    pub fn numel(&self) -> usize {
        self.0.shape.iter().product()
    }

    /// Get tensor data as f32 slice
    pub fn data(&self) -> Vec<f32> {
        let buffer_guard = self.0.data.read();
        let buffer = &*buffer_guard;
        let offset = self.0.offset;
        let numel = self.numel();

        // Convert bytes back to f32
        let mut result = Vec::with_capacity(numel);
        for i in 0..numel {
            let byte_offset = offset + i * 4;
            let bytes = &buffer.as_slice()[byte_offset..byte_offset + 4];
            let value = f32::from_le_bytes([bytes[0], bytes[1], bytes[2], bytes[3]]);
            result.push(value);
        }
        result
    }

    /// Update tensor data from a Vec<f32>
    /// This is used by optimizers to update weights
    pub fn set_data(&self, new_data: Vec<f32>) -> Result<()> {
        Self::validate_shape(&new_data, &self.0.shape)?;

        // Convert Vec<f32> to Arrow buffer
        let byte_data: Vec<u8> = new_data
            .iter()
            .flat_map(|f| f.to_le_bytes())
            .collect();
        let buffer = Buffer::from(byte_data);

        let mut data_guard = self.0.data.write();
        *data_guard = buffer;

        Ok(())
    }

    /// Clear gradient
    pub fn zero_grad(&self) {
        let mut grad = self.0.grad.lock();
        *grad = None;
    }

    /// Enable gradient tracking
    pub fn requires_grad_(self) -> Self {
        let internal = &*self.0;
        Tensor(Arc::new(TensorInternal {
            data: Arc::clone(&internal.data),
            shape: internal.shape.clone(),
            strides: internal.strides.clone(),
            offset: internal.offset,
            device: internal.device,
            requires_grad: true,
            grad: parking_lot::Mutex::new(None),
            op: internal.op.clone(),
            inputs: internal.inputs.clone(),
        }))
    }

    /// Get gradient (if computed)
    pub fn grad(&self) -> Option<Tensor> {
        self.0.grad.lock().clone()
    }

    /// Validate shape matches data size
    fn validate_shape(data: &[f32], shape: &[usize]) -> Result<()> {
        let expected: usize = shape.iter().product();
        if data.len() != expected {
            return Err(TetnusError::ShapeMismatch {
                expected: vec![expected],
                actual: vec![data.len()],
            });
        }
        Ok(())
    }

    /// Compute strides from shape (row-major order)
    fn compute_strides(shape: &[usize]) -> Vec<usize> {
        let mut strides = vec![1; shape.len()];
        for i in (0..shape.len().saturating_sub(1)).rev() {
            strides[i] = strides[i + 1] * shape[i + 1];
        }
        strides
    }
}

// Debug implementation
impl std::fmt::Debug for Tensor {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("Tensor")
            .field("shape", &self.0.shape)
            .field("device", &self.0.device)
            .field("requires_grad", &self.0.requires_grad)
            .finish()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tensor_creation() {
        let t = Tensor::new(vec![1.0, 2.0, 3.0, 4.0], vec![2, 2]).unwrap();
        assert_eq!(t.shape(), &[2, 2]);
        assert_eq!(t.numel(), 4);
        assert_eq!(t.ndim(), 2);
    }

    #[test]
    fn test_zeros() {
        let t = Tensor::zeros(vec![3, 2]).unwrap();
        assert_eq!(t.shape(), &[3, 2]);
        assert_eq!(t.data(), vec![0.0; 6]);
    }

    #[test]
    fn test_ones() {
        let t = Tensor::ones(vec![2, 3]).unwrap();
        assert_eq!(t.shape(), &[2, 3]);
        assert_eq!(t.data(), vec![1.0; 6]);
    }

    #[test]
    fn test_requires_grad() {
        let t = Tensor::ones(vec![2, 2]).unwrap().requires_grad_();
        assert!(t.0.requires_grad);
    }

    #[test]
    fn test_arange() {
        let t = Tensor::arange(0.0, 10.0, 2.0).unwrap();
        assert_eq!(t.shape(), &[5]);
        assert_eq!(t.data(), vec![0.0, 2.0, 4.0, 6.0, 8.0]);
    }

    #[test]
    fn test_arange_negative_step() {
        let t = Tensor::arange(10.0, 0.0, -2.0).unwrap();
        assert_eq!(t.shape(), &[5]);
        assert_eq!(t.data(), vec![10.0, 8.0, 6.0, 4.0, 2.0]);
    }

    #[test]
    fn test_arange_error() {
        let result = Tensor::arange(0.0, 10.0, 0.0);
        assert!(result.is_err());
    }

    #[test]
    fn test_linspace() {
        let t = Tensor::linspace(0.0, 1.0, 5).unwrap();
        assert_eq!(t.shape(), &[5]);
        let data = t.data();
        assert!((data[0] - 0.0).abs() < 1e-6);
        assert!((data[4] - 1.0).abs() < 1e-6);
    }

    #[test]
    fn test_linspace_single() {
        let t = Tensor::linspace(5.0, 10.0, 1).unwrap();
        assert_eq!(t.shape(), &[1]);
        assert_eq!(t.data(), vec![5.0]);
    }

    #[test]
    fn test_eye_square() {
        let t = Tensor::eye(3, None).unwrap();
        assert_eq!(t.shape(), &[3, 3]);
        let data = t.data();
        assert_eq!(data[0], 1.0);  // (0,0)
        assert_eq!(data[1], 0.0);  // (0,1)
        assert_eq!(data[4], 1.0);  // (1,1)
        assert_eq!(data[8], 1.0);  // (2,2)
    }

    #[test]
    fn test_eye_rectangular() {
        let t = Tensor::eye(2, Some(3)).unwrap();
        assert_eq!(t.shape(), &[2, 3]);
        let data = t.data();
        assert_eq!(data[0], 1.0);  // (0,0)
        assert_eq!(data[4], 1.0);  // (1,1)
    }

    #[test]
    fn test_rand() {
        let t = Tensor::rand(vec![100]).unwrap();
        assert_eq!(t.shape(), &[100]);
        let data = t.data();

        // Check values are in [0, 1)
        assert!(data.iter().all(|&x| x >= 0.0 && x < 1.0));

        // Check they're not all the same (very unlikely)
        let first = data[0];
        assert!(data.iter().any(|&x| (x - first).abs() > 0.01));
    }

    #[test]
    fn test_randn() {
        let t = Tensor::randn(vec![1000]).unwrap();
        assert_eq!(t.shape(), &[1000]);
        let data = t.data();

        // Check approximately normal: mean near 0, std near 1
        let mean: f32 = data.iter().sum::<f32>() / data.len() as f32;
        let variance: f32 = data.iter().map(|&x| (x - mean).powi(2)).sum::<f32>() / data.len() as f32;
        let std = variance.sqrt();

        assert!(mean.abs() < 0.2);  // Mean should be near 0
        assert!((std - 1.0).abs() < 0.2);  // Std should be near 1
    }

    #[test]
    fn test_full() {
        let t = Tensor::full(vec![2, 3], 3.14).unwrap();
        assert_eq!(t.shape(), &[2, 3]);
        assert!(t.data().iter().all(|&x| (x - 3.14).abs() < 1e-6));
    }
}
