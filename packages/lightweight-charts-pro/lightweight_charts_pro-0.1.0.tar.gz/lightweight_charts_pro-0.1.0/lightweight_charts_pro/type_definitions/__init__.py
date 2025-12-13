"""Type definitions for Streamlit Lightweight Charts Pro.

This module provides comprehensive type definitions, enumerations, and color classes
used throughout the charting library. It includes type-safe constants for chart
configuration, styling options, and data handling.

The module centralizes all type definitions to ensure consistency and type safety
across the entire library, enabling IDE autocompletion, type checking, and reducing
configuration errors.

Key Components:
    Enumerations:
        - ChartType: Available chart visualization types (candlestick, line, etc.)
        - LineStyle: Line rendering styles (solid, dashed, dotted)
        - MarkerShape: Marker shapes for data point annotations (circle, square, etc.)
        - PriceScaleMode: Price scale display modes (normal, logarithmic, percentage)
        - CrosshairMode: Crosshair behavior modes (normal, magnet)
        - And many more configuration enums

    Color Classes:
        - BackgroundSolid: Solid color backgrounds with validation
        - BackgroundGradient: Gradient backgrounds with top/bottom colors
        - Background: Union type for all background types

    Position and Alignment:
        - AnnotationPosition: Where annotations appear relative to data
        - HorzAlign: Horizontal text alignment (left, center, right)
        - VertAlign: Vertical text alignment (top, center, bottom)
        - MarkerPosition: Where markers appear relative to bars

    Trade Configuration:
        - TradeType: Trade direction (long, short)
        - TradeVisualization: How trades are visualized (markers, rectangles, etc.)

Features:
    - Type-safe enum values with proper IDE support
    - Comprehensive coverage of all chart configuration options
    - Clear documentation for each enum value
    - Compatible with TradingView's Lightweight Charts library
    - Python-native interface for configuration

Example Usage:
    Using enums for type-safe configuration::

        from lightweight_charts_pro.type_definitions import (
            ChartType,
            LineStyle,
            MarkerShape,
            PriceScaleMode,
        )

        # Create type-safe chart configuration
        chart_type = ChartType.CANDLESTICK
        line_style = LineStyle.SOLID
        marker_shape = MarkerShape.CIRCLE
        scale_mode = PriceScaleMode.LOGARITHMIC

    Using color classes::

        from lightweight_charts_pro.type_definitions import (
            BackgroundSolid,
            BackgroundGradient,
        )

        # Create solid background with validation
        solid_bg = BackgroundSolid(color="#ffffff")

        # Create gradient background
        gradient_bg = BackgroundGradient(
            top_color="#ffffff",
            bottom_color="#f0f0f0"
        )

    Using alignment enums::

        from lightweight_charts_pro.type_definitions import (
            HorzAlign,
            VertAlign,
        )

        # Configure text alignment
        horz_align = HorzAlign.CENTER
        vert_align = VertAlign.TOP

Note:
    All enums are designed to serialize correctly to JavaScript/JSON format
    for frontend compatibility. The enum values match the expected values
    in the TradingView Lightweight Charts library.

Version: 0.1.0
Author: Streamlit Lightweight Charts Contributors
License: MIT

"""

# ============================================================================
# Local Imports - Color classes
# ============================================================================
from lightweight_charts_pro.type_definitions.colors import (
    Background,
    BackgroundGradient,
    BackgroundSolid,
)

# ============================================================================
# Local Imports - Enumerations
# ============================================================================
# Type-safe enum definitions for chart configuration and styling
from lightweight_charts_pro.type_definitions.enums import (
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

__all__ = [
    # Enums
    "AnnotationPosition",
    "AnnotationType",
    # Colors
    "Background",
    "BackgroundGradient",
    "BackgroundSolid",
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
]
