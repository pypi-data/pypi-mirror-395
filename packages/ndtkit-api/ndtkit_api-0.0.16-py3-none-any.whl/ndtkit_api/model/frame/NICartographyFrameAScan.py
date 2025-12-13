from .NICartographyFrame import NICartographyFrame
from ...model.scans.ascan.NIAScan import NIAScan
from py4j.java_gateway import JavaObject
from ...ndtkit_socket_connection import call_api_method


class NICartographyFrameAScan(NICartographyFrame):
    """Represents an A-scan cartography frame that contains a 2D grid of ultrasonic A-scan data.

    This class extends NICartographyFrame to provide specialized functionality for working with
    A-scan data, including access to raw waveforms, B-scan and D-scan views, gate configurations,
    and spatial metadata. It serves as the main container for ultrasonic inspection data
    captured in A-scan mode.
    """

    def __init__(self, java_object: JavaObject):
        """Initialize the A-scan cartography frame with a Java object.

        Args:
            java_object (JavaObject): The underlying Java NICartographyFrameAScan object
        """
        super().__init__(java_object)
        self._java_object = java_object

    def get_file_path(self) -> str:
        """Get the file path associated with this cartography frame.

        Returns:
            str: The absolute file path
        """
        return self._java_object.getFilePath()

    def get_raw_data_values(self, row: int, column: int) -> NIAScan:
        """Get the raw A-scan data at the specified grid position.

        Args:
            row (int): Row index in the cartography grid
            column (int): Column index in the cartography grid

        Returns:
            NIAScan: The raw A-scan data object
        """
        return self._java_object.getRawDataValues(row, column)

    def get_raw_data_values_no_factor(self, row: int, column: int) -> NIAScan:
        """Get the raw A-scan data without any scaling factors applied.

        Args:
            row (int): Row index in the cartography grid
            column (int): Column index in the cartography grid

        Returns:
            NIAScan: The unscaled raw A-scan data object
        """
        return self._java_object.getRawDataValuesNoFactor(row, column)

    def get_ascan_length(self) -> int:
        """Get the number of samples in each A-scan.

        Returns:
            int: The number of samples per A-scan
        """
        return self._java_object.getAscanLength()

    def get_row(self, row_index: int) -> list[NIAScan]:
        """Get all A-scans in a specified row.

        Args:
            row_index (int): The row index to retrieve

        Returns:
            list[NIAScan]: List of A-scan objects in the row
        """
        row_of_ascans = self._java_object.getRow(row_index)
        return [NIAScan(ascan) for ascan in row_of_ascans]

    def get_column(self, column_index: int) -> list[NIAScan]:
        """Get all A-scans in a specified column.

        Args:
            row_column (int): The column index to retrieve

        Returns:
            List[Any]: List of A-scan objects in the column
        """
        column_of_ascans = self._java_object.getColumn(column_index)
        return [NIAScan(ascan) for ascan in column_of_ascans]

    def get_data_values(self, row: int, column: int) -> NIAScan:
        """Get the processed A-scan data at the specified grid position.

        Args:
            row (int): Row index in the cartography grid
            column (int): Column index in the cartography grid

        Returns:
            NIAScan: The processed A-scan data object
        """
        return self._java_object.getDataValues(row, column)

    def get_row_number(self) -> int:
        """Get the total number of rows in the cartography grid.

        Returns:
            int: The number of rows
        """
        return self._java_object.getRowNumber()

    def get_column_number(self) -> int:
        """Get the total number of columns in the cartography grid.

        Returns:
            int: The number of columns
        """
        return self._java_object.getColumnNumber()

    def get_x_resolution(self) -> float:
        """Get the spatial resolution in the X direction.

        Returns:
            float: The X resolution in millimeters
        """
        return self._java_object.getXResolution()

    def get_y_resolution(self) -> float:
        """Get the spatial resolution in the Y direction.

        Returns:
            float: The Y resolution in millimeters
        """
        return self._java_object.getYResolution()

    def get_num_rate(self) -> float:
        """Get the data digitalization rate.

        Returns:
            float: The digitalization rate in ns
        """
        return self._java_object.getNumRate()

    def set_full_range_bscan(self):
        """Configure B-scan to display the full depth range."""
        self._java_object.setFullRangeBScan()

    def get_ascan_gates(self):
        """Get all A-scan gates configured for this frame.

        Returns:
            list[NIAScanGate]: List of configured A-scan gates
        """
        return self._java_object.getAScanGates()

    def get_bscan_gate(self):
        """Get the gate used for B-scan display.

        Returns:
            NIAScanGate: The B-scan gate configuration
        """
        return self._java_object.getBScanGate()

    def get_velocity_from_file(self) -> float:
        """Get the ultrasonic velocity value stored in the data file.

        Returns:
            float: The ultrasonic velocity in meters per second
        """
        return self._java_object.getVelocityFromFile()

    def get_bscan_vertical_resolution(self) -> float:
        """Get the vertical resolution of the B-scan display.

        Returns:
            float: The B-scan vertical resolution in millimeters/pixel
        """
        return self._java_object.getBScanVerticalResolution()

    def get_bscan_data(self, bscan_position: int) -> list[list[float]]:
        """Get the B-scan data at a specified position.

        Args:
            bscan_position (int): The position index for the B-scan

        Returns:
            List[List[float]]: 2D array of B-scan amplitude values
        """
        return self._java_object.getBScanData(bscan_position)

    def get_dscan_data(self, dscan_position: int) -> list[list[float]]:
        """Get the D-scan data at a specified position.

        Args:
            dscan_position (int): The position index for the D-scan

        Returns:
            List[List[float]]: 2D array of D-scan amplitude values
        """
        return self._java_object.getDScanData(dscan_position)

    def get_acquisition_type(self):
        """Get the type of data acquisition used.

        Returns:
            Any: The acquisition type identifier
        """
        return self._java_object.getAcquisitionType()

    def set_x_origin_position(self, x_offset: float):
        """Set the X coordinate origin offset.

        Args:
            x_offset (float): The X offset in millimeters
        """
        self._java_object.setXOriginPosition(x_offset)

    def set_y_origin_position(self, y_offset: float):
        """Set the Y coordinate origin offset.

        Args:
            y_offset (float): The Y offset in millimeters
        """
        self._java_object.setYOriginPosition(y_offset)

    def get_x_origin_position(self) -> float:
        """Get the X coordinate origin offset.

        Returns:
            float: The X offset in millimeters
        """
        return self._java_object.getXOriginPosition()

    def get_y_origin_position(self) -> float:
        """Get the Y coordinate origin offset.

        Returns:
            float: The Y offset in millimeters
        """
        return self._java_object.getYOriginPosition()

    def get_current_ascan(self) -> NIAScan:
        """Get the currently selected A-scan.

        Returns:
            NIAScan: The current A-scan object
        """
        return self._java_object.getCurrentAscan()

    def get_row_tof_amp(self, index_row: int) -> list[list[list[float]]]:
        parameters = [
            {
                "type": "agi.ndtkit.api.model.frame.NICartographyFrameAScan",
                "value": self.get_uuid(),
            },
            {
                "type": "int",
                "value": index_row
            },
        ]
        return call_api_method("agi.ndtkit.api.model.frame", "NICartographyFrameAScan", "getRowTofAmp", parameters)  # type: ignore
