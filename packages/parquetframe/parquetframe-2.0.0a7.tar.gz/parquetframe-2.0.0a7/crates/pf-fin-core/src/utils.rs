/// Utility functions for financial calculations.

use arrow::array::{ArrayRef, Float64Array};
use arrow::datatypes::DataType;
use crate::{FinError, Result};

/// Validates that an array is Float64 type.
pub fn validate_float64_array(array: &ArrayRef) -> Result<()> {
    match array.data_type() {
        DataType::Float64 => Ok(()),
        _ => Err(FinError::InvalidParameter(
            format!("Expected Float64 array, got {:?}", array.data_type())
        )),
    }
}

/// Converts an ArrayRef to Float64Array, validating type.
pub fn as_float64_array(array: &ArrayRef) -> Result<&Float64Array> {
    validate_float64_array(array)?;
    array
        .as_any()
        .downcast_ref::<Float64Array>()
        .ok_or_else(|| FinError::CalculationError("Failed to downcast to Float64Array".to_string()))
}
