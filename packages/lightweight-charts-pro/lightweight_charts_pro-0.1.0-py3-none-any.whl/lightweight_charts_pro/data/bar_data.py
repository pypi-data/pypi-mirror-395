"""Bar chart data model for streamlit-lightweight-charts.

This module provides the BarData class for representing individual bar chart
data points with OHLC (Open, High, Low, Close) values and optional color
customization.

The BarData class extends OhlcData to provide bar-specific functionality
while maintaining compatibility with the OHLC data structure used throughout
the charting library.

Example:
    ```python
    from lightweight_charts_pro.data import BarData

    # Create a bar data point
    bar = BarData(
        time="2024-01-01",
        open=100.0,
        high=105.0,
        low=98.0,
        close=103.0,
        color="#4CAF50",  # Optional: Green bar
    )
    ```

"""

# Standard Imports
from dataclasses import dataclass
from typing import ClassVar

# Local Imports
from lightweight_charts_pro.data.ohlc_data import OhlcData
from lightweight_charts_pro.utils import validated_field


@dataclass
@validated_field("color", str, validator="color", allow_none=True)
class BarData(OhlcData):
    """Data class for a bar chart data point with OHLC values.

    Represents a single bar in a bar chart with Open, High, Low, and Close prices.
    Inherits from OhlcData and adds an optional color field for customizing
    individual bar colors.

    Bar charts display OHLC data as vertical bars where:
        - The bar height spans from low to high
        - A tick mark on the left indicates the open price
        - A tick mark on the right indicates the close price

    Attributes:
        time (int | str | datetime): UNIX timestamp in seconds, ISO string, or datetime.
            Automatically normalized to UNIX timestamp.
        open (float): Opening price for this bar. Required.
        high (float): Highest price for this bar. Required.
        low (float): Lowest price for this bar. Required.
        close (float): Closing price for this bar. Required.
        color (str | None): Optional color override for this specific bar.
            Accepts hex colors (e.g., "#2196F3") or rgba strings
            (e.g., "rgba(33, 150, 243, 1)"). If None, uses series default color.

    Example:
        Create bar data with custom color::

            bar = BarData(
                time="2024-01-01T09:30:00",
                open=100.0,
                high=105.0,
                low=98.0,
                close=103.0,
                color="#4CAF50"  # Green for bullish bar
            )

        Create bar data with default color::

            bar = BarData(
                time=1704067200,
                open=100.0,
                high=102.0,
                low=99.0,
                close=101.0
                # color not specified - uses series default
            )

    See Also:
        - OhlcData: Parent class with OHLC data structure
        - CandlestickData: Similar but for candlestick charts
        - HistogramData: For volume/histogram bars

    Note:
        Color validation is performed automatically via the validated_field
        decorator. Invalid color formats will raise a ColorValidationError
        during instantiation.

    """

    REQUIRED_COLUMNS: ClassVar[set] = set()
    OPTIONAL_COLUMNS: ClassVar[set] = {"color"}

    color: str | None = None
