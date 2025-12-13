from typing import Any, Dict

from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.private.PrivateScale import PrivateScale
from super_scad.type.Vector3 import Vector3


class Scale3D(ScadSingleChildParent):
    """
    Scales its child widget using a specified scaling factor.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 factor: Vector3 | float | None = None,
                 factor_x: float | None = None,
                 factor_y: float | None = None,
                 factor_z: float | None = None,
                 child: ScadWidget):
        """
        Object constructor.

        :param factor: The scaling factor along all three the axes.
        :param factor_x: The scaling factor along the x-axis.
        :param factor_y: The scaling factor along the y-axis.
        :param factor_z: The scaling factor along the z-axis.
        :param child: The child widget to be scaled.
        """
        ScadSingleChildParent.__init__(self, child=child)

        self._factor: Vector3 | float | None = factor
        """
        The scaling factor along all the two axes.
        """

        self._factor_x: float | None = factor_x
        """
        The scaling factor along the x-axis.
        """

        self._factor_y: float | None = factor_y
        """
        The scaling factor along the y-axis.
        """

        self._factor_z: float | None = factor_z
        """
        The scaling factor along the z-axis.
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
        validator.validate_exclusive({'factor'}, {'factor_x', 'factor_y', 'factor_z'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def factor(self) -> Vector3:
        """
        Returns the scaling factor along all two axes.
        """
        if self._factor is None:
            self._factor = Vector3(self.factor_x, self.factor_y, self.factor_z)
        elif isinstance(self._factor, float):
            self._factor = Vector3(self._factor, self._factor, self._factor)

        return self._factor

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def factor_x(self) -> float:
        """
        Returns the scaling factor along the x-axis.
        """
        if self._factor_x is None:
            if isinstance(self._factor, Vector3):
                self._factor_x = self._factor.x
            elif isinstance(self._factor, float):
                self._factor_x = self._factor
            else:
                self._factor_x = 1.0

        return self._factor_x

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def factor_y(self) -> float:
        """
        Returns the scaling factor along the y-axis.
        """
        if self._factor_y is None:
            if isinstance(self._factor, Vector3):
                self._factor_y = self._factor.y
            elif isinstance(self._factor, float):
                self._factor_y = self._factor
            else:
                self._factor_y = 1.0

        return self._factor_y

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def factor_z(self) -> float:
        """
        Returns the scaling factor along the z-axis.
        """
        if self._factor_z is None:
            if isinstance(self._factor, Vector3):
                self._factor_z = self._factor.z
            elif isinstance(self._factor, float):
                self._factor_z = self._factor
            else:
                self._factor_z = 1.0

        return self._factor_z

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return PrivateScale(factor=self.factor, child=self.child)

# ----------------------------------------------------------------------------------------------------------------------
