# ParquetFrame

**High-performance data analytics with AI/ML capabilities**

[![PyPI version](https://badge.fury.io/py/parquetframe.svg)](https://badge.fury.io/py/parquetframe)
[![License](https://img.shields.io/badge/license-Apache%202-blue.svg)](LICENSE)

ParquetFrame is a unified data platform combining SQL, time series, geospatial, financial analysis, and AI/ML capabilities - all with familiar DataFrame interfaces.

## ✨ Features

- **SQL Engine**: Query DataFrames with SQL (DataFusion/DuckDB)
- **Time Series**: `.ts` accessor for resampling, rolling windows
- **GeoSpatial**: `.geo` accessor for spatial operations
- **Financial**: `.fin` accessor for technical indicators
- **AI/ML**: Tetnus ML framework + RAG with Knowlogy knowledge graph
- **Cloud**: S3, GCS, Azure Blob Storage support
- **Interactive CLI**: Rich REPL with syntax highlighting

## 🚀 Quick Start

```bash
pip install parquetframe
```

```python
import pandas as pd
import parquetframe as pf
import parquetframe.sql
import parquetframe.time
import parquetframe.finance

# SQL queries
result = pf.sql("SELECT * FROM df WHERE value > 100", df=df)

# Time series
daily = df.ts.resample('1D', agg='mean')

# Financial indicators
rsi = df.fin.rsi('close', 14)
macd = df.fin.macd('close')
```

## 📚 Documentation

- [Getting Started](docs/tutorials/getting_started.md)
- [API Reference](docs/api_reference.md)
- [SQL Guide](docs/sql/index.md)
- [Time Series](docs/time/index.md)
- [Financial Analysis](docs/finance/index.md)
- [GeoSpatial](docs/geo/index.md)

## 🎯 Use Cases

### Financial Analysis

```python
import parquetframe.finance

prices = pd.read_csv("stock.csv", index_col='date', parse_dates=True)
prices['SMA_20'] = prices.fin.sma('close', 20)
prices['RSI'] = prices.fin.rsi('close', 14)
```

### Time Series Forecasting

```python
import parquetframe.time

sensor_data = df.ts.resample('1H', agg='mean')
smoothed = sensor_data.ts.rolling('24H', agg='mean')
```

### GeoSpatial Analysis

```python
import geopandas as gpd
import parquetframe.geo

cities = gpd.read_file("cities.geojson")
buffered = cities.geo.buffer(1000)
```

### AI-Powered RAG

```python
from parquetframe.ai import SimpleRagPipeline
from parquetframe import knowlogy

# Query knowledge graph
formula = knowlogy.get_formula("variance")

# RAG with formula grounding
result = pipeline.run_query("Explain variance", user_context="analyst")
```

## 🏗️ Architecture

ParquetFrame combines:
- **Rust Core**: High-performance kernels (pf-time-core, pf-geo-core, pf-fin-core)
- **Python API**: Familiar pandas-style accessors
- **AI/ML**: Tetnus framework + Knowlogy knowledge graph
- **Cloud**: Multi-cloud storage integration

## 🔗 Project Links

- [Documentation](docs/)
- [Examples](examples/)
- [Tutorials](docs/tutorials/)

## 📄 License

Creative Commons Attribution-NonCommercial-NoDerivatives 4.0
International Public License

## 🙏 Acknowledgments

Built on top of:
- Apache Arrow / Polars / pandas
- DataFusion / DuckDB
- GeoPandas / Shapely
- PyTorch (Tetnus)
