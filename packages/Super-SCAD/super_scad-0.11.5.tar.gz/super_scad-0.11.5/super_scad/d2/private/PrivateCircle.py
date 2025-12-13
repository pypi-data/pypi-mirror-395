from typing import Dict, Set

from super_scad.private.PrivateOpenScadCommand import PrivateOpenScadCommand


class PrivateCircle(PrivateOpenScadCommand):
    """
    Widget for creating circles. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#circle.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 radius: float | None = None,
                 diameter: float | None = None,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None):
        """
        Object constructor.

        :param radius: The radius of the circle.
        :param diameter: The diameter of the circle.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        """
        PrivateOpenScadCommand.__init__(self, command='circle', args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_map(self) -> Dict[str, str]:
        """
        Returns the map from SuperSCAD arguments to OpenSCAD arguments.
        """
        return {'radius': 'r', 'diameter': 'd', 'fa': '$fa', 'fs': '$fs', 'fn': '$fn'}

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_angles(self) -> Set[str]:
        """
        Returns the set with arguments that are angles.
        """
        return {'$fa'}

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_lengths(self) -> Set[str]:
        """
        Returns the set with arguments that are lengths.
        """
        return {'r', 'd', '$fs'}

# ----------------------------------------------------------------------------------------------------------------------
