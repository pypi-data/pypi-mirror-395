/// CPU compute kernels using rayon for parallelization

use rayon::prelude::*;

/// Parallel matrix multiplication: C = A * B
/// A: (m, k), B: (k, n) -> C: (m, n)
pub fn cpu_matmul(
    a: &[f32],
    b: &[f32],
    c: &mut [f32],
    m: usize,
    k: usize,
    n: usize,
) {
    // Simple parallel implementation
    c.par_chunks_mut(n)
        .enumerate()
        .for_each(|(i, c_row)| {
            for j in 0..n {
                let mut sum = 0.0;
                for p in 0..k {
                    sum += a[i * k + p] * b[p * n + j];
                }
                c_row[j] = sum;
            }
        });
}

/// Element-wise addition: C = A + B
pub fn cpu_add(a: &[f32], b: &[f32], c: &mut [f32]) {
    c.par_iter_mut()
        .zip(a.par_iter().zip(b.par_iter()))
        .for_each(|(c_val, (a_val, b_val))| {
            *c_val = a_val + b_val;
        });
}

/// Element-wise subtraction: C = A - B
pub fn cpu_sub(a: &[f32], b: &[f32], c: &mut [f32]) {
    c.par_iter_mut()
        .zip(a.par_iter().zip(b.par_iter()))
        .for_each(|(c_val, (a_val, b_val))| {
            *c_val = a_val - b_val;
        });
}

/// Element-wise multiplication: C = A * B
pub fn cpu_mul(a: &[f32], b: &[f32], c: &mut [f32]) {
    c.par_iter_mut()
        .zip(a.par_iter().zip(b.par_iter()))
        .for_each(|(c_val, (a_val, b_val))| {
            *c_val = a_val * b_val;
        });
}

/// Element-wise division: C = A / B
pub fn cpu_div(a: &[f32], b: &[f32], c: &mut [f32]) {
    c.par_iter_mut()
        .zip(a.par_iter().zip(b.par_iter()))
        .for_each(|(c_val, (a_val, b_val))| {
            *c_val = a_val / b_val;
        });
}

/// Element-wise exponential: C = exp(A)
pub fn cpu_exp(a: &[f32], c: &mut [f32]) {
    c.par_iter_mut()
        .zip(a.par_iter())
        .for_each(|(c_val, a_val)| {
            *c_val = a_val.exp();
        });
}

/// Element-wise natural logarithm: C = ln(A)
pub fn cpu_log(a: &[f32], c: &mut [f32]) {
    c.par_iter_mut()
        .zip(a.par_iter())
        .for_each(|(c_val, a_val)| {
            *c_val = a_val.ln();
        });
}

/// Sum reduction
pub fn cpu_sum(a: &[f32]) -> f32 {
    a.par_iter().sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cpu_matmul() {
        // 2x3 * 3x2 = 2x2
        let a = vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0];
        let b = vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0];
        let mut c = vec![0.0; 4];

        cpu_matmul(&a, &b, &mut c, 2, 3, 2);

        // Expected: [[22, 28], [49, 64]]
        assert_eq!(c[0], 22.0);
        assert_eq!(c[1], 28.0);
        assert_eq!(c[2], 49.0);
        assert_eq!(c[3], 64.0);
    }

    #[test]
    fn test_cpu_add() {
        let a = vec![1.0, 2.0, 3.0];
        let b = vec![4.0, 5.0, 6.0];
        let mut c = vec![0.0; 3];

        cpu_add(&a, &b, &mut c);

        assert_eq!(c, vec![5.0, 7.0, 9.0]);
    }
}
