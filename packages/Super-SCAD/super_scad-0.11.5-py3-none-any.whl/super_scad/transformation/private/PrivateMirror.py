from typing import Dict, Set

from super_scad.private.PrivateSingleChildOpenScadCommand import PrivateSingleChildOpenScadCommand
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type.Vector2 import Vector2
from super_scad.type.Vector3 import Vector3


class PrivateMirror(PrivateSingleChildOpenScadCommand):
    """
    Transforms the child widget to a mirror of the original, as if it were the mirror image seen through a plane
    intersecting the origin. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#mirror.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 vector: Vector2 | Vector3,
                 child: ScadWidget):
        """
        Object constructor.

        :param vector:  The normal vector of the origin-intersecting mirror plane used, meaning the vector coming
                        perpendicularly out of the plane. Each coordinate of the original widget is altered such that
                        it becomes equidistant on the other side of this plane from the closest point on the plane.
        :param child: The widget to be mirrored.
        """
        PrivateSingleChildOpenScadCommand.__init__(self, command='mirror', args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_map(self) -> Dict[str, str]:
        """
        Returns the map from SuperSCAD arguments to OpenSCAD arguments.
        """
        return {'vector': 'v'}

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_lengths(self) -> Set[str]:
        """
        Returns the set with arguments that are lengths.
        """
        return {'v'}

# ----------------------------------------------------------------------------------------------------------------------
