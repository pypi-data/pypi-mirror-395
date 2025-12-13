"""Python wrapper for Java enum NIEnumDefectShapeType.

This enum maps the defect shape fitting types used by the API. It extends
EnumWrapper to provide conversion helpers between Python and Java enums.
"""
from enum import unique
from ..enum_wrapper import EnumWrapper


@unique
class NIEnumDefectShapeType(EnumWrapper):
    """Python representation of Java NIEnumDefectShapeType."""

    RECTANGLE_FITTING = "RECTANGLE_FITTING"
    CIRCLE_FITTING = "CIRCLE_FITTING"
    ELLIPSE_FITTING = "ELLIPSE_FITTING"
    RECTANGLE_LENGTH_FITTING = "RECTANGLE_LENGTH_FITTING"
    CONVEX_HULL = "CONVEX_HULL"
    EDGE = "EDGE"

    def get_java_enum_class_path(self) -> str:
        """Return the Java enum class path for NIEnumDefectShapeType."""
        return "agi.ndtkit.api.model.NIEnumDefectShapeType"
