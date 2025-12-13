"""Wrapper for Java enum NIEnumRoiFormat.

This enum represents ROI formats (layout, selection, mask) used across the API.
It provides helpers to convert to/from the Java enum using the Py4J gateway.
"""

from enum import Enum, unique
from typing import Any
from .ndtkit_socket_connection import gateway


@unique
class EnumWrapper(Enum):
    """Python representation of Java Enum."""

    def get_java_enum_class_path(self) -> str:
        """Get the Java enum class path.

        Override this method in subclasses to provide the correct Java enum class path.
        """
        raise NotImplementedError("Subclasses must implement get_java_enum_class_path method.")

    def to_java_enum(self) -> Any:
        """Return the corresponding Java enum instance.

        The generator tries several likely Java package locations for the enum class and
        returns the Java enum instance using valueOf(name).
        Raises RuntimeError if the Java enum class cannot be found via the gateway.
        """
        return gateway.jvm.Class.forName(self.get_java_enum_class_path()).getEnumConstants()[0].valueOf(self.value)

    @classmethod
    def from_java_enum(cls, java_enum):
        """Convert a Java NIEnumRoiFormat instance to the Python enum.

        Returns None if no matching Python enum is found.
        """
        try:
            java_name = str(java_enum.name())
            for member in cls:
                if member.value == java_name:
                    return member
            return None
        except Exception:
            return None
