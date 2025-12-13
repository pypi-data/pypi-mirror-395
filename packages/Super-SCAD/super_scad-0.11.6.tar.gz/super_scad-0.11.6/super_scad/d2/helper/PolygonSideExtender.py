import math
from typing import List

from super_scad.scad.Context import Context
from super_scad.type import Vector2


class PolygonSideExtender:
    """
    A polygon side extender extends the sides of a polygon by eps for a clear overlap by working at the nodes of the
    polygon.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Returns a modified list of nodes such that it appears that the sides are extended by eps for a clear overlap.
        """

        self._nodes: List[Vector2] | None = None
        """
        The nodes of the polygon.
        """

        self._inner_angles: List[float] | None = None
        """
        The inner angles of the polygon.
        """

        self._normal_angles: List[float] | None = None
        """
        The absolute angles of the normal of each node.
        """

        self._is_clockwise: bool | None = None
        """
        Whether the nodes are in a clockwise direction.
        """

        self._extend_by_eps_sides: set[int] | None = None
        """
        The set of sides that must be extended by eps for a clear overlap.
        """

        self._current_node: Vector2 | None = None
        """
        The current node of the polygon being processed.
        """

        self._current_inner_angle: float | None = None
        """
        The current inner angle at the current node of the polygon being processed
        """

        self._current_normal_angle: float | None = None
        """
        The current normal angle at the current node of the polygon being processed.
        """

        self._index: int | None = None
        """
        The index of the current node of the polygon being processed.
        """

        self._new_nodes: List[Vector2] = []
        """
        The new nodes of the polygon.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def extend_sides(self,
                     *,
                     context: Context,
                     nodes: List[Vector2],
                     inner_angles: List[float],
                     normal_angles: List[float],
                     is_clockwise: bool,
                     extend_by_eps_sides: set[int]) -> List[Vector2]:
        """
        Returns a modified list of nodes such that it appears that the sides are extended by eps for a clear overlap.

        @param context: The build context.
        @param nodes: The nodes of the polygon.
        @param inner_angles: The inner angles of the polygon.
        @param normal_angles: The absolute angles of the normal of each node.
        @param is_clockwise: Whether the nodes are in a clockwise direction.
        @param extend_by_eps_sides: The set of sides that must be extended by eps for a clear overlap.
        """
        self._nodes = nodes
        self._inner_angles = inner_angles
        self._normal_angles = normal_angles
        self._is_clockwise = is_clockwise
        self._extend_by_eps_sides = extend_by_eps_sides

        self._new_nodes = []
        n = len(self._nodes)
        for self._index in range(n):
            self._set_currents()

            extend_by_eps_side1 = (self._index - 1) % n in self._extend_by_eps_sides
            extend_by_eps_side2 = self._index in self._extend_by_eps_sides

            if self._current_inner_angle <= 180.0:
                # Outer corner.
                if not extend_by_eps_side1 and not extend_by_eps_side2:
                    self._extend_outer_corner_no_sides(context)

                elif not extend_by_eps_side1 and extend_by_eps_side2:
                    self._extend_outer_corner_side2(context)

                elif extend_by_eps_side1 and not extend_by_eps_side2:
                    self._extend_outer_corner_side1(context)

                elif extend_by_eps_side1 and extend_by_eps_side2:
                    self._extend_outer_corner_side1_and_side2(context)

                else:
                    raise ValueError('Someone broke math.')
            else:
                # Inner corner.
                if not extend_by_eps_side1 and not extend_by_eps_side2:
                    self._extend_inner_corner_no_sides(context)

                elif not extend_by_eps_side1 and extend_by_eps_side2:
                    self._extend_inner_corner_side2(context)

                elif extend_by_eps_side1 and not extend_by_eps_side2:
                    self._extend_inner_corner_side1(context)

                elif extend_by_eps_side1 and extend_by_eps_side2:
                    self._extend_inner_corner_side1_and_side2(context)

                else:
                    raise ValueError('Someone broke math.')

        return self._new_nodes

    # ------------------------------------------------------------------------------------------------------------------
    def _set_currents(self) -> None:
        """
        Set the current properties for the current node being processed.
        """
        self._current_node = self._nodes[self._index]
        self._current_inner_angle = self._inner_angles[self._index]
        self._current_normal_angle = self._normal_angles[self._index]

    # ------------------------------------------------------------------------------------------------------------------
    def _extend_inner_corner_no_sides(self, context: Context) -> None:
        """
        Handles the case were at an inner corner neither sides are extended.

        :param context: The build context.
        """
        self._new_nodes.append(self._current_node)

    # ------------------------------------------------------------------------------------------------------------------
    def _extend_inner_corner_side1(self, context: Context) -> None:
        """
        Handles the case were at an inner corner the first side is extended only.

        :param context: The build context.
        """
        if self._is_clockwise:
            angle = self._current_normal_angle + 0.5 * self._current_inner_angle
        else:
            angle = self._current_normal_angle - 0.5 * self._current_inner_angle
        self._new_nodes.append(self._current_node + Vector2.from_polar(context.eps, angle))

    # ------------------------------------------------------------------------------------------------------------------
    def _extend_inner_corner_side2(self, context: Context) -> None:
        """
        Handles the case were at an inner corner the second side is extended only.

        :param context: The build context.
        """
        if self._is_clockwise:
            angle = self._current_normal_angle - 0.5 * self._current_inner_angle
        else:
            angle = self._current_normal_angle + 0.5 * self._current_inner_angle
        self._new_nodes.append(self._current_node + Vector2.from_polar(context.eps, angle))

    # ------------------------------------------------------------------------------------------------------------------
    def _extend_inner_corner_side1_and_side2(self, context: Context) -> None:
        """
        Handles the case were at an inner corner both the first and the second side must be extended.

        :param context: The build context.
        """
        alpha = 0.5 * (360.0 - self._current_inner_angle)
        length = context.eps / math.sin(math.radians(alpha))
        length = min(length,
                     Vector2.distance(self._current_node, self._nodes[(self._index - 1) % len(self._nodes)]),
                     Vector2.distance(self._current_node, self._nodes[(self._index + 1) % len(self._nodes)]))
        eps0 = Vector2.from_polar(length, self._current_normal_angle + 180.0)
        self._new_nodes.append(self._current_node + eps0)

    # ------------------------------------------------------------------------------------------------------------------
    def _extend_outer_corner_no_sides(self, context: Context) -> None:
        """
        Handles the case were at an outer corner neither sides must be extended.

        :param context: The build context.
        """
        self._new_nodes.append(self._current_node)

    # ------------------------------------------------------------------------------------------------------------------
    def _extend_outer_corner_side1(self, context: Context) -> None:
        """
        Handles the case were at an outer corner the first side must be extended only.

        :param context: The build context.
        """
        if self._is_clockwise:
            angle = self._current_normal_angle - 0.5 * self._current_inner_angle - 90.0
        else:
            angle = self._current_normal_angle + 0.5 * self._current_inner_angle + 90.0
        self._new_nodes.append(self._current_node + Vector2.from_polar(context.eps, angle))
        self._new_nodes.append(self._current_node)

    # ------------------------------------------------------------------------------------------------------------------
    def _extend_outer_corner_side2(self, context: Context) -> None:
        """
        Handles the case were at an outer corner the second side must be extended only.

        :param context: The build context.
        """
        self._new_nodes.append(self._current_node)
        if self._is_clockwise:
            angle = self._current_normal_angle + 0.5 * self._current_inner_angle + 90.0
        else:
            angle = self._current_normal_angle - 0.5 * self._current_inner_angle - 90.0
        self._new_nodes.append(self._current_node + Vector2.from_polar(context.eps, angle))

    # ------------------------------------------------------------------------------------------------------------------
    def _extend_outer_corner_side1_and_side2(self, context: Context) -> None:
        """
        Handles the case were at an outer corner both the first and the second sides must be extended.

        :param context: The build context.
        """
        if self._current_inner_angle >= 90.0:
            self._extend_outer_corner_side1_and_side2_oblique(context)
        else:
            self._extend_outer_corner_side1_and_side2_sharp(context)

    # ------------------------------------------------------------------------------------------------------------------
    def _extend_outer_corner_side1_and_side2_sharp(self, context: Context) -> None:
        """
        Handles the case were at a sharp outer corner both the first and the second sides must be extended.

        :param context: The build context.
        """
        if self._is_clockwise:
            angle1 = self._current_normal_angle - 0.5 * self._current_inner_angle - 90.0
            angle2 = self._current_normal_angle + 0.5 * self._current_inner_angle + 90.0
        else:
            angle1 = self._current_normal_angle + 0.5 * self._current_inner_angle + 90.0
            angle2 = self._current_normal_angle - 0.5 * self._current_inner_angle - 90.0
        self._new_nodes.append(self._current_node + Vector2.from_polar(context.eps, angle1))
        self._new_nodes.append(self._current_node + Vector2.from_polar(context.eps,
                                                                       self._current_normal_angle + 180.0))
        self._new_nodes.append(self._current_node + Vector2.from_polar(context.eps, angle2))

    # ------------------------------------------------------------------------------------------------------------------
    def _extend_outer_corner_side1_and_side2_oblique(self, context: Context) -> None:
        """
        Handles the case were at an oblique outer corner both the first and the second sides must be extended.

        :param context: The build context.
        """
        length = context.eps / math.cos(math.radians(0.5 * (180.0 - self._current_inner_angle)))
        self._new_nodes.append(self._current_node + Vector2.from_polar(length, self._current_normal_angle + 180.0))

# ----------------------------------------------------------------------------------------------------------------------
