from py4j.java_gateway import JavaObject


class NIColorPalette:
    """Represents a color palette used for displaying C-scans in NDTKit."""

    def __init__(self, java_object: JavaObject):
        """Initialize the NIColorPalette with a Java object.

        Args:
            java_object (JavaObject): The underlying Java NIColorPalette object
        """
        self._java_object = java_object

    def real_limits(self):
        """Set the limits of the color palette to minimal and maximal values contained in the C-scan."""
        self._java_object.realLimits()
