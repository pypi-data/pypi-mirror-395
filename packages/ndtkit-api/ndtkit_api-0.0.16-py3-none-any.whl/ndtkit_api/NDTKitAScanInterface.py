from .ndtkit_socket_connection import gateway
from .model.frame.NICartographyFrameAScan import NICartographyFrameAScan
from .model.ascan.NIAScanConfiguration import NIAScanConfiguration


def open_ascan(ascanFilePath: str, scanId: int = -1, displayResult: bool = True) -> NICartographyFrameAScan:
    """Open an A-scan file using default configuration.
    
    Args:
        ascanFilePath (str): The file path to open
        scanId (int, optional): The ID of the A-Scan in file tree. Use -1 if file doesn't 
                              have several a-scan representations. Defaults to -1.
        displayResult (bool, optional): If True, displays frame in NDTKit application. 
                                      Defaults to True.
    
    Returns:
        NICartographyFrameAScan: The created A-scan cartography frame
        
    Raises:
        NIApiException: If an error occurs during file opening
    """
    ascan_frame_java = gateway.jvm.agi.ndtkit.api.NDTKitAScanInterface.openAScan(ascanFilePath, scanId, displayResult)
    return NICartographyFrameAScan(ascan_frame_java)  # pyright: ignore[reportArgumentType]


def read_nkap_file(nkap_file: str) -> NIAScanConfiguration:
    """Read an NKAP configuration file containing A-scan settings.
    
    Args:
        nkap_file (str): Path to the NKAP configuration file containing gates, gain, 
                        and other A-scan settings
    
    Returns:
        NIAScanConfiguration: The A-scan configuration object containing the loaded settings
        
    Raises:
        NIApiException: If an error occurs reading the configuration file
    """
    ascan_config = gateway.jvm.agi.ndtkit.api.NDTKitAScanInterface.readNKAPFile(nkap_file)
    return NIAScanConfiguration(ascan_config)  # pyright: ignore[reportArgumentType]
