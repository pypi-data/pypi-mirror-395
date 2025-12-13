from typing import Any, Dict

from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.private.PrivatePaint import PrivatePaint
from super_scad.type.Color import Color


class Paint(ScadSingleChildParent):
    """
    Paints a child widget using a specified color and opacity. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#color.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 color: Color | str | None = None,
                 child: ScadWidget) -> None:
        """
        Object constructor.

        :param color: The color and opacity of the child widget.
        :param child: The child widget to be painted.
        """
        ScadSingleChildParent.__init__(self, child=child)

        self._color: Color | str | None = color
        """
        The color and opacity of the child widget.
        """

        self.__validate_arguments(locals())

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __validate_arguments(args: Dict[str, Any]) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.

        :param args: The arguments supplied to the constructor.
        """
        validator = ArgumentValidator(args)
        validator.validate_exclusive({'color'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def color(self) -> Color:
        """
        Returns the color and opacity of the child widget.
        """
        if isinstance(self._color, str):
            self._color = Color(self._color)

        return self._color

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return PrivatePaint(color=self.color, child=self.child)

# ----------------------------------------------------------------------------------------------------------------------
