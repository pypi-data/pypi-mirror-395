from typing import List

from super_scad.private.PrivateMultiChildOpenScadCommand import PrivateMultiChildOpenScadCommand
from super_scad.scad.ScadWidget import ScadWidget


class Union(PrivateMultiChildOpenScadCommand):
    """
    Creates a union of all its child widgets. This is the sum of all children (logical or). See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/CSG_Modelling#union.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, children: List[ScadWidget]):
        """
        Object constructor.

        :param children: The child widgets.
        """
        PrivateMultiChildOpenScadCommand.__init__(self, command='union', args=locals(), children=children)

# ----------------------------------------------------------------------------------------------------------------------
