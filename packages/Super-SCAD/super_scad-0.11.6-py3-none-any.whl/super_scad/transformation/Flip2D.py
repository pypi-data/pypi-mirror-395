from typing import Any, Dict

from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.private.PrivateRotate import PrivateRotate
from super_scad.type.Vector2 import Vector2


class Flip2D(ScadSingleChildParent):
    """
    Flips its child about the x or y-axis.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 horizontal: bool | None = None,
                 vertical: bool | None = None,
                 flip_x: bool | None = None,
                 flip_y: bool | None = None,
                 child: ScadWidget) -> None:
        """
        Object constructor.

        :param horizontal: Whether to flip the child widget horizontally (i.e., flip around the y-axis).
        :param vertical: Whether to flip the child widget vertically (i.e., flip around the x-axis).
        :param flip_x: Whether to flip the child widget around the x-asis (i.e., vertical flip).
        :param flip_y: Whether to flip the child widget around the y-asis (i.e., horizontal flip).
        :param child: The child widget to be flipped.
        """
        ScadSingleChildParent.__init__(self, child=child)

        self._horizontal: bool | None = horizontal
        """
        Whether to flip the child widget horizontally (i.e., flip around the y-axis).
        """

        self._vertical: bool | None = vertical
        """
        Whether to flip the child widget vertically (i.e., flip around the x-axis).
        """

        self._flip_x: bool | None = flip_x
        """
        Whether to flip the child widget around the x-asis (i.e., vertical flip).
        """

        self._flip_y: bool | None = flip_y
        """
        Whether to flip the child widget around the y-asis (i.e., horizontal flip).
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
        validator.validate_exclusive({'horizontal', 'vertical'}, {'flip_x', 'flip_y'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def horizontal(self) -> bool:
        """
        Returns whether to flip the child widget horizontally (i.e., flip around the y-axis).
        """
        if self._horizontal is None:
            horizontal = self._horizontal or False
            flip_y = self._flip_y or False
            self._horizontal = horizontal or flip_y

        return self._horizontal

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def vertical(self) -> bool:
        """
        Returns whether to flip the child widget vertically (i.e., flip around the x-axis).
        """
        if self._vertical is None:
            vertical = self._vertical or False
            flip_x = self._flip_x or False
            self._vertical = vertical or flip_x

        return self._vertical

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def flip_x(self) -> bool:
        """
        Returns whether to flip the child widget around the x-asis (i.e., vertical flip).
        """
        if self._flip_x is None:
            self._flip_x = self.vertical or False

        return self._flip_x

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def flip_y(self) -> bool:
        """
        Returns whether to flip the child widget around the y-asis (i.e., horizontal flip).
        """
        if self._flip_y is None:
            self._flip_y = self.horizontal or False

        return self._flip_y

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        angle = Vector2(x=180.0 if self.flip_x else 0.0, y=180.0 if self.flip_y else 0.0)

        return PrivateRotate(angle=angle, child=self.child)

# ----------------------------------------------------------------------------------------------------------------------
