from super_scad.scad.Unit import Unit
from super_scad.scad.unit.LengthUnit import LengthUnit


class LightYearUnit(LengthUnit):
    """
    The lightyear. The distance that light travels in a vacuum in one Julian year. See
    https://en.wikipedia.org/wiki/Light-year.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def id(self) -> int:
        """
        Returns the ID or enumeration value of this unit of length.
        """
        return Unit.LIGHT_YEAR.value

    # ------------------------------------------------------------------------------------------------------------------
    def meters(self) -> float:
        """
        Returns one light-year expressed in meters.
        """
        return 9.4607304725808e15

# ----------------------------------------------------------------------------------------------------------------------
