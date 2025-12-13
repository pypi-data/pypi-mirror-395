from super_scad.scad.Unit import Unit
from super_scad.scad.unit.LengthUnit import LengthUnit


class FootUnit(LengthUnit):
    """
    The imperial foot. One foot is 12 inch. See https://en.wikipedia.org/wiki/Thousandth_of_an_inch.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def id(self) -> int:
        """
        Returns the ID or enumeration value of this unit of length.
        """
        return Unit.FOOT.value

    # ------------------------------------------------------------------------------------------------------------------
    def meters(self) -> float:
        """
        Returns one foot expressed in meters.
        """
        return 3.048e-1

# ----------------------------------------------------------------------------------------------------------------------
