from super_scad.scad.Unit import Unit
from super_scad.scad.unit.LengthUnit import LengthUnit


class InchUnit(LengthUnit):
    """
    The imperial inch. See https://en.wikipedia.org/wiki/Inch.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def id(self) -> int:
        """
        Returns the ID or enumeration value of this unit of length.
        """
        return Unit.INCH.value

    # ------------------------------------------------------------------------------------------------------------------
    def meters(self) -> float:
        """
        Returns one inch expressed in meters.
        """
        return 2.54e-2

# ----------------------------------------------------------------------------------------------------------------------
