"""Utilities for Streamlit Lightweight Charts Pro.

This module provides utility functions and decorators that enhance the functionality
of the charting library. It includes tools for method chaining, data processing,
and other common operations used throughout the package.

The module exports:
    - chainable_property: Decorator for creating chainable properties
    - chainable_field: Decorator for creating chainable fields

These utilities enable the fluent API design pattern used throughout the library,
allowing for intuitive method chaining when building charts and configuring options.

Example Usage:
    ```python
    from lightweight_charts_pro.utils import chainable_property, chainable_field


    class ChartConfig:
        @chainable_property
        def height(self, value: int):
            self._height = value
            return self

        @chainable_field
        def width(self):
            return self._width
    ```

Note:
    Trade visualization utilities have been moved to frontend plugins to avoid
    circular imports with the options module. The functionality is still available
    but accessed directly from the relevant modules when needed.

Version: 0.1.0
Author: Streamlit Lightweight Charts Contributors
License: MIT

"""

# ============================================================================
# Local Imports
# ============================================================================
# Case conversion utilities for snake_case <-> camelCase transformations
from .case_converter import CaseConverter, camel_to_snake, snake_to_camel

# Chainable decorators for fluent API design
from .chainable import chainable_field, chainable_property, validated_field

# Color manipulation and validation utilities
from .color_utils import add_opacity, hex_to_rgba, is_hex_color

# Data processing and validation utilities
from .data_utils import is_valid_color, normalize_time

# Serialization utilities for converting Python objects to JavaScript-compatible dicts
from .serialization import (
    DEFAULT_CONFIG,
    SerializableMixin,
    SerializationConfig,
    SimpleSerializableMixin,
)

# Trade visualization utilities have been removed - functionality is handled by frontend plugins
# to avoid circular imports with the options module

__all__ = [
    "CaseConverter",
    "DEFAULT_CONFIG",
    "SerializableMixin",
    "SerializationConfig",
    "SimpleSerializableMixin",
    "add_opacity",
    "camel_to_snake",
    "chainable_field",
    "chainable_property",
    "hex_to_rgba",
    "is_hex_color",
    "is_valid_color",
    "normalize_time",
    "snake_to_camel",
    "validated_field",
]
