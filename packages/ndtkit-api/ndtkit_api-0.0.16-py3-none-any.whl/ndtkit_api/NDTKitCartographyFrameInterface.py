"""Wrapper for Java class NDTKitCartographyFrameInterface from package agi.ndtkit.api.

This module provides static methods that wrap the Java API functionality.
Methods preserve Java documentation and handle type conversion.
"""

from typing import Any, List
from .ndtkit_socket_connection import gateway
from .model.frame.ScanType import ScanType
from .model.frame.NICartographyFrame import NICartographyFrame


@staticmethod
def get_all_cartographies(frame_type: ScanType) -> List[NICartographyFrame]:
    """Get all cartography displayed in main frame of given scan type {@link ScanType}.

    Args:
        frame_type: frame type ( c-scan, a-scan ... )

    Returns:
        list of cartographies.
    """
    all_cartographies = gateway.jvm.agi.ndtkit.api.NDTKitCartographyFrameInterface.getAllCartographies(frame_type.to_java_enum())
    return [] if not all_cartographies else [NICartographyFrame(frame) for frame in all_cartographies]


@staticmethod
def get_report_c_scan_frame_or_current_selected_c_scan_frame() -> NICartographyFrame | None:
    """Return current selected frame.

    Returns:
        NICartographyFrame frame cartography.

    Raises:
        NIApiException: if an error occurs.
    """
    java_object = gateway.jvm.agi.ndtkit.api.NDTKitCartographyFrameInterface.getReportCScanFrameOrCurrentSelectedCScanFrame()
    return None if not java_object else NICartographyFrame(java_object)  # type: ignore


@staticmethod
def get_report_frame_or_current_selected_frame(id_report_scan: str = "") -> NICartographyFrame | None:
    """Return current selected frame if, display a chooser if no frame is selected.

    Returns:
        frame cartography.

    Raises:
        NIApiException: if an error occurs.
    """
    if id_report_scan:
        java_object = gateway.jvm.agi.ndtkit.api.NDTKitCartographyFrameInterface.getReportFrameOrCurrentSelectedFrame(id_report_scan)  # type: ignore
    else:
        java_object = gateway.jvm.agi.ndtkit.api.NDTKitCartographyFrameInterface.getReportFrameOrCurrentSelectedFrame()  # type: ignore
    return None if not java_object else NICartographyFrame(java_object)  # type: ignore


@staticmethod
def get_current_selected_frame() -> NICartographyFrame | None:
    """Returns the current selected frame.

    If no frame is selected return null.
    Does not take automation into account.

    Returns:
        the selected frame.
    """
    java_object = gateway.jvm.agi.ndtkit.api.NDTKitCartographyFrameInterface.getCurrentSelectedFrame()  # type: ignore
    return None if not java_object else NICartographyFrame(java_object)  # type: ignore


@staticmethod
def get_frame(uuid_to_found: str, type: ScanType) -> NICartographyFrame | None:
    """Returns the current selected frame.

    If no frame is selected return null.
    Does not take automation into account.

    Returns:
        the selected frame.
    """
    java_object = gateway.jvm.agi.ndtkit.api.NDTKitCartographyFrameInterface.getFrame(uuid_to_found, type.to_java_enum())  # type: ignore
    return None if not java_object else NICartographyFrame(java_object)  # type: ignore


@staticmethod
def get_api_version() -> str:
    """Get the version of the integrated API.

    Returns:
        the version of the API.
    """
    return gateway.jvm.agi.ndtkit.api.NDTKitCartographyFrameInterface.getApiVersion()  # type: ignore


@staticmethod
def close_all_frames() -> None:
    """Close all internal frames displayed.

    Raises:
        NIApiException: if an error occurs when closing all frames.
    """
    return gateway.jvm.agi.ndtkit.api.NDTKitCartographyFrameInterface.closeAllFrames()  # type: ignore


@staticmethod
def close_frame(frame_title: str) -> None:
    """Close a frame thanks to its title.

    Raises:
        NIApiException: if an error occurs when closing the frame.
    """
    return gateway.jvm.agi.ndtkit.api.NDTKitCartographyFrameInterface.closeFrame(frame_title)  # type: ignore


@staticmethod
def get_main_ndt_kit_frame() -> Any:
    """Returns the whole software application (can be useful to place a dialog thanks to this Window).
    """
    return gateway.jvm.agi.ndtkit.api.NDTKitCartographyFrameInterface.getMainNDTKitFrame()  # type: ignore
