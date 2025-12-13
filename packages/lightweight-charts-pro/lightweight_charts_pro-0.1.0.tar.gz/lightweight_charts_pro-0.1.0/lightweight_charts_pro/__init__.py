"""Lightweight Charts Pro - Framework-agnostic Python core library.

This package provides a comprehensive Python interface to TradingView's Lightweight
Charts library. It includes data models, type definitions, chart components, and
utilities that enable creating professional financial charts in any Python framework.

The package is framework-agnostic and can be integrated with:
    - Streamlit for rapid dashboarding
    - Dash/Plotly for interactive web applications
    - Django/Flask for custom web backends
    - Jupyter notebooks for data analysis
    - Qt/Tkinter for desktop applications

Key Components:
    Data Models:
        Classes for representing different chart data types (OHLC, candlesticks,
        line data, histograms, etc.) with validation and serialization support.

    Type Definitions:
        Enumerations and constants for chart configuration including colors,
        line styles, marker shapes, crosshair modes, and visualization options.

    Chart Components:
        Base classes for creating and managing charts, series, and their options.
        Includes support for multiple chart types and advanced features like
        synchronized charts and custom visualizations.

    Series Classes:
        Specialized series implementations for different visualization types
        including candlesticks, lines, areas, histograms, bands, and ribbons.

    Options Configuration:
        Comprehensive options classes for configuring chart behavior, appearance,
        layout, localization, price scales, time scales, and interactions.

    Utilities:
        Helper functions and classes for data processing, serialization, color
        validation, time normalization, and case conversion.

Example:
    Basic usage with any framework::

        from lightweight_charts_pro import (
            LineData,
            LineSeries,
            ChartOptions,
            LineStyle,
        )

        # Create chart data
        data = LineData(time=1234567890, value=100.5)

        # Configure chart options
        options = ChartOptions()
        options.layout.background.color = "#FFFFFF"

        # Create a line series
        series = LineSeries()
        series.line_style = LineStyle.SOLID
        series.line_width = 2

Note:
    This package focuses on the core data structures and business logic.
    Framework-specific rendering implementations are provided in separate
    companion packages (e.g., streamlit-lightweight-charts-pro).

Version:
    0.1.0

License:
    MIT License - See LICENSE file for details

"""

# ============================================================================
# Local Imports - Chart base classes
# ============================================================================
# Base classes for chart and chart manager implementations
from lightweight_charts_pro.charts import BaseChart, BaseChartManager

# ============================================================================
# Local Imports - Chart options
# ============================================================================
# Configuration classes for chart appearance, behavior, and interactions
from lightweight_charts_pro.charts.options import (
    ChartOptions,
    CrosshairLineOptions,
    CrosshairOptions,
    CrosshairSyncOptions,
    GridLineOptions,
    GridOptions,
    KineticScrollOptions,
    LayoutOptions,
    LegendOptions,
    LineOptions,
    LocalizationOptions,
    PaneHeightOptions,
    PriceFormatOptions,
    PriceLineOptions,
    PriceScaleMargins,
    PriceScaleOptions,
    RangeConfig,
    RangeSwitcherOptions,
    SyncOptions,
    TimeScaleOptions,
    TrackingModeOptions,
    TradeVisualizationOptions,
    WatermarkOptions,
)

# ============================================================================
# Local Imports - Series classes
# ============================================================================
# Specialized series for different chart visualization types
from lightweight_charts_pro.charts.series import (
    AreaSeries,
    BandSeries,
    BarSeries,
    BaselineSeries,
    CandlestickSeries,
    GradientRibbonSeries,
    HistogramSeries,
    LineSeries,
    RibbonSeries,
    Series,
    SignalSeries,
    TrendFillSeries,
)

# ============================================================================
# Local Imports - Data models
# ============================================================================
# Data model classes for various chart types (OHLC, candlesticks, lines, etc.)
from lightweight_charts_pro.data import (
    AreaData,
    BarData,
    BaselineData,
    CandlestickData,
    Data,
    HistogramData,
    LineData,
    OhlcData,
    OhlcvData,
    SingleValueData,
)

# ============================================================================
# Local Imports - Type definitions
# ============================================================================
# Enumerations and type constants for chart configuration
from lightweight_charts_pro.type_definitions import (
    AnnotationPosition,
    AnnotationType,
    BackgroundStyle,
    ChartType,
    ColorType,
    ColumnNames,
    CrosshairMode,
    HorzAlign,
    LastPriceAnimationMode,
    LineStyle,
    LineType,
    MarkerPosition,
    MarkerShape,
    PriceLineSource,
    PriceScaleMode,
    TooltipPosition,
    TooltipType,
    TrackingActivationMode,
    TrackingExitMode,
    TradeType,
    TradeVisualization,
    VertAlign,
)

# ============================================================================
# Local Imports - Types and configuration
# ============================================================================
# Type definitions for series configuration and chart options
from lightweight_charts_pro.types import (
    Options,
    SeriesConfigChange,
    SeriesConfigState,
    SeriesConfiguration,
    SeriesStyleConfig,
    SeriesType,
    SeriesVisibilityConfig,
)

# ============================================================================
# Local Imports - Utilities
# ============================================================================
# Utility functions and classes for data processing and serialization
from lightweight_charts_pro.utils import (
    CaseConverter,
    SerializableMixin,
    SerializationConfig,
    SimpleSerializableMixin,
    chainable_field,
    chainable_property,
    is_valid_color,
    normalize_time,
    snake_to_camel,
    validated_field,
)

# ============================================================================
# Package metadata
# ============================================================================
# Package version following semantic versioning (MAJOR.MINOR.PATCH)
__version__ = "0.1.0"

# ============================================================================
# Public API exports
# ============================================================================
# List of public symbols exported by this package
# This controls what is imported when using "from lightweight_charts_pro import *"
__all__ = [
    # Version
    "__version__",
    # Data models
    "AreaData",
    "BarData",
    "BaselineData",
    "CandlestickData",
    "Data",
    "HistogramData",
    "LineData",
    "OhlcData",
    "OhlcvData",
    "SingleValueData",
    # Type definitions
    "AnnotationPosition",
    "AnnotationType",
    "BackgroundStyle",
    "ChartType",
    "ColorType",
    "ColumnNames",
    "CrosshairMode",
    "HorzAlign",
    "LastPriceAnimationMode",
    "LineStyle",
    "LineType",
    "MarkerPosition",
    "MarkerShape",
    "PriceLineSource",
    "PriceScaleMode",
    "TooltipPosition",
    "TooltipType",
    "TrackingActivationMode",
    "TrackingExitMode",
    "TradeType",
    "TradeVisualization",
    "VertAlign",
    # Types and configuration
    "Options",
    "SeriesConfigChange",
    "SeriesConfigState",
    "SeriesConfiguration",
    "SeriesStyleConfig",
    "SeriesType",
    "SeriesVisibilityConfig",
    # Utilities
    "CaseConverter",
    "SerializableMixin",
    "SerializationConfig",
    "SimpleSerializableMixin",
    "chainable_field",
    "chainable_property",
    "is_valid_color",
    "normalize_time",
    "snake_to_camel",
    "validated_field",
    # Chart base classes
    "BaseChart",
    "BaseChartManager",
    # Chart options
    "ChartOptions",
    "CrosshairLineOptions",
    "CrosshairOptions",
    "CrosshairSyncOptions",
    "GridLineOptions",
    "GridOptions",
    "KineticScrollOptions",
    "LayoutOptions",
    "LegendOptions",
    "LineOptions",
    "LocalizationOptions",
    "PaneHeightOptions",
    "PriceFormatOptions",
    "PriceLineOptions",
    "PriceScaleMargins",
    "PriceScaleOptions",
    "RangeConfig",
    "RangeSwitcherOptions",
    "SyncOptions",
    "TimeScaleOptions",
    "TrackingModeOptions",
    "TradeVisualizationOptions",
    "WatermarkOptions",
    # Series classes
    "AreaSeries",
    "BandSeries",
    "BarSeries",
    "BaselineSeries",
    "CandlestickSeries",
    "GradientRibbonSeries",
    "HistogramSeries",
    "LineSeries",
    "RibbonSeries",
    "Series",
    "SignalSeries",
    "TrendFillSeries",
]
