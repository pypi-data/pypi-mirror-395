import math
import typing
from dataclasses import dataclass

Vector2 = typing.NewType('Vector2', None)


@dataclass(frozen=True)
class Vector2:
    """
    A coordinate in 2D space.
    """

    # ------------------------------------------------------------------------------------------------------------------
    x: float
    """
    The x-coordinate of this point.
    """

    y: float
    """
    The y-coordinate of this point.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __repr__(self):
        return f"[{self.x}, {self.y}]"

    # ------------------------------------------------------------------------------------------------------------------
    def __add__(self, other: Vector2):
        return Vector2(self.x + other.x, self.y + other.y)

    # ------------------------------------------------------------------------------------------------------------------
    def __sub__(self, other: Vector2):
        return Vector2(self.x - other.x, self.y - other.y)

    # ------------------------------------------------------------------------------------------------------------------
    def __truediv__(self, other: float):
        return Vector2(self.x / other, self.y / other)

    # ------------------------------------------------------------------------------------------------------------------
    def __mul__(self, other: float):
        return Vector2(self.x * other, self.y * other)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def from_polar(length: float, angle: float) -> Vector2:
        """
        Creates a 2-dimensional vector from polar coordinates.

        @param length: The length of the vector.
        @param angle: The angle of the vector.
        """
        return Vector2(length * math.cos(math.radians(angle)), length * math.sin(math.radians(angle)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle(self) -> float:
        """
        Returns the angle of this vector.
        """
        return math.degrees(math.atan2(self.y, self.x))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def is_origin(self) -> bool:
        """
        Returns whether this vector is the origin.
        """
        return self.x == 0.0 and self.y == 0.0

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def is_not_origin(self) -> bool:
        """
        Returns whether this vector is not the origin.
        """
        return self.x != 0.0 or self.y != 0.0

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def length(self) -> float:
        """
        Returns the length of this vector.
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def unit(self) -> Vector2:
        """
        Returns the unit vector of this vector.
        """
        length = self.length

        return Vector2(self.x / length, self.y / length)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def distance(p: Vector2, q: Vector2) -> float:
        """
        Returns the Euclidean distance between two vectors p and q.

        @param p: Vector p.
        @param q: Vector q.
        """
        return math.sqrt((p.x - q.x) ** 2 + (p.y - q.y) ** 2)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def intermediate(p: Vector2, q: Vector2, ratio: float = 0.5) -> Vector2:
        """
        Returns the intermediate point between two vectors p and q.

        @param p: Vector p.
        @param q: Vector q.
        @param ratio: The ratio between the two vectors.
        """
        diff = q - p

        return p + Vector2.from_polar(ratio * diff.length, diff.angle)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def cross_product(p: Vector2, q: Vector2) -> float:
        """
        Returns the cross-product of two vectors.
        """
        return p.x * q.y - p.y * q.x

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def dot_product(p: Vector2, q: Vector2) -> float:
        """
        Returns the dot product of two vectors.
        """
        return p.x * q.x + p.y * q.y

    # ------------------------------------------------------------------------------------------------------------------
    def rotate(self, angle: float) -> Vector2:
        """
        Returns a copy of this vector rotated counterclockwise.

        :param angle: The angle of rotation.
        """
        radians = math.radians(angle)

        return Vector2(self.x * math.cos(radians) - self.y * math.sin(radians),
                       self.x * math.sin(radians) + self.y * math.cos(radians))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def orientation(p: Vector2, q: Vector2, r: Vector2) -> float:
        """
        Returns the orientation of an ordered triplet (p, q, r), a.k.a., the cross product of q - p and q - r.
        * = 0.0: Collinear points;
        * > 0.0: Clockwise points;
        * < 0.0: Counterclockwise points.

        @param p: Point p.
        @param q: Point q.
        @param r: Point r.
        """
        return ((q.y - p.y) * (r.x - q.x)) - ((q.x - p.x) * (r.y - q.y))

# ----------------------------------------------------------------------------------------------------------------------
