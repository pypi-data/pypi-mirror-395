from super_scad.scad.Unit import Unit
from super_scad.scad.unit.LengthUnit import LengthUnit


class YardUnit(LengthUnit):
    """
    The imperial yard. One yard is 3 feet. See https://en.wikipedia.org/wiki/Yard.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def id(self) -> int:
        """
        Returns the ID or enumeration value of this unit of length.
        """
        return Unit.YARD.value

    # ------------------------------------------------------------------------------------------------------------------
    def meters(self) -> float:
        """
        Returns one foot expressed in meters.
        """
        return 9.144e-1

# ----------------------------------------------------------------------------------------------------------------------
