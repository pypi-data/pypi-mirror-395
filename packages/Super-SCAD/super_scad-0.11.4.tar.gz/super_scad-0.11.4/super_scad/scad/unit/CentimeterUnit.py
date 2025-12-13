from super_scad.scad.Unit import Unit
from super_scad.scad.unit.LengthUnit import LengthUnit


class CentimeterUnit(LengthUnit):
    """
    The metric centimeter.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def id(self) -> int:
        """
        Returns the ID or enumeration value of this unit of length.
        """
        return Unit.CM.value

    # ------------------------------------------------------------------------------------------------------------------
    def meters(self) -> float:
        """
        Returns one centimeter expressed in meters.
        """
        return 1e-2

# ----------------------------------------------------------------------------------------------------------------------
