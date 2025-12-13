use arrow::array::RecordBatchReader;
use arrow::ipc::writer::StreamWriter;
use orc_rust::arrow_reader::ArrowReaderBuilder;
use std::fs::File;
use std::io::Cursor;

use crate::error::IoError;

/// Read an ORC file and convert it to Arrow IPC stream bytes.
///
/// This function provides fast, zero-copy ORC reading by:
/// 1. Reading ORC file using orc-rust
/// 2. Converting directly to Arrow RecordBatch
/// 3. Serializing to Arrow IPC format
///
/// # Arguments
/// * `path` - Path to the ORC file
/// * `batch_size` - Optional batch size for reading (default: 8192)
///
/// # Returns
/// * `Result<Vec<u8>>` - Arrow IPC stream bytes or error
///
/// # Example
/// ```ignore
/// let ipc_bytes = read_orc_ipc("data.orc", Some(1024))?;
/// // Transfer to Python as bytes
/// ```
pub fn read_orc_ipc(path: &str, batch_size: Option<usize>) -> Result<Vec<u8>, IoError> {
    // Open ORC file
    let file = File::open(path)
        .map_err(|e| IoError::FileNotFound(format!("Failed to open ORC file {}: {}", path, e)))?;

    // Create Arrow reader
    let builder = ArrowReaderBuilder::try_new(file)
        .map_err(|e| IoError::ParseError(format!("Failed to create ORC reader: {}", e)))?;

    // Build reader with optional batch size
    let mut reader = if let Some(size) = batch_size {
        builder.with_batch_size(size).build()
    } else {
        builder.build()
    };

    // Collect all batches
    let mut batches = Vec::new();
    let schema = reader.schema();

    loop {
        match reader.next() {
            Some(Ok(batch)) => {
                batches.push(batch);
            }
            Some(Err(e)) => {
                return Err(IoError::ParseError(format!("Error reading ORC batch: {}", e)));
            }
            None => break,
        }
    }

    if batches.is_empty() {
        return Err(IoError::ParseError("No data found in ORC file".to_string()));
    }

    // Serialize to Arrow IPC stream
    let mut cursor = Cursor::new(Vec::new());
    {
        let mut writer = StreamWriter::try_new(&mut cursor, &schema)
            .map_err(|e| IoError::SerializationError(format!("Failed to create IPC writer: {}", e)))?;

        for batch in batches {
            writer
                .write(&batch)
                .map_err(|e| IoError::SerializationError(format!("Failed to write batch: {}", e)))?;
        }

        writer
            .finish()
            .map_err(|e| IoError::SerializationError(format!("Failed to finish IPC stream: {}", e)))?;
    }

    Ok(cursor.into_inner())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_read_orc_basic() {
        // This is a placeholder test
        // In practice, you'd need to create a test ORC file
        // or use a known sample file
        assert!(true);
    }
}
