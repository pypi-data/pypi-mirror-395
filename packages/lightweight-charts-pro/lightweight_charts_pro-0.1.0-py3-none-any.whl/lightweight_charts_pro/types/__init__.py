"""Type definitions for lightweight-charts-pro.

This module provides type definitions, base classes, and configuration structures
for the charting library. It includes the base Options class and comprehensive
type definitions for series configuration management.

The module serves as a central location for type definitions that are used
throughout the library for type safety, serialization, and configuration
management.

Key Components:
    Base Classes:
        - Options: Abstract base class for all option/configuration classes

    Series Configuration Types:
        - SeriesConfigChange: Represents configuration changes from frontend
        - SeriesConfigState: Complete series configuration state
        - SeriesConfiguration: Complete series configuration structure
        - SeriesStyleConfig: Style configuration for series
        - SeriesVisibilityConfig: Visibility configuration for series

    Type Aliases:
        - SeriesType: Literal type for chart series types
        - ConfigValue: Union type for configuration values
        - ConfigDict: Dictionary type for configuration data

Features:
    - Type-safe configuration with dataclass support
    - Automatic camelCase/snake_case conversion for frontend compatibility
    - Chainable API for fluent configuration
    - Dictionary serialization/deserialization support

Example Usage:
    Using base Options class::

        from lightweight_charts_pro.types import Options
        from dataclasses import dataclass

        @dataclass
        class MyOptions(Options):
            color: str = "#000000"
            width: int = 2

        opts = MyOptions(color="#FF0000")
        # Serialize to dict with camelCase keys
        data = opts.asdict()  # {"color": "#FF0000", "width": 2}

    Using series configuration types::

        from lightweight_charts_pro.types import (
            SeriesConfiguration,
            SeriesStyleConfig,
        )

        # Create style configuration
        style = SeriesStyleConfig(color="#FF0000", line_width=2)

        # Create complete configuration
        config = SeriesConfiguration(style=style)
        config_dict = config.asdict()

Version: 0.1.0
License: MIT

"""

# ============================================================================
# Local Imports - Base classes
# ============================================================================
from lightweight_charts_pro.types.options import Options

# ============================================================================
# Local Imports - Series configuration types
# ============================================================================
from lightweight_charts_pro.types.series_config_types import (
    ChartSeriesConfigs,
    CompleteSeriesConfigState,
    ConfigDict,
    ConfigValue,
    SeriesConfigBackendData,
    SeriesConfigChange,
    SeriesConfigChangesResult,
    SeriesConfigPersistenceOptions,
    SeriesConfigState,
    SeriesConfiguration,
    SeriesInputConfig,
    SeriesStyleConfig,
    SeriesType,
    SeriesVisibilityConfig,
)

__all__ = [
    "ChartSeriesConfigs",
    "CompleteSeriesConfigState",
    "ConfigDict",
    "ConfigValue",
    "Options",
    "SeriesConfigBackendData",
    "SeriesConfigChange",
    "SeriesConfigChangesResult",
    "SeriesConfigPersistenceOptions",
    "SeriesConfigState",
    "SeriesConfiguration",
    "SeriesInputConfig",
    "SeriesStyleConfig",
    "SeriesType",
    "SeriesVisibilityConfig",
]
