"""Wrapper for com.agi.ndtkit.common._2d.matrix.BooleanMember Java class.

This module provides a thin Python wrapper exposing the main methods of the
Java BooleanMember class. Conversion helpers turn Java primitive boolean[][]
into Python List[List[bool]] and convert Java Point2D-like constructs where
appropriate. We intentionally avoid constructing complex Java primitive
arrays from pure Python in this helper to remain robust across Py4J
configurations; callers that need to create a Java BooleanMember should use
`gateway.jvm.com.agi.ndtkit.common._2d.matrix.BooleanMember` directly.
"""
from typing import List, Tuple
from py4j.java_gateway import JavaObject


class BooleanMember:
    """Python wrapper for com.agi.ndtkit.common._2d.matrix.BooleanMember.

    Instantiated with a Py4J JavaObject instance representing the Java
    BooleanMember. The wrapper exposes Pythonic getters/setters and
    convenience conversions.
    """

    def __init__(self, java_object: JavaObject):
        self._java_object = java_object

    def get_matrix(self) -> List[List[bool]]:
        """Return the underlying boolean matrix as a Python list-of-lists.

        Each row is converted to a list of bool values. If the Java matrix is
        None, an empty list is returned.
        """
        jmat = self._java_object.getMatrix()
        if jmat is None:
            return []
        # jmat is a Java boolean[][] (primitive arrays) which are iterable
        py_rows: List[List[bool]] = []
        for r in jmat:
            # r is a boolean[] row
            py_rows.append([bool(x) for x in r])
        return py_rows

    def set_matrix(self, matrix: List[List[bool]]) -> None:
        self._java_object.setMatrix(matrix)

    def get_row_offset(self) -> int:
        return int(self._java_object.getRowOffset())

    def set_row_offset(self, v: int) -> None:
        self._java_object.setRowOffset(v)

    def get_col_offset(self) -> int:
        return int(self._java_object.getColOffset())

    def set_col_offset(self, v: int) -> None:
        self._java_object.setColOffset(v)

    def clone(self) -> "BooleanMember":
        """Return a new BooleanMember wrapper for the Java-cloned instance."""
        cloned = self._java_object.clone()
        return BooleanMember(cloned)

    def intersection_score(self, other: 'BooleanMember') -> Tuple[float, float]:
        """Compute the intersection score with another BooleanMember.

        `other` may be another BooleanMember wrapper or a Java BooleanMember.
        Returns a tuple (score, nbPixels) as floats.
        """
        other_java = getattr(other, "_java_object", other)
        res = self._java_object.intersectionScore(other_java)
        # result is a Java double[]; convert to Python tuple
        return (float(res[0]), float(res[1]))

    def __eq__(self, other: object) -> bool:  # type: ignore[override]
        if other is None:
            return False
        other_java = getattr(other, "_java_object", other)
        try:
            return bool(self._java_object.equals(other_java))
        except Exception:
            return False

    def __repr__(self) -> str:
        try:
            rows = len(self._java_object.getMatrix())
            cols = len(self._java_object.getMatrix()[0])
            return f"BooleanMember({rows}x{cols}, row_offset={self.get_row_offset()}, col_offset={self.get_col_offset()})"
        except Exception:
            return "BooleanMember(<java object>)"
