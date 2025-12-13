"""Python wrapper for Java com.agi.db.partacquisition.model.Flaw.

This module provides a thin, Pythonic wrapper around the Java Flaw class
exposing the most commonly used getters/setters and a few convenience
methods. Complex returned objects are returned as-is (Java objects) so the
client can either use the raw Java object or wrap it with a dedicated
wrapper if available.
"""
from typing import List, Optional
from py4j.java_gateway import JavaObject
from .DataStatistics import DataStatistics
from .DefectGeometricInfos import DefectGeometricInfos
from .DistancesToLayouts import DistancesToLayouts


class Flaw:
    """Wrapper for com.agi.db.partacquisition.model.Flaw Java objects.

    The wrapper expects an instance of Py4J JavaObject and exposes most of
    the Java getters/setters as snake_case methods returning Python-native
    primitives where appropriate.
    """

    def __init__(self, java_object: JavaObject):
        self._java_object = java_object

    # Identification
    def get_id(self) -> Optional[int]:
        java_id = self._java_object.getId()
        return None if java_id is None else int(java_id)

    def set_id(self, id_value: int) -> None:
        self._java_object.setId(id_value)

    def get_defect_name(self) -> str:
        return self._java_object.getDefectName()

    def set_defect_name(self, name: str) -> None:
        self._java_object.setDefectName(name)

    # Comments / notes
    def get_comment(self) -> str:
        return self._java_object.getComment()

    def set_comment(self, comment: str) -> None:
        self._java_object.setComment(comment)

    def get_note(self) -> Optional[str]:
        return self._java_object.getNote()

    def set_note(self, note: str) -> None:
        self._java_object.setNote(note)

    def build_id_and_comment(self) -> str:
        return self._java_object.builIdAndComment()

    # Level / reduction
    def get_level(self) -> int:
        return int(self._java_object.getLevel())

    def set_level(self, level: int) -> None:
        self._java_object.setLevel(level)

    def has_been_reduced(self) -> bool:
        return bool(self._java_object.isHasBeenReduced())

    def set_has_been_reduced(self, reduced: bool) -> None:
        self._java_object.setHasBeenReduced(reduced)

    # Hole information
    def get_hole_id(self) -> int:
        return int(self._java_object.getHoleId())

    def set_hole_id(self, hole_id: int) -> None:
        self._java_object.setHoleId(hole_id)

    def get_hole_diameter(self) -> float:
        return float(self._java_object.getHoleDiameter())

    def set_hole_diameter(self, diameter: float) -> None:
        self._java_object.setHoleDiameter(diameter)

    # Detection / density / shape types (Java enums)
    def get_detection_type(self) -> str:
        return self._java_object.getDetectionType().getJsonValue()

    def get_density_type(self) -> str:
        return self._java_object.getDensityType().getJsonValue()

    def get_shape_type(self) -> str:
        return self._java_object.getShapeType().getJsonValue()

    # Palette
    def get_min_palette(self) -> float:
        return float(self._java_object.getMinPalette())

    def set_min_palette(self, v: float) -> None:
        self._java_object.setMinPalette(v)

    def get_max_palette(self) -> float:
        return float(self._java_object.getMaxPalette())

    def set_max_palette(self, v: float) -> None:
        self._java_object.setMaxPalette(v)

    # Statistics / geometry
    def get_defect_stat(self) -> DataStatistics:
        return DataStatistics(self._java_object.getDefectStat())

    def get_overthickness_stat(self) -> DataStatistics:
        return DataStatistics(self._java_object.getOverthicknessStat())

    def set_overthickness_stat(self, stat: DataStatistics) -> None:
        target = getattr(stat, "_java_object", stat)
        self._java_object.setOverthicknessStat(target)

    def get_geometric_information(self) -> DefectGeometricInfos:
        return DefectGeometricInfos(self._java_object.getGeometricInformation())

    def set_geometric_information(self, geo: DefectGeometricInfos) -> None:
        target = getattr(geo, "_java_object", geo)
        self._java_object.setGeometricInformation(target)

    def get_distances_to_layouts(self) -> DistancesToLayouts:
        return DistancesToLayouts(self._java_object.getDistancesToLayouts())

    def set_distances_from_layouts(self, distances: DistancesToLayouts) -> None:
        target = getattr(distances, "_java_object", distances)
        # Java Flaw has setDistancesFromLayouts in the source
        self._java_object.setDistancesFromLayouts(target)

    # Sub-flaws / parent
    def get_sub_flaws(self) -> List['Flaw']:
        return list(self._java_object.getSubFlaws())

    def set_sub_flaws(self, sub_flaws: List['Flaw']) -> None:
        # accept list of wrappers or Java objects
        java_list = [getattr(s, "_java_object", s) for s in sub_flaws]
        self._java_object.setSubFlaws(java_list)

    def get_parent_flaw(self) -> 'Flaw':
        return self._java_object.getParentFlaw()

    def set_parent_flaw(self, parent: 'Flaw') -> None:
        target = getattr(parent, "_java_object", parent)
        self._java_object.setParentFlaw(target)

    def is_multiple(self) -> bool:
        return bool(self._java_object.isMultiple())

    # Misc
    def get_flaw_nbr(self) -> int:
        return int(self._java_object.getFlawNbr())

    def set_flaw_nbr(self, n: int) -> None:
        self._java_object.setFlawNbr(n)

    def get_palette_environment_id(self) -> int:
        return int(self._java_object.getPaletteEnvironmentId())

    def set_palette_environment_id(self, env_id: int) -> None:
        self._java_object.setPaletteEnvironmentId(env_id)

    def get_offset_comment_and_id_x(self) -> float:
        return float(self._java_object.getOffsetCommentAndIdX())

    def set_offset_comment_and_id_x(self, x: float) -> None:
        self._java_object.setOffsetCommentAndIdX(x)

    def get_offset_comment_and_id_y(self) -> float:
        return float(self._java_object.getOffsetCommentAndIdY())

    def set_offset_comment_and_id_y(self, y: float) -> None:
        self._java_object.setOffsetCommentAndIdY(y)
