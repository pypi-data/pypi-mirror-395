from super_scad.scad.Unit import Unit
from super_scad.scad.unit.LengthUnit import LengthUnit


class KilometerUnit(LengthUnit):
    """
    The metric kilometer.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def id(self) -> int:
        """
        Returns the ID or enumeration value of this unit of length.
        """
        return Unit.KM.value

    # ------------------------------------------------------------------------------------------------------------------
    def meters(self) -> float:
        """
        Returns one kilometer expressed in meters.
        """
        return 1e3

# ----------------------------------------------------------------------------------------------------------------------
