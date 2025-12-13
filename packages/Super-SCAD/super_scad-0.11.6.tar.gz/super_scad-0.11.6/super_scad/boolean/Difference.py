from typing import List

from super_scad.private.PrivateMultiChildOpenScadCommand import PrivateMultiChildOpenScadCommand
from super_scad.scad.ScadWidget import ScadWidget


class Difference(PrivateMultiChildOpenScadCommand):
    """
    Subtracts the second (and all further) child widgets from the first child widgets (logical and not).
    See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/CSG_Modelling#difference.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, children: List[ScadWidget]):
        """
        Object constructor.

        :param children: The child widgets.
        """
        PrivateMultiChildOpenScadCommand.__init__(self, command='difference', args=locals(), children=children)

# ----------------------------------------------------------------------------------------------------------------------
