from py4j.java_gateway import JavaObject
from .NIAScanGate import NIAScanGate


class NIAScanConfiguration:
    """A class representing the AScan configuration that contains settings for gates, gain, and FFT.
    This configuration is used when working with A-Scan data in NDTKit.

    This class wraps the Java NIAScanConfiguration object and provides access to its functionality
    through the Python interface.
    """

    def __init__(self, java_object: JavaObject):
        """Initialize the NIAScanConfiguration with a Java object.

        Args:
            java_object (JavaObject): The underlying Java NIAScanConfiguration object
        """
        self._java_object = java_object

    def get_gates(self) -> list[NIAScanGate]:
        """Gets the list of A-Scan gates configured for this scan.

        Returns:
            list[NIAScanGate]: A list of gate objects
        """
        return [NIAScanGate(gate) for gate in self._java_object.getGates()]

    def get_gain(self) -> float:
        """Gets the gain value configured for this A-Scan.

        Returns:
            float: The gain value in decibels (dB)
        """
        return self._java_object.getGain()

    def get_fft_gate(self) -> NIAScanGate:
        """Gets the FFT gate configuration used for frequency analysis.

        Returns:
            NIAScanGate: The gate configuration used for FFT analysis
        """
        return NIAScanGate(self._java_object.getFftGate())
