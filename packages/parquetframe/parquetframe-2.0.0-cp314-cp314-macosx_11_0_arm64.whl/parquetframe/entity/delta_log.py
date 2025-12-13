"""
Delta Log (Write-Ahead Log) for entity transactions.

Provides O(1) write complexity through append-only log with background compaction.

Architecture:
    entity_storage/
      ├── base.parquet          # Main data file
      ├── delta_log.jsonl       # Write-ahead log (append-only)
      └── delta_log.jsonl.lock  # Lock for WAL append only

Write Path: O(1)
    1. Append change to delta_log.jsonl (atomic, microseconds)
    2. Background compaction merges WAL into base.parquet

Read Path: O(WAL_size)
    1. Read base.parquet
    2. Apply deltas from delta_log.jsonl in memory
    3. Return merged view

Mathematical Justification:
    File Locks: T_write ≈ k · S_total (unscalable)
    With WAL:   T_write ≈ k · S_record (scalable)
"""

import json
import os
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any

import pandas as pd

try:
    import fcntl
except ImportError:
    # Windows compatibility
    fcntl = None

    class FcntlMock:
        LOCK_EX = 2
        LOCK_UN = 8

        @staticmethod
        def flock(fd, op):
            pass

    if os.name == "nt":
        fcntl = FcntlMock()


def json_serializer(obj):
    """Custom JSON serializer for datetime objects."""
    if isinstance(obj, datetime | date):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} is not JSON serializable")


class DeltaLog:
    """
    Lightweight Write-Ahead Log for entity operations.

    Provides:
    - O(1) write complexity via append-only log
    - Crash safety through durable WAL
    - High concurrency (readers + writers don't block)
    - Background compaction to merge deltas

    Example:
        >>> log = DeltaLog(Path("./data/users"))
        >>> log.append("UPSERT", {"user_id": "u1", "name": "Alice"})
        >>> log.append("DELETE", {"user_id": "u2"})
        >>>
        >>> # Read with deltas applied
        >>> base_df = pd.DataFrame(...)
        >>> merged_df = log.replay(base_df)
    """

    def __init__(
        self,
        storage_path: Path,
        primary_key: str,
        compaction_threshold: int = 1000,
        compaction_size_mb: float = 10.0,
    ):
        """
        Initialize Delta Log.

        Args:
            storage_path: Directory containing entity data
            primary_key: Name of primary key field
            compaction_threshold: Compact after N operations
            compaction_size_mb: Compact when WAL exceeds size (MB)
        """
        self.storage_path = Path(storage_path)
        self.primary_key = primary_key
        self.compaction_threshold = compaction_threshold
        self.compaction_size_mb = compaction_size_mb

        # WAL files
        self.wal_path = self.storage_path / "delta_log.jsonl"
        self.lock_path = self.storage_path / "delta_log.jsonl.lock"
        self.base_path = self.storage_path / "base.parquet"

        # Ensure directory exists
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def append(self, operation: str, data: dict[str, Any]) -> None:
        """
        Append operation to WAL with atomic write.

        This is the critical O(1) operation - only appends to log,
        doesn't touch the main data file.

        Args:
            operation: Operation type ("UPSERT" or "DELETE")
            data: Entity data (must include primary key)

        Example:
            >>> log.append("UPSERT", {"id": 1, "name": "Alice"})
            >>> log.append("DELETE", {"id": 2})
        """
        # Validate operation
        if operation not in ("UPSERT", "DELETE"):
            raise ValueError(f"Invalid operation: {operation}")

        # Ensure primary key present
        if self.primary_key not in data:
            raise ValueError(f"Primary key '{self.primary_key}' not in data")

        # Create log record with metadata
        record = {
            "ts": time.time(),
            "op": operation,
            "data": data,
        }

        # Atomic append with file lock (microseconds)
        with open(self.lock_path, "w") as lock_file:
            try:
                # Acquire exclusive lock
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)

                # Append to WAL
                with open(self.wal_path, "a") as wal:
                    wal.write(json.dumps(record, default=json_serializer) + "\n")
                    wal.flush()
                    os.fsync(wal.fileno())  # Ensure durability

            finally:
                # Release lock
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)

    def replay(self, base_df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply WAL deltas to base DataFrame.

        This merges the base data with all pending operations
        from the delta log.

        Args:
            base_df: Base DataFrame from parquet file

        Returns:
            Merged DataFrame with deltas applied

        Example:
            >>> base = pd.read_parquet("base.parquet")
            >>> merged = log.replay(base)
        """
        # If no WAL, return base as-is
        if not self.wal_path.exists() or self.wal_path.stat().st_size == 0:
            return base_df

        # Read all delta records
        deltas = []
        with open(self.wal_path) as f:
            for line in f:
                if line.strip():
                    deltas.append(json.loads(line))

        if not deltas:
            return base_df

        # Apply deltas in order
        result_df = base_df.copy()

        for delta in deltas:
            op = delta["op"]
            data = delta["data"]
            pk_value = data[self.primary_key]

            if op == "UPSERT":
                # Remove existing row if present
                result_df = result_df[result_df[self.primary_key] != pk_value]
                # Append new row without triggering concat warnings on empty frames
                if result_df.empty:
                    # Create a new frame with the same columns
                    # Ensure all expected columns exist in the row
                    row_dict = {col: data.get(col, pd.NA) for col in result_df.columns}
                    result_df = pd.DataFrame([row_dict])
                else:
                    new_row = pd.DataFrame([data])
                    # Align columns to existing frame to avoid dtype inference issues
                    new_row = new_row.reindex(columns=result_df.columns)
                    result_df = pd.concat([result_df, new_row], ignore_index=True)

            elif op == "DELETE":
                # Remove row
                result_df = result_df[result_df[self.primary_key] != pk_value]

        return result_df

    def should_compact(self) -> bool:
        """
        Check if compaction is needed.

        Compaction is triggered when:
        - WAL has >= compaction_threshold records, OR
        - WAL file size >= compaction_size_mb

        Returns:
            True if compaction should run
        """
        if not self.wal_path.exists():
            return False

        # Check file size
        size_mb = self.wal_path.stat().st_size / (1024 * 1024)
        if size_mb >= self.compaction_size_mb:
            return True

        # Check record count
        try:
            with open(self.wal_path) as f:
                count = sum(1 for line in f if line.strip())
            return count >= self.compaction_threshold
        except Exception:
            return False

    def compact(self, base_df: pd.DataFrame | None = None) -> pd.DataFrame:
        """
        Compact WAL into base Parquet file.

        This is the "vacuum" operation that merges deltas into
        the main data file and truncates the WAL.

        Args:
            base_df: Optional base DataFrame (will load if None)

        Returns:
            Compacted DataFrame

        Example:
            >>> log.compact()  # Merge WAL → base.parquet
        """
        # Load base if not provided
        if base_df is None:
            if self.base_path.exists():
                base_df = pd.read_parquet(self.base_path)
            else:
                base_df = pd.DataFrame()

        # Apply all deltas
        merged_df = self.replay(base_df)

        # Write to temporary file
        temp_path = self.base_path.with_suffix(".parquet.tmp")
        merged_df.to_parquet(temp_path, index=False)

        # Atomic rename (overwrites base)
        temp_path.replace(self.base_path)

        # Truncate WAL (atomic clear)
        with open(self.lock_path, "w") as lock_file:
            try:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
                # Clear WAL
                with open(self.wal_path, "w") as _:
                    pass  # Truncate to empty
            finally:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)

        return merged_df

    def count_deltas(self) -> int:
        """
        Count number of delta records in WAL.

        Returns:
            Number of pending delta operations
        """
        if not self.wal_path.exists():
            return 0

        try:
            with open(self.wal_path) as f:
                return sum(1 for line in f if line.strip())
        except Exception:
            return 0

    def get_stats(self) -> dict[str, Any]:
        """
        Get statistics about the delta log.

        Returns:
            Dictionary with delta log statistics
        """
        stats = {
            "delta_count": self.count_deltas(),
            "wal_exists": self.wal_path.exists(),
            "wal_size_mb": 0.0,
            "base_exists": self.base_path.exists(),
            "should_compact": self.should_compact(),
        }

        if self.wal_path.exists():
            stats["wal_size_mb"] = self.wal_path.stat().st_size / (1024 * 1024)

        return stats

    def clear(self) -> None:
        """
        Clear the delta log (WAL).

        This removes all pending operations without compacting them.
        Use with caution as it discards uncommitted changes.
        """
        with open(self.lock_path, "w") as lock_file:
            try:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
                # Clear WAL if it exists
                if self.wal_path.exists():
                    with open(self.wal_path, "w") as _:
                        pass  # Truncate to empty
            finally:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


__all__ = ["DeltaLog"]
