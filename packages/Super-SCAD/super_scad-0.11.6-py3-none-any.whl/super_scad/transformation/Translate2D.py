from typing import Any, Dict

from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.private.PrivateTranslate import PrivateTranslate
from super_scad.type.Vector2 import Vector2


class Translate2D(ScadSingleChildParent):
    """
    Translates (moves) its child widget along the specified vector. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#translate.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 vector: Vector2 | None = None,
                 x: float | None = None,
                 y: float | None = None,
                 child: ScadWidget):
        """
        Object constructor.

        :param vector: The vector over which the child widget is translated.
        :param x: The distance the child widget is translated to along the x-axis.
        :param y: The distance the child widget is translated to along the y-axis.
        :param child: The child widget to be translated.
        """
        ScadSingleChildParent.__init__(self, child=child)

        self._vector: Vector2 | None = vector
        """
        The vector over which the child widget is translated.
        """

        self._x: float | None = x
        """
        The distance the child widget is translated to along the x-axis.
        """

        self._y: float | None = y
        """
        The distance the child widget is translated to along the y-axis.
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
        validator.validate_exclusive({'vector'}, {'x', 'y'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def vector(self) -> Vector2:
        """
        Returns the vector over which the child widget is translated.
        """
        if self._vector is None:
            self._vector = Vector2(self.x, self.y)

        return self._vector

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def x(self) -> float:
        """
        Returns distance the child widget is translated to along the x-axis.
        """
        if self._x is None:
            if not self._vector is None:
                self._x = self.vector.x
            else:
                self._x = 0.0

        return self._x

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def y(self) -> float:
        """
        Returns distance the child widget is translated to along the y-axis.
        """
        if self._y is None:
            if not self._vector is None:
                self._y = self.vector.y
            else:
                self._y = 0.0

        return self._y

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return PrivateTranslate(vector=self.vector, child=self.child)

# ----------------------------------------------------------------------------------------------------------------------
