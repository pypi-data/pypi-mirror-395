from typing import List

from super_scad.private.PrivateMultiChildOpenScadCommand import PrivateMultiChildOpenScadCommand
from super_scad.scad.ScadWidget import ScadWidget


class Hull(PrivateMultiChildOpenScadCommand):
    """
    Creates a convex hull of the child widgets. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#hull.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 children: List[ScadWidget]):
        """
        Object constructor.

        :param children: The child widgets.
        """
        PrivateMultiChildOpenScadCommand.__init__(self, command='hull', args=locals(), children=children)

# ----------------------------------------------------------------------------------------------------------------------
