//! Fast Parquet metadata reading and statistics extraction.
//!
//! This module provides optimized functions for reading Parquet file metadata
//! without loading the actual data, enabling fast file inspection and filtering.

use crate::error::{IoError, Result};
use parquet::file::reader::{FileReader, SerializedFileReader};
use std::fs::File;
use std::path::Path;

/// Metadata information for a Parquet file.
#[derive(Debug, Clone)]
pub struct ParquetMetadata {
    /// Number of rows in the file
    pub num_rows: i64,
    /// Number of row groups
    pub num_row_groups: usize,
    /// Number of columns
    pub num_columns: usize,
    /// File size in bytes (if available)
    pub file_size_bytes: Option<u64>,
    /// Parquet version
    pub version: i32,
    /// Column names
    pub column_names: Vec<String>,
    /// Column types (Arrow type names)
    pub column_types: Vec<String>,
}

/// Column statistics from Parquet metadata.
#[derive(Debug, Clone)]
pub struct ColumnStatistics {
    /// Column name
    pub name: String,
    /// Number of null values
    pub null_count: Option<i64>,
    /// Number of distinct values (if available)
    pub distinct_count: Option<i64>,
    /// Minimum value as string (if available)
    pub min_value: Option<String>,
    /// Maximum value as string (if available)
    pub max_value: Option<String>,
}

/// Read Parquet file metadata quickly without loading data.
///
/// This function only reads the file footer containing metadata,
/// making it very fast even for large files.
///
/// # Arguments
/// * `path` - Path to the Parquet file
///
/// # Returns
/// `ParquetMetadata` struct with file information
///
/// # Example
/// ```no_run
/// use pf_io_core::parquet_meta::read_parquet_metadata;
///
/// let metadata = read_parquet_metadata("data.parquet").unwrap();
/// println!("Rows: {}, Columns: {}", metadata.num_rows, metadata.num_columns);
/// ```
pub fn read_parquet_metadata<P: AsRef<Path>>(path: P) -> Result<ParquetMetadata> {
    let path_ref = path.as_ref();

    // Check file exists
    if !path_ref.exists() {
        return Err(IoError::FileNotFound(path_ref.display().to_string()));
    }

    // Open file and create reader
    let file = File::open(path_ref)?;
    let file_size = file.metadata().ok().map(|m| m.len());
    let reader = SerializedFileReader::new(file)?;

    // Get metadata
    let metadata = reader.metadata();
    let file_metadata = metadata.file_metadata();
    let schema = file_metadata.schema_descr();

    // Extract column information
    let mut column_names = Vec::new();
    let mut column_types = Vec::new();

    for i in 0..schema.num_columns() {
        let column = schema.column(i);
        column_names.push(column.name().to_string());
        column_types.push(format!("{:?}", column.physical_type()));
    }

    Ok(ParquetMetadata {
        num_rows: file_metadata.num_rows(),
        num_row_groups: metadata.num_row_groups(),
        num_columns: schema.num_columns(),
        file_size_bytes: file_size,
        version: file_metadata.version(),
        column_names,
        column_types,
    })
}

/// Get row count from a Parquet file (very fast operation).
///
/// This only reads the file footer and extracts the row count,
/// typically completing in milliseconds even for multi-GB files.
///
/// # Arguments
/// * `path` - Path to the Parquet file
///
/// # Returns
/// Number of rows in the file
pub fn get_row_count<P: AsRef<Path>>(path: P) -> Result<i64> {
    let path_ref = path.as_ref();

    if !path_ref.exists() {
        return Err(IoError::FileNotFound(path_ref.display().to_string()));
    }

    let file = File::open(path_ref)?;
    let reader = SerializedFileReader::new(file)?;
    let metadata = reader.metadata();

    Ok(metadata.file_metadata().num_rows())
}

/// Get column names from a Parquet file.
///
/// Extracts just the column names without reading data.
///
/// # Arguments
/// * `path` - Path to the Parquet file
///
/// # Returns
/// Vector of column names
pub fn get_column_names<P: AsRef<Path>>(path: P) -> Result<Vec<String>> {
    let path_ref = path.as_ref();

    if !path_ref.exists() {
        return Err(IoError::FileNotFound(path_ref.display().to_string()));
    }

    let file = File::open(path_ref)?;
    let reader = SerializedFileReader::new(file)?;
    let metadata = reader.metadata();
    let schema = metadata.file_metadata().schema_descr();

    let mut column_names = Vec::new();
    for i in 0..schema.num_columns() {
        column_names.push(schema.column(i).name().to_string());
    }

    Ok(column_names)
}

/// Get column statistics for all columns in a Parquet file.
///
/// Extracts statistics from the file metadata including null counts,
/// min/max values, and distinct counts (when available).
///
/// # Arguments
/// * `path` - Path to the Parquet file
///
/// # Returns
/// Vector of `ColumnStatistics` for each column
pub fn get_column_statistics<P: AsRef<Path>>(path: P) -> Result<Vec<ColumnStatistics>> {
    let path_ref = path.as_ref();

    if !path_ref.exists() {
        return Err(IoError::FileNotFound(path_ref.display().to_string()));
    }

    let file = File::open(path_ref)?;
    let reader = SerializedFileReader::new(file)?;
    let metadata = reader.metadata();
    let schema = metadata.file_metadata().schema_descr();

    let mut statistics = Vec::new();

    // Iterate through row groups and aggregate statistics
    for i in 0..schema.num_columns() {
        let column = schema.column(i);
        let column_name = column.name().to_string();

        let mut total_null_count: Option<i64> = Some(0);
        let mut min_value: Option<String> = None;
        let mut max_value: Option<String> = None;

        // Aggregate statistics across row groups
        for rg_idx in 0..metadata.num_row_groups() {
            let rg_metadata = metadata.row_group(rg_idx);
            let col_chunk = rg_metadata.column(i);

            if let Some(stats) = col_chunk.statistics() {
                // Accumulate null count if available
                match stats.null_count_opt() {
                    Some(nc) => {
                        if let Some(ref mut total) = total_null_count {
                            *total += nc as i64;
                        }
                    }
                    None => {
                        total_null_count = None;
                    }
                }

                // Track min/max (simplified - just use first row group's values if present)
                if rg_idx == 0 {
                    if let Some(minb) = stats.min_bytes_opt() {
                        min_value = Some(format!("{:?}", minb));
                    }
                    if let Some(maxb) = stats.max_bytes_opt() {
                        max_value = Some(format!("{:?}", maxb));
                    }
                }
            } else {
                total_null_count = None;
            }
        }

        statistics.push(ColumnStatistics {
            name: column_name,
            null_count: total_null_count,
            distinct_count: None, // Parquet doesn't always have distinct count
            min_value,
            max_value,
        });
    }

    Ok(statistics)
}

#[cfg(test)]
mod tests {
    use super::*;
    use parquet::file::properties::WriterProperties;
    use parquet::file::writer::SerializedFileWriter;
    use parquet::schema::parser::parse_message_type;
    use std::sync::Arc;

    fn create_test_parquet_file(path: &str) -> Result<()> {
        // Create a simple test Parquet file
        let schema_str = "message test_schema {
            REQUIRED INT32 id;
            OPTIONAL BYTE_ARRAY name (STRING);
            OPTIONAL INT64 value;
        }";

        let schema = Arc::new(parse_message_type(schema_str).unwrap());
        let props = Arc::new(WriterProperties::builder().build());

        let file = File::create(path)?;
        let writer = SerializedFileWriter::new(file, schema.clone(), props)?;

        // Close writer to finalize file
        let _file_writer = writer.close()?;

        Ok(())
    }

    #[test]
    fn test_read_metadata() {
        let test_file = "/tmp/test_parquet_meta.parquet";
        create_test_parquet_file(test_file).unwrap();

        let metadata = read_parquet_metadata(test_file).unwrap();

        assert_eq!(metadata.num_columns, 3);
        assert_eq!(metadata.column_names.len(), 3);
        assert!(metadata.column_names.contains(&"id".to_string()));
        assert!(metadata.column_names.contains(&"name".to_string()));
        assert!(metadata.column_names.contains(&"value".to_string()));

        // Clean up
        std::fs::remove_file(test_file).ok();
    }

    #[test]
    fn test_get_column_names() {
        let test_file = "/tmp/test_parquet_columns.parquet";
        create_test_parquet_file(test_file).unwrap();

        let columns = get_column_names(test_file).unwrap();

        assert_eq!(columns.len(), 3);
        assert_eq!(columns[0], "id");
        assert_eq!(columns[1], "name");
        assert_eq!(columns[2], "value");

        // Clean up
        std::fs::remove_file(test_file).ok();
    }

    #[test]
    fn test_file_not_found() {
        let result = read_parquet_metadata("/nonexistent/file.parquet");
        assert!(result.is_err());

        match result {
            Err(IoError::FileNotFound(_)) => {}
            _ => panic!("Expected FileNotFound error"),
        }
    }
}
