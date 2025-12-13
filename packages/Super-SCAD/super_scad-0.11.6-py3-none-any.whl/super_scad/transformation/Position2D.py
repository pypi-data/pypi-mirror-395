from typing import Any, Dict

from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Rotate2D import Rotate2D
from super_scad.transformation.Translate2D import Translate2D
from super_scad.type import Vector2
from super_scad.type.Angle import Angle


class Position2D(ScadSingleChildParent):
    """
    A convenience widget that first rotates its child about the z-axis and then translates its child widget along the
    specified vector.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 angle: float | None = None,
                 vector: Vector2 | None = None,
                 x: float | None = None,
                 y: float | None = None,
                 child: ScadWidget):
        """
        Object constructor.

        :param angle: The angle of rotation (around the z-axis).
        :param vector: The vector over which the child widget is translated.
        :param x: The distance the child widget is translated to along the x-axis.
        :param y: The distance the child widget is translated to along the y-axis.
        """
        ScadSingleChildParent.__init__(self, child=child)

        self._angle: float | None = angle
        """
        The angle of rotation (around the z-axis).
        """

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
    def angle(self) -> float:
        """
        Returns the angle of rotation (around the z-axis).
        """
        if self._angle is None:
            self._angle = 0.0

        return Angle.normalize(self._angle)

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
            if self._vector is not None:
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
            if self._vector is not None:
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
        child = self.child

        if self.angle != 0.0:
            child = Rotate2D(angle=self.angle, child=child)

        if self.vector.is_not_origin:
            child = Translate2D(vector=self.vector, child=child)

        return child

# ----------------------------------------------------------------------------------------------------------------------
