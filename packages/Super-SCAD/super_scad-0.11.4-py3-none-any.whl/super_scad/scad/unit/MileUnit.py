from super_scad.scad.Unit import Unit
from super_scad.scad.unit.LengthUnit import LengthUnit


class MileUnit(LengthUnit):
    """
    The imperial mile, a.k.a. terrestrial mile. One mile is 5280 feet. See https://en.wikipedia.org/wiki/Mile.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def id(self) -> int:
        """
        Returns the ID or enumeration value of this unit of length.
        """
        return Unit.MILE.value

    # ------------------------------------------------------------------------------------------------------------------
    def meters(self) -> float:
        """
        Returns one foot expressed in meters.
        """
        return 1.609344e3

# ----------------------------------------------------------------------------------------------------------------------
