from .ndtkit_socket_connection import gateway, call_api_method
from .model.frame.NICartographyFrameCScan import NICartographyFrameCScan
from . import NDTKitCartographyFrameInterface
from .model.frame.ScanType import ScanType


def open_cscan(cscanFilePath: str, displayResult: bool = True) -> NICartographyFrameCScan:
    """Load a C-scan from a file and optionally display it in NDTKit.

    If the file is a multi C-scan container, a file tree will be displayed
    and the user must select a C-scan to open.

    Args:
        cscanFilePath (str): Path to the file to open. Should be a valid C-scan file.
        displayResult (bool, optional): If False, prevents the C-scan from being displayed 
            in the interface. Defaults to True.

    Returns:
        NICartographyFrameCScan: The loaded C-scan frame object.

    Raises:
        NIApiException: If an error occurs during loading (file doesn't exist, 
            invalid format, etc.).
    """
    cscan_frame_java = gateway.jvm.agi.ndtkit.api.NDTKitCScanInterface.openCScan(cscanFilePath, displayResult)[0]  # pyright: ignore[reportIndexIssue]
    return NICartographyFrameCScan(cscan_frame_java)


def save_cscan(cscan: NICartographyFrameCScan, filepath: str):
    """Save a C-scan frame to a file in NKC format.

    Args:
        cscan (NICartographyFrameCScan): The C-scan frame to save
        filepath (str): The path where the file will be saved

    Raises:
        NIApiException: If an error occurs during file writing
    """
    gateway.jvm.agi.ndtkit.api.NDTKitCScanInterface.saveCscan(cscan._java_object, filepath)  # type: ignore


def create_cscan(data: list[list[float]], acquisition_name: str, x_res: float, y_res: float) -> NICartographyFrameCScan | None:
    """Create a new C-scan from 2D data array and display it.

    Args:
        data (list[list[float]]): 2D array of float data representing the C-scan values
        acquisition_name (str): Name for the C-scan (used for association)
        x_res (float): X-axis resolution in millimeters
        y_res (float): Y-axis resolution in millimeters

    Returns:
        NICartographyFrameCScan | None: The created C-scan frame, or None if creation fails

    Raises:
        NIApiException: If an error occurs during C-scan creation
    """
    parameters = [
        {
            "type": "float[][]",
            "value": str(data)
        },
        {
            "type": "java.lang.String",
            "value": acquisition_name
        },
        {
            "type": "float",
            "value": x_res
        },
        {
            "type": "float",
            "value": y_res
        }
    ]
    json_result = call_api_method("agi.ndtkit.api", "NDTKitCScanInterface", "createCscan", parameters)
    return NDTKitCartographyFrameInterface.get_frame(json_result["uuid"], ScanType.C_SCAN)  # type: ignore
