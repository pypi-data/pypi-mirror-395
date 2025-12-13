import math
import typing
from dataclasses import dataclass

Vector3 = typing.NewType('Vector3', None)


@dataclass(frozen=True)
class Vector3:
    """
    A coordinate in 3D space.
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

    z: float
    """
    The z-coordinate of this point.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __repr__(self):
        return f"[{self.x}, {self.y}, {self.z}]"

    # ------------------------------------------------------------------------------------------------------------------
    def __add__(self, other: Vector3):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    # ------------------------------------------------------------------------------------------------------------------
    def __sub__(self, other: Vector3):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    # ------------------------------------------------------------------------------------------------------------------
    def __truediv__(self, other: float):
        return Vector3(self.x / other, self.y / other, self.z / other)

    # ------------------------------------------------------------------------------------------------------------------
    def __mul__(self, other: float):
        return Vector3(self.x * other, self.y * other, self.z * other)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def from_polar(length: float, *, azimuth: float, inclination: float) -> Vector3:
        """
        Creates a 3-dimensional vector from polar coordinates.

        @param length: The length of the vector.
        @param azimuth: The azimuth, i.e., the angle of the vector in the xy-plane.
        @param inclination: The inclination, i.e., the angle of the vector in the z-axis.
        """
        phi_radians = math.radians(azimuth)
        theta_radians = math.radians(inclination)

        return Vector3(length * math.sin(theta_radians) * math.cos(phi_radians),
                       length * math.sin(theta_radians) * math.sin(phi_radians),
                       length * math.cos(theta_radians))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def distance(p: Vector3, q: Vector3) -> float:
        """
        Returns the Euclidean distance between two vectors p and q.

        @param p: Vector p.
        @param q: Vector q.
        """
        return math.sqrt((p.x - q.x) ** 2 + (p.y - q.y) ** 2 + (p.z - q.z) ** 2)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def length(self) -> float:
        """
        Returns the length of this vector.
        """
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def normal(self) -> Vector3:
        """
        Returns the unit vector of this vector.
        """
        length = self.length

        return Vector3(self.x / length, self.y / length, self.z / length)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def azimuth(self) -> float:
        """
        Returns the azimuth, i.e., the angle of the vector in the xy-plane.
        """
        return math.atan2(self.y, self.x)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def theta(self) -> float:
        """
        Returns the inclination, i.e., the angle between this vector and the z-axis.
        """
        return math.acos(self.z / self.length)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def is_origin(self) -> bool:
        """
        Returns whether this vector is the origin.
        """
        return self.x == 0.0 and self.y == 0.0 and self.z == 0.0

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def is_not_origin(self) -> bool:
        """
        Returns whether this vector is not the origin.
        """
        return self.x != 0.0 or self.y != 0.0 or self.z != 0.0

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def cross_product(v1: Vector3, v2: Vector3) -> Vector3:
        """
        Returns the cross-product of two vectors.
        """
        return Vector3(v1.y * v2.z - v1.z * v2.y,
                       v1.z * v2.x - v1.x * v2.z,
                       v1.x * v2.y - v1.y * v2.x)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def dot_product(v1: Vector3, v2: Vector3) -> float:
        """
        Returns the dot product of two vectors.
        """
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

    # ------------------------------------------------------------------------------------------------------------------
    def rotate_x(self, angle: float) -> Vector3:
        """
        Returns a copy of this vector rotated around the x-axis using the right-hand rule.

        :param angle: The angle of rotation.
        """
        radians = math.radians(angle)

        return Vector3(self.x,
                       self.y * math.cos(radians) - self.z * math.sin(radians),
                       self.y * math.sin(radians) + self.z * math.cos(radians))

    # ------------------------------------------------------------------------------------------------------------------
    def rotate_y(self, angle: float) -> Vector3:
        """
        Returns a copy of this vector rotated around the y-axis using the right-hand rule.

        :param angle: The angle of rotation.
        """
        radians = math.radians(angle)

        return Vector3(self.x * math.cos(radians) + self.z * math.sin(radians),
                       self.y,
                       -self.x * math.sin(radians) + self.z * math.cos(radians))

    # ------------------------------------------------------------------------------------------------------------------
    def rotate_z(self, angle: float) -> Vector3:
        """
        Returns a copy of this vector rotated around the z-axis using the right-hand rule.

        :param angle: The angle of rotation.
        """
        radians = math.radians(angle)

        return Vector3(self.x * math.cos(radians) - self.y * math.sin(radians),
                       self.x * math.sin(radians) + self.y * math.cos(radians),
                       self.z)

# ----------------------------------------------------------------------------------------------------------------------
