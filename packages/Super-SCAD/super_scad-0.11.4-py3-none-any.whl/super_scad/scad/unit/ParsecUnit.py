from super_scad.scad.Unit import Unit
from super_scad.scad.unit.LengthUnit import LengthUnit


class ParsecUnit(LengthUnit):
    """
    The parsec unit is 30 856 775 814 913 673 m. See https://en.wikipedia.org/wiki/Parsec.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def id(self) -> int:
        """
        Returns the ID or enumeration value of this unit of length.
        """
        return Unit.PARSEC.value

    # ------------------------------------------------------------------------------------------------------------------
    def meters(self) -> float:
        """
        Returns one parsec unit expressed in meters.
        """
        return 3.0856775814913673e16

# ----------------------------------------------------------------------------------------------------------------------
