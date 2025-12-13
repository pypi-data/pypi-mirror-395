from typing import Any, Dict, List, Set

from super_scad.d2.PolygonMixin import PolygonMixin
from super_scad.d2.private.PrivateSquare import PrivateSquare
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type.Vector2 import Vector2


class Rectangle(PolygonMixin, ScadWidget):
    """
    Widget for creating rectangles.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 size: Vector2 | None = None,
                 width: float | None = None,
                 depth: float | None = None,
                 center: bool = False,
                 extend_by_eps_sides: bool | List[bool] | Set[int] | None = None):
        """
        Object constructor.

        :param size: The size of the rectangle.
        :param width: The width (the size along the x-axis) of the rectangle.
        :param depth: The depth (the size along the y-axis) of the rectangle.
        :param center: Whether the rectangle is centered at its position.
        :param extend_by_eps_sides: Whether to extend sides by eps for a clear overlap.
        """
        ScadWidget.__init__(self)
        PolygonMixin.__init__(self, extend_by_eps_sides=extend_by_eps_sides)

        self._size: Vector2 | None = size
        """
        The size of the rectangle.
        """

        self._width: float | None = width
        """
        The width of the rectangle.
        """

        self._depth: float | None = depth
        """
        The depth of the rectangle.
        """

        self._center: bool = center
        """
        Whether the rectangle center is at the center of the rectangle.
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
        validator.validate_exclusive({'size'}, {'width', 'depth'})
        validator.validate_required({'width', 'size'},
                                    {'depth', 'size'},
                                    {'center'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def size(self) -> Vector2:
        """
        Returns the size of this rectangle.
        """
        if self._size is None:
            self._size = Vector2(self._width, self._depth)

        return self._size

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def width(self) -> float:
        """
        Returns the width (the size along the x-axis) of this rectangle.
        """
        if self._width is None:
            self._width = self._size.x

        return self._width

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def depth(self) -> float:
        """
        Returns the depth (the size along the y-axis) of this rectangle.
        """
        if self._depth is None:
            self._depth = self._size.y

        return self._depth

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the rectangle is centered at this origin.
        """
        return self._center

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def sides(self) -> int:
        """
        Returns the number of sides of this rectangle.
        """
        return 4

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def nodes(self) -> List[Vector2]:
        """
        Returns the nodes of this rectangle.
        """
        if self.center:
            return [Vector2(-0.5 * self.width, -0.5 * self.depth),
                    Vector2(-0.5 * self.width, 0.5 * self.depth),
                    Vector2(0.5 * self.width, 0.5 * self.depth),
                    Vector2(0.5 * self.width, -0.5 * self.depth)]

        return [Vector2.origin,
                Vector2(0.0, self.depth),
                Vector2(self.width, self.depth),
                Vector2(self.width, 0.0)]

    # ------------------------------------------------------------------------------------------------------------------
    def _build_polygon(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return PrivateSquare(size=self.size, center=self.center)

# ----------------------------------------------------------------------------------------------------------------------
