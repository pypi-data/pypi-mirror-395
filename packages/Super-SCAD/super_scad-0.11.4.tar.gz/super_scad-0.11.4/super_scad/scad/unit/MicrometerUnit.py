from super_scad.scad.Unit import Unit
from super_scad.scad.unit.LengthUnit import LengthUnit


class MicrometerUnit(LengthUnit):
    """
    The metric micrometer.

    """

    # ------------------------------------------------------------------------------------------------------------------
    def id(self) -> int:
        """
        Returns the ID or enumeration value of this unit of length.
        """
        return Unit.UM.value

    # ------------------------------------------------------------------------------------------------------------------
    def meters(self) -> float:
        """
        Returns one micrometer expressed in meters.
        """
        return 1e-6

# ----------------------------------------------------------------------------------------------------------------------
