from typing import Any, Dict

from super_scad.private.PrivateOpenScadCommand import PrivateOpenScadCommand
from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.scad.ScadWidget import ScadWidget


class PrivateSingleChildOpenScadCommand(PrivateOpenScadCommand, ScadSingleChildParent):
    """
    Parent widget for OpenSCAD commands with a single child.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, command: str, args: Dict[str, Any], child: ScadWidget):
        """
        Object constructor.

        :param command: The OpenSCAD command.
        :param args: The arguments of the command.
        :param child: The child SuperSCAD widget of this single-child parent.
        """
        PrivateOpenScadCommand.__init__(self, command=command, args=args)
        ScadSingleChildParent.__init__(self, child=child)

# ----------------------------------------------------------------------------------------------------------------------
