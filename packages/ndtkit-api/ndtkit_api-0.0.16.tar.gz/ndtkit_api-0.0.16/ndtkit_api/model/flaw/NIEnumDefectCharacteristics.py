"""Python wrapper for agi.ndtkit.api.model.flaw.NIEnumDefectChacacteristics.

This enum maps the defect characteristics used by the API. It extends
EnumWrapper to provide conversion helpers between Python and Java enums.
"""
from enum import unique
from ndtkit_api.enum_wrapper import EnumWrapper


@unique
class NIEnumDefectCharacteristics(EnumWrapper):
    DEFECT_SURFACE = "DEFECT_SURFACE"
    OUTLINE_SURFACE = "OUTLINE_SURFACE"
    THETA = "THETA"
    OUTLINE_WIDTH = "OUTLINE_WIDTH"
    OUTLINE_LENGTH = "OUTLINE_LENGTH"
    AXIS_POSITIION = "AXIS_POSITIION"
    AXIS_3D_POSITIION = "AXIS_3D_POSITIION"
    AVERAGE_VALUE = "AVERAGE_VALUE"
    MAX_VALUE = "MAX_VALUE"
    MIN_VALUE = "MIN_VALUE"
    STANDARD_DEVIATION = "STANDARD_DEVIATION"
    INCREASING_COLOR_SURFACE = "INCREASING_COLOR_SURFACE"
    DECREASING_COLOR_SURFACE = "DECREASING_COLOR_SURFACE"
    DEFECT_LENGTH = "DEFECT_LENGTH"
    CAD_POSITION = "CAD_POSITION"
    LEVEL = "LEVEL"
    DEFECT_POSITION = "DEFECT_POSITION"
    DEFECT_HOLE_NUMBER = "DEFECT_HOLE_NUMBER"
    DEFECT_HOLE_DIAMETER = "DEFECT_HOLE_DIAMETER"
    DEFECT_HOLE_CRITERIA = "DEFECT_HOLE_CRITERIA"
    DEFECT_TYPE = "DEFECT_TYPE"
    MEDIAN_VALUE = "MEDIAN_VALUE"
    NOTE = "NOTE"
    DISTANCE_BETWEEN_GROUPED_DEFECTS = "DISTANCE_BETWEEN_GROUPED_DEFECTS"
    DISTANCE_FROM_BORDER = "DISTANCE_FROM_BORDER"
    OVERTHICKNESS_MIN = "OVERTHICKNESS_MIN"
    OVERTHICKNESS_MAX = "OVERTHICKNESS_MAX"
    OVERTHICKNESS_MEDIAN = "OVERTHICKNESS_MEDIAN"
    OVERTHICKNESS_MEAN = "OVERTHICKNESS_MEAN"
    NAME = "NAME"

    def get_java_enum_class_path(self) -> str:
        return "agi.ndtkit.api.model.flaw.NIEnumDefectChacacteristics"

    def get_ndtkit_enum_value(self):
        """Return the underlying Java DefectsTableCharacteristics enum value."""
        java_enum = self.to_java_enum()
        return java_enum.getNdtkitEnumValue() if java_enum is not None else None
