from typing import Set

from super_scad.private.PrivateOpenScadCommand import PrivateOpenScadCommand
from super_scad.type.Vector2 import Vector2


class PrivateSquare(PrivateOpenScadCommand):
    """
    Widget for creating squares. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#square.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, size: float | Vector2, center: bool = False):
        """
        Object constructor.

        :param size: The size of the square.
        :param center: Whether the square is centered at the origin.
        """
        PrivateOpenScadCommand.__init__(self, command='square', args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_lengths(self) -> Set[str]:
        """
        Returns the set with arguments that are lengths.
        """
        return {'size'}

# ----------------------------------------------------------------------------------------------------------------------
