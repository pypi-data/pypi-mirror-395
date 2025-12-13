from typing import List

from super_scad.private.PrivateMultiChildOpenScadCommand import PrivateMultiChildOpenScadCommand
from super_scad.scad.ScadWidget import ScadWidget


class Intersection(PrivateMultiChildOpenScadCommand):
    """
    Creates the intersection of all child widgets. This keeps the overlapping portion (logical and). See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/CSG_Modelling#intersection.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, children: List[ScadWidget]):
        """
        Object constructor.

        :param children: The child widgets.
        """
        PrivateMultiChildOpenScadCommand.__init__(self, command='intersection', args=locals(), children=children)

# ----------------------------------------------------------------------------------------------------------------------
