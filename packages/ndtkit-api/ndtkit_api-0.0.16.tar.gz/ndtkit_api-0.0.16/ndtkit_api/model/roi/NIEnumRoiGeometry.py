"""Wrapper for Java enum NIEnumRoiGeometry defined inside agi.ndtkit.api.model.roi.NIRoi.

Values mirror Java enum: RECTANGLE, POLYGON, LINE2D, ELLIPSOIDAL, CIRCULAR.
"""

from enum import unique
from ...enum_wrapper import EnumWrapper


@unique
class NIEnumRoiGeometry(EnumWrapper):
    """Python wrapper for agi.ndtkit.api.model.roi.NIRoi.NIEnumRoiGeometry."""

    RECTANGLE = "RECTANGLE"
    POLYGON = "POLYGON"
    LINE2D = "LINE2D"
    ELLIPSOIDAL = "ELLIPSOIDAL"
    CIRCULAR = "CIRCULAR"

    def get_java_enum_class_path(self) -> str:
        # Nested enum inside NIRoi class; use $ to access nested class via Py4J
        return "agi.ndtkit.api.model.roi.NIRoi$NIEnumRoiGeometry"
