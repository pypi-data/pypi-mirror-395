//! Fast Avro reader that produces Arrow IPC stream bytes.
//!
//! This function reads Avro data using Rust (apache-avro), converts to Arrow,
//! then serializes to Arrow IPC stream so Python can reconstruct a pyarrow.Table.

use crate::error::{IoError, Result};
use apache_avro::{Reader, Schema};
use arrow::array::{
    ArrayRef, BooleanBuilder, Float32Builder, Float64Builder, Int32Builder, Int64Builder,
    StringBuilder,
};
use arrow::datatypes::{DataType, Field, Schema as ArrowSchema, SchemaRef};
use arrow::ipc::writer::StreamWriter;
use arrow::record_batch::RecordBatch;
use std::fs::File;
use std::path::Path;
use std::sync::Arc;

/// Read an Avro file and return Arrow IPC stream bytes.
pub fn read_avro_ipc<P: AsRef<Path>>(path: P, batch_size: Option<usize>) -> Result<Vec<u8>> {
    let path_ref = path.as_ref();
    if !path_ref.exists() {
        return Err(IoError::FileNotFound(path_ref.display().to_string()));
    }

    let file = File::open(path_ref)?;
    let reader = Reader::new(file).map_err(|e| IoError::Other(format!("Avro read error: {}", e)))?;

    let avro_schema = reader.writer_schema();
    let arrow_schema = avro_schema_to_arrow(avro_schema)?;
    let schema_ref: SchemaRef = Arc::new(arrow_schema.clone());

    let batch_size = batch_size.unwrap_or(8192);
    let mut batches: Vec<RecordBatch> = Vec::new();
    let mut builders = create_builders(&arrow_schema);
    let mut row_count = 0;

    for value in reader {
        let value = value.map_err(|e| IoError::Other(format!("Avro value error: {}", e)))?;
        append_value_to_builders(&mut builders, &value, &arrow_schema)?;
        row_count += 1;

        if row_count >= batch_size {
            let batch = finish_batch(&mut builders, &schema_ref)?;
            batches.push(batch);
            builders = create_builders(&arrow_schema);
            row_count = 0;
        }
    }

    // Flush remaining rows
    if row_count > 0 {
        let batch = finish_batch(&mut builders, &schema_ref)?;
        batches.push(batch);
    }

    // Serialize to Arrow IPC stream
    let mut buffer = Vec::<u8>::new();
    {
        let mut writer = StreamWriter::try_new(&mut buffer, &schema_ref)
            .map_err(|e| IoError::Other(e.to_string()))?;
        for b in batches {
            writer.write(&b).map_err(|e| IoError::Other(e.to_string()))?;
        }
        writer.finish().map_err(|e| IoError::Other(e.to_string()))?;
    }

    Ok(buffer)
}

/// Convert Avro schema to Arrow schema.
fn avro_schema_to_arrow(avro_schema: &Schema) -> Result<ArrowSchema> {
    match avro_schema {
        Schema::Record(record_schema) => {
            let mut arrow_fields = Vec::new();
            for field in &record_schema.fields {
                let arrow_type = avro_type_to_arrow(&field.schema)?;
                arrow_fields.push(Field::new(&field.name, arrow_type, true));
            }
            Ok(ArrowSchema::new(arrow_fields))
        }
        _ => Err(IoError::Other(
            "Only Avro Record schemas are supported at top level".to_string(),
        )),
    }
}

/// Map Avro types to Arrow types.
fn avro_type_to_arrow(schema: &Schema) -> Result<DataType> {
    match schema {
        Schema::Null => Ok(DataType::Null),
        Schema::Boolean => Ok(DataType::Boolean),
        Schema::Int => Ok(DataType::Int32),
        Schema::Long => Ok(DataType::Int64),
        Schema::Float => Ok(DataType::Float32),
        Schema::Double => Ok(DataType::Float64),
        Schema::String | Schema::Bytes => Ok(DataType::Utf8),
        Schema::Union(union) => {
            // Handle nullable unions (e.g., ["null", "string"])
            if union.variants().len() == 2 {
                let non_null = union
                    .variants()
                    .iter()
                    .find(|s| !matches!(s, Schema::Null));
                if let Some(s) = non_null {
                    return avro_type_to_arrow(s);
                }
            }
            Err(IoError::Other(format!(
                "Unsupported Avro union type: {:?}",
                union
            )))
        }
        _ => Err(IoError::Other(format!(
            "Unsupported Avro type: {:?}",
            schema
        ))),
    }
}

/// Create column builders for each field in the schema.
fn create_builders(schema: &ArrowSchema) -> Vec<Box<dyn ArrayBuilder>> {
    schema
        .fields()
        .iter()
        .map(|field| create_builder(field.data_type()))
        .collect()
}

/// Trait for type-erased array builders.
trait ArrayBuilder {
    fn append_value(&mut self, value: &apache_avro::types::Value) -> Result<()>;
    fn finish(&mut self) -> ArrayRef;
}

/// Create a builder for a specific data type.
fn create_builder(data_type: &DataType) -> Box<dyn ArrayBuilder> {
    match data_type {
        DataType::Boolean => Box::new(BooleanBuilderWrapper(BooleanBuilder::new())),
        DataType::Int32 => Box::new(Int32BuilderWrapper(Int32Builder::new())),
        DataType::Int64 => Box::new(Int64BuilderWrapper(Int64Builder::new())),
        DataType::Float32 => Box::new(Float32BuilderWrapper(Float32Builder::new())),
        DataType::Float64 => Box::new(Float64BuilderWrapper(Float64Builder::new())),
        DataType::Utf8 => Box::new(StringBuilderWrapper(StringBuilder::new())),
        _ => Box::new(StringBuilderWrapper(StringBuilder::new())), // fallback
    }
}

// Wrapper structs for each builder type

struct BooleanBuilderWrapper(BooleanBuilder);
impl ArrayBuilder for BooleanBuilderWrapper {
    fn append_value(&mut self, value: &apache_avro::types::Value) -> Result<()> {
        match value {
            apache_avro::types::Value::Boolean(b) => {
                self.0.append_value(*b);
                Ok(())
            }
            apache_avro::types::Value::Null => {
                self.0.append_null();
                Ok(())
            }
            _ => Err(IoError::Other(format!("Expected boolean, got {:?}", value))),
        }
    }
    fn finish(&mut self) -> ArrayRef {
        Arc::new(self.0.finish())
    }
}

struct Int32BuilderWrapper(Int32Builder);
impl ArrayBuilder for Int32BuilderWrapper {
    fn append_value(&mut self, value: &apache_avro::types::Value) -> Result<()> {
        match value {
            apache_avro::types::Value::Int(i) => {
                self.0.append_value(*i);
                Ok(())
            }
            apache_avro::types::Value::Null => {
                self.0.append_null();
                Ok(())
            }
            _ => Err(IoError::Other(format!("Expected int, got {:?}", value))),
        }
    }
    fn finish(&mut self) -> ArrayRef {
        Arc::new(self.0.finish())
    }
}

struct Int64BuilderWrapper(Int64Builder);
impl ArrayBuilder for Int64BuilderWrapper {
    fn append_value(&mut self, value: &apache_avro::types::Value) -> Result<()> {
        match value {
            apache_avro::types::Value::Long(l) => {
                self.0.append_value(*l);
                Ok(())
            }
            apache_avro::types::Value::Null => {
                self.0.append_null();
                Ok(())
            }
            _ => Err(IoError::Other(format!("Expected long, got {:?}", value))),
        }
    }
    fn finish(&mut self) -> ArrayRef {
        Arc::new(self.0.finish())
    }
}

struct Float32BuilderWrapper(Float32Builder);
impl ArrayBuilder for Float32BuilderWrapper {
    fn append_value(&mut self, value: &apache_avro::types::Value) -> Result<()> {
        match value {
            apache_avro::types::Value::Float(f) => {
                self.0.append_value(*f);
                Ok(())
            }
            apache_avro::types::Value::Null => {
                self.0.append_null();
                Ok(())
            }
            _ => Err(IoError::Other(format!("Expected float, got {:?}", value))),
        }
    }
    fn finish(&mut self) -> ArrayRef {
        Arc::new(self.0.finish())
    }
}

struct Float64BuilderWrapper(Float64Builder);
impl ArrayBuilder for Float64BuilderWrapper {
    fn append_value(&mut self, value: &apache_avro::types::Value) -> Result<()> {
        match value {
            apache_avro::types::Value::Double(d) => {
                self.0.append_value(*d);
                Ok(())
            }
            apache_avro::types::Value::Null => {
                self.0.append_null();
                Ok(())
            }
            _ => Err(IoError::Other(format!("Expected double, got {:?}", value))),
        }
    }
    fn finish(&mut self) -> ArrayRef {
        Arc::new(self.0.finish())
    }
}

struct StringBuilderWrapper(StringBuilder);
impl ArrayBuilder for StringBuilderWrapper {
    fn append_value(&mut self, value: &apache_avro::types::Value) -> Result<()> {
        match value {
            apache_avro::types::Value::String(s) => {
                self.0.append_value(s);
                Ok(())
            }
            apache_avro::types::Value::Bytes(b) => {
                let s = String::from_utf8_lossy(b);
                self.0.append_value(s.as_ref());
                Ok(())
            }
            apache_avro::types::Value::Null => {
                self.0.append_null();
                Ok(())
            }
            _ => {
                // Fallback: convert to string
                self.0.append_value(&format!("{:?}", value));
                Ok(())
            }
        }
    }
    fn finish(&mut self) -> ArrayRef {
        Arc::new(self.0.finish())
    }
}

/// Append an Avro record value to the builders.
fn append_value_to_builders(
    builders: &mut [Box<dyn ArrayBuilder>],
    value: &apache_avro::types::Value,
    schema: &ArrowSchema,
) -> Result<()> {
    match value {
        apache_avro::types::Value::Record(fields) => {
            for (i, field) in schema.fields().iter().enumerate() {
                let field_value = fields
                    .iter()
                    .find(|(name, _)| name == field.name())
                    .map(|(_, v)| v)
                    .unwrap_or(&apache_avro::types::Value::Null);
                builders[i].append_value(field_value)?;
            }
            Ok(())
        }
        _ => Err(IoError::Other(format!(
            "Expected Avro Record, got {:?}",
            value
        ))),
    }
}

/// Finish builders and create a RecordBatch.
fn finish_batch(
    builders: &mut [Box<dyn ArrayBuilder>],
    schema: &SchemaRef,
) -> Result<RecordBatch> {
    let columns: Vec<ArrayRef> = builders.iter_mut().map(|b| b.finish()).collect();
    RecordBatch::try_new(schema.clone(), columns)
        .map_err(|e| IoError::Other(format!("RecordBatch creation error: {}", e)))
}
