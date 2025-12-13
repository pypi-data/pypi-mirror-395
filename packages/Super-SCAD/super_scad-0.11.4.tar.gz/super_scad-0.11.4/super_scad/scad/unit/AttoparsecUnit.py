from super_scad.scad.Unit import Unit
from super_scad.scad.unit.LengthUnit import LengthUnit


class AttoparsecUnit(LengthUnit):
    """
    The attoparsec unit is 3.085 677 581 491 367 3 cm. See
    https://en.wikipedia.org/wiki/List_of_humorous_units_of_measurement#Attoparsec.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def id(self) -> int:
        """
        Returns the ID or enumeration value of this unit of length.
        """
        return Unit.ATTOPARSEC.value

    # ------------------------------------------------------------------------------------------------------------------
    def meters(self) -> float:
        """
        Returns one attoparsec unit expressed in meters.
        """
        return 3.0856775814913673e-2

# ----------------------------------------------------------------------------------------------------------------------
