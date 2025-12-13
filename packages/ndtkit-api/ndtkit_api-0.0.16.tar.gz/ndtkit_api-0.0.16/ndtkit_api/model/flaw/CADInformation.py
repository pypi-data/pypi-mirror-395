"""Python wrapper for com.agi.db.partacquisition.model.CADInformation.

This wrapper exposes the common getters/setters and converts Java
Point3d objects to Python (x, y, z) tuples for convenience. Setting the
contour or center accepts Python tuples/lists and constructs the proper
Java objects through the Py4J gateway.
"""
from typing import List, Optional, Tuple
from py4j.java_gateway import JavaObject
from ...ndtkit_socket_connection import gateway


class CADInformation:
    """Wrapper for com.agi.db.partacquisition.model.CADInformation."""

    def __init__(self, java_object: JavaObject):
        self._java_object = java_object

    def get_id(self) -> Optional[int]:
        v = self._java_object.getId()
        return None if v is None else int(v)

    def set_id(self, id_value: int) -> None:
        self._java_object.setId(id_value)

    # Contour (List[Point3d] <-> List[tuple])
    def get_contour(self) -> List[Tuple[float, float, float]]:
        """Return the contour as a list of (x, y, z) tuples."""
        java_list = self._java_object.getContour()
        if java_list is None:
            return []
        return [(float(p.x), float(p.y), float(p.z)) for p in java_list]

    def set_contour(self, points: List[Tuple[float, float, float]]) -> None:
        """Accept a list of (x, y, z) tuples and set the Java contour list."""
        java_list = gateway.jvm.java.util.ArrayList()
        for p in points:
            x, y, z = float(p[0]), float(p[1]), float(p[2])
            java_point = gateway.jvm.org.jogamp.vecmath.Point3d(x, y, z)
            java_list.add(java_point)
        self._java_object.setContour(java_list)

    # Centers and file path
    def get_x_center(self) -> float:
        return float(self._java_object.getxCenter())

    def set_x_center(self, v: float) -> None:
        self._java_object.setxCenter(v)

    def get_y_center(self) -> float:
        return float(self._java_object.getyCenter())

    def set_y_center(self, v: float) -> None:
        self._java_object.setyCenter(v)

    def get_z_center(self) -> float:
        return float(self._java_object.getzCenter())

    def set_z_center(self, v: float) -> None:
        self._java_object.setzCenter(v)

    def get_center(self) -> Optional[Tuple[float, float, float]]:
        """Return the center as (x, y, z) tuple or None if not set."""
        java_pt = self._java_object.getCenter()
        return (float(java_pt.x), float(java_pt.y), float(java_pt.z)) if java_pt else None

    def set_center(self, p: Tuple[float, float, float]) -> None:
        self._java_object.setxCenter(float(p[0]))
        self._java_object.setyCenter(float(p[1]))
        self._java_object.setzCenter(float(p[2]))

    def get_filepathname(self) -> Optional[str]:
        return self._java_object.getFilepathname()

    def set_filepathname(self, path: str) -> None:
        self._java_object.setFilepathname(path)
