"""Wrapper for Java class NDTKitBScansInterface from package agi.ndtkit.api.

This module provides static methods for processing and generating B/D-Scans.
All methods wrap the corresponding Java API functionality and preserve documentation.
"""

from .ndtkit_socket_connection import gateway
from .model.frame.NICartographyFrameCScan import NICartographyFrameCScan


def generate_bscan(cscan: NICartographyFrameCScan | None = None) -> None:
    """Generate a B-Scan from the current selected C-Scan or the one provided as an argument.

    This function requires that conditions for generating a B-Scan are met:
    - An A-Scan must be present in NDTkit
    - An associated C-Scan must be present and selected

    Raises:
        Exception: if an error occurs (no A-Scan, no C-Scan, or problem generating B-Scan)
    """
    if cscan:
        gateway.jvm.agi.ndtkit.api.NDTKitBScansInterface.generateBScan(cscan._java_object)  # type: ignore
    else:
        gateway.jvm.agi.ndtkit.api.NDTKitBScansInterface.generateBScan()  # type: ignore


def generate_dscan(cscan: NICartographyFrameCScan | None = None) -> None:
    """Generate a B-Scan from the current selected C-Scan or the one provided as an argument.

    This function requires that conditions for generating a D-Scan are met:
    - An A-Scan must be present in NDTkit
    - An associated C-Scan must be present and selected

    Raises:
        Exception: if an error occurs (no A-Scan, no C-Scan, or problem generating D-Scan)
    """
    if cscan:
        gateway.jvm.agi.ndtkit.api.NDTKitBScansInterface.generateDScan(cscan._java_object)  # type: ignore
    else:
        gateway.jvm.agi.ndtkit.api.NDTKitBScansInterface.generateDScan()  # type: ignore
