from py4j.java_gateway import JavaObject
from ...ndtkit_socket_connection import gateway


class Shape:
    """Base class for ROI shapes."""

    def __init__(self, java_object: JavaObject):
        self._java_object = java_object

    def get_points(self) -> list[tuple[float, float]]:
        """Get the points defining the shape.

        Returns:
            list[tuple[float, float]]: List of (x, y) points
        """
        java_points = gateway.jvm.com.agi.ndtkit.common.geometry.Shape2DHelper.getShapePoints2D(self._java_object)
        return None if not java_points else [(point.getX(), point.getY()) for point in java_points]  # type: ignore

    @staticmethod
    def create_rectangle_shape(x: float, y: float, width: float, height: float) -> 'Shape':
        return Shape(gateway.jvm.java.awt.geom.Rectangle2D.Double(float(x), float(y), float(width), float(height)))  # type: ignore
