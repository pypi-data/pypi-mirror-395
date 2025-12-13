from typing import Dict, Set, Tuple

from super_scad.private.PrivateSingleChildOpenScadCommand import PrivateSingleChildOpenScadCommand
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type.Vector2 import Vector2
from super_scad.type.Vector3 import Vector3


class PrivateResize(PrivateSingleChildOpenScadCommand):
    """
    Modifies the size of the child widget to match the given x and y. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#resize.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 new_size: Vector2 | Vector3 | None = None,
                 auto: bool | Tuple[bool, bool] | Tuple[bool, bool, bool] = None,
                 convexity: int | None = None,
                 child: ScadWidget) -> None:
        """
        Object constructor.

        :param new_size: The new_size along all two axes.
        :param auto: Whether to auto-scale any 0-dimensions to match.
        :param convexity: Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line 
                          through the child widget.
        :param child: The widget to be resized.
        """
        PrivateSingleChildOpenScadCommand.__init__(self, command='resize', args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_map(self) -> Dict[str, str]:
        """
        Returns the map from SuperSCAD arguments to OpenSCAD arguments.
        """
        return {'new_size': 'newsize'}

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_lengths(self) -> Set[str]:
        """
        Returns the set with arguments that are lengths.
        """
        return {'newsize'}

# ----------------------------------------------------------------------------------------------------------------------
