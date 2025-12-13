from typing import List, Set

from super_scad.private.PrivateOpenScadCommand import PrivateOpenScadCommand
from super_scad.type.Vector2 import Vector2


class PrivatePolygon(PrivateOpenScadCommand):
    """
    Class for polygons. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#polygon.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 points: List[Vector2],
                 paths: List[List[int]] | None = None,
                 convexity: int | None = None):
        """
        Object constructor.

        :param points: The list of 2D points of the polygon.
        :param paths: The order to traverse the points.
        :param convexity: Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line 
                          through the child widget.
        """
        PrivateOpenScadCommand.__init__(self, command='polygon', args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_lengths(self) -> Set[str]:
        """
        Returns the set with arguments that are lengths.
        """
        return {'points'}

# ----------------------------------------------------------------------------------------------------------------------
