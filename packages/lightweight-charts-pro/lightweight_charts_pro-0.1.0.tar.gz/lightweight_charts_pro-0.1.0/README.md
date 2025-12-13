# Lightweight Charts Pro (Python)

Framework-agnostic Python core library for TradingView Lightweight Charts Pro.

## Overview

This package provides the foundational Python classes and utilities used by all Python framework wrappers (Streamlit, Flask, Django, FastAPI, etc.).

## Features

- **Data Models**: Type-safe data classes for all chart types
- **Options Classes**: Comprehensive chart configuration options
- **Base Classes**: `BaseChart` and `BaseChartManager` for framework extensions
- **Validators**: Data validation and type checking
- **Type Definitions**: Enums and type hints
- **Exceptions**: Standardized error handling

## Installation

```bash
pip install lightweight-charts-pro
```

## Usage

```python
from lightweight_charts_pro.charts import BaseChart
from lightweight_charts_pro.charts.options import ChartOptions, LineOptions
from lightweight_charts_pro.data import LineData

# Use in your framework wrapper
class MyFrameworkChart(BaseChart):
    def render(self):
        # Framework-specific rendering logic
        pass
```

## Development

```bash
# Install in development mode
pip install -e .

# Run tests
pytest

# Type checking
mypy lightweight_charts_pro
```

## License

MIT
