from typing import Any, Dict

from super_scad.boolean.Intersection import Intersection
from super_scad.d2.Circle import Circle
from super_scad.d2.Rectangle import Rectangle
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Translate2D import Translate2D


class Semicircle(ScadWidget):
    """
    Widget for creating semicircles.
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

        :param radius: The radius of the semicircle.
        :param diameter: The diameter of the semicircle.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of three or more override fa and fs.
        :param fn4n: Whether to create a semicircle based on circle with a multiple of four vertices.
        """
        ScadWidget.__init__(self)

        self._radius: float | None = radius
        """
        The radius of the semicircle.
        """

        self._diameter: float | None = diameter
        """
        The diameter of the semicircle.
        """

        self._fa: float | None = fa
        """
        The minimum angle (in degrees) of each fragment.
        """

        self._fs: float | None = fs
        """
        The fixed number of fragments in 360 degrees.
        """

        self._fn: int | None = fn
        """
        The fixed number of fragments in 360 degrees.
        """

        self._fn4n: bool | None = fn4n
        """
        Whether to create a semicircle based on circle with a multiple of four vertices.
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
        Returns the radius of this semicircle.
        """
        if self._radius is None:
            self._radius = 0.5 * self._diameter

        return self._radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter(self) -> float:
        """
        Returns the diameter of this semicircle.
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
        Returns whether to create a semicircle with multiple of four vertices.
        """
        return self._fn4n

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return Intersection(children=[Circle(diameter=self.diameter,
                                             fa=self.fa,
                                             fs=self.fs,
                                             fn=self.fn,
                                             fn4n=self.fn4n),
                                      Translate2D(x=-(self.radius + context.eps),
                                                  child=Rectangle(width=self.diameter + 2 * context.eps,
                                                                  depth=self.radius + context.eps))])

# ----------------------------------------------------------------------------------------------------------------------
