from typing import Any, Dict

from super_scad.d3.private.PrivateCube import PrivateCube
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Translate3D import Translate3D
from super_scad.type.Vector3 import Vector3


class Cuboid(ScadWidget):
    """
    Class for cuboids.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 size: Vector3 | None = None,
                 width: float | None = None,
                 depth: float | None = None,
                 height: float | None = None,
                 center: bool = False,
                 extend_by_eps_front: bool = False,
                 extend_by_eps_back: bool = False,
                 extend_by_eps_top: bool = False,
                 extend_by_eps_bottom: bool = False,
                 extend_by_eps_left: bool = False,
                 extend_by_eps_right: bool = False):
        """
        Object constructor.

        :param size: The size of the cuboid.
        :param width: The width (the size along the x-axis) of the cuboid.
        :param depth: The depth (the size along the y-axis) of the cuboid.
        :param height: The height (the size along the y-axis) of the cuboid.
        :param center: Whether the cuboid is centered at the origin.
        :param extend_by_eps_front: Whether to extend the front face of the cuboid by eps for a clear overlap.
        :param extend_by_eps_back: Whether to extend the back face of the cuboid by eps for a clear overlap.
        :param extend_by_eps_top: Whether to extend the top face of the cuboid by eps for a clear overlap.
        :param extend_by_eps_bottom: Whether to extend the bottom face of the cuboid by eps for a clear overlap.
        :param extend_by_eps_left: Whether to extend the left face of the cuboid by eps for a clear overlap.
        :param extend_by_eps_right: Whether to extend the right face of the cuboid by eps for a clear overlap.
        """
        ScadWidget.__init__(self)

        self._size: Vector3 | None = size
        """
        The size of the cuboid.
        """

        self._width: float | None = width
        """
        The width (the size along the x-axis) of the cuboid.
        """

        self._depth: float | None = depth
        """
        The depth (the size along the y-axis) of the cuboid.
        """

        self._height: float | None = height
        """
        The height (the size along the y-axis) of the cuboid.
        """

        self._center: bool = center
        """
        Whether the cuboid is centered at the origin.
        """

        self._extend_by_eps_front: bool = extend_by_eps_front
        """
        Whether to extend the front face of the cuboid by eps for a clear overlap.
        """

        self._extend_by_eps_back: bool = extend_by_eps_back
        """        
        Whether to extend the back face of the cuboid by eps for a clear overlap.
        """

        self._extend_by_eps_top: bool = extend_by_eps_top
        """
        Whether to extend the top face of the cuboid by eps for a clear overlap.
        """

        self._extend_by_eps_bottom: bool = extend_by_eps_bottom
        """
        Whether to extend the bottom face of the cuboid by eps for a clear overlap.
        """

        self._extend_by_eps_left: bool = extend_by_eps_left
        """
        Whether to extend the left face of the cuboid by eps for a clear overlap.
        """

        self._extend_by_eps_right: bool = extend_by_eps_right
        """
        Whether to extend the right face of the cuboid by eps for a clear overlap.
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
        validator.validate_exclusive({'size'}, {'width', 'depth', 'height'})
        validator.validate_required({'size', 'width'},
                                    {'size', 'depth'},
                                    {'size', 'height'},
                                    {'center'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the cuboid is centered at the origin.
        """
        return self._center

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def size(self) -> Vector3:
        """
        Returns the size of the cuboid.
        """
        if self._size is None:
            self._size = Vector3(x=self.width, y=self.depth, z=self.height)

        return self._size

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def width(self) -> float:
        """
        Returns the width of the cuboid.
        """
        if self._width is None:
            self._width = self._size.x

        return self._width

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def depth(self) -> float:
        """
        Returns the depth of the cuboid.
        """
        if self._depth is None:
            self._depth = self._size.y

        return self._depth

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def height(self) -> float:
        """
        Returns the height of the cuboid.
        """
        if self._height is None:
            self._height = self._size.z

        return self._height

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_front(self) -> bool:
        """
        Return whether to extend the front face of the cuboid by eps for a clear overlap.
        """
        return self._extend_by_eps_front

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_back(self) -> bool:
        """
        Return whether to extend the back face of the cuboid by eps for a clear overlap.
        """
        return self._extend_by_eps_back

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_top(self) -> bool:
        """
        Return whether to extend the top face of the cuboid by eps for a clear overlap.
        """
        return self._extend_by_eps_top

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_bottom(self) -> bool:
        """
        Return whether to extend the bottom face of the cuboid by eps for a clear overlap.
        """
        return self._extend_by_eps_bottom

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_left(self) -> bool:
        """
        Return whether to extend the left face of the cuboid by eps for a clear overlap.
        """
        return self._extend_by_eps_left

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_right(self) -> bool:
        """
        Return whether to extend the front face of the cuboid by eps for a clear overlap.
        """
        return self._extend_by_eps_right

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        cuboid = PrivateCube(size=self._real_size(context), center=self.center)

        translate = self._real_translation(context)
        if translate.is_not_origin:
            cuboid = Translate3D(vector=translate, child=cuboid)

        return cuboid

    # ------------------------------------------------------------------------------------------------------------------
    def _real_translation(self, context) -> Vector3:
        """
        Return the translation of the cuboid accounting for extending by eps.

        @param context: The build context.
        """
        x = 0.0
        y = 0.0
        z = 0.0
        if self.center:
            if self.extend_by_eps_left:
                x -= 1.0
            if self.extend_by_eps_right:
                x += 1.0
            if self.extend_by_eps_front:
                y -= 1.0
            if self.extend_by_eps_back:
                y += 1.0
            if self.extend_by_eps_top:
                z += 1.0
            if self.extend_by_eps_bottom:
                z -= 1.0
            translate = Vector3(x=x, y=y, z=z) * 0.5 * context.eps
        else:
            if self.extend_by_eps_left:
                x -= context.eps
            if self.extend_by_eps_front:
                y -= context.eps
            if self.extend_by_eps_bottom:
                z -= context.eps
            translate = Vector3(x=x, y=y, z=z)

        return translate

    # ------------------------------------------------------------------------------------------------------------------
    def _real_size(self, context) -> Vector3 | float:
        """
        Returns the real size of the cuboid.

        @param context: The build context
        """
        x = 0.0
        y = 0.0
        z = 0.0
        if self.extend_by_eps_left:
            x += context.eps
        if self.extend_by_eps_right:
            x += context.eps
        if self.extend_by_eps_front:
            y += context.eps
        if self.extend_by_eps_back:
            y += context.eps
        if self.extend_by_eps_top:
            z += context.eps
        if self.extend_by_eps_bottom:
            z += context.eps
        size = self.size + Vector3(x=x, y=y, z=z)

        if size.x == size.y and size.x == size.z:
            size = size.x

        return size

# ----------------------------------------------------------------------------------------------------------------------
