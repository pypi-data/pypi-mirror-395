from ..ndtkit_socket_connection import gateway
from enum import unique
from ..enum_wrapper import EnumWrapper

_ALL_SPECIAL_VALUES_CACHE: list[int] | None = None


@unique
class NIEnumSpecialValue(EnumWrapper):
    """Helper class for handling NDTKit's special values in data.

    This class provides access to and validation of special numerical values
    that represent specific states in NDTKit's data processing. These include:

    Special Values:
        - NOE (No Echo): Indicates no ultrasonic echo was detected
        - NOS (No Synchro): Indicates a synchronization failure
        - MASK: Masked or suppressed data point (equivalent to 'sup')
        - NAN (Not a Number): Indicates no acquisition was made at this point
        - ERROR: Indicates an error value

    The class caches the list of special values from the Java API for efficient
    repeated access and provides methods to check if a value is a special value.
    """

    NOE = "NOE"
    NOS = "NOS"
    MASK = "MASK"
    NAN = "NAN"
    ERROR = "ERROR"

    @staticmethod
    def get_all_values() -> list[int]:
        """Get a list of all defined special values.

        This method caches the values from the Java API on first call for efficiency.
        Subsequent calls return the cached values.

        Returns:
            list[int]: List of integer codes representing special values (NOE, NOS, etc.)
        """
        global _ALL_SPECIAL_VALUES_CACHE
        if _ALL_SPECIAL_VALUES_CACHE is None:
            special_values_java = gateway.jvm.agi.ndtkit.api.model.NIEnumSpecialValue.getAllValues()
            _ALL_SPECIAL_VALUES_CACHE = [
                int(special_value)
                for special_value in special_values_java
            ] if special_values_java else []

        return _ALL_SPECIAL_VALUES_CACHE

    @staticmethod
    def is_special_value(value: float) -> bool:
        """Test if a value matches any of the defined special values.

        A small tolerance (1E-6) is used for floating point comparisons to account
        for potential numerical precision differences.

        Args:
            value (float): The value to test

        Returns:
            bool: True if the value matches a special value within tolerance,
                False otherwise
        """
        for special_value in NIEnumSpecialValue.get_all_values():
            if abs(special_value - value) < 1E-6:
                return True
        return False

    def get_java_enum_class_path(self) -> str:
        return "agi.ndtkit.api.model.NIEnumSpecialValue"

    def get_value(self) -> int:
        return self.to_java_enum().getValue()
