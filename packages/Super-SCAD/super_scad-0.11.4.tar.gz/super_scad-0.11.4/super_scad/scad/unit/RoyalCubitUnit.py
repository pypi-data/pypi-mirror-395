from super_scad.scad.Unit import Unit
from super_scad.scad.unit.LengthUnit import LengthUnit


class RoyalCubitUnit(LengthUnit):
    """
    The royal cubit. Most commonly understood to be approximately 0.5236 meters.
    See https://en.wikipedia.org/wiki/Cubit#Ancient_Egyptian_royal_cubit.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def id(self) -> int:
        """
        Returns the ID or enumeration value of this unit of length.
        """
        return Unit.ROYAL_CUBIT.value

    # ------------------------------------------------------------------------------------------------------------------
    def meters(self) -> float:
        """
        Returns one foot expressed in meters.
        """
        return 5.236e-1

# ----------------------------------------------------------------------------------------------------------------------
