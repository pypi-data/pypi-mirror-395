from py4j.java_gateway import JavaObject


class NIAScan:
    """Represents a single A-scan waveform with amplitude and time-of-flight data.

    An A-scan is an ultrasonic waveform that represents reflected ultrasonic energy
    as a function of time. This class provides access to the amplitude values,
    time-of-flight measurements, and any sub-scans that may be part of a more
    complex scanning pattern.
    """

    def __init__(self, java_object: JavaObject, json_model=None):
        """Initialize an A-scan object.

        Args:
            java_object (JavaObject): The underlying Java NIAScan object
            json_model (dict, optional): Optional JSON model containing cached data.
                                       Defaults to None.
        """
        self._java_object = java_object
        self.json_model = json_model

    def get_all_tof_values_from_this_ascan_and_sub_ascans(self) -> list[float]:
        """Get all time-of-flight values from this A-scan and its sub-scans.

        Returns:
            list[float]: List of time-of-flight values in microseconds
        """
        return self._java_object.getAllTofValuesFromThisAScanAndSubAscans()

    def get_all_amp_values_from_this_ascan_and_sub_ascans(self) -> list[float]:
        """Get all amplitude values from this A-scan and its sub-scans.

        Returns:
            list[float]: List of amplitude values in percentage of full scale
        """
        return self._java_object.getAllAmpValuesFromThisAScanAndSubAscans()

    def get_amp_values(self) -> list[float]:
        """Get the amplitude values for this A-scan.

        First checks for cached values in the JSON model, then falls back to
        retrieving from the Java object.

        Returns:
            list[float]: List of amplitude values in percentage of full scale
        """
        if self.json_model and "amp" in self.json_model:
            return self.json_model["amp"]
        return self._java_object.getAmpValues()

    def get_tof_values(self) -> list[float]:
        """Get the time-of-flight values for this A-scan.

        Returns:
            list[float]: List of time-of-flight values in microseconds
        """
        return self._java_object.getTofValues()

    def get_sub_ascans(self):
        """Get any sub-scans associated with this A-scan.

        Returns:
            list[NIAScan]: List of sub-scan objects, or None if no sub-scans exist
        """
        return self._java_object.getSubAscans()

    def get_row(self) -> int:
        """Get the row index of this A-scan in its parent cartography grid.

        Returns:
            int: The row index
        """
        return self._java_object.getRow()

    def get_column(self) -> int:
        """Get the column index of this A-scan in its parent cartography grid.

        Returns:
            int: The column index
        """
        return self._java_object.getColumn()
