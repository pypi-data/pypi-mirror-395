"""Python wrapper for Java com.agi.db.partacquisition.model.DefectGeometricInfos.

This wrapper mirrors the Java API and exposes common getters/setters in a
Pythonic snake_case form. Complex objects (Matrix, Point3d, BooleanMember,
CADInformation) are returned as raw Java objects so callers can wrap them
with dedicated wrappers if/when available.
"""
from typing import List, Optional
from py4j.java_gateway import JavaObject
from ...ndtkit_socket_connection import gateway
from .BooleanMember import BooleanMember
from .CADInformation import CADInformation


class DefectGeometricInfos:
    """Thin wrapper around com.agi.db.partacquisition.model.DefectGeometricInfos."""

    def __init__(self, java_object: JavaObject):
        self._java_object = java_object

    def get_id(self) -> Optional[int]:
        v = self._java_object.getId()
        return None if v is None else int(v)

    def set_id(self, id_value: int) -> None:
        self._java_object.setId(id_value)

    # Dimensions
    def get_width(self) -> float:
        return float(self._java_object.getWidth())

    def set_width(self, w: float) -> None:
        self._java_object.setWidth(w)

    def get_height(self) -> float:
        return float(self._java_object.getHeight())

    def set_height(self, h: float) -> None:
        self._java_object.setHeight(h)

    def get_theta(self) -> float:
        return float(self._java_object.getTheta())

    def set_theta(self, theta: float) -> None:
        self._java_object.setTheta(theta)

    def get_real_defect_area(self) -> float:
        return float(self._java_object.getRealDefectArea())

    def set_real_defect_area(self, area: float) -> None:
        self._java_object.setRealDefectArea(area)

    # Convex hull / contour
    def get_convex_hull_points(self) -> List[List[float]]:
        """Return the Java Matrix representing convex hull points."""
        return self._java_object.getConvexHullPoints().getArray()

    def set_convex_hull_points(self, matrix: List[List[float]]) -> None:
        java_matrix = gateway.jvm.com.agi.ndtkit.common.math.Matrix(matrix)
        self._java_object.setConvexHullPoints(java_matrix)

    def get_contour3d(self) -> List[tuple]:
        """Return the 3D contour points as a list of (x, y, z) tuples."""
        vals = self._java_object.getContour3d()
        if vals is None:
            return []
        return [(float(pt.x), float(pt.y), float(pt.z)) for pt in vals]

    def set_contour3d(self, points: List[tuple]) -> None:
        java_points_list = gateway.jvm.java.util.ArrayList()
        for p in points:
            java_points_list.add(gateway.jvm.org.jogamp.vecmath.Point3d(float(p[0]), float(p[1]), float(p[2])))
        self._java_object.setContour3d(java_points_list)

    # 3D center
    def get_center3d(self) -> Optional[tuple]:
        """Return the Java Point3d object or None if not set."""
        java_point3d = self._java_object.getCenter3D()
        return (float(java_point3d.x), float(java_point3d.y), float(java_point3d.z)) if java_point3d else None

    def set_center3d(self, p: tuple) -> None:
        java_point3d = gateway.jvm.org.jogamp.vecmath.Point3d(float(p[0]), float(p[1]), float(p[2]))
        self._java_object.setCenter3D(java_point3d)

    # Pixels scheme (BooleanMember)
    def get_pixels_scheme(self) -> BooleanMember:
        return BooleanMember(self._java_object.getPixelsScheme())

    def set_pixels_scheme(self, scheme: BooleanMember) -> None:
        target = getattr(scheme, '_java_object', scheme)
        self._java_object.setPixelsScheme(target)

    # individual x/y/z centers for 3D
    def get_x_center3d(self) -> float:
        return float(self._java_object.getxCenter3D())

    def set_x_center3d(self, v: float) -> None:
        self._java_object.setxCenter3D(v)

    def get_y_center3d(self) -> float:
        return float(self._java_object.getyCenter3D())

    def set_y_center3d(self, v: float) -> None:
        self._java_object.setyCenter3D(v)

    def get_z_center3d(self) -> float:
        return float(self._java_object.getzCenter3D())

    def set_z_center3d(self, v: float) -> None:
        self._java_object.setzCenter3D(v)

    # outline surface
    def get_outline_surface(self) -> float:
        return float(self._java_object.getOutlineSurface())

    def set_outline_surface(self, v: float) -> None:
        self._java_object.setOutlineSurface(v)

    # 2D center / top
    def get_x(self) -> float:
        return float(self._java_object.getX())

    def set_x(self, v: float) -> None:
        self._java_object.setX(v)

    def get_y(self) -> float:
        return float(self._java_object.getY())

    def set_y(self, v: float) -> None:
        self._java_object.setY(v)

    def get_z(self) -> float:
        return float(self._java_object.getZ())

    def set_z(self, v: float) -> None:
        self._java_object.setZ(v)

    def get_x_top(self) -> float:
        return float(self._java_object.getxTop())

    def set_x_top(self, v: float) -> None:
        self._java_object.setxTop(v)

    def get_y_top(self) -> float:
        return float(self._java_object.getyTop())

    def set_y_top(self, v: float) -> None:
        self._java_object.setyTop(v)

    # center convenience: Java getCenter() returns a Point2D; we return the Java object
    def get_center(self) -> tuple:
        java_center = self._java_object.getCenter()
        return (float(java_center.getX()), float(java_center.getY()))

    def set_center(self, point2d: tuple) -> None:
        self._java_object.setCenter(gateway.jvm.java.awt.geom.Point2D.Double(float(point2d[0]), float(point2d[1])))

    # radius
    def get_radius(self) -> float:
        return float(self._java_object.getRadius())

    def set_radius(self, r: float) -> None:
        self._java_object.setRadius(r)

    # CAD information
    def get_cad(self) -> Optional[CADInformation]:
        java_cad = self._java_object.getCad()
        return CADInformation(java_cad) if java_cad else None

    def set_cad(self, cad: CADInformation) -> None:
        target = getattr(cad, '_java_object', cad)
        self._java_object.setCad(target)
