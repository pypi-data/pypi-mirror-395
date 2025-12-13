from typing import Any, Dict

from super_scad.d2.private.PrivateCircle import PrivateCircle
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.util.Radius2Sides4n import Radius2Sides4n


class Circle(ScadWidget):
    """
    Widget for creating circles. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#circle.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 radius: float | None = None,
                 diameter: float | None = None,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 fn4n: bool | None = None,
                 extend_by_eps_radius: bool = False):
        """
        Object constructor.

        :param radius: The radius of the circle.
        :param diameter: The diameter of the circle.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        :param fn4n: Whether to create a circle with a multiple of 4 vertices.
        :param extend_by_eps_radius: Whether to extend the radius by eps (or the diameter by 2*eps) for a clear overlap.
        """
        ScadWidget.__init__(self)

        self._radius: float | None = radius
        """
        The radius of the circle.
        """

        self._diameter: float | None = diameter
        """
        The diameter of the circle.
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
        Whether to create a circle with a multiple of 4 vertices.
        """

        self._extend_by_eps_radius: bool = extend_by_eps_radius
        """
        Whether to extend the radius by eps (or the diameter by 2*eps).
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
        validator.validate_exclusive({'fn4n'}, {'fa', 'fs', 'fn'})
        validator.validate_required({'radius', 'diameter'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius(self) -> float:
        """
        Returns the radius of the circle.
        """
        if self._radius is None:
            self._radius = 0.5 * self._diameter

        return self._radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter(self) -> float:
        """
        Returns the diameter of the circle.
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
        Returns the fixed number of fragments in 360 degrees. Values of 3 or more override $fa and $fs.
        """
        return self._fn

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn4n(self) -> bool | None:
        """
        Returns whether to create a circle with multiple of 4 vertices.
        """
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
    @property
    def extend_by_eps_radius(self) -> bool:
        """
        Returns whether to extend the radius by eps (or the diameter by 2*eps) for a clear overlap.
        """
        return self._extend_by_eps_radius

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        diameter = self.diameter
        if self.extend_by_eps_radius:
            diameter += 2.0 * context.eps

        return PrivateCircle(diameter=diameter, fa=self.fa, fs=self.fs, fn=self.real_fn(context))

# ----------------------------------------------------------------------------------------------------------------------
