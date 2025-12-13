from py4j.java_gateway import JavaObject


class NIAScanGate:
    """
    Represents an A-scan gate.
    """

    def __init__(self, java_object: JavaObject):
        """Initialize the gate with a Java object.

        Args:
            java_object (JavaObject): The underlying Java NIAScanGate object
        """
        self._java_object = java_object

    def set_velocity(self, us_velocity: float):
        """Set the ultrasonic velocity for this gate.

        Args:
            us_velocity (float): The ultrasonic velocity in meters per second
        """
        self._java_object.setVelocity(us_velocity)

    def get_start(self) -> float:
        """Get the start position of the gate.

        Returns:
            float: The start position in microseconds
        """
        return self._java_object.getStart()

    def get_end(self) -> float:
        """Get the end position of the gate.

        Returns:
            float: The end position in microseconds
        """
        return self._java_object.getEnd()

    def get_height(self) -> float:
        """Get the height threshold (in %) of the gate.

        Returns:
            float: The gate height threshold in percentage of full scale
        """
        return self._java_object.getHeight()

    def get_name(self) -> str:
        """Get the name of this gate.

        Returns:
            str: The gate name
        """
        return self._java_object.getName()
