"""Wrapper for Java enum ScanType from agi.ndtkit.api.model.frame.NICartographyFrame.

This enum represents different types of scans available in NDTKit.
"""

from enum import unique
from ...enum_wrapper import EnumWrapper


@unique
class ScanType(EnumWrapper):
    """Enumerate representing the type of scans.

    Corresponds to Java enum agi.ndtkit.api.model.frame.NICartographyFrame.ScanType.
    """

    C_SCAN = "C_SCAN"
    B_SCAN = "B_SCAN"
    A_SCAN = "A_SCAN"
    IMAGE = "IMAGE"
    C_SCAN_3D = "C_SCAN_3D"
    C_SCAN_SEGMENTATION = "C_SCAN_2D_SEGMENTATION"
    CUSTOM_SCAN = "CUSTOMIZED"

    def get_java_enum_class_path(self) -> str:
        return "agi.ndtkit.api.model.frame.NICartographyFrame$ScanType"
