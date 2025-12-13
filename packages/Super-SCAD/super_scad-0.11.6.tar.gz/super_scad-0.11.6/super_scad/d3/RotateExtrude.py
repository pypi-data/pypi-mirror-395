from typing import Dict, Set

from super_scad.private.PrivateSingleChildOpenScadCommand import PrivateSingleChildOpenScadCommand
from super_scad.scad.ScadWidget import ScadWidget


class RotateExtrude(PrivateSingleChildOpenScadCommand):
    """
    Rotational extrusion spins a 2D shape around the Z-axis to form a solid which has rotational symmetry. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#rotate_extrude.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 angle: float = 360.0,
                 convexity: int | None = None,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 child: ScadWidget):
        """
        Object constructor.

        :param angle: Specifies the number of degrees to sweep, starting at the positive X axis. The direction of the
                      sweep follows the Right-Hand Rule, hence a negative angle sweeps clockwise.
        :param convexity: Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line
                          through the child widget.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        :param child: The 2D child widget.
        """
        PrivateSingleChildOpenScadCommand.__init__(self, command='rotate_extrude', args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_map(self) -> Dict[str, str]:
        """
        Returns the map from SuperSCAD arguments to OpenSCAD arguments.
        """
        return {'fa': '$fa', 'fs': '$fs', 'fn': '$fn'}

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_angles(self) -> Set[str]:
        """
        Returns the set with arguments that are angles.
        """
        return {'angle'}

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_lengths(self) -> Set[str]:
        """
        Returns the set with arguments that are lengths.
        """
        return {'$fs'}

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle(self) -> float:
        """
        Returns the number of degrees to sweep, starting at the positive X axis. The direction of the sweep follows the
        Right-Hand Rule, hence a negative angle sweeps clockwise.
        """
        return self._args['angle']

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def convexity(self) -> int | None:
        """
        Returns the convexity.
        """
        return self._args.get('convexity')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fa(self) -> float | None:
        """
        Returns the minimum angle (in degrees) of each fragment.
        """
        return self._args.get('fa')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fs(self) -> float | None:
        """
        Returns the minimum circumferential length of each fragment.
        """
        return self._args.get('fs')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn(self) -> int | None:
        """
        Returns the fixed number of fragments in 360 degrees. Values of 3 or more override $fa and $fs.
        """
        return self._args.get('fn')

# ----------------------------------------------------------------------------------------------------------------------
