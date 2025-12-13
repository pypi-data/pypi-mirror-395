from super_scad.scad.Unit import Unit
from super_scad.scad.unit.LengthUnit import LengthUnit


class LiUnit(LengthUnit):
    """
    The Chinese li 市里. One li is 500 meters. See https://en.wikipedia.org/wiki/Li_(unit).
    """

    # ------------------------------------------------------------------------------------------------------------------
    def id(self) -> int:
        """
        Returns the ID or enumeration value of this unit of length.
        """
        return Unit.LI.value

    # ------------------------------------------------------------------------------------------------------------------
    def meters(self) -> float:
        """
        Returns one li expressed in meters.
        """
        return 5e2

    # ------------------------------------------------------------------------------------------------------------------
    def symbol(self) -> str:
        """
        Returns the symbol for a li.
        """
        return '里'

# ----------------------------------------------------------------------------------------------------------------------
