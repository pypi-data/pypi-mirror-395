"""
Enhanced I/O module for ParquetFrame Phase 2.

Provides support for advanced file formats including Apache Avro
with high-performance backends and schema inference capabilities.
"""

from .avro import AvroReader, AvroWriter, infer_avro_schema

__all__ = [
    "AvroReader",
    "AvroWriter",
    "infer_avro_schema",
]
