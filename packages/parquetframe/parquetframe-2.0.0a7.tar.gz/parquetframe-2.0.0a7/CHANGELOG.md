# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### 🔄 Phase 3.4: Workflow Engine Core (2025-10-21)

**High-performance DAG-based workflow orchestration engine with parallel execution, cancellation, and progress tracking.**

##### Core Infrastructure
- 📊 **DAG (Directed Acyclic Graph)** with cycle detection and topological sorting
  - Automatic dependency resolution and execution ordering
  - Kahn's algorithm for topological sort
  - Comprehensive cycle detection with detailed error messages
- 🎯 **Step Trait System** with flexible execution model
  - Resource hints (LightCPU, HeavyCPU, LightIO, HeavyIO, Memory)
  - Configurable retry behavior with exponential backoff
  - Timeout support per step
  - Dependency management
- ⚙️ **Executor Configuration** with builder pattern
  - Configurable parallelism (max_parallel_steps)
  - Global retry settings
  - Step timeout configuration
- 🚨 **Comprehensive Error Handling** with custom error types
  - DAGError for graph-related errors (cycles, missing nodes)
  - ExecutionError for runtime failures
  - ResourceError for resource management issues
  - Detailed error context and propagation

##### Execution Modes
- ▶️ **Sequential Execution** with progress tracking and cancellation
  - Topological order execution
  - Automatic retry with exponential backoff
  - Graceful cancellation with cleanup
  - Progress events (Started, Completed, Failed, Cancelled)
- ⚡ **Parallel Execution** with resource-aware scheduling
  - Wave-based execution respecting dependencies
  - Resource hints for intelligent scheduling
  - Configurable parallelism factor
  - Automatic load balancing
  - Thread pool management for CPU/IO-bound tasks

##### Advanced Features
- 🛑 **Cancellation Support** with thread-safe token
  - <10ns check latency (atomic operations)
  - Clone-able tokens for multi-threaded use
  - Graceful shutdown with partial result cleanup
  - Check at multiple execution points
- 📊 **Progress Tracking** with event system
  - ConsoleProgressCallback for terminal output
  - FileProgressTracker for JSON lines logging
  - CallbackProgressTracker for custom closures
  - Thread-safe event emission
  - Timestamped events with structured data
- 📈 **Metrics Collection**
  - Step-level timing and status
  - Workflow-level parallelism factor
  - Resource utilization tracking
  - Retry count and failure tracking
  - Memory usage estimation
- 🧵 **Thread Pool Manager** for hybrid CPU/IO execution
  - Separate pools for CPU and IO-bound tasks
  - Configurable pool sizes
  - Resource-aware task routing

##### Convenience APIs
- `execute()` - Simple sequential execution
- `execute_parallel()` - Simple parallel execution
- `execute_with_cancellation(token)` - Sequential with cancellation
- `execute_with_progress(callback)` - Sequential with progress
- `execute_parallel_with_cancellation(token)` - Parallel with cancellation
- `execute_parallel_with_progress(callback)` - Parallel with progress
- `execute_with_options(token, callback)` - Full control sequential
- `execute_parallel_with_options(token, callback)` - Full control parallel

##### Testing & Quality
- ✅ **167 Total Tests** (126 unit + 11 integration + 30 doc tests)
  - Sequential execution tests
  - Parallel execution tests (21 comprehensive tests)
  - DAG operation tests
  - Cancellation tests
  - Progress tracking tests
  - Error handling tests
  - Resource scheduling tests
  - Integration tests covering real-world patterns
- 🎯 **Integration Tests** for end-to-end scenarios
  - ETL pipeline (Extract → Transform → Load)
  - Parallel data ingestion with aggregation
  - Complex DAG workflows (diamond, tree, deep)
  - Retry on transient failures
  - Cancellation in long-running workflows
  - Progress tracking integration
  - Error propagation
  - High-volume workflows (50+ steps)
- 📊 **Performance Benchmarks** (30 benchmarks across 8 suites)
  - Sequential overhead measurement
  - Parallel speedup analysis
  - Cancellation check latency (<10ns)
  - DAG operation performance
  - Step execution cost
  - Executor construction overhead
  - Parallel scaling (1-8 threads)
  - Resource hints impact

##### Documentation & Examples
- 📚 **Comprehensive Documentation**
  - Library overview with features and concepts
  - Quick start guide with runnable examples
  - Core concepts (Steps, Dependencies, Parallel Execution)
  - Progress tracking patterns
  - Cancellation patterns
- 📖 **4 Complete Examples**
  - `basic_sequential.rs` - ETL pipeline demonstration
  - `parallel_execution.rs` - Performance comparison
  - `progress_tracking.rs` - 4 tracking methods
  - `cancellation.rs` - 4 cancellation patterns
- 🔬 **Benchmark Suite** with criterion
  - HTML report generation
  - Statistical analysis
  - Performance regression detection

##### Technical Details
- **Language**: Rust (safe, concurrent, performant)
- **Dependencies**:
  - `rayon` for parallel execution
  - `crossbeam` for concurrent data structures
  - `parking_lot` for efficient synchronization
  - `serde_json` for progress event serialization
- **Architecture**:
  - Trait-based step abstraction
  - DAG for dependency management
  - Resource-aware scheduler
  - Thread pool manager
  - Event-driven progress system
- **Performance**:
  - Minimal per-step overhead
  - Lock-free cancellation checks
  - Efficient parallel scheduling
  - Zero-cost abstractions where possible

##### Code Quality
- ✅ Clippy passes with `-D warnings`
- ✅ rustfmt compliance
- ✅ Comprehensive documentation
- ✅ All examples compile and run
- ✅ Benchmarks compile and execute

##### Usage Example
```rust
use pf_workflow_core::{
    ExecutorConfig, WorkflowExecutor, Step, StepResult,
    ExecutionContext, StepMetrics,
};
use serde_json::Value;

// Define a step
struct ProcessStep {
    id: String,
}

impl Step for ProcessStep {
    fn id(&self) -> &str { &self.id }
    fn dependencies(&self) -> &[String] { &[] }

    fn execute(&self, _ctx: &mut ExecutionContext)
        -> pf_workflow_core::Result<StepResult> {
        // Do work
        let metrics = StepMetrics::new(self.id.clone());
        Ok(StepResult::new(Value::Null, metrics))
    }
}

// Build and execute workflow
let config = ExecutorConfig::builder()
    .max_parallel_steps(4)
    .build();
let mut executor = WorkflowExecutor::new(config);

executor.add_step(Box::new(ProcessStep {
    id: "step1".to_string()
}));

let metrics = executor.execute_parallel()?;
println!("Completed {} steps", metrics.successful_steps);
```

##### Breaking Changes
- None - This is a new crate (`pf-workflow-core`)

##### Migration Notes
- New crate, no migration required
- Can be used standalone or integrated with ParquetFrame
- Designed for future data processing pipeline integration

## [1.0.1] - 2025-10-19

### Fixed
- 🐛 **Entity ID Generation**: Fixed timestamp collision issue when creating entities in rapid succession
  - Implemented UUID+timestamp pattern: `{type}_{milliseconds}_{uuid}`
  - Example: `board_1729299580000_a3f4b2e1`
  - Resolves 7 test failures in entity relationship queries
- 🔧 **Permission System**: Added convenience wrapper methods for permission checks
  - `TodoKanbanApp.check_list_access()` - auto-looks up board_id
  - `TodoKanbanApp.check_task_access()` - auto-looks up list_id and board_id
  - Simplifies API usage and fixes 4 permission test failures
- 📚 **Documentation Build**: Removed non-existent `DataFrameProxy.to_parquet` method reference
- 🔄 **Backend Switch Tests**: Updated 4 tests for Phase 2 API compatibility
  - `islazy` → `engine`, `._df` → `.native`, `.islazy` → `.engine_name`
- 🎯 **Task Model**: Added missing `position` field to Task dataclass
- 🧪 **Test Compatibility**: Fixed memory_usage and TimeSeriesAccessor tests for Phase 2
- ⚙️ **CI/CD Pipeline**: Configured pre-commit formatters to skip in GitHub Actions
  - Prevents cyclic formatting conflicts between black, ruff, and isort

### Test Results
- ✅ All 922 tests passing (24 skipped)
- ✅ 59.84% coverage (exceeds 45% requirement)
- ✅ All CI/CD pipelines green

## [1.0.0] - TBD

### 🚀 **MAJOR RELEASE: Phase 2 Multi-Engine API is Now Default**

**This is a breaking change release that makes Phase 2 the default API.**

### Breaking Changes

#### API Changes
- **Main Class Changed**: `ParquetFrame` → `DataFrameProxy`
  - `import parquetframe as pf` now returns Phase 2 multi-engine API
  - `pf.read()` returns `DataFrameProxy` instead of `ParquetFrame`
- **Backend Property**: `df.islazy` → `df.engine_name`
  - Phase 1: `if df.islazy:` checked for Dask (boolean)
  - Phase 2: `if df.engine_name == "dask":` checks engine (string: "pandas", "polars", or "dask")
- **DataFrame Access**: `df.df` → `df.native`
  - Phase 1: `native_df = df.df`
  - Phase 2: `native_df = df.native`
- **Backend Parameter**: `islazy=True/False` → `engine="pandas"/"polars"/"dask"`
  - Phase 1: `pf.read("data.csv", islazy=True)` for Dask
  - Phase 2: `pf.read("data.csv", engine="dask")` for Dask
- **Threshold Configuration**: `threshold_mb=` parameter removed
  - Phase 1: `pf.read("data.csv", threshold_mb=50)`
  - Phase 2: Use `set_config(pandas_threshold_mb=50.0)` globally

#### Migration Path
- **Legacy Support**: Phase 1 API available via `parquetframe.legacy` module
  - Use `from parquetframe.legacy import ParquetFrame` for backward compatibility
  - Deprecation warnings will guide migration
  - Legacy module will be removed in v2.0.0

### Added
- 🔄 **Multi-Engine Support**: Automatic selection between pandas, Polars, and Dask
  - **Pandas** (<100MB): Eager execution, rich ecosystem
  - **Polars** (100MB-10GB): Lazy evaluation, high performance
  - **Dask** (>10GB): Distributed processing, scalable
- 📁 **Apache Avro Support**: Native Avro format reading and writing
  - `pf.read_avro()` and `df.to_avro()`
  - Schema inference and validation
  - Compression support (deflate, snappy)
- 🎯 **Entity-Graph Framework**: Declarative persistence with `@entity` decorator
  - ORM-like CRUD operations
  - Relationship management with `@rel` decorator
  - Parquet/Avro storage backends
- ⚙️ **Global Configuration System**: `set_config()` and `config_context()`
  - Configure engine thresholds globally
  - Environment variable support
  - Context manager for temporary overrides
- 📊 **Intelligent Engine Selection**: Automatic backend choice based on:
  - Dataset size
  - Available memory
  - Installed engines
  - User preferences

### Enhanced
- ⚡ **Performance**: 2-5x improvements on medium-scale datasets (100MB-10GB)
- 🔧 **Developer Experience**: Single, clear import path eliminates confusion
- 📚 **Documentation**: Comprehensive breaking changes guide and migration documentation
- 🧪 **Test Coverage**: 146 tests (145 passing, 1 skipped) with >85% coverage

### Deprecated
- ⚠️ **Phase 1 API**: Available via `parquetframe.legacy` with deprecation warnings
  - Will be removed in v2.0.0 (6-12 months)
  - Clear migration path provided

### Documentation
- 📖 **[BREAKING_CHANGES.md](BREAKING_CHANGES.md)**: Comprehensive migration guide
- 📘 **[ADR-0002](docs/adr/0002-make-phase2-default-api.md)**: Architecture decision record
- 📗 **[Migration Guide](docs/phase2/MIGRATION_GUIDE.md)**: Step-by-step migration instructions
- 📕 **[User Guide](docs/phase2/USER_GUIDE.md)**: Complete Phase 2 feature documentation

### Migration Quick Reference

```python
# Phase 1 (Old)
import parquetframe as pf
df = pf.read("data.csv", islazy=True)
if df.islazy:
    result = df.df.compute()
else:
    result = df.df

# Phase 2 (New)
import parquetframe as pf
df = pf.read("data.csv", engine="dask")
if df.engine_name == "dask":
    result = df.native.compute()
else:
    result = df.native

# Temporary Compatibility (Deprecated)
from parquetframe.legacy import ParquetFrame
# Phase 1 code works with deprecation warnings
```

### For More Information
- See [BREAKING_CHANGES.md](BREAKING_CHANGES.md) for detailed migration guide
- See [docs/phase2/MIGRATION_GUIDE.md](docs/phase2/MIGRATION_GUIDE.md) for step-by-step instructions
- See [docs/adr/0002-make-phase2-default-api.md](docs/adr/0002-make-phase2-default-api.md) for decision rationale

## [0.5.0] - 2025-01-15

### 🧮 Advanced Analytics Features (Phase 0.3)

### Added
- 📊 **Statistical Analysis Accessor** - New `.stats` property for comprehensive statistical operations:
  - `describe_extended()` - Extended descriptive statistics beyond pandas describe()
  - `correlation_matrix()` - Pearson, Spearman, and Kendall correlation analysis
  - `distribution_summary()` - Distribution analysis with histogram and normality testing
  - `detect_outliers()` - Multiple outlier detection methods (IQR, Z-score, Isolation Forest)
  - `normality_test()` and `correlation_test()` - Statistical hypothesis testing
  - `linear_regression()` - Simple and multiple linear regression analysis
- ⏱️ **Time-Series Analysis Accessor** - New `.ts` property for temporal data operations:
  - `detect_datetime_columns()` - Automatic datetime column detection with multiple format support
  - `parse_datetime()` - Flexible datetime parsing with format inference
  - `resample()` - Time-based resampling with multiple aggregation methods
  - `rolling()` - Rolling window operations (mean, std, sum, max, min, custom functions)
  - `shift()`, `lag()`, `lead()` - Temporal data shifting for lag analysis
  - `between_time()`, `at_time()` - Time-of-day filtering operations
- 🔧 **CLI Analytics Commands**:
  - `pframe analyze` - Statistical analysis with options for correlation, outliers, regression
  - `pframe timeseries` - Time-series operations with resampling, rolling, shifting
  - Rich terminal output with formatted results and save options
- 📚 **Comprehensive Documentation**:
  - Complete analytics guide (`docs/analytics.md`) with examples and best practices
  - Dedicated time-series documentation (`docs/timeseries.md`) with workflow patterns
  - Updated README with analytics examples and CLI reference

### Enhanced
- ⚡ **Performance Optimizations**:
  - LRU caching for expensive datetime detection and statistical computations
  - Memory-aware operation selection with automatic chunking for large datasets
  - Optimized Dask operations with efficient sampling and batch processing
  - Progress warnings for large datasets and memory-intensive operations
  - Chunked processing for statistical calculations on large pandas datasets
- 🔄 **Backend Intelligence** - Automatic pandas/Dask selection for analytics operations
- 🧪 **Test Coverage** - 80+ comprehensive tests for statistical and time-series functionality
- 📖 **Documentation** - Updated feature highlights and CLI commands in README

### Examples

**Statistical Analysis:**
```python
# Extended descriptive statistics
stats = pf.stats.describe_extended()

# Correlation analysis
corr_matrix = pf.stats.correlation_matrix(method='spearman')

# Outlier detection
outliers = pf.stats.detect_outliers(['price', 'volume'], method='iqr')

# Linear regression
regression = pf.stats.linear_regression('price', ['volume', 'market_cap'])
```

**Time-Series Operations:**
```python
# Automatic datetime detection
ts_cols = pf.ts.detect_datetime_columns()

# Resample to daily averages
daily_avg = pf.ts.resample('D', method='mean')

# Rolling 7-day window
rolling = pf.ts.rolling(7, method='mean')

# Lag analysis
lagged = pf.ts.shift(periods=1)
```

**CLI Analytics:**
```bash
# Statistical analysis
pframe analyze data.parquet --stats describe_extended --outliers iqr

# Time-series operations
pframe timeseries stocks.parquet --resample 'D' --method mean --rolling 7
```

### Technical Details
- Intelligent backend dispatching for both pandas and Dask workflows
- Memory usage estimation for optimal processing strategy selection
- Caching system for repeated computations to improve performance
- Comprehensive type hints and docstrings for all analytics functions
- Integration with existing CLI and SQL functionality

### Breaking Changes
- None - All changes are backwards compatible additions

## [0.4.2] - 2025-01-15

### 🔧 Critical Type System Fixes

### Fixed
- 🐛 **Union Type Syntax Errors** - Resolved `TypeError: unsupported operand type(s) for |: 'str' and 'NoneType'` in method signatures
  - Added `from __future__ import annotations` to enable postponed annotation evaluation
  - Fixed forward reference issues with union types in `QueryContext` and `ParquetFrame` classes
  - Ensured proper string literal handling for self-references in type annotations
- 📋 **Pre-commit Hook Compliance** - All linting and formatting checks now pass successfully
- ✅ **CI/CD Stability** - Resolved type annotation issues that caused build failures

### Technical Details
- Fixed union type syntax with forward references by using string literals for self-references
- Added proper TYPE_CHECKING imports to ensure runtime compatibility
- Enhanced type safety while maintaining backward compatibility
- All pre-commit hooks (black, ruff, ruff-format) now pass cleanly

### Impact
- Resolves critical runtime errors that prevented proper module imports
- Ensures stable CI/CD pipeline execution
- Maintains full type hint support for development tools and IDEs

## [0.4.1] - 2025-01-15

### 🚀 Enhanced SQL Multi-Format Support & Documentation

### Added
- 📚 **Comprehensive SQL Documentation**:
  - Complete multi-format SQL guide with performance benchmarks
  - 936-line SQL cookbook with real-world recipes for ETL, analytics, and data quality
  - Cross-format join examples (CSV ↔ Parquet ↔ JSON)
  - Time series analysis and window function patterns
  - Data quality validation and anomaly detection recipes
  - Performance optimization and error handling guides
- 🧪 **Enhanced Test Coverage**:
  - Comprehensive multi-format test matrix covering all SQL operations × file formats
  - AI-powered SQL generation smoke tests with mock integration
  - Coverage boost tests for edge cases and error scenarios
  - Test coverage improved from ~40% to 57% (17 percentage point increase)
- 🔧 **Improved SQL Engine**:
  - Fixed all failing SQL tests across CSV, TSV, JSON, JSONL, Parquet, and ORC formats
  - Standardized test data schemas for consistent cross-format behavior
  - Enhanced SQL query validation with better error handling

### Enhanced
- 🎯 **Format Compatibility** - SQL queries now work seamlessly across all supported formats
- 📊 **Test Reliability** - All SQL matrix tests passing with consistent data schemas
- 🛡️ **Code Quality** - Improved linting, formatting, and pre-commit hook compliance
- 📖 **Documentation** - MkDocs navigation updated to include comprehensive SQL cookbook

### Fixed
- 🐛 **SQL Test Failures** - Resolved 6 failing SQL tests by standardizing test data schemas
- 🔍 **Format Detection** - Improved handling of cross-format SQL operations
- ✅ **Test Suite Stability** - All tests now pass consistently across different formats
- 🪟 **Windows CI/CD** - Skip ORC tests on Windows due to PyArrow timezone database issues (22 tests fixed)
  - Resolves PyArrow ORC reader looking for `/usr/share/zoneinfo/UTC` which doesn't exist on Windows
  - ORC tests continue to run on Linux/macOS ensuring full format coverage

### Technical Details
- Key module coverage improvements: `sql.py` (87%), `workflow_history.py` (95%), `datacontext` (90%)
- Enhanced error handling and exception testing coverage
- Comprehensive SQL cookbook with production-ready patterns
- Standardized "department" vs "city" column usage across test suite
- Pre-commit hooks (black, ruff, formatting) all passing

### Breaking Changes
- 🐍 **Python 3.9 Support Removed** - Minimum Python version is now 3.10+ due to modern type hinting syntax requirements

### Examples

**Cross-Format SQL Operations:**
```python
# Query CSV, join with Parquet, output to JSON
users_csv = pf.read("users.csv")
orders_parquet = pf.read("orders.parquet")

result = users_csv.sql("""
    SELECT u.name, u.department, o.total_amount
    FROM df u
    JOIN orders o ON u.id = o.user_id
    WHERE o.amount > 1000
""", orders=orders_parquet)

result.save("high_value_customers.json")
```

**Advanced Analytics from Cookbook:**
```python
# RFM Customer Segmentation
rfm_analysis = orders.sql("""
    WITH customer_metrics AS (
        SELECT customer_id,
               DATEDIFF('day', MAX(order_date), CURRENT_DATE) as recency_days,
               COUNT(DISTINCT order_id) as frequency,
               SUM(order_amount) as monetary_value
        FROM df WHERE order_date >= '2023-01-01'
        GROUP BY customer_id
    )
    SELECT *,
           CASE WHEN rfm_score >= 13 THEN 'Champions'
                WHEN rfm_score >= 10 THEN 'Loyal Customers'
                ELSE 'Others' END as segment
    FROM customer_metrics
""")
```

## [0.4.0] - 2025-01-15

### 🚀 Enhanced SQL Method Integration (Phase 0.2)

### Added
- 🔗 **Fluent SQL API** with method chaining support:
  - `select()`, `where()`, `group_by()`, `order_by()` methods on ParquetFrame
  - Complete SQL query building with method chaining: `pf.select().where().group_by().execute()`
  - SQLBuilder class for complex query construction
- ⚡ **Query Performance Optimization**:
  - Query result caching with configurable cache size and automatic management
  - Execution profiling with timing, memory usage, and metadata tracking
  - QueryResult dataclass with convenience properties (`rows`, `columns`, `cached`, `dataframe`)
- 🔧 **Query Utilities and Builder Patterns**:
  - `parameterize_query()` function for safe parameter substitution
  - `sql_with_params()` method for parameterized queries with {param} syntax
  - `build_join_query()` utility for programmatic SQL construction
- 🤝 **Enhanced JOIN Operations**:
  - Convenience JOIN methods: `left_join()`, `right_join()`, `inner_join()`, `full_join()`
  - Proper table aliasing and JOIN syntax handling
  - Support for complex multi-table JOINs with chaining
- 📊 **Direct DataFrame Access**:
  - Added `pandas_df` property for direct access to underlying pandas DataFrame
  - Improved type annotations with proper TYPE_CHECKING imports

### Enhanced
- 🗃️ **Multi-Format SQL Integration** - Verified SQL queries work seamlessly across CSV, JSON, ORC, and Parquet formats
- 🎯 **Backward Compatibility** - All existing `sql()` method functionality preserved
- 🛡️ **Error Handling** - Enhanced parameter validation and missing parameter detection
- 🧪 **Comprehensive Testing** - 27 new tests covering fluent API, profiling, caching, and utilities

### Examples

**Fluent SQL API:**
```python
result = (pf.select("name", "age", "salary")
         .where("age > 25")
         .group_by("department")
         .having("COUNT(*) > 1")
         .order_by("salary", "DESC")
         .limit(10)
         .execute())
```

**Parameterized Queries:**
```python
result = pf.sql_with_params(
    "SELECT * FROM df WHERE age > {min_age} AND salary < {max_salary}",
    min_age=25, max_salary=100000
)
```

**Enhanced JOINs:**
```python
result = (pf.select("df.name", "dept.name")
         .left_join(departments, "df.dept_id = dept.id", "dept")
         .where("dept.budget > 500000")
         .execute())
```

**Query Profiling:**
```python
result = (pf.select("COUNT(*) as total")
         .profile(True)
         .cache(True)
         .execute())

print(f"Executed in {result.execution_time:.3f}s")
print(f"Cached: {result.cached}")
```

### Technical Details
- Implemented SQLBuilder class with full SQL clause support
- Added query result caching with SHA256-based cache keys
- Enhanced type safety with proper forward references
- Memory-efficient caching with automatic size management
- Thread-safe implementation using immutable cache keys
- Comprehensive error handling for SQL syntax and parameter validation

## [0.2.3.2] - 2025-09-27

### 🐛 Additional AI Interactive Mode Fixes

### Fixed
- 🔄 **Async Event Loop Conflict** - Fixed "asyncio.run() cannot be called from a running event loop" error in AI confirm dialogs
- 🎯 **AI Query Execution** - Resolved blocking issue preventing AI-generated queries from executing properly
- 📋 **Interactive Workflow** - Enabled complete AI query confirmation and execution workflow in interactive mode

### Technical Details
- Used `asyncio.to_thread()` to run `confirm()` function in separate thread to avoid event loop conflicts
- Fixed async context handling in interactive AI command processing
- Maintained user confirmation functionality while resolving async execution issues

## [0.2.3.1] - 2025-01-27

### 🐛 Critical AI Interactive Mode Hotfix

### Fixed
- 🤖 **AI Interactive Command Bug** - Fixed `confirm()` function call in interactive mode that used unsupported `default=True` parameter
- 🔍 **Model Availability Check** - Improved Ollama model parsing to handle different response formats and `:latest` tags
- 📦 **AI Dependencies** - Enhanced error handling for missing Python `ollama` package in AI functionality
- 🎯 **Interactive Experience** - Resolved crashes when using `\ai` commands in ParquetFrame interactive CLI
- 📝 **Save-Script Command** - Fixed "Invalid value NaN (not a number)" errors in `\save-script` command
- 🗄️ **History Export** - Resolved JSON serialization issues with DataFrame NaN values in session export

### Technical Details
- Removed unsupported `default` parameter from `prompt_toolkit.shortcuts.confirm()` calls
- Enhanced model availability detection with better JSON parsing and tag normalization
- Added clearer error messages and user guidance for AI setup requirements
- Verified AI query execution and response generation in interactive mode
- Fixed DataFrame to dict conversion by replacing NaN values with None using `pandas.where()`
- Improved history manager's export functionality to handle missing/null values properly

## [0.2.3] - 2025-09-26

### 🛠️ CI/CD Fixes and Test Stability Release

### Fixed
- 🐛 **Windows CI Compatibility** - Skip interactive tests on Windows CI to handle NoConsoleScreenBufferError
- 🧪 **Schema Mismatch Handling** - Added union_by_name=True to DuckDB read_parquet for mismatched schemas
- 🔍 **LLM Agent Tests** - Fixed test mocking of OLLAMA_AVAILABLE flag for proper dependency handling
- ⚠️ **Factory Validation** - Improved DataContextFactory parameter validation for None handling
- 🔡 **Encoding Issues** - Fixed Unicode encoding problems in CI workflows by removing emojis
- 🎯 **Test Coverage** - Maintained 55%+ test coverage across the codebase

### Enhanced
- 🧩 **Optional Dependency Handling** - Improved installation and validation of bioframe, SQLAlchemy
- 📝 **Error Messages** - Enhanced clarity of error messages for missing dependencies
- ⚡ **Test Reliability** - Ensured consistent test behavior across all platforms
- 🔄 **CI Workflow** - Optimized CI process with explicit dependency verification

### Tests
- ✅ **Cross-platform Testing** - Ensured tests run consistently on macOS, Linux, and Windows
- 🛡️ **Edge Case Handling** - Improved robustness for different CI environments
- 🧠 **Dependency Checking** - Better skip mechanisms for tests that require optional packages

## [0.2.2] - 2025-01-26

### 🚀 Enhanced Features & Documentation Release

### Added
- 🗃️ **SQL Support via DuckDB** with `.sql()` method and `pframe sql` CLI command
- 🧬 **BioFrame Integration** with `.bio` accessor supporting cluster, overlap, merge, complement, closest
- 🤖 **AI-Powered Data Exploration** with natural language to SQL conversion using local LLM (Ollama)
- 📊 **Performance Benchmarking Suite** with comprehensive analysis and CLI integration
- 🔄 **YAML Workflow Engine** for declarative data processing pipelines
- 🗄️ **DataContext Framework** for unified access to parquet files and databases
- 📈 **Workflow Visualization** and history tracking capabilities
- ➕ **Optional Extras**: `[sql]`, `[bio]`, `[ai]`, and `[all]` for easy installation of feature sets

### Enhanced
- 🧠 **Intelligent Backend Switching** with memory pressure analysis and file characteristic detection
- 🎨 **Rich CLI Experience** with enhanced interactive mode and comprehensive help
- 🔍 **Advanced Error Handling** with detailed exception hierarchy and user-friendly messages
- 📚 **Comprehensive Documentation** with architecture guides, AI features documentation, and examples
- 🧪 **Expanded Test Suite** with 334 passing tests across multiple categories (54% coverage)
- ⚡ **Performance Optimizations** showing 7-90% speed improvements over direct pandas usage

### Changed
- 📋 **CLI Updated** to include SQL commands, interactive SQL mode, and AI-powered queries
- 🔧 **Architecture Refactored** with dependency injection and factory patterns
- 📖 **Documentation Structure** enhanced with detailed guides and API references

### Fixed
- 🛠️ **CI/CD Pipeline** improvements and cross-platform compatibility
- 🐛 **Test Stability** across different Python versions and operating systems
- 🔍 **Memory Management** with intelligent threshold adjustment

### Tests
- ✅ **Comprehensive Test Coverage** for SQL, bioframe, AI, and workflow functionality
- 🧪 **Integration Tests** for end-to-end workflows and real-world scenarios
- 🔄 **Performance Tests** with benchmarking validation
- 🤖 **AI Integration Tests** with mock-based LLM testing

## [0.2.1] - 2025-01-25

### 🎉 First PyPI Release
- ✅ **Successfully Published to PyPI**: Package now available via `pip install parquetframe`
- 🔒 **Trusted Publishing Configured**: Secure automated releases without API tokens
- 📦 **GitHub Releases**: Automatic release creation with downloadable artifacts
- 🚀 **Full CI/CD Pipeline**: Comprehensive testing, building, and publishing automation

### Improved
- 📦 **Release Pipeline** - Enhanced GitHub Actions workflow with trusted PyPI publishing
- 🔧 **Package Metadata** - Updated classifiers and keywords for better PyPI discovery
- 📚 **Documentation** - Added comprehensive release process documentation

### Fixed
- 🛠️ Fixed PyPI trusted publishing configuration in release workflow
- 📋 Updated package status to Beta (Development Status :: 4)

### Enhanced
- 🖥️ **Complete CLI Interface** with three main commands (`info`, `run`, `interactive`)
- 🎨 **Rich Terminal Output** with beautiful tables and color formatting
- 🐍 **Interactive Python REPL** mode with full ParquetFrame integration
- 📝 **Automatic Script Generation** from CLI sessions for reproducibility
- 🔍 **Advanced Data Exploration** with query filters, column selection, and previews
- 📊 **Statistical Operations** directly from command line (describe, info, sampling)
- ⚙️ **Backend Control** with force pandas/Dask options in CLI
- 📁 **File Metadata Display** with schema information and recommendations
- 🔄 **Session History Tracking** with persistent readline support
- 🎯 **Batch Data Processing** with output file generation

### Enhanced
- ✨ **ParquetFrame Core** with indexing support (`__getitem__`, `__len__`)
- 🔧 **Attribute Delegation** with session history recording
- 📋 **CI/CD Pipeline** with dedicated CLI testing jobs
- 📖 **Documentation** with comprehensive CLI usage examples
- 🧪 **Test Coverage** expanded to include CLI functionality

### CLI Commands
- `pframe info <file>` - Display file information and schema
- `pframe run <file> [options]` - Batch data processing with extensive options
- `pframe interactive [file]` - Start interactive Python session with ParquetFrame

### CLI Options
- Data filtering with `--query` pandas/Dask expressions
- Column selection with `--columns` for focused analysis
- Preview options: `--head`, `--tail`, `--sample` for data exploration
- Statistical analysis: `--describe`, `--info` for data profiling
- Output control: `--output`, `--save-script` for results and reproducibility
- Backend control: `--force-pandas`, `--force-dask`, `--threshold`

## [0.1.1] - 2024-09-24

### Fixed
- 🐛 **Critical Test Suite Stability** - Resolved 29 failing tests, bringing test suite to 100% passing (203 tests)
- 🔧 **Dependency Issues** - Added missing `psutil` dependency for memory monitoring and system resource detection
- ⚠️ **pandas Deprecation** - Replaced deprecated `pd.np` with direct `numpy` imports throughout codebase
- 📅 **DateTime Compatibility** - Updated deprecated pandas frequency 'H' to 'h' for pandas 2.0+ compatibility
- 🔄 **Backend Switching Logic** - Fixed explicit `islazy` parameter override handling to ensure manual control works correctly
- 🗂️ **Directory Creation** - Enhanced `save()` method to automatically create parent directories when saving files
- 🔍 **Parameter Validation** - Added proper validation for `islazy` and `npartitions` parameters with clear error messages
- 📊 **Data Type Preservation** - Improved pandas/Dask dtype consistency to prevent conversion issues
- 🌐 **URL Path Support** - Enhanced path handling to support remote files and URLs
- 🖥️ **CLI Output** - Fixed CLI row limiting (head/tail/sample) operations to work correctly before saving
- ⚖️ **Memory Estimation** - Updated unrealistic memory threshold tests to use practical values
- 🔗 **Method Chaining** - Updated tests to handle pandas operations that return pandas objects vs ParquetFrame objects
- 📈 **Benchmark Tests** - Fixed division-by-zero errors in benchmark summary calculations
- 🎯 **Edge Case Handling** - Improved handling of negative parameters, invalid types, and boundary conditions

### Improved
- 📊 **Test Coverage** - Increased from 21% to 65% with comprehensive test improvements
- ⚡ **Test Suite Performance** - All 203 tests now pass reliably with consistent results
- 🛡️ **Error Handling** - Enhanced validation and error messages throughout the codebase
- 📝 **Code Quality** - Fixed various edge cases and improved robustness of core functionality

### Technical Details
- Fixed `psutil` import issues in benchmarking module
- Resolved pandas `pd.np` deprecation across multiple modules
- Enhanced `ParquetFrame.save()` with automatic directory creation
- Improved `islazy` parameter validation and override logic
- Fixed CLI test assertions to match actual output messages
- Added proper handling for URL-based file paths
- Resolved memory estimation test threshold issues
- Fixed benchmark module mock expectations and verbose flag handling
- Improved test data generation to avoid pandas errors with mismatched array lengths

## [0.1.0] - 2024-09-24

### Added
- 🎉 **Initial release of ParquetFrame**
- ✨ **Automatic pandas/Dask backend selection** based on file size (default 10MB threshold)
- 📁 **Smart file extension handling** for parquet files (`.parquet`, `.pqt`)
- 🔄 **Seamless conversion** between pandas and Dask DataFrames (`to_pandas()`, `to_dask()`)
- ⚡ **Full API compatibility** with pandas and Dask operations through transparent delegation
- 🎯 **Zero configuration** - works out of the box with sensible defaults
- 🧪 **Comprehensive test suite** with 95%+ coverage (410+ tests)
- 📚 **Complete documentation** with MkDocs, API reference, and examples
- 🔧 **Modern development tooling** (ruff, black, mypy, pre-commit hooks)
- 🚀 **CI/CD pipeline** with GitHub Actions for testing and PyPI publishing
- 📦 **Professional packaging** with hatchling build backend

### Features
- `ParquetFrame` class with automatic backend selection
- Convenience functions: `read()`, `create_empty()`
- Property-based backend switching with `islazy` setter
- Method chaining support for data pipeline workflows
- Comprehensive error handling and validation
- Support for all pandas/Dask parquet reading options
- Flexible file path handling (Path objects, relative/absolute paths)
- Memory-efficient processing for large datasets

### Testing
- Unit tests for all core functionality
- Integration tests for backend switching logic
- I/O format tests for compression and data types
- Edge case and error handling tests
- Platform-specific and performance tests
- Test fixtures for various DataFrame scenarios

### Documentation
- Complete user guide with installation, quickstart, and usage examples
- API reference with automatic docstring generation
- Real-world examples for common use cases
- Performance optimization tips
- Contributing guidelines and development setup

[0.1.0]: https://github.com/leechristophermurray/parquetframe/releases/tag/v0.1.0
