"""Base options class for lightweight-charts-pro.

This module provides the base Options class that serves as the foundation for all
configuration and option classes throughout the library. It provides common
functionality for serialization, deserialization, and dictionary conversion.

The Options class integrates serialization capabilities with abstract base class
functionality to create a consistent interface for all configuration objects.

Features:
    - Automatic camelCase key conversion for frontend compatibility
    - Dictionary serialization via asdict() method
    - Dictionary deserialization via fromdict() class method
    - Configuration updates via update() method
    - Integration with SerializableMixin for consistent serialization

Example:
    Creating a custom options class::

        from dataclasses import dataclass
        from lightweight_charts_pro.types import Options

        @dataclass
        class ChartLayoutOptions(Options):
            background_color: str = "#FFFFFF"
            text_color: str = "#000000"
            font_size: int = 12

        # Create instance
        opts = ChartLayoutOptions(background_color="#F0F0F0")

        # Serialize to dict with camelCase keys
        data = opts.asdict()
        # Result: {"backgroundColor": "#F0F0F0", "textColor": "#000000", "fontSize": 12}

        # Update from dict
        opts.update({"backgroundColor": "#FFFFFF"})

        # Create from dict
        new_opts = ChartLayoutOptions.fromdict({"backgroundColor": "#E0E0E0"})

Version: 0.1.0
License: MIT

"""

# Standard Imports
from abc import ABC
from dataclasses import dataclass, fields
from typing import Any

# Local Imports
from lightweight_charts_pro.utils.case_converter import CaseConverter
from lightweight_charts_pro.utils.serialization import SerializableMixin


@dataclass
class Options(SerializableMixin, ABC):
    """Abstract base class for all option and configuration classes.

    This class provides a consistent interface for all configuration objects
    in the library. It combines serialization capabilities from SerializableMixin
    with abstract base class functionality to create reusable configuration
    objects that can be easily converted to/from dictionaries.

    The class handles:
        - Serialization to JavaScript-compatible dictionaries with camelCase keys
        - Deserialization from dictionaries with either camelCase or snake_case keys
        - Updates from partial configuration dictionaries
        - Integration with dataclass functionality

    All configuration classes in the library should inherit from this base class
    to ensure consistent behavior across different option types (chart options,
    series options, layout options, etc.).

    Example:
        Creating a custom options subclass::

            from dataclasses import dataclass
            from lightweight_charts_pro.types.options import Options

            @dataclass
            class PriceLineOptions(Options):
                color: str = "#FF0000"
                line_width: int = 2
                line_visible: bool = True

            # Use the options
            opts = PriceLineOptions(color="#00FF00")
            opts_dict = opts.asdict()  # {"color": "#00FF00", "lineWidth": 2, ...}

    Note:
        This is an abstract base class and should not be instantiated directly.
        Always create concrete subclasses for specific configuration needs.

    """

    def asdict(self) -> dict[str, Any]:
        """Serialize the options to a dictionary with camelCase keys.

        Converts the options object to a dictionary suitable for frontend
        consumption. All keys are automatically converted from snake_case
        to camelCase, and all values are processed for JavaScript compatibility
        (enums converted to values, NaN to zero, etc.).

        Returns:
            dict[str, Any]: Dictionary representation with camelCase keys.
                The dictionary is ready for JSON serialization and frontend use.

        Example:
            >>> @dataclass
            ... class MyOptions(Options):
            ...     background_color: str = "#FFFFFF"
            ...     line_width: int = 2
            >>> opts = MyOptions()
            >>> opts.asdict()
            {'backgroundColor': '#FFFFFF', 'lineWidth': 2}

        """
        return self._serialize_to_dict()

    def update(self, config: dict[str, Any]) -> "Options":
        """Update options from a configuration dictionary.

        Updates the current options instance with values from the provided
        dictionary. Supports both camelCase (from frontend) and snake_case
        (from Python code) keys. Only updates attributes that exist on the
        options object.

        This method is useful for applying partial configuration updates
        without creating a new instance.

        Args:
            config (dict[str, Any]): Configuration dictionary with option
                values. Keys can be in either camelCase or snake_case format.
                Only keys matching existing attributes will be applied.

        Returns:
            Options: Self reference for method chaining.

        Example:
            >>> opts = MyOptions(color="#FF0000", width=2)
            >>> opts.update({"color": "#00FF00"})  # Returns opts
            >>> opts.update({"lineWidth": 3})  # camelCase also works
            >>> opts.color
            '#00FF00'

        Note:
            Keys that don't match any attribute are silently ignored.
            This allows for flexible partial updates without errors.

        """
        # Convert camelCase keys to snake_case for attribute lookup
        # This ensures both frontend (camelCase) and Python (snake_case)
        # formats work correctly
        snake_config = CaseConverter.convert_dict_keys(config, to_camel=False)

        # Iterate through each key-value pair in the converted config
        for key, value in snake_config.items():
            # Only update attributes that exist on this instance
            # This prevents setting arbitrary attributes
            if hasattr(self, key):
                setattr(self, key, value)

        # Return self to enable method chaining
        return self

    @classmethod
    def fromdict(cls, data: dict[str, Any]) -> "Options":
        """Create a new options instance from a dictionary.

        Factory method that creates a new instance of the options class
        from a dictionary. Handles both camelCase and snake_case keys,
        and filters out keys that don't correspond to class fields.

        This is the primary way to deserialize options objects from
        frontend data or stored configurations.

        Args:
            data (dict[str, Any]): Dictionary containing option values.
                Keys can be in either camelCase (from JavaScript) or
                snake_case (from Python). Only keys matching class fields
                will be used.

        Returns:
            Options: New instance of the options class with values from
                the dictionary. Fields not present in the dictionary will
                use their default values.

        Example:
            >>> data = {"backgroundColor": "#FFFFFF", "lineWidth": 2}
            >>> opts = MyOptions.fromdict(data)
            >>> opts.background_color
            '#FFFFFF'
            >>> opts.line_width
            2

        Note:
            Invalid keys (not matching class fields) are silently ignored.
            This allows for flexible deserialization of partial data.

        """
        # Convert camelCase keys from frontend to snake_case for Python
        # This ensures consistent attribute naming regardless of input format
        snake_data = CaseConverter.convert_dict_keys(data, to_camel=False)

        # Get the set of valid field names from the dataclass definition
        # This ensures we only use keys that correspond to actual fields
        valid_fields = {f.name for f in fields(cls)}

        # Filter the input data to only include valid fields
        # This prevents TypeError from unexpected kwargs during instantiation
        filtered_data = {k: v for k, v in snake_data.items() if k in valid_fields}

        # Create and return a new instance with the filtered data
        return cls(**filtered_data)
