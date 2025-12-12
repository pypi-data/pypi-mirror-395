"""
Component utilities for typed access to Lance data.

Uses existing Pydantic models from schema_proto for type-safe access.
"""

import datetime
from typing import Any, Dict


def _convert_timestamps_for_pydantic(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert datetime objects to int (microseconds) for Pydantic validation.

    PyArrow converts proto timestamps to datetime, but Pydantic expects int.
    """
    converted = {}
    for key, value in data.items():
        if isinstance(value, datetime.datetime):
            # Convert to microseconds (PyArrow timestamp[us])
            converted[key] = int(value.timestamp() * 1_000_000)
        else:
            converted[key] = value
    return converted


# Re-export Pydantic models from schema_proto
_MODELS = None
try:
    from avcloud.experimental.schema_proto.typed_models import (
        get_dataset_pydantic_models,
    )

    # Get all component models
    _MODELS = get_dataset_pydantic_models()

    # Wrap models to auto-convert timestamps
    if _MODELS:
        _original_models = dict(_MODELS)
        for name, model_cls in _original_models.items():
            # Create wrapper class that handles timestamp conversion
            def make_wrapper(original_cls):
                class WrappedModel(original_cls):
                    def __init__(self, **data):
                        converted_data = _convert_timestamps_for_pydantic(data)
                        super().__init__(**converted_data)

                WrappedModel.__name__ = original_cls.__name__
                WrappedModel.__module__ = original_cls.__module__
                return WrappedModel

            _MODELS[name] = make_wrapper(model_cls)

        # Export to module namespace
        globals().update(_MODELS)

except (ImportError, Exception):
    # Fallback if schema_proto not available
    _MODELS = None


class ComponentRow:
    """Simple wrapper for component row data.

    Provides attribute-style access to row fields.
    For basic use cases when you don't need full Pydantic validation.
    """

    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(f"No attribute '{name}'")
        return self._data.get(name)

    def __repr__(self) -> str:
        keys = list(self._data.keys())[:5]
        return f"ComponentRow(keys={keys}...)"

    def to_dict(self) -> Dict[str, Any]:
        """Get underlying dict."""
        return self._data


def from_dict(component_name: str, data: Dict[str, Any]) -> Any:
    """Create a component instance from a dictionary/table row.

    Uses Pydantic models from schema_proto if available, otherwise ComponentRow.

    Args:
        component_name: Name of component ('Camera', 'Lidar', etc.)
        data: Dictionary with component data (from table row)

    Returns:
        Pydantic model instance or ComponentRow

    Example:
        from avcloud.experimental.toolkit import read_component, components, from_dict

        # Read data
        table = read_component('/data', 'camera')

        # Option 1: Use components.Camera (recommended)
        for row in table.to_pylist():
            camera = components.Camera(**row)
            print(f"Scene: {camera.scene_id}")
            # Type-safe access to camera fields
            if camera.camera.front:
                print(f"Front camera data: {len(camera.camera.front)} bytes")

        # Option 2: Use from_dict (equivalent)
        row = table.to_pylist()[0]
        camera = from_dict('Camera', row)  # Same as components.Camera(**row)

        # Option 3: Simple ComponentRow for basic access
        row = ComponentRow(table.to_pylist()[0])
        print(row.scene_id)
    """
    # Try to use Pydantic model
    if _MODELS and component_name in _MODELS:
        model_cls = _MODELS[component_name]
        try:
            # Convert datetime to int (microseconds) for timestamp fields
            # PyArrow converts proto timestamps to datetime, but Pydantic expects int
            import datetime

            converted_data = {}
            for key, value in data.items():
                if isinstance(value, datetime.datetime):
                    # Convert to microseconds (PyArrow timestamp[us])
                    converted_data[key] = int(value.timestamp() * 1_000_000)
                else:
                    converted_data[key] = value

            return model_cls(**converted_data)
        except Exception:
            # Fall back to ComponentRow if validation fails
            pass

    # Fallback to simple dict wrapper
    return ComponentRow(data)


# Build __all__ dynamically
__all__ = ["from_dict", "ComponentRow"]
if _MODELS:
    __all__.extend(_MODELS.keys())
