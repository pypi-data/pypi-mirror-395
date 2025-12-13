from typing import List, Set

from super_scad.private.PrivateOpenScadCommand import PrivateOpenScadCommand
from super_scad.type.Vector3 import Vector3


class PrivatePolyhedron(PrivateOpenScadCommand):
    """
    Widget for creating polyhedrons. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Primitive_Solids#polyhedron.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 points: List[Vector3],
                 faces: List[List[int]],
                 convexity: int | None = None):
        """
        Object constructor.

        :param points: String representation of a list of 3D points.
        :param faces:  String representation of the faces that collectively enclose the solid.
        :param convexity: Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line 
                          through the child widget.
        """
        PrivateOpenScadCommand.__init__(self, command='polyhedron', args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_lengths(self) -> Set[str]:
        """
        Returns the set with arguments that are lengths.
        """
        return {'points'}

# ----------------------------------------------------------------------------------------------------------------------
