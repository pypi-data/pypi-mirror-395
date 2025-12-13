from super_scad.boolean.Union import Union
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget


class Empty(ScadWidget):
    """
    Widget for creating empty OpenSCAD nodes.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return Union(children=[])

# ----------------------------------------------------------------------------------------------------------------------
