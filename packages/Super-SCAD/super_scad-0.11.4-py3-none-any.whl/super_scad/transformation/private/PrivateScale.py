from typing import Dict, Set

from super_scad.private.PrivateSingleChildOpenScadCommand import PrivateSingleChildOpenScadCommand
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type.Vector2 import Vector2
from super_scad.type.Vector3 import Vector3


class PrivateScale(PrivateSingleChildOpenScadCommand):
    """
    Scales its child widget using the specified vector. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#scale.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 factor: Vector2 | Vector3,
                 child: ScadWidget) -> None:
        """
        Object constructor.

        :param factor: The scaling factor to apply.
        :param child: The child widget to be scaled.
        """
        PrivateSingleChildOpenScadCommand.__init__(self, command='scale', args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_map(self) -> Dict[str, str]:
        """
        Returns the map from SuperSCAD arguments to OpenSCAD arguments.
        """
        return {'factor': 'v'}

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_scales(self) -> Set[str]:
        """
        Returns the set with arguments that are scales and factors.
        """
        return {'v'}

# ----------------------------------------------------------------------------------------------------------------------
