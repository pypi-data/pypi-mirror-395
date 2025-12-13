//! Fast readers that produce Arrow IPC stream bytes.
//!
//! These functions read data using Rust (parquet/csv), then serialize to
//! Arrow IPC stream so Python can reconstruct a pyarrow.Table without copies.

use crate::error::{IoError, Result};
use arrow::datatypes::SchemaRef;
use arrow::ipc::writer::StreamWriter;
use arrow::record_batch::RecordBatch;
use parquet::arrow::ProjectionMask;
use std::fs::File;
use std::path::Path;

/// Read a Parquet file and return Arrow IPC stream bytes with optional projection and row-group selection.
pub fn read_parquet_ipc<P: AsRef<Path>>(
    path: P,
    columns: Option<&[String]>,
    row_groups: Option<&[usize]>,
    batch_size: Option<usize>,
) -> Result<Vec<u8>> {
    let path_ref = path.as_ref();
    if !path_ref.exists() {
        return Err(IoError::FileNotFound(path_ref.display().to_string()));
    }

    // Open Parquet file
    let file = File::open(path_ref)?;

    // Use parquet->arrow RecordBatch reader (Arrow/Parquet 57 API expects a ChunkReader, e.g., File)
    let mut builder = parquet::arrow::arrow_reader::ParquetRecordBatchReaderBuilder::try_new(file)
        .map_err(|e| IoError::Other(e.to_string()))?;

    // Row-group selection
    if let Some(rgs) = row_groups {
        builder = builder.with_row_groups(rgs.to_vec());
    }

    // Column projection by name -> indices using ProjectionMask
    if let Some(cols) = columns {
        let meta = builder.metadata();
        let schema = meta.file_metadata().schema_descr();
        // Map names to leaf column indices in schema descriptor
        // If a name is not found, ignore silently (could also error)
        let mut leaves: Vec<usize> = Vec::new();
        for name in cols {
            for i in 0..schema.num_columns() {
                if schema.column(i).name() == name {
                    leaves.push(i);
                    break;
                }
            }
        }
        if !leaves.is_empty() {
            let mask = ProjectionMask::leaves(schema, leaves);
            builder = builder.with_projection(mask);
        }
    }

    if let Some(bs) = batch_size {
        builder = builder.with_batch_size(bs);
    }

    let rb_reader = builder.build().map_err(|e| IoError::Other(e.to_string()))?;

    // Collect batches
    let mut batches: Vec<RecordBatch> = Vec::new();
    for maybe_batch in rb_reader {
        let batch = maybe_batch.map_err(|e| IoError::Other(e.to_string()))?;
        batches.push(batch);
    }

    // Determine schema
    let schema: SchemaRef = match batches.first() {
        Some(b) => b.schema(),
        None => {
            let empty = arrow::datatypes::Schema::empty();
            std::sync::Arc::new(empty)
        }
    };

    // Serialize to Arrow IPC stream
    let mut buffer = Vec::<u8>::new();
    {
        let mut writer = StreamWriter::try_new(&mut buffer, &schema)
            .map_err(|e| IoError::Other(e.to_string()))?;
        for b in batches {
            writer.write(&b).map_err(|e| IoError::Other(e.to_string()))?;
        }
        writer.finish().map_err(|e| IoError::Other(e.to_string()))?;
    }

    Ok(buffer)
}

/// Read a CSV file and return Arrow IPC stream bytes.
/// Uses Arrow 57 CSV API with automatic schema inference.
pub fn read_csv_ipc<P: AsRef<Path>>(
    path: P,
    delimiter: u8,
    has_header: bool,
    infer_schema: bool,
    batch_size: Option<usize>,
) -> Result<Vec<u8>> {
    use arrow::csv::{ReaderBuilder, reader::Format};
    use std::io::BufReader;
    use std::sync::Arc;

    let path_ref = path.as_ref();
    if !path_ref.exists() {
        return Err(IoError::FileNotFound(path_ref.display().to_string()));
    }

    let file = File::open(path_ref)?;
    let batch_sz = batch_size.unwrap_or(8192);

    // Build CSV format
    let format = Format::default()
        .with_delimiter(delimiter)
        .with_header(has_header);

    // Infer schema if requested, otherwise use a simple string schema
    let schema: SchemaRef = if infer_schema {
        // Open file again for schema inference (small overhead)
        let infer_file = File::open(path_ref)?;
        let mut buf_reader = BufReader::new(infer_file);
        // Use arrow's infer_schema_from_files or infer directly from format
        let (inferred, _) = format.infer_schema(&mut buf_reader, Some(100))
            .map_err(|e| IoError::Other(format!("Schema inference failed: {}", e)))?;
        Arc::new(inferred)
    } else {
        // If not inferring, we still need a schema. Arrow 57 requires it.
        // We'll do a quick inference anyway since we can't proceed without a schema.
        let infer_file = File::open(path_ref)?;
        let mut buf_reader = BufReader::new(infer_file);
        let (inferred, _) = format.infer_schema(&mut buf_reader, Some(100))
            .map_err(|e| IoError::Other(format!("Schema inference failed: {}", e)))?;
        Arc::new(inferred)
    };

    // Build the reader with the schema
    let reader = ReaderBuilder::new(schema.clone())
        .with_format(format)
        .with_batch_size(batch_sz)
        .build(file)
        .map_err(|e| IoError::Other(format!("CSV reader build failed: {}", e)))?;

    // Collect batches
    let mut batches = Vec::new();
    for batch_result in reader {
        let batch = batch_result.map_err(|e| IoError::Other(format!("CSV read error: {}", e)))?;
        batches.push(batch);
    }

    // Serialize to Arrow IPC stream
    let mut buffer = Vec::<u8>::new();
    {
        let mut writer = StreamWriter::try_new(&mut buffer, &schema)
            .map_err(|e| IoError::Other(e.to_string()))?;
        for b in batches {
            writer.write(&b).map_err(|e| IoError::Other(e.to_string()))?;
        }
        writer.finish().map_err(|e| IoError::Other(e.to_string()))?;
    }

    Ok(buffer)
}
