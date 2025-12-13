import math
import random
from abc import ABC, abstractmethod
from typing import List, Set

from super_scad.d2.helper.PolygonSideExtender import PolygonSideExtender
from super_scad.d2.private.PrivatePolygon import PrivatePolygon
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2
from super_scad.type.Angle import Angle


# class PolygonMixin(ScadWidget, ABC):
class PolygonMixin(ABC):
    """
    A mixin for all polygonal and polygonal like widgets in SuperSCAD.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 convexity: int | None = None,
                 extend_by_eps_sides: bool | List[bool] | Set[int] | None):
        """
        Object constructor.

        :param convexity: Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line
                          through the polygon.
        :param extend_by_eps_sides: Whether to extend sides by eps for a clear overlap.
        """
        self._inner_angles: List[float] | None = None
        """
        The inner angles of the polygon (in the same order as the primary points).
        """

        self._normal_angles: List[float] | None = None
        """
        The absolute angles of the normal of each node.
        """

        self._is_clockwise: bool | None = None
        """
        Whether the nodes of the polygon are in a clockwise order.
        """

        self._convexity: int | None = convexity
        """
        Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line through the polygon.
        """

        self._extend_by_eps_sides = extend_by_eps_sides
        """
        Whether to extend sides by eps for a clear overlap.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def is_clockwise_order(nodes: List[Vector2], delta: float) -> bool:
        """
        Returns whether the nodes of a polygon are given in a clockwise order.

        @param nodes: The nodes of the polygon.
        @param delta: The minimum distance between the line segment and the nodes.
        """
        radius = 0.0
        for node in nodes:
            radius = max(radius, abs(node.x), abs(node.y))

        n = len(nodes)
        for index1 in range(10 * n):
            min_distance = radius
            for index2 in range(1, n):
                if index2 != index1 % n:
                    min_distance = min(min_distance, Vector2.distance(nodes[index1 % n], nodes[index2]))

            p1 = nodes[(index1 - 1) % n]
            p2 = nodes[index1 % n]
            p3 = nodes[(index1 + 1) % n]

            leg1 = (p2 - p1)
            leg2 = (p2 - p3)
            height = abs(Vector2.cross_product(leg1, leg2)) / Vector2.distance(leg2, leg1)
            q1 = p2 + Vector2.from_polar(random.uniform(0.25, 0.75) * min(height, min_distance),
                                         0.5 * (leg1.angle + leg2.angle))
            if not PolygonMixin._to_close(p1, p3, q1, delta):
                q2 = Vector2.from_polar(2.0 * radius, random.uniform(0.0, 360.0))
                number_of_intersections = PolygonMixin._count_intersections(nodes, q1, q2, delta)
                if number_of_intersections is not None:
                    orientation = Vector2.orientation(p1, p2, q1)
                    assert orientation != 0.0

                    return (orientation > 0.0) == (number_of_intersections % 2 == 1)

        raise ValueError('Not a proper polygon.')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _to_close(segment_start: Vector2, segment_end: Vector2, node: Vector2, delta: float) -> bool:
        """
        Returns whether a node is to close to a line segment for reliable computation of the separation between line
        segments and nodes.

        :param segment_start: The start point of the line segment.
        :param segment_end: The end point of the line segment.
        :param node: The node.
        :param delta: The minimum distance between nodes, vertices and line segments for reliable computation of the
                      separation between line segments and nodes.

        """
        tmp1 = segment_end - segment_start
        tmp2 = (node - segment_start).rotate(-tmp1.angle)

        return -delta <= tmp2.x <= (tmp1.length + delta) and -delta <= tmp2.y <= delta

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _do_intersect(segment_start: Vector2,
                      segment_end: Vector2,
                      vertex_start: Vector2,
                      vertex_end: Vector2) -> bool:
        """
        Returns whether a line segment and a vertex intersect.

        @param segment_start: The start point of the line segment.
        @param segment_end: The end point of the line segment.
        @param vertex_start: The start point of the vertex.
        @param vertex_end:  The end point of the vertex.
        """
        o1 = Vector2.orientation(segment_start, segment_end, vertex_start)
        o2 = Vector2.orientation(segment_start, segment_end, vertex_end)
        o3 = Vector2.orientation(vertex_start, vertex_end, segment_start)
        o4 = Vector2.orientation(vertex_start, vertex_end, segment_end)

        return (math.copysign(1, o1) != math.copysign(1, o2)) and (math.copysign(1, o3) != math.copysign(1, o4))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _count_intersections(nodes: List[Vector2],
                             segment_start: Vector2,
                             segment_end: Vector2,
                             delta: float) -> int | None:
        """
        Returns the number of intersections between a line segment (segment_start, segment_end) and the vertices of the
        polygon.

        :param nodes: The nodes of the polygon.
        :param segment_start: Start point of the line segment.
        :param segment_end: End point of the line segment.
        :param delta: The minimum distance between nodes, vertices and line segments for reliable computation of the
                      separation between line segments and nodes.
        """
        intersections = 0

        n = len(nodes)
        for i in range(n):
            vertex_start = nodes[i]
            vertex_end = nodes[(i + 1) % n]

            if PolygonMixin._to_close(segment_start, segment_end, vertex_start, delta):
                return None

            if PolygonMixin._to_close(vertex_start, vertex_end, segment_start, delta):
                return None

            # segment_end is twice as far from the origin as any node from the origin.

            if PolygonMixin._do_intersect(segment_start, segment_end, vertex_start, vertex_end):
                intersections += 1

        return intersections

    # ------------------------------------------------------------------------------------------------------------------
    def _compute_angles(self, context: Context) -> None:
        """
        Returns the inner angles of the polygon (in the same order as the primary points).

        :param context: The build context.
        """
        self._inner_angles = []
        self._normal_angles = []

        nodes = self.nodes
        self._is_clockwise = self.is_clockwise_order(nodes, context.delta)

        n = len(nodes)
        for i in range(n):
            if self._is_clockwise:
                p1 = nodes[(i - 1) % n]
                p2 = nodes[i]
                p3 = nodes[(i + 1) % n]
            else:
                p1 = nodes[(i + 1) % n]
                p2 = nodes[i]
                p3 = nodes[(i - 1) % n]

            inner_angle = Angle.normalize((p3 - p2).angle - (p2 - p1).angle - 180.0)
            normal_angle = Angle.normalize((p1 - p2).angle + 0.5 * inner_angle)

            self._inner_angles.append(inner_angle)
            self._normal_angles.append(normal_angle)

    # ------------------------------------------------------------------------------------------------------------------
    def is_clockwise(self, context: Context) -> bool:
        """
        Returns whether the nodes of this polygon are in a clockwise order.

        :param context: The build context.
        """
        if self._is_clockwise is None:
            self._compute_angles(context)

        return self._is_clockwise

    # ------------------------------------------------------------------------------------------------------------------
    def inner_angles(self, context: Context) -> List[float]:
        """
        Returns the inner angles of the polygon (in the same order as the primary points).

        :param context: The build context.
        """
        if self._inner_angles is None:
            self._compute_angles(context)

        return self._inner_angles

    # ------------------------------------------------------------------------------------------------------------------
    def normal_angles(self, context: Context) -> List[float]:
        """
        Returns the absolute angles of the normal of each node.

        :param context: The build context.
        """
        if self._normal_angles is None:
            self._compute_angles(context)

        return self._normal_angles

    # ------------------------------------------------------------------------------------------------------------------
    @property
    @abstractmethod
    def nodes(self) -> List[Vector2]:
        """
        Returns the nodes of this polygon.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_sides(self) -> Set[int]:
        """
        Returns the set of sides that must be extended by eps for clear overlap.
        """
        if not isinstance(self._extend_by_eps_sides, set):
            if self._extend_by_eps_sides is None or self._extend_by_eps_sides is False:
                self._extend_by_eps_sides = set()

            elif self._extend_by_eps_sides is True:
                self._extend_by_eps_sides = {index for index in range(self.sides)}

            elif isinstance(self._extend_by_eps_sides, list):
                self._extend_by_eps_sides = set(index for index in range(len(self._extend_by_eps_sides)) \
                                                if self._extend_by_eps_sides[index])

            else:
                raise ValueError(f'Parameter extend_by_eps_sides must be a boolean, '
                                 f'set of integers, a list of booleans or None, got {type(self._extend_by_eps_sides)}')

        return self._extend_by_eps_sides

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def sides(self) -> int:
        """
        Returns the number of sides of this polygon.
        """
        return len(self.nodes)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def convexity(self) -> int | None:
        """
        Returns the convexity of the polygon.
        """
        return self._convexity

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        if self.extend_by_eps_sides:
            return self._build_polygon_extended(context)

        return self._build_polygon(context)

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def _build_polygon(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def _build_polygon_extended(self, context: Context) -> ScadWidget:
        """
        Builds a polygon with extended sides.

        @param context: The build context.
        """
        polygon_side_extender = self._create_polygon_side_extender()
        new_nodes = polygon_side_extender.extend_sides(context=context,
                                                       nodes=self.nodes,
                                                       inner_angles=self.inner_angles(context),
                                                       normal_angles=self.normal_angles(context),
                                                       is_clockwise=self.is_clockwise(context),
                                                       extend_by_eps_sides=self.extend_by_eps_sides)

        return PrivatePolygon(points=new_nodes, convexity=self.convexity)

    # ------------------------------------------------------------------------------------------------------------------
    def _create_polygon_side_extender(self) -> PolygonSideExtender:
        """
        Returns a polygon side extender that extends this polygon.
        """
        return PolygonSideExtender()

# ----------------------------------------------------------------------------------------------------------------------
