from typing import Any, Dict, List, Set

from super_scad.d2.PolygonMixin import PolygonMixin
from super_scad.d2.private.PrivateSquare import PrivateSquare
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2


class Square(PolygonMixin, ScadWidget):
    """
    Widget for creating squares.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 size: float,
                 center: bool = False,
                 extend_by_eps_sides: bool | List[bool] | Set[int] | None = None):
        """
        Object constructor.

        :param size: The size of the square.
        :param center: Whether the square is centered at the origin.
        :param extend_by_eps_sides: Whether to extend sides by eps for a clear overlap.
        """
        ScadWidget.__init__(self)
        PolygonMixin.__init__(self, extend_by_eps_sides=extend_by_eps_sides)

        self._size: float = size
        """
        The size of the square.
        """

        self._center: bool = center
        """
        Whether the square is centered at the origin.
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
        validator.validate_required({'size'}, {'center'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def size(self) -> float:
        """
        Returns the size of this square.
        """
        return self._size

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether this square is centered at its position.
        """
        return self._center

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def sides(self) -> int:
        """
        Returns the number of sides of this square.
        """
        return 4

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def nodes(self) -> List[Vector2]:
        """
        Returns the nodes of this square.
        """
        if self.center:
            return [Vector2(-0.5 * self.size, -0.5 * self.size),
                    Vector2(-0.5 * self.size, 0.5 * self.size),
                    Vector2(0.5 * self.size, 0.5 * self.size),
                    Vector2(0.5 * self.size, -0.5 * self.size)]

        return [Vector2.origin,
                Vector2(0.0, self.size),
                Vector2(self.size, self.size),
                Vector2(self.size, 0.0)]

    # ------------------------------------------------------------------------------------------------------------------
    def _build_polygon(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return PrivateSquare(size=self.size, center=self.center)

# ----------------------------------------------------------------------------------------------------------------------
