"""Wrapper for Java enum NIEnumRoiFormat.

This enum represents ROI formats (layout, selection, mask) used across the API.
It provides helpers to convert to/from the Java enum using the Py4J gateway.
"""

from enum import unique
from ...enum_wrapper import EnumWrapper


@unique
class NIEnumRoiFormat(EnumWrapper):
    """Python representation of Java NIEnumRoiFormat."""

    LAYOUT = "LAYOUT"
    SELECTION = "SELECTION"
    MASK = "MASK"

    def get_java_enum_class_path(self) -> str:
        """Get the Java enum class path."""
        return "agi.ndtkit.api.model.roi.NIRoi$NIEnumRoiFormat"
