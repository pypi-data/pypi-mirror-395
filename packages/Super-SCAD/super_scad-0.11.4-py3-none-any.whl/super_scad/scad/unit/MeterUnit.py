from super_scad.scad.Unit import Unit
from super_scad.scad.unit.LengthUnit import LengthUnit


class MeterUnit(LengthUnit):
    """
    The metric meter.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def id(self) -> int:
        """
        Returns the ID or enumeration value of this unit of length.
        """
        return Unit.M.value

    # ------------------------------------------------------------------------------------------------------------------
    def meters(self) -> float:
        """
        Returns one meter expressed in meters.
        """
        return 1e0

# ----------------------------------------------------------------------------------------------------------------------
