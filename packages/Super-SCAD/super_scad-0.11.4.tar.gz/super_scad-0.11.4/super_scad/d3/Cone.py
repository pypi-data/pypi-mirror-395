from typing import Any, Dict

from super_scad.d3.private.PrivateCylinder import PrivateCylinder
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.util.Radius2Sides4n import Radius2Sides4n


class Cone(ScadWidget):
    """
    Widget for creating cones. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Primitive_Solids#cylinder.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 height: float,
                 bottom_radius: float | None = None,
                 bottom_diameter: float | None = None,
                 top_radius: float | None = None,
                 top_diameter: float | None = None,
                 center: bool = False,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 fn4n: bool | None = None):
        """
        Object constructor.

        :param height: The height of the cone.
        :param bottom_radius: The radius at the bottom of the cone.
        :param bottom_diameter: The diameter at the bottom of the cone.
        :param top_radius: The radius at the top of the cone.
        :param top_diameter: The diameter at the top of the cone.
        :param center: Whether the cone is centered in the z-direction.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        :param fn4n: Whether to create a cone with a multiple of 4 vertices.
        """
        ScadWidget.__init__(self)

        self._height: float = height
        """
        The height of the cone.
        """

        self._bottom_radius: float | None = bottom_radius
        """
        The bottom radius of the cone.
        """

        self._bottom_diameter: float | None = bottom_diameter
        """
        The bottom diameter of the cone.
        """

        self._top_radius: float | None = top_radius
        """
        The top radius of the cone.
        """

        self._top_diameter: float | None = top_diameter
        """
        The top diameter of the cone.
        """

        self._center: bool = center
        """
        Whether the cone is centered in the z-direction.
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
        The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        """

        self._fn4n: bool | None = fn4n
        """
        Whether to create a cone with a multiple of 4 vertices.
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
        validator.validate_exclusive({'bottom_radius'}, {'bottom_diameter'})
        validator.validate_exclusive({'top_radius'}, {'top_diameter'})
        validator.validate_exclusive({'fn4n'}, {'fa', 'fs', 'fn'})
        validator.validate_required({'height'},
                                    {'bottom_radius', 'bottom_diameter'},
                                    {'top_radius', 'top_diameter'},
                                    {'center'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the cone is centered along the z-as.
        """
        return self._center

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_radius(self) -> float:
        """
        Returns the bottom radius of the cone.
        """
        if self._bottom_radius is None:
            self._bottom_radius = 0.5 * self._bottom_diameter

        return self._bottom_radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_diameter(self) -> float:
        """
        Returns the bottom diameter of the cone.
        """
        if self._bottom_diameter is None:
            self._bottom_diameter = 2.0 * self._bottom_radius

        return self._bottom_diameter

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_radius(self) -> float:
        """
        Returns the top radius of the cone.
        """
        if self._top_radius is None:
            self._top_radius = 0.5 * self._top_diameter

        return self._top_radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_diameter(self) -> float:
        """
        Returns the top diameter of the cone.
        """
        if self._top_diameter is None:
            self._top_diameter = 2.0 * self._top_radius

        return self._top_diameter

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def height(self) -> float:
        """
        Returns the height of the cone.
        """
        return self._height

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
            return Radius2Sides4n.r2sides4n(context, max(self.bottom_radius, self.top_radius))

        return self.fn

    # ----------------------------------------f--------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return PrivateCylinder(height=self.height,
                               bottom_diameter=self.bottom_diameter,
                               top_diameter=self.top_diameter,
                               center=self.center,
                               fa=self.fa,
                               fs=self.fs,
                               fn=self.real_fn(context))

# ----------------------------------------------------------------------------------------------------------------------
