"""Wrapper for Java class NDTKitDefectDetectionInterface from package agi.ndtkit.api.

This module provides static methods for defect detection, management, and analysis.
All methods wrap the corresponding Java API functionality and handle type conversion.
"""

from typing import List, Optional
from .ndtkit_socket_connection import gateway
from .model.frame.NICartographyFrame import NICartographyFrame
from .model.frame.NICartographyFrameCScan import NICartographyFrameCScan
from .model.NIEnumDefectShapeType import NIEnumDefectShapeType
from .model.flaw.Flaw import Flaw
from .model.flaw.NIEnumDefectCharacteristics import NIEnumDefectCharacteristics
from .model.roi.Shape import Shape


def apply_defect_detection(config_file_path: Optional[str], cscan: NICartographyFrameCScan) -> None:
    """Run defect detection with the given configuration file.

    Args:
        config_file_path: Path to the configuration file for detection parameters.
                        If None, the default configuration will be used.
        cscan: The C-Scan frame on which to run the detection.

    Raises:
        Exception: if an error occurs during defect detection
    """
    file_obj = None if not config_file_path else gateway.jvm.java.io.File(config_file_path)
    gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.applyDefectDetection(file_obj, cscan._java_object)


def apply_defects_from_matrix(defect_matrix: List[List[bool]],
                              selected_cscan: NICartographyFrameCScan,
                              shape_type: NIEnumDefectShapeType) -> List[Flaw]:
    """Apply defect detection using a boolean matrix as defect indicators.

    Args:
        defect_matrix: 2D boolean matrix where True values represent defects.
                        Must have the same size as the C-Scan matrix.
        selected_cscan: The C-Scan where defects will be applied.
        shape_type: The shape type that will surround the defects.

    Returns:
        List of detected Flaw objects.
    """

    rows = len(defect_matrix)
    cols = len(defect_matrix[0]) if rows > 0 else 0
    java_matrix = gateway.new_array(gateway.jvm.boolean, rows, cols)
    for r in range(rows):
        for c in range(cols):
            java_matrix[r][c] = defect_matrix[r][c]

    java_flaws = gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.applyDefects(
        java_matrix, selected_cscan._java_object, shape_type.to_java_enum())
    return [Flaw(flaw) for flaw in java_flaws] if java_flaws else []


def apply_defects_from_shapes(shapes: List[Shape],
                              selected_cscan: NICartographyFrameCScan,
                              shape_type: NIEnumDefectShapeType) -> List[Flaw]:
    """Apply defect detection using given shapes as defects.

    Args:
        shapes: List of Shape objects to be treated as defects.
        selected_cscan: The C-Scan where defects will be applied.
        shape_type: The shape type that will surround the defects.

    Returns:
        List of detected Flaw objects.
    """
    java_shapes = gateway.jvm.java.util.ArrayList()  # type: ignore
    for shape in shapes:
        shape_obj = getattr(shape, '_java_object', shape)
        java_shapes.add(shape_obj)

    java_flaws = gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.applyDefects(
        java_shapes, selected_cscan._java_object, shape_type.to_java_enum())  # type: ignore
    return [Flaw(flaw) for flaw in java_flaws] if java_flaws else []


def apply_defects_from_shapes_with_names(shapes: List[Shape],
                                         defects_names: List[str],
                                         selected_cscan: NICartographyFrameCScan,
                                         shape_type: NIEnumDefectShapeType) -> List[Flaw]:
    """Apply defect detection using shapes and assign names to detected defects.

    Args:
        shapes: List of Shape objects to be treated as defects.
        defects_names: List of names to assign to the detected defects.
        selected_cscan: The C-Scan where defects will be applied.
        shape_type: The shape type that will surround the defects.

    Returns:
        List of detected Flaw objects with assigned names.
    """
    java_shapes = gateway.jvm.java.util.ArrayList()
    for shape in shapes:
        shape_obj = getattr(shape, '_java_object', shape)
        java_shapes.add(shape_obj)

    java_names = gateway.jvm.java.util.ArrayList()
    for name in defects_names:
        java_names.add(name)

    java_flaws = gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.applyDefects(
        java_shapes, java_names, selected_cscan._java_object, shape_type.to_java_enum())
    return [Flaw(flaw) for flaw in java_flaws] if java_flaws else []


def get_list_of_flaws(defect_matrix: List[List[bool]],
                      selected_cscan: NICartographyFrameCScan,
                      shape_type: NIEnumDefectShapeType) -> List[Flaw]:
    """Get the list of defects represented by True values in the boolean matrix.

    Args:
        defect_matrix: 2D boolean matrix where True values represent defects.
        selected_cscan: The cartography on which to find the defects.
        shape_type: The shape type for the defects.

    Returns:
        List of Flaw objects.
    """
    # Convert Python list to Java 2D array
    rows = len(defect_matrix)
    cols = len(defect_matrix[0]) if rows > 0 else 0
    java_2d_array = gateway.new_array(gateway.jvm.boolean, rows)  # type: ignore

    for i in range(rows):
        java_2d_array[i] = gateway.new_array(gateway.jvm.boolean, cols)  # type: ignore
        for j in range(cols):
            java_2d_array[i][j] = bool(defect_matrix[i][j])  # type: ignore

    java_flaws = gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.getListOfFlaws(
        java_2d_array, selected_cscan._java_object, shape_type.to_java_enum())  # type: ignore
    return [Flaw(flaw) for flaw in java_flaws] if java_flaws else []


def apply_db_sizing(amp_carto: NICartographyFrameCScan, db_param: float) -> None:
    """Apply dB sizing to defects in the amplitude cartography.

    Requirement: A defect detection on the Amplitude cartography with an associated Time cartography.

    Args:
        amp_carto: The Amplitude C-Scan where defect detection has been performed.
        db_param: The dB value to apply for correcting defect sizes.

    Raises:
        Exception: if an error occurs during sizing
    """
    gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.applydBSizing(
        amp_carto._java_object, float(db_param))  # type: ignore


def apply_db_sizing_with_tof(tof_carto: Optional[NICartographyFrameCScan],
                             amp_carto: NICartographyFrameCScan,
                             db_param: float,
                             levels: List[int]) -> None:
    """Apply dB sizing to defects with Time-of-Flight cartography.

    Args:
        tof_carto: The Time-of-Flight C-Scan (can be None to use only Amplitude).
        amp_carto: The Amplitude C-Scan associated with the Time cartography.
        db_param: The dB value to apply for correcting defect sizes.
        levels: List of level indices to apply the sizing to.

    Raises:
        Exception: if an error occurs during sizing
    """
    tof_obj = tof_carto._java_object if tof_carto else None  # type: ignore
    java_levels = gateway.new_array(gateway.jvm.int, len(levels))  # type: ignore

    for i in range(len(levels)):
        java_levels[i] = int(levels[i])  # type: ignore

    gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.applydBSizing(
        tof_obj, amp_carto._java_object, float(db_param), java_levels)  # type: ignore


def apply_cad_transformation_file(cscan: NICartographyFrameCScan, filepath: str) -> None:
    """Apply CAD transformation matrix to get CAD location of defects.

    Args:
        cscan: The C-Scan to apply transformation to.
        filepath: Path to the CAD transformation file.

    Raises:
        Exception: if an error occurs during transformation
    """
    gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.applyCADTransformationFile(
        cscan._java_object, filepath)  # type: ignore


def load_defects_from_file(target_cscan: NICartographyFrameCScan, nkd_filepath: str) -> None:
    """Load defects from an NKD file and apply them to the given C-Scan.

    Args:
        target_cscan: The C-Scan where defects will be applied.
        nkd_filepath: Path to the NKD file containing defects.

    Raises:
        Exception: if an error occurs when loading defects
    """
    gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.loadDefects(
        target_cscan._java_object, nkd_filepath)  # type: ignore


def load_defects(nkd_filepath: str) -> List[Flaw]:
    """Load defects from an NKD file and return them as a list.

    Args:
        nkd_filepath: Path to the NKD file containing defects.

    Returns:
        List of Flaw objects loaded from the file.

    Raises:
        Exception: if an error occurs when loading defects
    """
    java_flaws = gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.loadDefects(nkd_filepath)
    return [Flaw(flaw) for flaw in java_flaws] if java_flaws else []


def write_defects(output_file: str, parent_scan: NICartographyFrame) -> None:
    """Write all defects from the given scan into an NKD file.

    Args:
        output_file: Path to the output NKD file.
        parent_scan: The scan (C-Scan or B-Scan) containing the defects.

    Raises:
        Exception: if an error occurs during writing
    """
    gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.writeDefects(output_file, parent_scan._java_object)


def write_defects_list(output_file: str, flaws: List[Flaw], parent_scan: NICartographyFrame) -> None:
    """Write the given flaws into an NKD file.

    Args:
        output_file: Path to the output NKD file.
        flaws: List of Flaw objects to write.
        parent_scan: The scan (C-Scan or B-Scan) associated with the defects.

    Raises:
        Exception: if an error occurs during writing
    """
    java_flaws = gateway.jvm.java.util.ArrayList()  # type: ignore
    for flaw in flaws:
        flaw_obj = getattr(flaw, '_java_object', flaw)
        java_flaws.add(flaw_obj)

    gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.writeDefects(output_file, java_flaws, parent_scan._java_object)


def change_defect_shape(flaw: Flaw, shape: Shape) -> None:
    """Change the shape of a defect.

    Warning: Geometric information (center, width, height, etc.) must be consistent.

    Args:
        flaw: The Flaw object to update.
        shape: The new Shape to assign to the defect.

    Raises:
        Exception: if an error occurs during shape change
    """
    flaw_obj = getattr(flaw, '_java_object', flaw)
    shape_obj = getattr(shape, '_java_object', shape)
    gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.changeDefectShape(flaw_obj, shape_obj)


def get_shape(flaw: Flaw) -> Shape:
    """Get the shape of a given flaw.

    Args:
        flaw: The Flaw object to get the shape from.

    Returns:
        The convex hull Shape of the defect.
    """
    flaw_obj = getattr(flaw, '_java_object', flaw)
    return Shape(gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.getShape(flaw_obj))  # type: ignore


def remove_defects(defects: List[Flaw], cscan: NICartographyFrameCScan) -> None:
    """Remove defects from the defect table.

    Args:
        defects: List of Flaw objects to remove.
        cscan: The C-Scan containing the defects.

    Raises:
        Exception: if an error occurs during removal
    """
    java_defects = gateway.jvm.java.util.ArrayList()  # type: ignore
    for defect in defects:
        defect_obj = getattr(defect, '_java_object', defect)
        java_defects.add(defect_obj)

    gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.removeDefects(java_defects, cscan._java_object)


def get_all_defects(cscan: NICartographyFrameCScan) -> List[Flaw]:
    java_flaws = gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.getAllDefects(cscan._java_object)
    return [Flaw(flaw) for flaw in java_flaws] if java_flaws else []


def get_selected_defects(cscan: NICartographyFrameCScan) -> List[Flaw]:
    """Get all currently selected defects from a C-Scan.

    Args:
        cscan: The C-Scan to get selected defects from.

    Returns:
        List of selected Flaw objects.
    """
    java_flaws = gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.getSelectDefects(cscan._java_object)
    return [Flaw(flaw) for flaw in java_flaws] if java_flaws else []


def change_defect_value(cscan: NICartographyFrameCScan,
                        defect_to_modify: Flaw,
                        characteristic_to_modify: NIEnumDefectCharacteristics,
                        new_value: str) -> None:
    """Change a characteristic value of a defect in the defect table.

    Args:
        cscan: The C-Scan containing the defect.
        defect_to_modify: The Flaw object to modify.
        characteristic_to_modify: The characteristic to modify (NIEnumDefectCharacteristics).
        new_value: The new value as a string.
    """
    defect_obj = getattr(defect_to_modify, '_java_object', defect_to_modify)
    gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.changeDefectValue(
        cscan._java_object, defect_obj, characteristic_to_modify.to_java_enum(), new_value)


def get_defect_value(cscan: NICartographyFrameCScan,
                     defect: Flaw,
                     characteristic_to_get: NIEnumDefectCharacteristics) -> str:
    """Get the real value of a defect characteristic.

    Args:
        cscan: The C-Scan containing the defect.
        defect: The Flaw object to get value from.
        characteristic_to_get: The characteristic to retrieve.

    Returns:
        The value of the characteristic as a string.
    """
    defect_obj = getattr(defect, '_java_object', defect)
    return gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.getDefectValue(
        cscan._java_object, defect_obj, characteristic_to_get.to_java_enum())  # type: ignore


def get_displayed_defect_value_from_table(cscan: NICartographyFrameCScan,
                                          defect: Flaw,
                                          characteristic_to_get: NIEnumDefectCharacteristics) -> str:
    """Get the displayed value of a defect characteristic from the table.

    Args:
        cscan: The C-Scan containing the defect.
        defect: The Flaw object to get value from.
        characteristic_to_get: The characteristic to retrieve.

    Returns:
        The displayed value of the characteristic as a string.
    """
    defect_obj = getattr(defect, '_java_object', defect)
    return gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.getDisplayedDefectValueFromTable(
        cscan._java_object, defect_obj, characteristic_to_get.to_java_enum())  # type: ignore


def add_defects(cscan: NICartographyFrameCScan, defects: List[Flaw]) -> None:
    """Add defects into a given C-Scan.

    Args:
        cscan: The C-Scan to add defects to.
        defects: List of Flaw objects to add.

    Raises:
        Exception: if an error occurs during addition
    """
    java_defects = gateway.jvm.java.util.ArrayList()  # type: ignore
    for defect in defects:
        defect_obj = getattr(defect, '_java_object', defect)
        java_defects.add(defect_obj)

    gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.addDefects(cscan._java_object, java_defects)


def save_defects(file_path: str, cscan: NICartographyFrame) -> None:
    """Save all defects from a given frame into an NKD file.

    Args:
        file_path: Path to the output file.
        cscan: The frame (C-Scan or B-Scan) containing defects.

    Raises:
        Exception: if an error occurs during saving
    """
    gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.saveDefects(file_path, cscan._java_object)


def group_defects(config_file_path: Optional[str], cscan: NICartographyFrameCScan) -> None:
    """Group defects from the given defect detection.

    Args:
        config_file_path: Path to the regrouping configuration file.
                        If None, the default config will be used.
        cscan: The C-Scan on which to operate.

    Raises:
        Exception: if an error occurs during grouping
    """
    file_obj = None
    if config_file_path is not None:
        file_obj = gateway.jvm.java.io.File(config_file_path)  # type: ignore
    gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.groupDefects(
        file_obj, cscan._java_object)  # type: ignore


def set_defect_table_configuration_from_file(config_file: str) -> None:
    """Set defect table column configuration from a file.

    This configuration will be applied to all defect tables.

    Args:
        config_file: Path to the defect table configuration file.
    """
    file_obj = gateway.jvm.java.io.File(config_file)  # type: ignore
    gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.setDefectTableConfigurationFromFile(
        file_obj)  # type: ignore


def set_defect_detection_tabs_closable(is_closable: bool) -> None:
    """Toggle the visibility of the close icon for the defect table.

    Args:
        is_closable: Set to False to hide the close icon.
    """
    gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.setDefectDetectionTabsClosable(
        bool(is_closable))  # type: ignore


def get_outline_shape(flaw: Flaw) -> Shape:
    """Compute and return the outline shape of a defect.

    Args:
        flaw: The Flaw object to get the outline for.

    Returns:
        The computed outline Shape of the defect.
    """
    flaw_obj = getattr(flaw, '_java_object', flaw)
    return Shape(gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.getOutlineShape(flaw_obj))  # type: ignore


def get_normal(flaw: Flaw) -> Optional[tuple]:
    """Get the normal vector of the best-fitting plane through 3D contour points.

    Uses planar regression to fit a least-squares plane to the 3D contour points.

    Args:
        flaw: The Flaw object containing 3D contour geometry.

    Returns:
        A normalized Vector3f representing the plane normal, or None if no contour.
    """
    flaw_obj = getattr(flaw, '_java_object', flaw)
    java_normal = gateway.jvm.agi.ndtkit.api.NDTKitDefectDetectionInterface.getNormal(flaw_obj)
    return (java_normal.getX(), java_normal.getY(), java_normal.getZ()) if java_normal else None
