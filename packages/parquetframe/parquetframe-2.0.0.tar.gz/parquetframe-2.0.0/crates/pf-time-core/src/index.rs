//! Time index structures and utilities.

/// Time index for time-series data.
#[derive(Debug, Clone)]
pub struct TimeIndex {
    /// Timestamps in nanoseconds since epoch
    pub timestamps: Vec<i64>,
}

impl TimeIndex {
    /// Create a new time index from timestamps.
    pub fn new(timestamps: Vec<i64>) -> Self {
        Self { timestamps }
    }

    /// Get the number of timestamps.
    pub fn len(&self) -> usize {
        self.timestamps.len()
    }

    /// Check if the index is empty.
    pub fn is_empty(&self) -> bool {
        self.timestamps.is_empty()
    }

    /// Check if timestamps are sorted.
    pub fn is_sorted(&self) -> bool {
        self.timestamps.windows(2).all(|w| w[0] <= w[1])
    }
}

/// Frequency specification for resampling.
#[derive(Debug, Clone)]
pub enum Frequency {
    /// Nanoseconds
    Nanoseconds(i64),
    /// Microseconds
    Microseconds(i64),
    /// Milliseconds
    Milliseconds(i64),
    /// Seconds
    Seconds(i64),
    /// Minutes
    Minutes(i64),
    /// Hours
    Hours(i64),
    /// Days
    Days(i64),
}

impl Frequency {
    /// Parse frequency from string (e.g., "1H", "30s", "5min").
    pub fn from_str(s: &str) -> Result<Self, String> {
        let s = s.trim().to_lowercase();

        // Try to find where numbers end
        let num_end = s.chars().position(|c| !c.is_numeric())
            .ok_or_else(|| format!("No unit specified in frequency: {}", s))?;

        let num_str = &s[..num_end];
        let unit = &s[num_end..];

        let num: i64 = num_str.parse()
            .map_err(|_| format!("Invalid frequency number: {}", num_str))?;

        match unit {
            "ns" => Ok(Frequency::Nanoseconds(num)),
            "us" => Ok(Frequency::Microseconds(num)),
            "ms" => Ok(Frequency::Milliseconds(num)),
            "s" => Ok(Frequency::Seconds(num)),
            "m" | "min" => Ok(Frequency::Minutes(num)),
            "h" | "hr" => Ok(Frequency::Hours(num)),
            "d" | "day" => Ok(Frequency::Days(num)),
            _ => Err(format!("Unknown frequency unit: {}", unit)),
        }
    }

    /// Convert to nanoseconds.
    pub fn to_nanoseconds(&self) -> i64 {
        match self {
            Frequency::Nanoseconds(n) => *n,
            Frequency::Microseconds(n) => n * 1_000,
            Frequency::Milliseconds(n) => n * 1_000_000,
            Frequency::Seconds(n) => n * 1_000_000_000,
            Frequency::Minutes(n) => n * 60 * 1_000_000_000,
            Frequency::Hours(n) => n * 60 * 60 * 1_000_000_000,
            Frequency::Days(n) => n * 24 * 60 * 60 * 1_000_000_000,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_frequency_parsing() {
        assert!(Frequency::from_str("1s").is_ok());
        assert!(Frequency::from_str("30min").is_ok());
        assert!(Frequency::from_str("1h").is_ok());
        assert_eq!(Frequency::from_str("1s").unwrap().to_nanoseconds(), 1_000_000_000);
    }

    #[test]
    fn test_time_index() {
        let idx = TimeIndex::new(vec![1, 2, 3, 4, 5]);
        assert_eq!(idx.len(), 5);
        assert!(idx.is_sorted());
    }
}
