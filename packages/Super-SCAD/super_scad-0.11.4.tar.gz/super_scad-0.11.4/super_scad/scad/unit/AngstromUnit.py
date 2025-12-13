from super_scad.scad.Unit import Unit
from super_scad.scad.unit.LengthUnit import LengthUnit


class AngstromUnit(LengthUnit):
    """
    The metric ångström is 10e−10m. See https://en.wikipedia.org/wiki/Angstrom.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def id(self) -> int:
        """
        Returns the ID or enumeration value of this unit of length.
        """
        return Unit.ANGSTROM.value

    # ------------------------------------------------------------------------------------------------------------------
    def meters(self) -> float:
        """
        Returns one ångström expressed in meters.
        """
        return 1e-10

# ----------------------------------------------------------------------------------------------------------------------
