"""Wrapper for Java class NDTKitROIInterface from package agi.ndtkit.api.

This module provides static methods that wrap the Java API functionality.
Methods preserve Java documentation and handle type conversion.
"""

from typing import Any, List
from .ndtkit_socket_connection import gateway
from .py4j_utils import to_java_list
from .model.frame.NICartographyFrame import NICartographyFrame
from .model.frame.NICartographyFrameCScan import NICartographyFrameCScan
from .model.roi.Shape import Shape
from .model.roi.NIEnumRoiFormat import NIEnumRoiFormat
from .model.roi.EnumShapeSelection import EnumShapeSelection
from .model.roi.NIEnumRoiGeometry import NIEnumRoiGeometry
from .model.roi.NIRoiSelection import NIRoiSelection
from .model.roi.NIRoiLayout import NIRoiLayout
from .model.roi.NIRoiMask import NIRoiMask
from .model.roi.NIRoi import NIRoi
from .model.roi.NIRoiLayout import NIRoiLayout
from .model.roi.NIRoiMask import NIRoiMask
from .model.roi.NIRoiSelection import NIRoiSelection


# Local helper used by the wrappers below to convert Java NIRoi instances
# into the appropriate Python wrapper (NIRoiLayout/NIRoiMask/NIRoiSelection)
def _wrap_roi(java_roi: Any):
    """Return the most specific Python ROI wrapper for a java_roi proxy."""
    if java_roi is None:
        return None
    # lazy imports to avoid touching top-of-file imports

    try:
        cls_name = java_roi.getClass().getSimpleName()
    except Exception:
        # fallback: return base wrapper
        return NIRoi(java_roi)

    if 'NIRoiLayout' in cls_name or 'Layout' in cls_name:
        return NIRoiLayout(java_roi)
    if 'NIRoiMask' in cls_name or 'Mask' in cls_name:
        return NIRoiMask(java_roi)
    if 'NIRoiSelection' in cls_name or 'Selection' in cls_name:
        return NIRoiSelection(java_roi)
    # default
    return NIRoi(java_roi)


def _wrap_roi_list(java_rois: list[Any]) -> list[NIRoi]:
    """Return a list of the most specific Python ROI wrappers for a list of java_roi proxies."""
    return [_wrap_roi(java_roi) for java_roi in java_rois]  # pyright: ignore[reportReturnType]


def get_shapes_from_rois(cscan: NICartographyFrame, roi_type: NIEnumRoiFormat, selection_mode: EnumShapeSelection) -> List[Shape]:
    """Get list of shapes (mask / selection or dressing layout) from given cartography.

    Args:
        cscan: source cartography (if null use current selected frame).
        roi_type: roi type (from enumerator #NDTKitCscanInterface.EnumRoiFormat)
        selection_mode: (from enumerator #NDTKitCscanInterface.EnumSelectedRoi)

    Returns:
        list of shapes
    """
    java_list_shapes = gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.getShapesFromRois(
        cscan._java_object, roi_type.to_java_enum(), selection_mode.to_java_enum())  # type: ignore
    return [Shape(java_shape) for java_shape in java_list_shapes]  # type: ignore


def create_layout_from_shape(shape: Shape, layout_name: str, x_res: float, y_res: float, roi_geometry: NIEnumRoiGeometry) -> NIRoiLayout:
    """Create mask from given shape.

    Args:
        shape: shape source.
        layout_name: the name of the layout.
        x_res: x resolution.
        y_res: y resolution.
        roi_geometry: roi geometry type ({@link NIEnumRoiGeometry}).

    Returns:
        the mask ROI.
    """
    return _wrap_roi(gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.createLayoutFromShape(shape._java_object, layout_name, x_res, y_res, roi_geometry.to_java_enum()))  # pyright: ignore[reportReturnType]


def create_layout_text_from_shape(shape: Shape, layout_name: str, x_res: float, y_res: float) -> NIRoiLayout:
    """Create mask from given shape.

    Args:
        shape: shape source.
        layout_name: the name of the layout.
        x_res: x resolution.
        y_res: y resolution.
        roi_geometry: roi geometry type ({@link NIEnumRoiGeometry}).

    Returns:
        the mask ROI.
    """
    return _wrap_roi(gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.createLayoutTextFromShape(shape._java_object, layout_name, x_res, y_res))  # pyright: ignore[reportReturnType]


def create_layout_from_shape_real_coordinates(shape: Shape, layout_name: str, roi_geometry: NIEnumRoiGeometry, cscan: NICartographyFrameCScan) -> NIRoiMask:
    """Create mask from given shape.

    Args:
        shape: shape source.
        layout_name: the name of the layout.
        x_res: x resolution.
        y_res: y resolution.
        roi_geometry: roi geometry type ({@link NIEnumRoiGeometry}).

    Returns:
        the mask ROI.
    """
    return _wrap_roi(gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.createLayoutFromShapeRealCoordinates(shape._java_object, layout_name, roi_geometry.to_java_enum(), cscan._java_object))  # pyright: ignore[reportReturnType]


def create_mask_from_shape(shape: Shape, x_res: float, y_res: float, roi_geometry: NIEnumRoiGeometry) -> NIRoiMask:
    """Create mask from given shape.

    Args:
        shape: shape source.
        x_res: x resolution.
        y_res: y resolution.
        roi_geometry: roi geometry type ({@link NIEnumRoiGeometry}).

    Returns:
        the mask.
    """
    return _wrap_roi(gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.createMaskFromShape(shape._java_object, x_res, y_res, roi_geometry.to_java_enum()))  # pyright: ignore[reportReturnType]


def create_mask_from_shape_real_coordinates(shape: Shape, roi_geometry: NIEnumRoiGeometry, cscan: NICartographyFrameCScan) -> NIRoiMask:
    """Create mask from given shape.

    Args:
        shape: shape source.
        x_res: x resolution.
        y_res: y resolution.
        roi_geometry: roi geometry type ({@link NIEnumRoiGeometry}).

    Returns:
        the mask.
    """
    return _wrap_roi(gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.createMaskFromShapeRealCoordinates(shape._java_object, roi_geometry.to_java_enum(), cscan._java_object))  # pyright: ignore[reportReturnType]


def create_selection_from_shape(shape: Shape, x_res: float, y_res: float, roi_geometry: NIEnumRoiGeometry) -> NIRoiSelection:
    """Create selection from given shape.

    Args:
        shape: shape source.
        x_res: x resolution.
        y_res: y resolution.
        roi_geometry: roi geometry type ({@link NIEnumRoiGeometry}).

    Returns:
        the selection.
    """
    return _wrap_roi(gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.createSelectionFromShape(shape._java_object, float(x_res), float(y_res), roi_geometry.to_java_enum()))  # pyright: ignore[reportReturnType]


def add_rois_to_cartography(target_frame: NICartographyFrame, rois: list[NIRoi]) -> None:
    """Add given rois (selections, masks or layouts) to the given cartography frame."""
    java_frame = target_frame._java_object
    java_roi_list = to_java_list([roi._java_object for roi in rois])
    gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.addRoisToCartography(java_frame, java_roi_list)


def remove_all_rois(frame: NICartographyFrame, roi_format: NIEnumRoiFormat) -> None:
    """Remove all ROIs of the given format from the provided frame."""
    gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.removeAllRois(frame._java_object, roi_format.to_java_enum())


def get_all_rois(frame: NICartographyFrame, roi_format: NIEnumRoiFormat, only_selected=False) -> List[NIRoi]:
    """Return all ROIs (wrapped) for the given frame and roi format."""
    java_list = gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.getAllRois(
        frame._java_object, roi_format.to_java_enum(), only_selected)  # type: ignore
    return _wrap_roi_list(java_list)  # type: ignore


def get_all_layouts(frame: NICartographyFrame) -> list[NIRoiLayout]:
    """Get all layouts from given C-Scan as `NIRoiLayout` wrappers."""
    java_list = gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.getAllLayouts(frame._java_object)  # type: ignore
    return _wrap_roi_list(java_list)  # type: ignore


def scale_roi(ni_roi: NIRoi, scale_x: float, scale_y: float) -> None:
    """Scale a roi; center isn't displaced."""
    gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.scaleROI(ni_roi._java_object, scale_x, scale_y)  # type: ignore


def regroup_rois(cscan: NICartographyFrame, rois_to_regroup: List[NIRoi]) -> NIRoi:
    """Regroup rois and return the grouped result as wrapped ROI objects."""
    java_roi = gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.regroupRois(
        cscan._java_object, to_java_list([roi._java_object for roi in rois_to_regroup]))
    return _wrap_roi(java_roi)  # type: ignore


def ungroup_rois(cscan: NICartographyFrame, rois_to_regroup: List[NIRoi]) -> None:
    """Ungroup given ROIs."""
    gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.ungroupRois(cscan._java_object, to_java_list([roi._java_object for roi in rois_to_regroup]))


def fill_with_value(cscan: NICartographyFrame, roi: NIRoi, value: float) -> None:
    """Change data of CScan inside the given ROI with the given value."""
    gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.fillWithValue(cscan._java_object, roi._java_object, float(value))


def read(roi_file_path: str, x_current_res: float = -1, y_current_res: float = -1) -> List[NIRoi]:
    """Read all rois from given file (selection *.sel, mask .msk or layout .drs) and wrap results."""
    if x_current_res >= 0 and y_current_res >= 0:
        java_list = gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.read(roi_file_path, x_current_res, y_current_res)
    else:
        java_list = gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.read(roi_file_path)
    return _wrap_roi_list(java_list)  # type: ignore


def draw_arrow(cscan: NICartographyFrameCScan, x1: float, y1: float, x2: float, y2: float) -> NIRoi:
    """Draw a layout arrow on the given C-Scan and return the drawn arrow object."""
    return _wrap_roi(gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.drawArrow(cscan._java_object, x1, y1, x2, y2))  # type: ignore


def display_all_layout_names() -> None:
    """Display all layout names or hide them if they are already all visible."""
    gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.displayAllLayoutNames()


def save(rois_to_save: list[NIRoi], selection_file: str) -> None:
    """Save the provided ROI inside the given file."""
    gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.save(to_java_list(
        [roi._java_object for roi in rois_to_save]), gateway.jvm.java.io.File(selection_file))  # type: ignore


def selection_mode() -> None:
    """Switch the UI into selection drawing mode."""
    gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.selectionMode()


def layout_mode() -> None:
    """Switch the UI into layout drawing mode."""
    gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.layoutMode()


def mask_mode() -> None:
    """Switch the UI into mask drawing mode."""
    gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.maskMode()


def add_rectangular_selection(cscan: NICartographyFrameCScan, x: float, y: float, width: float, height: float) -> NIRoiSelection:
    """
    Create a rectangular selection.

    Args:
        cscan: the cscan target frame.
        x: the X coordinate of the upper-left corner of the newly constructed rectangle.
        y: the Y coordinate of the upper-left corner of the newly constructed rectangle.
        width: the width of the newly constructed rectangle.
        height: the height of the newly constructed rectangle.

    Returns:
        object: the selection created.
    """
    return NIRoiSelection(gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.addRectangularSelection(cscan._java_object, float(x), float(y), float(width), float(height)))  # pyright: ignore[reportArgumentType]


def add_rectangular_layout(cscan: NICartographyFrameCScan, layout_name: str, x: float, y: float, width: float, height: float) -> NIRoiLayout:
    """
    Create a rectangular layout.

    Args:
        cscan: the cscan target frame.
        layout_name: the name of the layout that will be added. 
        x: the X coordinate of the upper-left corner of the newly constructed rectangle.
        y: the Y coordinate of the upper-left corner of the newly constructed rectangle.
        width: the width of the newly constructed rectangle.
        height: the height of the newly constructed rectangle.

    Returns:
        object: the layout created.
    """
    return NIRoiLayout(gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.addRectangularLayout(cscan._java_object, layout_name, float(x), float(y), float(width), float(height)))  # pyright: ignore[reportArgumentType]


def add_rectangular_mask(cscan: NICartographyFrameCScan, x: float, y: float, width: float, height: float) -> NIRoiMask:
    """
    Create a rectangular mask.

    Args:
        cscan: the cscan target frame.
        x: the X coordinate of the upper-left corner of the newly constructed rectangle.
        y: the Y coordinate of the upper-left corner of the newly constructed rectangle.
        width: the width of the newly constructed rectangle.
        height: the height of the newly constructed rectangle.

    Returns:
        object: the mask created.
    """
    return NIRoiMask(gateway.jvm.agi.ndtkit.api.NDTKitROIInterface.addRectangularMask(cscan._java_object, float(x), float(y), float(width), float(height)))  # pyright: ignore[reportArgumentType]
