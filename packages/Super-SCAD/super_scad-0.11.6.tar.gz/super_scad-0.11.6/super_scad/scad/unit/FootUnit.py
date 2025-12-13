from super_scad.scad.Unit import Unit
from super_scad.scad.unit.LengthUnit import LengthUnit


class FootUnit(LengthUnit):
    """
    The imperial foot. One foot is 12 inch. See https://en.wikipedia.org/wiki/Foot_(unit).
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

    # ------------------------------------------------------------------------------------------------------------------
    def symbol(self) -> str:
        """
        Returns the symbol for an imperial foot.
        """
        return 'ft'

# ----------------------------------------------------------------------------------------------------------------------
