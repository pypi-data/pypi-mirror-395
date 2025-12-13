import math
from typing import Any, Dict

from super_scad.d3.private.PrivateCylinder import PrivateCylinder
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Rotate3D import Rotate3D
from super_scad.transformation.Translate3D import Translate3D
from super_scad.type.Vector3 import Vector3
from super_scad.util.Radius2Sides4n import Radius2Sides4n


class Cylinder(ScadWidget):
    """
    Widget for creating cylinders.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 height: float | None = None,
                 start_point: Vector3 | None = None,
                 end_point: Vector3 | None = None,
                 radius: float | None = None,
                 diameter: float | None = None,
                 center: bool | None = None,
                 extend_by_eps_top: bool = False,
                 extend_by_eps_bottom: bool = False,
                 extend_by_eps_radius: bool = False,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 fn4n: bool | None = None):
        """
        Object constructor.

        :param height: The height of the cylinder.
        :param start_point: The start point of the cylinder.
        :param end_point: The end point of the cylinder.
        :param radius: The radius of the cylinder.
        :param diameter: The diameter of the cylinder.
        :param center: Whether the cylinder is centered along the z-as. Defaults to false.
        :param extend_by_eps_top: Whether to extend the top of the cylinder by eps for a clear overlap.
        :param extend_by_eps_bottom: Whether to extend the bottom of the cylinder by eps for a clear overlap.
        :param extend_by_eps_radius: Whether to extend the radius of the cylinder by eps for a clear overlap.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        :param fn4n: Whether to create a cylinder with a multiple of 4 vertices.
        """
        ScadWidget.__init__(self)

        self._height: float | None = height
        """
        The height of the cylinder.
        """

        self._start_point: Vector3 | None = start_point
        """
        The start point of the cylinder.
        """

        self._end_point: Vector3 | None = end_point
        """
        The end point of the cylinder.
        """

        self._radius: float | None = radius
        """
        The radius of the cylinder.
        """

        self._diameter: float | None = diameter
        """
        The diameter of the cylinder.
        """

        self._center: bool | None = center
        """
        Whether the cylinder is centered along the z-as. Defaults to false.
        """

        self._extend_by_eps_top: bool = extend_by_eps_top
        """
        Whether to extend the top of the cylinder by eps for a clear overlap.
        """

        self._extend_by_eps_bottom: bool = extend_by_eps_bottom
        """
        Whether to extend the bottom of the cylinder by eps for a clear overlap.
        """

        self._extend_by_eps_radius: bool = extend_by_eps_radius
        """
        Whether to extend the radius of the cylinder by eps for a clear overlap.
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
        Whether to create a cylinder with a multiple of 4 vertices.
        """

        self._explicit_height: bool = height is not None
        """
        Whether the height is explicit specified.
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
        validator.validate_exclusive({'height'}, {'start_point', 'end_point'})
        validator.validate_exclusive({'radius'}, {'diameter'})
        validator.validate_exclusive({'fn4n'}, {'fa', 'fs', 'fn'})
        validator.validate_required({'height', 'start_point'},
                                    {'height', 'end_point'},
                                    {'radius', 'diameter'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the cylinder is centered along the z-as.
        """
        if self._center is None:
            self._center = False

        return self._center

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius(self) -> float:
        """
        Returns the radius of the cylinder.
        """
        if self._radius is None:
            self._radius = 0.5 * self._diameter

        return self._radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter(self) -> float:
        """
        Returns the diameter of the cylinder.
        """
        if self._diameter is None:
            self._diameter = 2.0 * self._radius

        return self._diameter

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def height(self) -> float:
        """
        Returns the height/length of the cylinder.
        """
        if self._height is None:
            self._height = Vector3.distance(self._start_point, self._end_point)

        return self._height

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def start_point(self) -> Vector3:
        """
        Returns the start point of the cylinder.
        """
        if self._start_point is None:
            self._start_point = Vector3(0.0, 0.0, -self._height / 2.0 if self.center else 0.0)

        return self._start_point

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def end_point(self) -> Vector3:
        """
        Returns the end point of the cylinder.
        """
        if self._end_point is None:
            self._end_point = Vector3(0.0, 0.0, self._height / 2.0 if self.center else self._height)

        return self._end_point

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_top(self) -> bool:
        """
        Returns whether the top of the cylinder is extended by eps.
        """
        return self._extend_by_eps_top

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_bottom(self) -> bool:
        """
        Returns whether the bottom of the cylinder is extended by eps.
        """
        return self._extend_by_eps_bottom

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_radius(self) -> bool:
        """
        Returns whether the radius of the cylinder is extended by eps.
        """
        return self._extend_by_eps_radius

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
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        diameter = self.diameter
        if self.extend_by_eps_radius:
            diameter += 2.0 * context.eps

        height = self.height
        if self.extend_by_eps_top:
            height += context.eps
        if self.extend_by_eps_bottom:
            height += context.eps

        center = self.center and self.extend_by_eps_top == self.extend_by_eps_bottom

        cylinder = PrivateCylinder(height=height,
                                   diameter=diameter,
                                   center=center,
                                   fa=self.fa,
                                   fs=self.fs,
                                   fn=self.real_fn(context))

        if self._explicit_height:
            if not center:
                z = 0.0
                if self.extend_by_eps_bottom:
                    z -= context.eps
                if self.center:
                    z -= 0.5 * self.height
                if z != 0.0:
                    cylinder = Translate3D(z=z, child=cylinder)
        else:
            if self.extend_by_eps_bottom:
                cylinder = Translate3D(z=-context.eps, child=cylinder)

            diff = self.end_point - self.start_point
            cylinder = Translate3D(vector=self.start_point,
                                   child=Rotate3D(angle_y=math.degrees(math.acos(diff.z / diff.length)),
                                                  angle_z=math.degrees(math.atan2(diff.y, diff.x)),
                                                  child=cylinder))

        return cylinder

# ----------------------------------------------------------------------------------------------------------------------
