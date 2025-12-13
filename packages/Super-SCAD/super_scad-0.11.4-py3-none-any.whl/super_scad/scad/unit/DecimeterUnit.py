from super_scad.scad.Unit import Unit
from super_scad.scad.unit.LengthUnit import LengthUnit


class DecimeterUnit(LengthUnit):
    """
    The metric decimeter.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def id(self) -> int:
        """
        Returns the ID or enumeration value of this unit of length.
        """
        return Unit.DM.value

    # ------------------------------------------------------------------------------------------------------------------
    def meters(self) -> float:
        """
        Returns one decimeter expressed in meters.
        """
        return 1e-1

# ----------------------------------------------------------------------------------------------------------------------
