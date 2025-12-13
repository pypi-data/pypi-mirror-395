from py4j.java_gateway import JavaObject

from .ScanType import ScanType


class NICartographyFrame:
    """Abstract base class representing a cartography frame in NDTKit.

    This class is extended by specific frame types like AScan, CScan, BScan, etc. It provides
    common functionality for managing frame display and accessing frame data.
    """

    def __init__(self, java_object: JavaObject):
        """Initialize with a Java NDTKitInternalFrame object.

        Args:
            java_object (JavaObject): The underlying Java NDTKitInternalFrame object
        """
        self._java_object = java_object

    def minimize_frame(self, is_minimum: bool):
        """This frame is minimized.

        Args:
            is_minimum (bool): minimize frame if true, restore if false
        """
        self._java_object.minimizeFrame(is_minimum)

    def set_title(self, title: str):
        """Set the title of this frame.

        Args:
            title (str): The new title to display
        """
        self._java_object.setTitle(title)

    def get_scan_type(self):
        """Get the scan type of this frame.

        Returns:
            ScanType: The type of scan (ASCAN, BSCAN, CSCAN, etc.)
        """
        return ScanType(self._java_object.getScanType())

    def maximize_frame(self, is_maximum: bool):
        """This frame is resized to fully fit the software.

        Args:
            is_maximum (bool): maximize frame if true, restore if false
        """
        self._java_object.maximizeFrame(is_maximum)

    def get_projection_cuboid(self):
        """Retrieve the 3D projection cuboid that has been used for generating this frame.

        Returns:
            NIParallelepiped: The projection cuboid linked to this frame, or None if this
            frame doesn't come from a 3D frame
        """
        return self._java_object.getProjectionCuboid()

    def get_size(self):
        """Get the dimension of this frame.

        Returns:
            Dimension: The dimension of this frame
        """
        return self._java_object.getSize()

    def get_title(self) -> str:
        """Get the current frame title.

        Returns:
            str: The title of this frame
        """
        return self._java_object.getTitle()

    def json_of_scan_reader_parameter(self) -> str:
        """Get the scan reader parameters as JSON.

        Returns:
            str: JSON string containing the scan reader parameters
        """
        return self._java_object.jsonOfScanReaderParameter()

    def get_uuid(self) -> str:
        """Returns a unique identifier that can be used to identify NICartographyFrame 
        objects that point to the same internal frame.

        Returns:
            str: The UUID as a string
        """
        return str(self._java_object.getUUID())

    def get_file_path(self) -> str:
        """Get the origin file path of current frame.

        Returns:
            str: The absolute file path
        """
        return self._java_object.getFilePath()

    def set_file_path(self, filepath: str):
        """Change the file path of this frame.

        Args:
            filepath (str): The new file path to set
        """
        self._java_object.setFilePath(filepath)

    def change_size(self, width: int, height: int):
        """Change the size of this frame to the given dimensions.

        Args:
            width (int): the new width that will be applied
            height (int): the new height that will be applied
        """
        self._java_object.changeSize(width, height)

    def close(self):
        """Close this frame."""
        self._java_object.close()
