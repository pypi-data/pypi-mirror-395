import math

from super_scad.type import Vector2


class LineIntersection2D:
    """
    A utility class for computing the intersection point of two lines in 2D space.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def intersection(line_a1: Vector2,
                     line_a2: Vector2,
                     line_b1: Vector2,
                     line_b2: Vector2) -> Vector2 | None:
        """
        Returns the intersection point between two lines given tow points on each line.

        :param line_a1: The first point on the first line.
        :param line_a2: The second point on the first line.
        :param line_b1: The first point on the second line.
        :param line_b2: The second point on the second line.
        """
        a1 = line_a2.y - line_a1.y
        b1 = line_a1.x - line_a2.x
        c1 = a1 * line_a1.x + b1 * line_a1.y

        a2 = line_b2.y - line_b1.y
        b2 = line_b1.x - line_b2.x
        c2 = a2 * line_b1.x + b2 * line_b1.y

        determinant = a1 * b2 - a2 * b1

        if determinant == 0.0:
            return None

        x = (b2 * c1 - b1 * c2) / determinant
        y = (a1 * c2 - a2 * c1) / determinant

        if not math.isfinite(x) or not math.isfinite(y):
            return None

        return Vector2(x, y)

# ----------------------------------------------------------------------------------------------------------------------
