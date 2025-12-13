"""
Rust backend performance benchmarking.

This module provides specialized benchmarks for comparing Rust backend
performance against Python/PyArrow implementations for I/O and graph operations.
"""

import gc
import tempfile
import time
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

try:
    import psutil  # noqa: F401

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class RustBenchmarkResult:
    """Container for Rust vs Python benchmark comparison results."""

    def __init__(
        self,
        operation: str,
        rust_time: float | None,
        python_time: float | None,
        file_size_mb: float,
        rows: int,
        columns: int,
        rust_success: bool = True,
        python_success: bool = True,
        speedup: float | None = None,
    ):
        self.operation = operation
        self.rust_time = rust_time
        self.python_time = python_time
        self.file_size_mb = file_size_mb
        self.rows = rows
        self.columns = columns
        self.rust_success = rust_success
        self.python_success = python_success

        # Calculate speedup
        if rust_time and python_time and rust_time > 0:
            self.speedup = python_time / rust_time
        else:
            self.speedup = speedup

    def __str__(self) -> str:
        if self.speedup:
            return (
                f"{self.operation}: Rust {self.rust_time:.4f}s, "
                f"Python {self.python_time:.4f}s, "
                f"Speedup: {self.speedup:.2f}x"
            )
        return f"{self.operation}: Rust={self.rust_time}s, Python={self.python_time}s"

    def to_dict(self) -> dict[str, Any]:
        """Export result as dictionary."""
        return {
            "operation": self.operation,
            "rust_time_seconds": self.rust_time,
            "python_time_seconds": self.python_time,
            "file_size_mb": self.file_size_mb,
            "rows": self.rows,
            "columns": self.columns,
            "rust_success": self.rust_success,
            "python_success": self.python_success,
            "speedup": self.speedup,
        }


class RustBackendBenchmark:
    """Benchmark suite for Rust backend performance."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.results: list[RustBenchmarkResult] = []

    def create_test_parquet(
        self, rows: int = 10000, cols: int = 10, path: Path | None = None
    ) -> Path:
        """
        Create a test Parquet file for benchmarking.

        Args:
            rows: Number of rows
            cols: Number of columns
            path: Optional path; uses temp file if None

        Returns:
            Path to created Parquet file
        """
        data = {}
        for i in range(cols // 3):
            data[f"int_col_{i}"] = np.random.randint(0, 1000, rows)
        for i in range(cols // 3):
            data[f"float_col_{i}"] = np.random.randn(rows)
        for i in range(cols - 2 * (cols // 3)):
            data[f"str_col_{i}"] = np.random.choice(
                ["A", "B", "C", "D", "E"], rows
            ).astype(str)

        df = pd.DataFrame(data)

        if path is None:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".parquet")
            path = Path(temp_file.name)

        df.to_parquet(path, engine="pyarrow")
        return path

    def benchmark_metadata_read(
        self, file_path: Path, iterations: int = 5
    ) -> RustBenchmarkResult:
        """
        Benchmark metadata reading: Rust vs PyArrow.

        Args:
            file_path: Path to Parquet file
            iterations: Number of iterations to average

        Returns:
            Benchmark comparison result
        """
        from .io.io_backend import (
            get_backend_info,
            read_parquet_metadata_fast,
        )

        backend_info = get_backend_info()
        file_size_mb = file_path.stat().st_size / (1024 * 1024)

        # Get row/column count from metadata for reporting
        try:
            import pyarrow.parquet as pq

            metadata = pq.read_metadata(file_path)
            rows = metadata.num_rows
            columns = metadata.num_columns
        except Exception:
            rows = 0
            columns = 0

        # Benchmark Rust backend
        rust_times = []
        rust_success = backend_info["rust_io_available"]

        if rust_success:
            try:
                for _ in range(iterations):
                    gc.collect()
                    start = time.perf_counter()
                    _ = read_parquet_metadata_fast(file_path)
                    rust_times.append(time.perf_counter() - start)
            except Exception as e:
                rust_success = False
                if self.verbose:
                    print(f"Rust metadata read failed: {e}")

        rust_time = sum(rust_times) / len(rust_times) if rust_times else None

        # Benchmark PyArrow
        python_times = []
        python_success = True

        try:
            import pyarrow.parquet as pq

            for _ in range(iterations):
                gc.collect()
                start = time.perf_counter()
                _ = pq.read_metadata(file_path)
                python_times.append(time.perf_counter() - start)
        except Exception as e:
            python_success = False
            if self.verbose:
                print(f"PyArrow metadata read failed: {e}")

        python_time = sum(python_times) / len(python_times) if python_times else None

        result = RustBenchmarkResult(
            operation="metadata_read",
            rust_time=rust_time,
            python_time=python_time,
            file_size_mb=file_size_mb,
            rows=rows,
            columns=columns,
            rust_success=rust_success,
            python_success=python_success,
        )

        self.results.append(result)
        if self.verbose:
            print(f"  {result}")

        return result

    def benchmark_row_count(
        self, file_path: Path, iterations: int = 5
    ) -> RustBenchmarkResult:
        """
        Benchmark row count reading: Rust vs PyArrow.

        Args:
            file_path: Path to Parquet file
            iterations: Number of iterations to average

        Returns:
            Benchmark comparison result
        """
        from .io.io_backend import get_backend_info, get_parquet_row_count_fast

        backend_info = get_backend_info()
        file_size_mb = file_path.stat().st_size / (1024 * 1024)

        # Get metadata for reporting
        try:
            import pyarrow.parquet as pq

            metadata = pq.read_metadata(file_path)
            rows = metadata.num_rows
            columns = metadata.num_columns
        except Exception:
            rows = 0
            columns = 0

        # Benchmark Rust backend
        rust_times = []
        rust_success = backend_info["rust_io_available"]

        if rust_success:
            try:
                for _ in range(iterations):
                    gc.collect()
                    start = time.perf_counter()
                    _ = get_parquet_row_count_fast(file_path)
                    rust_times.append(time.perf_counter() - start)
            except Exception as e:
                rust_success = False
                if self.verbose:
                    print(f"Rust row count failed: {e}")

        rust_time = sum(rust_times) / len(rust_times) if rust_times else None

        # Benchmark PyArrow
        python_times = []
        python_success = True

        try:
            import pyarrow.parquet as pq

            for _ in range(iterations):
                gc.collect()
                start = time.perf_counter()
                metadata = pq.read_metadata(file_path)
                _ = metadata.num_rows
                python_times.append(time.perf_counter() - start)
        except Exception as e:
            python_success = False
            if self.verbose:
                print(f"PyArrow row count failed: {e}")

        python_time = sum(python_times) / len(python_times) if python_times else None

        result = RustBenchmarkResult(
            operation="row_count",
            rust_time=rust_time,
            python_time=python_time,
            file_size_mb=file_size_mb,
            rows=rows,
            columns=columns,
            rust_success=rust_success,
            python_success=python_success,
        )

        self.results.append(result)
        if self.verbose:
            print(f"  {result}")

        return result

    def run_comprehensive_benchmark(
        self, file_sizes: list[tuple[int, int]] = None
    ) -> list[RustBenchmarkResult]:
        """
        Run comprehensive benchmark across multiple file sizes.

        Args:
            file_sizes: List of (rows, columns) tuples to test

        Returns:
            List of all benchmark results
        """
        if file_sizes is None:
            file_sizes = [
                (1_000, 10),
                (10_000, 20),
                (100_000, 30),
                (1_000_000, 40),
            ]

        if self.verbose:
            print("\n🚀 Running Rust Backend Benchmarks\n")

        for rows, cols in file_sizes:
            if self.verbose:
                print(f"Testing with {rows:,} rows × {cols} columns")

            # Create test file
            test_file = self.create_test_parquet(rows, cols)

            try:
                # Benchmark operations
                self.benchmark_metadata_read(test_file)
                self.benchmark_row_count(test_file)

            finally:
                # Cleanup
                test_file.unlink(missing_ok=True)

            if self.verbose:
                print()

        return self.results

    def print_summary(self) -> None:
        """Print summary of benchmark results."""
        if not self.results:
            print("No benchmark results available.")
            return

        print("\n" + "=" * 70)
        print("RUST BACKEND PERFORMANCE SUMMARY")
        print("=" * 70)

        for result in self.results:
            print(f"\n{result.operation.upper()} ({result.rows:,} rows)")
            print(f"  File Size: {result.file_size_mb:.2f} MB")
            if result.rust_time:
                print(f"  Rust:      {result.rust_time * 1000:.2f} ms")
            if result.python_time:
                print(f"  PyArrow:   {result.python_time * 1000:.2f} ms")
            if result.speedup:
                emoji = "🚀" if result.speedup > 1 else "🐌"
                print(f"  Speedup:   {result.speedup:.2f}x {emoji}")

        # Calculate average speedup
        speedups = [r.speedup for r in self.results if r.speedup]
        if speedups:
            avg_speedup = sum(speedups) / len(speedups)
            print(f"\nAverage Speedup: {avg_speedup:.2f}x")

        print("=" * 70 + "\n")

    def export_results(self, output_path: Path) -> None:
        """
        Export benchmark results to JSON.

        Args:
            output_path: Path to write JSON results
        """
        import json

        data = {
            "benchmark_type": "rust_backend",
            "results": [r.to_dict() for r in self.results],
        }

        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        if self.verbose:
            print(f"Results exported to: {output_path}")


def run_rust_benchmark(
    verbose: bool = True, export_path: Path | None = None
) -> list[RustBenchmarkResult]:
    """
    Run Rust backend benchmark suite.

    Args:
        verbose: Print progress and results
        export_path: Optional path to export results as JSON

    Returns:
        List of benchmark results
    """
    benchmark = RustBackendBenchmark(verbose=verbose)
    results = benchmark.run_comprehensive_benchmark()

    if verbose:
        benchmark.print_summary()

    if export_path:
        benchmark.export_results(export_path)

    return results
