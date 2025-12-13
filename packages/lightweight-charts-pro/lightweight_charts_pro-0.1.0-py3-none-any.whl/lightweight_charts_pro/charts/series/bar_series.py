"""Bar series for streamlit-lightweight-charts.

This module provides the BarSeries class for creating bar charts that display
OHLC (Open, High, Low, Close) data as bars. Bar series are commonly used for
displaying price data with visible open/close markers on vertical bars.

The BarSeries class supports various styling options including up/down bar colors,
open price visibility, thin bar mode, and animation effects. It also supports
markers and price line configurations.

Key Features:
    - OHLC bar visualization with tick marks for open/close
    - Customizable up/down colors for bullish/bearish bars
    - Optional open price visibility
    - Thin bar mode for compact visualization
    - Support for colored individual bars
    - Markers and price lines support

Example:
    Basic bar series with OHLC data::

        from lightweight_charts_pro.charts.series import BarSeries
        from lightweight_charts_pro.data import BarData

        # Create OHLC bar data
        data = [
            BarData(
                time="2024-01-01",
                open=100.0,
                high=105.0,
                low=98.0,
                close=103.0
            ),
            BarData(
                time="2024-01-02",
                open=103.0,
                high=108.0,
                low=102.0,
                close=106.0
            )
        ]

        # Create bar series with custom styling
        series = BarSeries(data=data)
        series.up_color = "#26a69a"    # Green for bullish bars
        series.down_color = "#ef5350"  # Red for bearish bars
        series.open_visible = True     # Show open price ticks
        series.thin_bars = False       # Use regular width bars

Version: 0.1.0
Author: Streamlit Lightweight Charts Contributors
License: MIT

"""

# Standard Imports
import pandas as pd

# Local Imports
from lightweight_charts_pro.charts.series.base import Series
from lightweight_charts_pro.data import BarData
from lightweight_charts_pro.type_definitions import ChartType
from lightweight_charts_pro.utils import chainable_property


@chainable_property("up_color", str, validator="color")
@chainable_property("down_color", str, validator="color")
@chainable_property("open_visible", bool)
@chainable_property("thin_bars", bool)
class BarSeries(Series):
    """Bar series for lightweight charts.

    This class represents a bar series that displays data as bars.
    It's commonly used for price charts, volume overlays, and other
    bar-based visualizations.

    The BarSeries supports various styling options including bar colors,
    base value, and animation effects.

    Attributes:
        color: Color of the bars (set via property).
        base: Base value for the bars (set via property).
        up_color: Color for up bars (set via property).
        down_color: Color for down bars (set via property).
        open_visible: Whether open values are visible (set via property).
        thin_bars: Whether to use thin bars (set via property).
        price_lines: List of PriceLineOptions for price lines (set after construction)
        price_format: PriceFormatOptions for price formatting (set after construction)
        markers: List of markers to display on this series (set after construction)

    """

    DATA_CLASS = BarData

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.BAR

    def __init__(
        self,
        data: list[BarData] | pd.DataFrame | pd.Series,
        column_mapping: dict | None = None,
        visible: bool = True,
        price_scale_id: str = "right",
        pane_id: int | None = 0,
    ):
        """Initialize a bar series with the given data and configuration.

        Args:
            data: Bar data as list, DataFrame, or Series.
            column_mapping: Optional mapping of column names.
            visible: Whether the series is initially visible.
            price_scale_id: ID of the price scale to use.
            pane_id: ID of the pane to display the series in.

        """
        super().__init__(
            data=data,
            column_mapping=column_mapping,
            visible=visible,
            price_scale_id=price_scale_id,
            pane_id=pane_id,
        )

        # Initialize properties with default values
        self._up_color = "#26a69a"
        self._down_color = "#ef5350"
        self._open_visible = True
        self._thin_bars = True
