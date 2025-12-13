from super_scad.scad.Unit import Unit
from super_scad.scad.unit.LengthUnit import LengthUnit


class MillimeterUnit(LengthUnit):
    """
    The metric millimeter.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def id(self) -> int:
        """
        Returns the ID or enumeration value of this unit of length.
        """
        return Unit.MM.value

    # ------------------------------------------------------------------------------------------------------------------
    def meters(self) -> float:
        """
        Returns one millimeter expressed in meters.
        """
        return 1e-3

# ----------------------------------------------------------------------------------------------------------------------
