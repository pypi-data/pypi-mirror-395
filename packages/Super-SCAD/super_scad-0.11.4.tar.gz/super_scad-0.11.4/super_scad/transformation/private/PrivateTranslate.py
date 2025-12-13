from typing import Dict, Set

from super_scad.private.PrivateSingleChildOpenScadCommand import PrivateSingleChildOpenScadCommand
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type.Vector2 import Vector2
from super_scad.type.Vector3 import Vector3


class PrivateTranslate(PrivateSingleChildOpenScadCommand):
    """
    Translates (moves) its child widget along the specified vector. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#translate.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 vector: Vector2 | Vector3,
                 child: ScadWidget):
        """
        Object constructor.

        :param vector: The vector over which the child node is translated.
        :param child: The child widget to be translated.
        """
        PrivateSingleChildOpenScadCommand.__init__(self, command='translate', args=locals(), child=child)

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
