"""Wrapper for Java class NDTKitDimensionInterface from package agi.ndtkit.api.

This module provides static methods for managing dimensions shapes (lines with arrows
for measuring things over a C/B/D- Scan).
All methods wrap the corresponding Java API functionality and preserve documentation.
"""

from .ndtkit_socket_connection import gateway
from .model.frame.NICartographyFrameCScan import NICartographyFrameCScan


def delete_all_dimensions(frame: NICartographyFrameCScan) -> None:
    """Delete all dimensions displayed on the given frame, even if not selected.

    Args:
        frame: The frame on which dimensions will be erased.
    """
    gateway.jvm.agi.ndtkit.api.NDTKitDimensionInterface.deleteAllDimensions(frame._java_object)  # type: ignore


def add_dimension(
    frame: NICartographyFrameCScan,
    p1: tuple[float, float],
    p2: tuple[float, float],
    color: tuple[int, int, int] | None = None
) -> None:
    """Add an arrow showing the dimension over the current canvas of the given frame.

    If a color is provided, a colored arrow is added.
    Otherwise, a default arrow is added (which may throw an exception).

    Args:
        frame: The frame where the arrow must be drawn.
        p1: The first point (x, y) of the arrow.
        p2: The second point (x, y) of the arrow.
        color: An optional (R, G, B) tuple for the arrow's color.
               Values should be between 0 and 255.

    Raises:
        Exception: if an error occurs while drawing the arrow (as per the Java API,
                   this is specified for the non-colored version).
    """
    # Instantiate Java Point2D objects from Python tuples
    java_p1 = gateway.jvm.java.awt.geom.Point2D.Double(float(p1[0]), float(p1[1]))  # type: ignore
    java_p2 = gateway.jvm.java.awt.geom.Point2D.Double(float(p2[0]), float(p2[1]))  # type: ignore

    if color:
        # Call the overloaded Java method for colored dimensions
        # Instantiate Java Color object from Python tuple
        java_color = gateway.jvm.java.awt.Color(color[0], color[1], color[2])  # type: ignore
        gateway.jvm.agi.ndtkit.api.NDTKitDimensionInterface.addDimension(  # type: ignore
            frame._java_object, java_p1, java_p2, java_color
        )
    else:
        # Call the base Java method for dimensions
        # This one is declared to throw NIApiException
        gateway.jvm.agi.ndtkit.api.NDTKitDimensionInterface.addDimension(  # type: ignore
            frame._java_object, java_p1, java_p2
        )
