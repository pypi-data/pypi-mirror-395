from super_scad.private.PrivateSingleChildOpenScadCommand import PrivateSingleChildOpenScadCommand
from super_scad.scad.ScadWidget import ScadWidget


class PrivateProjection(PrivateSingleChildOpenScadCommand):
    """
    Creates 2d drawings from 3d models. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#3D_to_2D_Projection.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, cut: bool, child: ScadWidget) -> None:
        """
        Object constructor.

        :param cut: Whether to cut the 3D model at height 0.0.
        :param child: The child widget.
        """
        PrivateSingleChildOpenScadCommand.__init__(self, command='projection', args=locals(), child=child)

# ----------------------------------------------------------------------------------------------------------------------
