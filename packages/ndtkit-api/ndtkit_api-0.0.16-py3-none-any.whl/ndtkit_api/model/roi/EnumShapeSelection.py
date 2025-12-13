"""Wrapper for Java enum EnumShapeSelection defined in NDTKitROIInterface.

Represents selection mode when retrieving shapes: ONLY_SELECTED or ALL.
"""

from enum import unique
from ...enum_wrapper import EnumWrapper


@unique
class EnumShapeSelection(EnumWrapper):
    """Python wrapper for agi.ndtkit.api.NDTKitROIInterface.EnumShapeSelection."""

    ONLY_SELECTED = "ONLY_SELECTED"
    ALL = "ALL"

    def get_java_enum_class_path(self) -> str:
        return "agi.ndtkit.api.NDTKitROIInterface$EnumShapeSelection"
