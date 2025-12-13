"""Python wrapper for Java com.agi.db.partacquisition.model.DataStatistics.

This wrapper exposes the frequently used getters/setters and convenience
methods from the Java class. It purposely returns Python-native primitives
for scalar values and Python lists/sets for collection values where
possible. For complex objects not wrapped in this repository the raw Java
object is returned so callers can wrap them later if desired.
"""
from typing import List, Optional
from py4j.java_gateway import JavaObject


class DataStatistics:
    """Thin wrapper around com.agi.db.partacquisition.model.DataStatistics.

    Accepts a Py4J JavaObject instance and delegates calls to the Java
    object. Methods are provided in a Pythonic snake_case style.
    """

    def __init__(self, java_object: JavaObject):
        self._java_object = java_object

    # Basic stats
    def get_min(self) -> Optional[float]:
        v = self._java_object.getMin()
        return None if v is None else float(v)

    def set_min(self, value: Optional[float]) -> None:
        self._java_object.setMin(value)

    def get_max(self) -> Optional[float]:
        v = self._java_object.getMax()
        return None if v is None else float(v)

    def set_max(self, value: Optional[float]) -> None:
        self._java_object.setMax(value)

    def get_mean(self) -> Optional[float]:
        v = self._java_object.getMean()
        return None if v is None else float(v)

    def set_mean(self, value: Optional[float]) -> None:
        self._java_object.setMean(value)

    def get_standard_deviation(self) -> Optional[float]:
        v = self._java_object.getStandardDeviation()
        return None if v is None else float(v)

    def set_standard_deviation(self, value: Optional[float]) -> None:
        self._java_object.setStandardDeviation(value)

    # Median: the Java class exposes both a Double field (`median`) and a
    # getMedian() method that returns a float (computes it from data if
    # necessary). We expose both: `get_median_field` -> underlying field,
    # `get_median` -> the Java method.
    def get_median_field(self) -> Optional[float]:
        v = self._java_object.median if hasattr(self._java_object, "median") else None
        return None if v is None else float(v)

    def set_median_field(self, value: Optional[float]) -> None:
        # There is a setMedian(Double) method on the Java object
        self._java_object.setMedian(value)

    def get_median(self) -> float:
        """Call the Java getMedian() method (returns float).

        The Java implementation may compute the median from stored
        dataValues if needed.
        """
        return float(self._java_object.getMedian())

    # Data values (without special values)
    def get_data_without_special_values(self) -> List[float]:
        vals = self._java_object.getDataWithoutSpecialValues()
        return [] if vals is None else list(vals)

    def set_data_without_special_values(self, values: List[float]) -> None:
        # Py4J will convert a Python list to a java.util.List when possible
        self._java_object.setDataWithoutSpecialValues(values)

    def clean_up(self) -> None:
        self._java_object.cleanUp()

    # Counts and derived areas/ratios
    def get_color_piece_points_number(self) -> int:
        return int(self._java_object.getColorPiecePointsNumber())

    def set_color_piece_points_number(self, n: int) -> None:
        self._java_object.setColorPiecePointsNumber(n)

    def get_visible_specimen_points_area(self) -> float:
        return float(self._java_object.getVisibleSpecimenPointsArea())

    def get_nan_points_area(self) -> float:
        return float(self._java_object.getNaNPointsArea())

    def get_noe_points_area(self) -> float:
        return float(self._java_object.getNoEPointsArea())

    def get_nos_points_area(self) -> float:
        return float(self._java_object.getNoSPointsArea())

    def get_mask_points_area(self) -> float:
        return float(self._java_object.getMaskPointsArea())

    def get_visible_specimen_points_ratio(self) -> float:
        return float(self._java_object.getVisibleSpecimenPointsRatio())

    def get_nan_points_ratio(self) -> float:
        return float(self._java_object.getNaNPointsRatio())

    def get_noe_points_ratio(self) -> float:
        return float(self._java_object.getNoEPointsRatio())

    def get_nos_points_ratio(self) -> float:
        return float(self._java_object.getNoSPointsRatio())

    def get_masked_points_ratio(self) -> float:
        return float(self._java_object.getMaskedPointsRatio())

    # Points number
    def get_points_number(self) -> int:
        return int(self._java_object.getPointsNumber())

    def set_points_number(self, n: int) -> None:
        self._java_object.setPointsNumber(n)

    # Individual setters for the various counters present in Java
    def set_nan_points_number(self, n: int) -> None:
        self._java_object.setNanPointsNumber(n)

    def set_noe_points_number(self, n: int) -> None:
        self._java_object.setNoePointsNumber(n)

    def set_nos_points_number(self, n: int) -> None:
        self._java_object.setNosPointsNumber(n)

    def set_out_of_scale_min_number(self, n: int) -> None:
        self._java_object.setOutOfScaleMinNumber(n)

    def set_out_of_scale_max_number(self, n: int) -> None:
        self._java_object.setOutOfScaleMaxNumber(n)

    def set_mask_points_number(self, n: int) -> None:
        self._java_object.setMaskPointsNumber(n)

    def get_out_of_scale_max_number(self) -> int:
        return int(self._java_object.getOutOfScaleMaxNumber())

    def get_out_of_scale_min_number(self) -> int:
        return int(self._java_object.getOutOfScaleMinNumber())

    # Raw data list and transient data
    def get_data(self) -> List[float]:
        vals = self._java_object.getData()
        return [] if vals is None else list(vals)

    def set_data(self, values: List[float]) -> None:
        self._java_object.setData(values)
