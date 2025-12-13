from typing import Set

from super_scad.private.PrivateOpenScadCommand import PrivateOpenScadCommand
from super_scad.type.Vector3 import Vector3


class PrivateCube(PrivateOpenScadCommand):
    """
    Class for cubes. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Primitive_Solids#cube.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, size: float | Vector3, center: bool = False):
        """
        Object constructor.

        :param size: The size of the cube.
        :param center: Whether the cube is centered at the origin.
        """
        PrivateOpenScadCommand.__init__(self, command='cube', args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_lengths(self) -> Set[str]:
        """
        Returns the set with arguments that are lengths.
        """
        return {'size'}

# ----------------------------------------------------------------------------------------------------------------------
