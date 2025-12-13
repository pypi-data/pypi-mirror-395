from super_scad.scad.Unit import Unit
from super_scad.scad.unit.LengthUnit import LengthUnit


class AstronomicalUnit(LengthUnit):
    """
    The astronomical unit is 149 597 870 700 m. See https://en.wikipedia.org/wiki/Astronomical_unit.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def id(self) -> int:
        """
        Returns the ID or enumeration value of this unit of length.
        """
        return Unit.ASTRONOMICAL_UNIT.value

    # ------------------------------------------------------------------------------------------------------------------
    def meters(self) -> float:
        """
        Returns one astronomical unit expressed in meters.
        """
        return 1.495978707e11

# ----------------------------------------------------------------------------------------------------------------------
