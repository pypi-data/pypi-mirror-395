"""Wrapper for Java NIRoi class.

Provides convenient access to common NIRoi operations used across the API.
"""
from py4j.java_gateway import JavaObject
from typing import Any, Optional
from .Shape import Shape


class NIRoi:
    """Python wrapper for agi.ndtkit.api.model.roi.NIRoi Java class."""

    def __init__(self, java_object: JavaObject):
        self._java_object = java_object

    def get_shape(self) -> Optional[Shape]:
        """Return a Shape wrapper for this ROI's shape."""
        try:
            java_shape = self._java_object.getShape()
            return None if not java_shape else Shape(java_shape)
        except Exception:
            return None

    def set_shape(self, shape: Any) -> None:
        """Set the underlying shape. Accepts a Shape wrapper or a Java shape object."""
        if hasattr(shape, '_java_object'):
            self._java_object.setShape(shape._java_object)
        else:
            self._java_object.setShape(shape)

    def get_name(self) -> str:
        """Return the ROI layout name (or empty string)."""
        return self._java_object.getName()

    def set_name(self, name: str) -> None:
        """Set the ROI layout name."""
        self._java_object.setName(name)

    def get_level(self) -> int:
        """Return the selection level of the ROI."""
        return self._java_object.getLevel()

    def set_level(self, level: int) -> None:
        """Set the selection level of the ROI."""
        self._java_object.setLevel(level)

    def get_creation_resolution_x(self) -> float:
        """Return the X creation resolution for this ROI."""
        return float(self._java_object.getCreationResolutionX())

    def get_creation_resolution_y(self) -> float:
        """Return the Y creation resolution for this ROI."""
        return float(self._java_object.getCreationResolutionY())

    def delete(self, frame: Any) -> None:
        """Delete this ROI from the given NICartographyFrame.

        `frame` can be a NICartographyFrame wrapper (has _java_object) or the Java object itself.
        """
        target = getattr(frame, '_java_object', frame)
        self._java_object.delete(target)

    def is_selected(self) -> bool:
        """Return whether the ROI is selected."""
        return bool(self._java_object.isSelected())

    def set_selected(self, selected: bool) -> None:
        """Select/unselect this ROI."""
        self._java_object.setSelected(selected)

    def get_angle(self) -> float:
        """Return the ROI angle."""
        return float(self._java_object.getAngle())
