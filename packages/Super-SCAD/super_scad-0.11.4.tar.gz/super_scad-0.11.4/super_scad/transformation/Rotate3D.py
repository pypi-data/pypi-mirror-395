from typing import Any, Dict

from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.private.PrivateRotate import PrivateRotate
from super_scad.type.Vector3 import Vector3


class Rotate3D(ScadSingleChildParent):
    """
    Rotates its child degrees about the axis of the coordinate system or around an arbitrary axis. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#rotate.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 angle: float | Vector3 | None = None,
                 angle_x: float | None = None,
                 angle_y: float | None = None,
                 angle_z: float | None = None,
                 vector: Vector3 | None = None,
                 child: ScadWidget) -> None:
        """
        Object constructor.

        :param angle: The angle of rotation around all axis or a vector.
        :param angle_x: The angle of rotation around the x-axis.
        :param angle_y: The angle of rotation around the y-axis.
        :param angle_z: The angle of rotation around the z-axis.
        :param vector: The vector of rotation.
        :param child: The widget to be rotated.
        """
        ScadSingleChildParent.__init__(self, child=child)

        self._angle: float | Vector3 | None = angle
        """
        The angle of rotation around all axis or a vector.
        """

        self._angle_x: float | None = angle_x
        """
        The angle of rotation around the x-axis.
        """

        self._angle_y: float | None = angle_y
        """
        The angle of rotation around the y-axis.
        """

        self._angle_z: float | None = angle_z
        """
        The angle of rotation around the z-axis.
        """

        self._vector: Vector3 | None = vector
        """ 
        The vector of rotation.
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
        validator.validate_exclusive({'angle', 'vector'}, {'angle_x', 'angle_y', 'angle_z'})
        validator.validate_required({'angle_x', 'angle_y', 'angle_z', 'angle'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle(self) -> float | Vector3 | None:
        """
        Returns angle of rotation around all axis or a vector.
        """
        if self._vector is not None:
            return self._angle

        if self._angle is None:
            self._angle = Vector3(self.angle_x, self.angle_y, self.angle_z)

        return self._angle

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle_x(self) -> float | None:
        """
        Returns the angle of rotation around the x-axis.
        """
        if self._vector is not None:
            return None

        if self._angle_x is None:
            if self._angle is not None:
                self._angle_x = self._angle.x
            else:
                self._angle_x = 0.0

        return self._angle_x

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle_y(self) -> float | None:
        """
        Returns the angle of rotation around the y-axis.
        """
        if self._vector is not None:
            return None

        if self._angle_y is None:
            if self._angle is not None:
                self._angle_y = self._angle.y
            else:
                self._angle_y = 0.0

        return self._angle_y

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle_z(self) -> float | None:
        """
        Returns the angle of rotation around the z-axis.
        """
        if self._vector is not None:
            return None

        if self._angle_z is None:
            if self._angle is not None:
                self._angle_z = self._angle.z
            else:
                self._angle_z = 0.0

        return self._angle_z

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def vector(self) -> Vector3 | None:
        """
        Returns the vector of rotation.
        """
        return self._vector

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return PrivateRotate(angle=self.angle, vector=self.vector, child=self.child)

# ----------------------------------------------------------------------------------------------------------------------
