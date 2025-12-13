from super_scad.scad.Unit import Unit
from super_scad.scad.unit.LengthUnit import LengthUnit


class ThouUnit(LengthUnit):
    """
    The imperial thou. One thou is one thousand of an inch. See https://en.wikipedia.org/wiki/Thousandth_of_an_inch.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def id(self) -> int:
        """
        Returns the ID or enumeration value of this unit of length.
        """
        return Unit.THOU.value

    # ------------------------------------------------------------------------------------------------------------------
    def meters(self) -> float:
        """
        Returns one inch expressed in meters.
        """
        return 2.54e-5

# ----------------------------------------------------------------------------------------------------------------------
