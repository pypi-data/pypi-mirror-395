from typing import Any, Dict, List, Set

from super_scad.d2.PolygonMixin import PolygonMixin
from super_scad.d2.private.PrivatePolygon import PrivatePolygon
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type.Vector2 import Vector2


class Polygon(PolygonMixin, ScadWidget):
    """
    Widget for creating polygons. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#polygon.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 primary: List[Vector2] | None = None,
                 points: List[Vector2] | None = None,
                 secondary: List[Vector2] | None = None,
                 secondaries: List[List[Vector2]] | None = None,
                 convexity: int | None = None,
                 extend_by_eps_sides: bool | List[bool] | Set[int] | None = None):
        """
        Object constructor.

        :param primary: The list of 2D points of the polygon.
        :param points: Alias for primary.
        :param secondary: The secondary path that will be subtracted from the polygon.
        :param secondaries: The secondary paths that will be subtracted form the polygon.
        :param convexity: Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line
                          through the child widget.
        :param extend_by_eps_sides: Whether to extend sides by eps for a clear overlap.
        """
        ScadWidget.__init__(self)
        PolygonMixin.__init__(self, convexity=convexity, extend_by_eps_sides=extend_by_eps_sides)

        self._primary: List[Vector2] | None = primary
        """
        The list of 2D points of the polygon.
        """

        self._points: List[Vector2] | None = points
        """
        Alias for primary.
        """

        self._secondary: List[Vector2] | None = secondary
        """
        The secondary path that will be subtracted from the polygon.
        """

        self._secondaries: List[List[Vector2]] | None = secondaries
        """
        The secondary paths that will be subtracted form the polygon.
        """

        self.__validate_arguments(locals())

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __validate_arguments(args: Dict[str, Any]) -> None:
        """
        Validates the arguments supplied to the
         constructor of this SuperSCAD widget.

        :param args: The arguments supplied to the constructor.
        """
        validator = ArgumentValidator(args)
        validator.validate_exclusive({'primary'}, {'points'})
        validator.validate_exclusive({'secondary'}, {'secondaries'})
        validator.validate_required({'primary', 'points'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def primary(self) -> List[Vector2]:
        """
        Returns the points of the polygon.
        """
        if self._primary is None:
            self._primary = self._points

        return self._primary

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def secondaries(self) -> List[List[Vector2]] | None:
        """
        Returns the points of the polygon.
        """
        if self._secondaries is not None:
            return self._secondaries

        if self._secondary is not None:
            self._secondaries = [self._secondary]

        return self._secondaries

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def nodes(self) -> List[Vector2]:
        """
        Returns the nodes of the polygon.
        """
        return self.primary

    # ------------------------------------------------------------------------------------------------------------------
    def _build_polygon(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        secondaries = self.secondaries
        if secondaries is None:
            return PrivatePolygon(points=self.primary, convexity=self.convexity)

        points = self.primary
        n = 0
        m = n + len(points)
        paths = [list(range(n, m))]
        n = m

        for secondary in secondaries:
            m = n + len(secondary)
            points += secondary
            paths.append(list(range(n, m)))
            n = m

        return PrivatePolygon(points=points, paths=paths, convexity=self.convexity)

# ----------------------------------------------------------------------------------------------------------------------
