from typing import Any, List
from ...ndtkit_socket_connection import call_api_method
from .NICartographyFrame import NICartographyFrame
from ..framecomponents.palette.NIColorPalette import NIColorPalette


class NICartographyFrameCScan(NICartographyFrame):
    """Represents a C-scan frame in NDTKit.

    A C-scan is a 2D ultrasonic scan that displays amplitude or time-of-flight data.
    This class extends NICartographyFrame to provide C-scan specific functionality including:
    - Data access and manipulation 
    - Resolution and origin position control
    - Palette management
    - Zooming and geometric transformations
    - Defect detection
    - Screenshot capabilities
    - Metadata handling

    The C-scan data is represented as a 2D array of float values, with methods to get/set this data
    as well as access properties like resolution, unit type, and position information.
    """

    def get_identifier(self) -> int:
        """Get the unique identifier for this C-scan frame.

        Returns:
            int: The identifier number
        """
        return self._java_object.getIdentifier()

    def set_identifier(self, id: int):
        """Set the unique identifier for this C-scan frame.

        Args:
            id (int): The new identifier to assign
        """
        self._java_object.setIdentifier(id)

    def get_x_resolution(self) -> float:
        """Get the X-axis resolution of the C-scan in mm.

        Returns:
            float: The X resolution value in millimeters
        """
        return self._java_object.getXResolution()

    def get_y_resolution(self) -> float:
        """Get the Y-axis resolution of the C-scan in mm.

        Returns:
            float: The Y resolution value in millimeters
        """
        return self._java_object.getYResolution()

    def get_x_origin(self) -> float:
        """Get the X coordinate of the C-scan origin in mm.

        Returns:
            float: X coordinate of the origin in millimeters
        """
        return self._java_object.getXOrigin()

    def get_intrinsic_x_origin(self) -> float:
        """Get the intrinsic X coordinate of the C-scan origin.
        This represents the original X origin before any transformations.

        Returns:
            float: Intrinsic X coordinate of the origin
        """
        return self._java_object.getIntrinsicXOrigin()

    def get_y_origin(self) -> float:
        """Get the Y coordinate of the C-scan origin in mm.

        Returns:
            float: Y coordinate of the origin in millimeters
        """
        return self._java_object.getYOrigin()

    def get_intrinsic_y_origin(self) -> float:
        """Get the intrinsic Y coordinate of the C-scan origin.
        This represents the original Y origin before any transformations.

        Returns:
            float: Intrinsic Y coordinate of the origin
        """
        return self._java_object.getIntrinsicYOrigin()

    def get_data_bound(self, roi) -> List[List[float]]:
        """Get the data values within the bounds of a Region of Interest (ROI).

        Args:
            roi: The Region of Interest object defining the bounds

        Returns:
            List[List[float]]: 2D array of data values within the ROI bounds
        """
        return self._java_object.getDataBound(roi)

    def get_flat_data(self, roi=None) -> List[Any]:
        """Get the C-scan data as a flattened 1D array.

        Args:
            roi: Optional Region of Interest to limit data retrieval

        Returns:
            List[Any]: Flattened array of C-scan data values
        """
        return self._java_object.getFlatData(roi) if roi else self._java_object.getFlatData()

    def add_processing_into_historic_list(self, text: str):
        """Add a processing step description to the frame's processing history.

        Args:
            text (str): Description of the processing step to record
        """
        self._java_object.addProcessingIntoHistoricList(text)

    def get_file_path(self) -> str:
        """Get the file path from which this C-scan was loaded.

        Returns:
            str: Absolute path to the source file
        """
        return self._java_object.getFilePath()

    def set_automation_identifier(self, report_identifier: str):
        """Set the automation identifier used for automated report generation.

        Args:
            report_identifier (str): The identifier to use for automation/reporting
        """
        self._java_object.setAutomationIdentifier(report_identifier)

    def get_automation_identifier(self) -> str:
        """Get the automation identifier used for automated report generation.

        Returns:
            str: The current automation/report identifier
        """
        return self._java_object.getAutomationIdentifier()

    def get_unit(self):
        """Get the measurement unit type for the C-scan data.

        Returns:
            NIEnumUnit: The unit type (e.g. PERCENT, DB, MM, etc.)
        """
        return self._java_object.getUnit()

    def get_palette(self) -> NIColorPalette:
        """Get the color palette used for displaying the C-scan.

        Returns:
            NIColorPalette: The current color palette object
        """
        return NIColorPalette(self._java_object.getPalette())

    def load_palette(self, palette_pathname: str):
        """Load a color palette from a file for coloring the C-scan.

        Args:
            palette_pathname (str): Path to the palette file to load
        """
        self._java_object.loadPalette(palette_pathname)

    def get_defects_detection(self):
        """Get the defect detection results for this C-scan.

        Returns:
            Any: Object containing defect detection information
        """
        return self._java_object.getDefectsDetection()

    def zoom(self, x: float, y: float, width: float, height: float, ignore_ratio: bool = False):
        """Zoom the C-scan display to a specified region.

        Args:
            x (float): X coordinate of the zoom region in mm
            y (float): Y coordinate of the zoom region in mm
            width (float): Width of the zoom region in mm
            height (float): Height of the zoom region in mm
            ignore_ratio (bool, optional): If True, ignore aspect ratio constraints. Defaults to False.
        """
        self._java_object.zoom(x, y, width, height, ignore_ratio)

    def rotate(self, angle: int):
        """Rotate the C-scan by a specified angle.

        Args:
            angle (int): Rotation angle in degrees
        """
        self._java_object.rotate(angle)

    def horizontal_symmetry(self):
        """Apply horizontal symmetry (flip) to the C-scan image."""
        self._java_object.horizontalSymmetry()

    def vertical_symmetry(self):
        """Apply vertical symmetry (flip) to the C-scan image."""
        self._java_object.verticalSymmetry()

    def get_amplitude_reference(self) -> float:
        """Get the reference amplitude value for dB calculations.

        Returns:
            float: The reference amplitude value
        """
        return self._java_object.getAmplitudeReference()

    def get_velocity(self) -> float:
        """Get the ultrasonic wave velocity used for time-of-flight calculations.

        Returns:
            float: The velocity value in meters/second
        """
        return self._java_object.getVelocity()

    def get_ply_thickness(self) -> float:
        """Get the ply thickness used for layer calculations.

        Returns:
            float: The ply thickness in millimeters
        """
        return self._java_object.getPlyThickness()

    def get_screenshot(self, representation_type, display_palette: bool, display_roi_layer: bool,
                       display_mask_layer: bool, display_defect_layer: bool, display_dressing_layer: bool,
                       display_rulers: bool, display_at_real_size: bool):
        """Capture a screenshot of the C-scan display with specified options.

        Args:
            representation_type: Type of image representation
            display_palette (bool): Whether to display the color palette
            display_roi_layer (bool): Whether to display Regions of Interest
            display_mask_layer (bool): Whether to display masks
            display_defect_layer (bool): Whether to display detected defects
            display_dressing_layer (bool): Whether to display dressing elements
            display_rulers (bool): Whether to display measurement rulers
            display_at_real_size (bool): Whether to capture at actual size

        Returns:
            Any: The captured screenshot image
        """
        return self._java_object.getScreenshot(representation_type, display_palette, display_roi_layer,
                                               display_mask_layer, display_defect_layer, display_dressing_layer,
                                               display_rulers, display_at_real_size)

    def set_unit_without_conversion(self, unit):
        """Change the unit type without converting the underlying data values.

        Args:
            unit (NIEnumUnit): The new unit type to set
        """
        self._java_object.setUnitWithoutConversion(unit)

    def set_resolution_unit(self, unit):
        """Set the unit type for resolution measurements.

        Args:
            unit (NIEnumUnit): The unit type to use for resolution
        """
        self._java_object.setResolutionUnit(unit)

    def set_y_origin_position(self, position_in_mm: float):
        """Set the Y coordinate of the C-scan origin.

        Args:
            position_in_mm (float): Y position in millimeters
        """
        self._java_object.setYOriginPosition(position_in_mm)

    def set_x_origin_position(self, position_in_mm: float):
        """Set the X coordinate of the C-scan origin.

        Args:
            position_in_mm (float): X position in millimeters
        """
        self._java_object.setXOriginPosition(position_in_mm)

    def get_comment(self) -> str:
        """Get the comment associated with this C-scan.

        Returns:
            str: The comment text
        """
        return self._java_object.getComment()

    def set_comment(self, comment: str):
        """Set a comment for this C-scan.

        Args:
            comment (str): The comment text to set
        """
        self._java_object.setComment(comment)

    def get_min_value(self) -> float:
        """Get the minimum data value in the C-scan.

        Returns:
            float: The minimum value
        """
        return self._java_object.getMinValue()

    def get_max_value(self) -> float:
        """Get the maximum data value in the C-scan.

        Returns:
            float: The maximum value
        """
        return self._java_object.getMaxValue()

    def get_metadata(self, metadata_id: str) -> Any:
        """Get metadata associated with a specific identifier.

        Args:
            metadata_id (str): The identifier of the metadata to retrieve

        Returns:
            Any: The metadata value
        """
        return self._java_object.getMetadata(metadata_id)

    def set_metadata(self, metadata_id: str, metadata: Any):
        """Set metadata with a specific identifier.

        Args:
            metadata_id (str): The identifier for the metadata
            metadata (Any): The metadata value to store
        """
        self._java_object.setMetadata(metadata_id, metadata)

    def apply_zoom(self, zoom_fit):
        """Apply a zoom preset to the C-scan display.

        Args:
            zoom_fit: The zoom preset to apply
        """
        self._java_object.applyZoom(zoom_fit)

    def get_event_manager(self):
        """Get the event manager for this C-scan frame.

        Returns:
            Any: The event manager object
        """
        return self._java_object.getEventManager()

    def is_still_displayed(self) -> bool:
        """Check if this C-scan frame is still being displayed.

        Returns:
            bool: True if the frame is displayed, False otherwise
        """
        return self._java_object.isStillDisplayed()

    def request_focus(self):
        """Request keyboard/input focus for this C-scan frame."""
        self._java_object.requestFocus()

    def get_zoom_factor_x(self) -> float:
        """Get the current X-axis zoom factor.

        Returns:
            float: The X zoom factor
        """
        return self._java_object.getZoomFactorX()

    def get_zoom_factor_y(self) -> float:
        """Get the current Y-axis zoom factor.

        Returns:
            float: The Y zoom factor
        """
        return self._java_object.getZoomFactorY()

    def get_dynamic_layer_manager(self):
        """Get the manager for dynamic display layers.

        Returns:
            Any: The dynamic layer manager object
        """
        return self._java_object.getDynamicLayerManager()

    def refresh_layers(self):
        """Force a refresh of all display layers in the C-scan frame."""
        self._java_object.refreshLayers()

    def duplicate(self) -> 'NICartographyFrameCScan':
        """Create a duplicate copy of this C-scan frame.

        Returns:
            NICartographyFrameCScan: A new C-scan frame with the same data and settings
        """
        return NICartographyFrameCScan(self._java_object.duplicate())

    def json_of_scan_reader_parameter(self) -> str:
        """Get the scan reader parameters as a JSON string.

        Returns:
            str: JSON representation of reader parameters
        """
        return self._java_object.jsonOfScanReaderParameter()

    def set_auto_update_data(self, auto_update_data: bool):
        """Enable or disable automatic data updates.

        Args:
            auto_update_data (bool): True to enable auto updates, False to disable
        """
        self._java_object.setAutoUpdateData(auto_update_data)

    def update_data(self, update_palette: bool):
        """Force an update of the C-scan data and optionally the palette.

        Args:
            update_palette (bool): True to also update the color palette
        """
        self._java_object.updateData(update_palette)

    def get_projection_cuboid(self):
        """Get the 3D projection cuboid used to generate this C-scan.

        Returns:
            NIParallelepiped: The 3D projection cuboid or None if not from a 3D scan
        """
        return self._java_object.getProjectionCuboid()

    def get_position3d(self, real_x: float, real_y: float):
        """Get the 3D position for a point in the C-scan's 2D coordinates.

        Args:
            real_x (float): X coordinate in the C-scan in mm
            real_y (float): Y coordinate in the C-scan in mm

        Returns:
            NIPosition3D: The corresponding 3D position
        """
        return self._java_object.getPosition3d(real_x, real_y)

    def get_horizontal_echodynamic_curve(self):
        """Get the horizontal echodynamic curve data.
        This represents signal amplitude variation along horizontal scan lines.

        Returns:
            Any: The horizontal echodynamic curve data
        """
        return self._java_object.getHorizontalEchodynamicCurve()

    def get_vertical_echodynamic_curve(self):
        """Get the vertical echodynamic curve data.
        This represents signal amplitude variation along vertical scan lines.

        Returns:
            Any: The vertical echodynamic curve data
        """
        return self._java_object.getVerticalEchodynamicCurve()

    def get_data(self, roi=None) -> list[list[float]]:
        """Get the 2D array of C-scan data values.

        Args:
            roi: Optional Region of Interest to limit data retrieval

        Returns:
            list[list[float]]: 2D array of C-scan amplitude or time-of-flight values
        """
        if (roi):
            return self._java_object.get_data(roi)

        parameters = [
            {
                "type": "agi.ndtkit.api.model.frame.NICartographyFrameCScan",
                "value": self.get_uuid(),
            }
        ]
        return call_api_method("agi.ndtkit.api.model.frame", "NICartographyFrameCScan", "getData", parameters)  # pyright: ignore[reportReturnType]

    def set_data(self, data: list[list[float]]):
        """Set the 2D array of C-scan data values.

        Args:
            data (list[list[float]]): 2D array of values to set as the C-scan data
        """
        parameters = [
            {
                "type": "agi.ndtkit.api.model.frame.NICartographyFrameCScan",
                "value": self.get_uuid(),
            },
            {
                "type": "float[][]",
                "value": str(data)
            }
        ]
        call_api_method("agi.ndtkit.api.model.frame", "NICartographyFrameCScan", "setData", parameters)
