from typing import Any, Dict

from super_scad.d2.Semicircle import Semicircle
from super_scad.d3.private.PrivateSphere import PrivateSphere
from super_scad.d3.RotateExtrude import RotateExtrude
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Rotate2D import Rotate2D
from super_scad.util.Radius2Sides4n import Radius2Sides4n


class Sphere(ScadWidget):
    """
    Class for spheres. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Primitive_Solids#sphere.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 radius: float | None = None,
                 diameter: float | None = None,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 fn4n: bool | None = None):
        """
        Object constructor.

        :param radius: The radius of the sphere.
        :param diameter: The diameter of the sphere.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of three or more override fa and fs.
        :param fn4n: Whether to create a sphere with a multiple of four vertices.
        """
        ScadWidget.__init__(self)

        self._radius: float | None = radius
        """
        The radius of the sphere.
        """

        self._diameter: float | None = diameter
        """
        The diameter of the sphere.
        """

        self._fa: float | None = fa
        """
        The minimum angle (in degrees) of each fragment.
        """

        self._fs: float | None = fs
        """
        The minimum circumferential length of each fragment.
        """

        self._fn: int | None = fn
        """
        The fixed number of fragments in 360 degrees.
        """

        self._fn4n: bool | None = fn4n
        """
        Whether to create a sphere with a multiple of four vertices.
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
        validator.validate_exclusive({'radius'}, {'diameter'})
        validator.validate_required({'radius', 'diameter'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius(self) -> float:
        """
        Returns the radius of the sphere.
        """
        if self._radius is None:
            self._radius = 0.5 * self._diameter

        return self._radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter(self) -> float:
        """
        Returns the diameter of the sphere.
        """
        if self._diameter is None:
            self._diameter = 2.0 * self._radius

        return self._diameter

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fa(self) -> float | None:
        """
        Returns the minimum angle (in degrees) of each fragment.
        """
        return self._fa

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fs(self) -> float | None:
        """
        Returns the minimum circumferential length of each fragment.
        """
        return self._fs

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn(self) -> int | None:
        """
        Returns the fixed number of fragments in 360 degrees. Values of three or more override fa and fs.
        """
        return self._fn

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn4n(self) -> bool:
        """
        Returns whether to create a circle with multiple of 4 vertices.
        """
        if self._fn4n is None:
            self._fn4n = False

        return self._fn4n

    # ------------------------------------------------------------------------------------------------------------------
    def real_fn(self, context: Context) -> int | None:
        """
        Returns the real fixed number of fragments in 360 degrees.
        """
        if self.fn4n:
            return Radius2Sides4n.r2sides4n(context, self.radius)

        return self.fn

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        if not self.fn4n:
            return PrivateSphere(diameter=self.diameter, fa=self.fa, fs=self.fs, fn=self.real_fn(context))

        return RotateExtrude(angle=360.0,
                             fn=self.real_fn(context),
                             child=Rotate2D(angle=-90.0, child=Semicircle(diameter=self.diameter, fn4n=True)))

# ----------------------------------------------------------------------------------------------------------------------
