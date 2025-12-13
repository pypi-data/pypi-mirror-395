"""Python wrapper for Java com.agi.db.partacquisition.model.DistancesToLayouts.

Provides a thin, Pythonic wrapper around the Java POJO. Methods return
Python primitives for scalar values and the raw Java objects for complex
values (Point2D) so callers can wrap them if desired. Setter convenience
accepts either a Java Point2D-like object (with getX/getY) or a (x, y)
sequence.
"""
from typing import Optional
from py4j.java_gateway import JavaObject
from ...ndtkit_socket_connection import gateway


class DistancesToLayouts:
    """Wrapper for com.agi.db.partacquisition.model.DistancesToLayouts."""

    def __init__(self, java_object: JavaObject):
        self._java_object = java_object

    def get_id(self) -> Optional[int]:
        v = self._java_object.getId()
        return None if v is None else int(v)

    def set_id(self, id_value: int) -> None:
        self._java_object.setId(id_value)

    # D1
    def get_d1_layout_name(self) -> Optional[str]:
        return self._java_object.getD1LayoutName()

    def set_d1_layout_name(self, name: str) -> None:
        self._java_object.setD1LayoutName(name)

    def get_d1_is_x_positive_distance_to_layout(self) -> bool:
        return bool(self._java_object.getD1IsXPositiveDistanceToLayout())

    def set_d1_is_x_positive_distance_to_layout(self, v: bool) -> None:
        self._java_object.setD1IsXPositiveDistanceToLayout(v)

    def get_d1x_value_distance_to_layout(self) -> float:
        return float(self._java_object.getD1xValueDistanceToLayout())

    def set_d1x_value_distance_to_layout(self, v: float) -> None:
        self._java_object.setD1xValueDistanceToLayout(v)

    def get_d1_is_y_positive_distance_to_layout(self) -> bool:
        return bool(self._java_object.getD1IsYPositiveDistanceToLayout())

    def set_d1_is_y_positive_distance_to_layout(self, v: bool) -> None:
        self._java_object.setD1IsYPositiveDistanceToLayout(v)

    def get_d1_is_vertical_distance_to_layout(self) -> bool:
        return bool(self._java_object.getD1IsVerticalDistanceToLayout())

    def set_d1_is_vertical_distance_to_layout(self, v: bool) -> None:
        self._java_object.setD1IsVerticalDistanceToLayout(v)

    def get_d1_is_horizontal_distance_to_layout(self) -> bool:
        return bool(self._java_object.getD1IsHorizontalDistanceToLayout())

    def set_d1_is_horizontal_distance_to_layout(self, v: bool) -> None:
        self._java_object.setD1IsHorizontalDistanceToLayout(v)

    def get_d1_target_point_distance_to_layout(self) -> tuple:
        """Return Java Point2D representing target point for D1."""
        java_point2d = self._java_object.getD1TargetPointDistanceToLayout()
        return (java_point2d.getX(), java_point2d.getY())

    def set_d1_target_point_distance_to_layout(self, pt: tuple) -> None:
        x, y = pt[0], pt[1]
        pt_obj = gateway.jvm.java.awt.geom.Point2D.Double(float(x), float(y))
        self._java_object.setD1TargetPointDistanceToLayout(pt_obj)

    def get_d1x_target_point_distance_to_layout(self) -> float:
        return float(self._java_object.getD1xTargetPointDistanceToLayout())

    def set_d1x_target_point_distance_to_layout(self, v: float) -> None:
        self._java_object.setD1xTargetPointDistanceToLayout(v)

    def get_d1y_target_point_distance_to_layout(self) -> float:
        return float(self._java_object.getD1yTargetPointDistanceToLayout())

    def set_d1y_target_point_distance_to_layout(self, v: float) -> None:
        self._java_object.setD1yTargetPointDistanceToLayout(v)

    # D2 (mirror of D1)
    def get_d2_layout_name(self) -> Optional[str]:
        return self._java_object.getD2LayoutName()

    def set_d2_layout_name(self, name: str) -> None:
        self._java_object.setD2LayoutName(name)

    def get_d2_is_x_positive_distance_to_layout(self) -> bool:
        return bool(self._java_object.getD2IsXPositiveDistanceToLayout())

    def set_d2_is_x_positive_distance_to_layout(self, v: bool) -> None:
        self._java_object.setD2IsXPositiveDistanceToLayout(v)

    def get_d2x_value_distance_to_layout(self) -> float:
        return float(self._java_object.getD2xValueDistanceToLayout())

    def set_d2x_value_distance_to_layout(self, v: float) -> None:
        self._java_object.setD2xValueDistanceToLayout(v)

    def get_d2_is_y_positive_distance_to_layout(self) -> bool:
        return bool(self._java_object.getD2IsYPositiveDistanceToLayout())

    def set_d2_is_y_positive_distance_to_layout(self, v: bool) -> None:
        self._java_object.setD2IsYPositiveDistanceToLayout(v)

    def get_d2_is_vertical_distance_to_layout(self) -> bool:
        return bool(self._java_object.getD2IsVerticalDistanceToLayout())

    def set_d2_is_vertical_distance_to_layout(self, v: bool) -> None:
        self._java_object.setD2IsVerticalDistanceToLayout(v)

    def get_d2_is_horizontal_distance_to_layout(self) -> bool:
        return bool(self._java_object.getD2IsHorizontalDistanceToLayout())

    def set_d2_is_horizontal_distance_to_layout(self, v: bool) -> None:
        self._java_object.setD2IsHorizontalDistanceToLayout(v)

    def get_d2_target_point_distance_to_layout(self) -> tuple:
        java_point2d = self._java_object.getD2TargetPointDistanceToLayout()
        return (java_point2d.getX(), java_point2d.getY())

    def set_d2_target_point_distance_to_layout(self, pt: tuple) -> None:
        x, y = pt[0], pt[1]
        pt_obj = gateway.jvm.java.awt.geom.Point2D.Double(float(x), float(y))
        self._java_object.setD2TargetPointDistanceToLayout(pt_obj)

    def get_d2x_target_point_distance_to_layout(self) -> float:
        return float(self._java_object.getD2xTargetPointDistanceToLayout())

    def set_d2x_target_point_distance_to_layout(self, v: float) -> None:
        self._java_object.setD2xTargetPointDistanceToLayout(v)

    def get_d2y_target_point_distance_to_layout(self) -> float:
        return float(self._java_object.getD2yTargetPointDistanceToLayout())

    def set_d2y_target_point_distance_to_layout(self, v: float) -> None:
        self._java_object.setD2yTargetPointDistanceToLayout(v)
