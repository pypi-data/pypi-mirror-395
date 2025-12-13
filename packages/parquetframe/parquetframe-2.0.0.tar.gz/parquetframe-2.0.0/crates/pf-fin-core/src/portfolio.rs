/// Portfolio analytics and risk metrics.
///
/// Implements portfolio calculations including returns, volatility,
/// Value at Risk (VaR), Sharpe Ratio, and other risk metrics.

use arrow::array::{Array, ArrayRef, Float64Array, Float64Builder};
use crate::{FinError, Result};
use crate::utils::as_float64_array;
use std::sync::Arc;

/// Calculate simple returns from prices.
///
/// # Arguments
/// * `prices` - Array of price values
///
/// # Returns
/// Array of simple returns (price[t] / price[t-1] - 1)
pub fn returns(prices: &ArrayRef) -> Result<ArrayRef> {
    let array = as_float64_array(prices)?;
    let len = array.len();
    let mut builder = Float64Builder::with_capacity(len);

    builder.append_null(); // First value has no return

    for i in 1..len {
        if array.is_null(i) || array.is_null(i - 1) {
            builder.append_null();
        } else {
            let prev_price = array.value(i - 1);
            let curr_price = array.value(i);

            if prev_price == 0.0 {
                builder.append_null();
            } else {
                builder.append_value((curr_price / prev_price) - 1.0);
            }
        }
    }

    Ok(Arc::new(builder.finish()) as ArrayRef)
}

/// Calculate historical volatility (annualized standard deviation).
///
/// # Arguments
/// * `returns_array` - Array of returns
/// * `periods_per_year` - Number of periods per year (e.g., 252 for daily, 12 for monthly)
///
/// # Returns
/// Annualized volatility
pub fn volatility(returns_array: &ArrayRef, periods_per_year: usize) -> Result<f64> {
    let array = as_float64_array(returns_array)?;

    let values: Vec<f64> = (0..array.len())
        .filter_map(|i| if !array.is_null(i) { Some(array.value(i)) } else { None })
        .collect();

    if values.is_empty() {
        return Err(FinError::CalculationError("No valid values for volatility calculation".to_string()));
    }

    let mean = values.iter().sum::<f64>() / values.len() as f64;
    let variance = values.iter().map(|x| (x - mean).powi(2)).sum::<f64>() / values.len() as f64;
    let std_dev = variance.sqrt();

    Ok(std_dev * (periods_per_year as f64).sqrt())
}

/// Calculate Sharpe Ratio.
///
/// # Arguments
/// * `returns_array` - Array of returns
/// * `risk_free_rate` - Risk-free rate (annualized)
/// * `periods_per_year` - Number of periods per year
///
/// # Returns
/// Sharpe Ratio
pub fn sharpe_ratio(
    returns_array: &ArrayRef,
    risk_free_rate: f64,
    periods_per_year: usize,
) -> Result<f64> {
    let array = as_float64_array(returns_array)?;

    let values: Vec<f64> = (0..array.len())
        .filter_map(|i| if !array.is_null(i) { Some(array.value(i)) } else { None })
        .collect();

    if values.is_empty() {
        return Err(FinError::CalculationError("No valid values for Sharpe ratio calculation".to_string()));
    }

    let mean_return = values.iter().sum::<f64>() / values.len() as f64;
    let annualized_return = mean_return * periods_per_year as f64;

    let variance = values.iter().map(|x| (x - mean_return).powi(2)).sum::<f64>() / values.len() as f64;
    let std_dev = variance.sqrt();
    let annualized_vol = std_dev * (periods_per_year as f64).sqrt();

    if annualized_vol == 0.0 {
        return Err(FinError::CalculationError("Volatility is zero".to_string()));
    }

    Ok((annualized_return - risk_free_rate) / annualized_vol)
}

/// Calculate Sortino Ratio (downside deviation).
///
/// # Arguments
/// * `returns_array` - Array of returns
/// * `risk_free_rate` - Risk-free rate (annualized)
/// * `periods_per_year` - Number of periods per year
///
/// # Returns
/// Sortino Ratio
pub fn sortino_ratio(
    returns_array: &ArrayRef,
    risk_free_rate: f64,
    periods_per_year: usize,
) -> Result<f64> {
    let array = as_float64_array(returns_array)?;

    let values: Vec<f64> = (0..array.len())
        .filter_map(|i| if !array.is_null(i) { Some(array.value(i)) } else { None })
        .collect();

    if values.is_empty() {
        return Err(FinError::CalculationError("No valid values for Sortino ratio calculation".to_string()));
    }

    let mean_return = values.iter().sum::<f64>() / values.len() as f64;
    let annualized_return = mean_return * periods_per_year as f64;

    // Calculate downside deviation (only negative returns)
    let downside_values: Vec<f64> = values.iter().filter(|&&x| x < 0.0).copied().collect();

    if downside_values.is_empty() {
        return Ok(f64::INFINITY); // No downside risk
    }

    let downside_variance = downside_values.iter().map(|x| x.powi(2)).sum::<f64>() / values.len() as f64;
    let downside_dev = downside_variance.sqrt();
    let annualized_downside_dev = downside_dev * (periods_per_year as f64).sqrt();

    if annualized_downside_dev == 0.0 {
        return Ok(f64::INFINITY);
    }

    Ok((annualized_return - risk_free_rate) / annualized_downside_dev)
}

/// Calculate Value at Risk (VaR) using historical method.
///
/// # Arguments
/// * `returns_array` - Array of returns
/// * `confidence_level` - Confidence level (e.g., 0.95 for 95%)
///
/// # Returns
/// VaR value (positive number representing potential loss)
pub fn value_at_risk(returns_array: &ArrayRef, confidence_level: f64) -> Result<f64> {
    if confidence_level <= 0.0 || confidence_level >= 1.0 {
        return Err(FinError::InvalidParameter(
            "Confidence level must be between 0 and 1".to_string(),
        ));
    }

    let array = as_float64_array(returns_array)?;

    let mut values: Vec<f64> = (0..array.len())
        .filter_map(|i| if !array.is_null(i) { Some(array.value(i)) } else { None })
        .collect();

    if values.is_empty() {
        return Err(FinError::CalculationError("No valid values for VaR calculation".to_string()));
    }

    values.sort_by(|a, b| a.partial_cmp(b).unwrap());

    let percentile = 1.0 - confidence_level;
    let index = (values.len() as f64 * percentile).ceil() as usize - 1;
    let index = index.min(values.len() - 1);

    Ok(-values[index]) // Return as positive number
}

/// Calculate Conditional Value at Risk (CVaR / Expected Shortfall).
///
/// # Arguments
/// * `returns_array` - Array of returns
/// * `confidence_level` - Confidence level (e.g., 0.95 for 95%)
///
/// # Returns
/// CVaR value (positive number representing expected loss beyond VaR)
pub fn conditional_value_at_risk(returns_array: &ArrayRef, confidence_level: f64) -> Result<f64> {
    if confidence_level <= 0.0 || confidence_level >= 1.0 {
        return Err(FinError::InvalidParameter(
            "Confidence level must be between 0 and 1".to_string(),
        ));
    }

    let array = as_float64_array(returns_array)?;

    let mut values: Vec<f64> = (0..array.len())
        .filter_map(|i| if !array.is_null(i) { Some(array.value(i)) } else { None })
        .collect();

    if values.is_empty() {
        return Err(FinError::CalculationError("No valid values for CVaR calculation".to_string()));
    }

    values.sort_by(|a, b| a.partial_cmp(b).unwrap());

    let percentile = 1.0 - confidence_level;
    let cutoff_index = (values.len() as f64 * percentile).ceil() as usize;

    let tail_values = &values[..cutoff_index.min(values.len())];

    if tail_values.is_empty() {
        return value_at_risk(returns_array, confidence_level);
    }

    let mean_tail = tail_values.iter().sum::<f64>() / tail_values.len() as f64;

    Ok(-mean_tail) // Return as positive number
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_returns() {
        let prices = Arc::new(Float64Array::from(vec![100.0, 102.0, 101.0, 103.0, 105.0])) as ArrayRef;
        let result = returns(&prices).unwrap();
        let result_array = as_float64_array(&result).unwrap();

        assert!(result_array.is_null(0));
        assert!((result_array.value(1) - 0.02).abs() < 0.0001); // 2% gain
        assert!((result_array.value(2) - (-0.0098)).abs() < 0.0001); // ~-1% loss
    }

    #[test]
    fn test_sharpe_ratio() {
        let returns_data = Arc::new(Float64Array::from(vec![
            0.01, 0.02, -0.01, 0.03, 0.01, 0.02, -0.02, 0.04, 0.01, 0.02,
        ])) as ArrayRef;

        let sharpe = sharpe_ratio(&returns_data, 0.02, 252).unwrap();
        assert!(sharpe > 0.0); // Should be positive with positive mean returns
    }

    #[test]
    fn test_value_at_risk() {
        let returns_data = Arc::new(Float64Array::from(vec![
            -0.05, -0.03, -0.01, 0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06,
        ])) as ArrayRef;

        let var_95 = value_at_risk(&returns_data, 0.95).unwrap();
        assert!(var_95 > 0.0); // VaR should be positive
        assert!(var_95 <= 0.05); // Should be within worst returns
    }
}
