from typing import Any, Dict

from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.private.PrivateMirror import PrivateMirror
from super_scad.type.Vector2 import Vector2


class Mirror2D(ScadSingleChildParent):
    """
    Transforms the child widget to a mirror of the original, as if it were the mirror image seen through a plane
    intersecting the origin. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#mirror.
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

        :param vector:  The normal vector of the origin-intersecting mirror plane used, meaning the vector coming
                        perpendicularly out of the plane. Each coordinate of the original widget is altered such that
                        it becomes equidistant on the other side of this plane from the closest point on the plane.
        :param x:  The x-coordinate of the origin-intersecting mirror plane.
        :param y:  The y-coordinate of the origin-intersecting mirror plane.
        :param child: The widget to be mirrored.
        """
        ScadSingleChildParent.__init__(self, child=child)

        self._vector: Vector2 | None = vector
        """
        The normal vector of the origin-intersecting mirror plane used, meaning the vector coming perpendicularly out of 
        the plane
        """

        self._x: float | None = x
        """
        The x-coordinate of the origin-intersecting mirror plane.
        """

        self._y: float | None = y
        """
        The y-coordinate of the origin-intersecting mirror plane.
        """

        self._normal: Vector2 | None = None
        """
        The normalized normal vector of the origin-intersecting mirror plane used.
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
        validator.validate_required({'x', 'y', 'vector'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def normal(self) -> Vector2:
        """
        The normal vector of the origin-intersecting mirror plane.
        """
        if self._normal is None:
            if self._vector is not None:
                self._normal = self._vector.unit
            else:
                self._normal = Vector2(self._x or 0.0,
                                       self._y or 0.0).unit

                self._normal = self._normal * (-1.0 if self._normal.x < 0.0 else 1.0)

        return self._normal

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return PrivateMirror(vector=self.normal, child=self.child)

# ----------------------------------------------------------------------------------------------------------------------
