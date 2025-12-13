from typing import Any, Dict

from super_scad.d3.Cuboid import Cuboid
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector3


class Cube(ScadWidget):
    """
    Widget for creating cubes. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Primitive_Solids#cube.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 size: float,
                 center: bool = False,
                 extend_by_eps_front: bool = False,
                 extend_by_eps_back: bool = False,
                 extend_by_eps_top: bool = False,
                 extend_by_eps_bottom: bool = False,
                 extend_by_eps_left: bool = False,
                 extend_by_eps_right: bool = False):
        """
        Object constructor.

        :param size: The size of the cube.
        :param center: Whether the cube is centered at the origin.
        :param extend_by_eps_front: Whether to extend the front face of the cube by eps for a clear overlap.
        :param extend_by_eps_back: Whether to extend the back face of the cube by eps for a clear overlap.
        :param extend_by_eps_top: Whether to extend the top face of the cube by eps for a clear overlap.
        :param extend_by_eps_bottom: Whether to extend the bottom face of the cube by eps for a clear overlap.
        :param extend_by_eps_left: Whether to extend the left face of the cube by eps for a clear overlap.
        :param extend_by_eps_right: Whether to extend the right face of the cube by eps for a clear overlap.
        """
        ScadWidget.__init__(self)

        self._size: float = size
        """
        The size of the cube.
        """

        self._center: bool = center
        """
        Whether the cube is centered at the origin.
        """

        self._extend_by_eps_front: bool = extend_by_eps_front
        """
        Whether to extend the front face of the cube by eps for a clear overlap.
        """

        self._extend_by_eps_back: bool = extend_by_eps_back
        """        
        Whether to extend the back face of the cube by eps for a clear overlap.
        """

        self._extend_by_eps_top: bool = extend_by_eps_top
        """
        Whether to extend the top face of the cube by eps for a clear overlap.
        """

        self._extend_by_eps_bottom: bool = extend_by_eps_bottom
        """
        Whether to extend the bottom face of the cube by eps for a clear overlap.
        """

        self._extend_by_eps_left: bool = extend_by_eps_left
        """
        Whether to extend the left face of the cube by eps for a clear overlap.
        """

        self._extend_by_eps_right: bool = extend_by_eps_right
        """
        Whether to extend the right face of the cube by eps for a clear overlap.
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
        validator.validate_required({'size'}, {'center'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the cube is centered at the origin.
        """
        return self._center

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def size(self) -> float:
        """
        Returns the size of the cube.
        """
        return self._size

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_front(self) -> bool:
        """
        Return whether to extend the front face of the cube by eps for a clear overlap.
        """
        return self._extend_by_eps_front

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_back(self) -> bool:
        """
        Return whether to extend the back face of the cube by eps for a clear overlap.
        """
        return self._extend_by_eps_back

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_top(self) -> bool:
        """
        Return whether to extend the top face of the cube by eps for a clear overlap.
        """
        return self._extend_by_eps_top

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_bottom(self) -> bool:
        """
        Return whether to extend the bottom face of the cube by eps for a clear overlap.
        """
        return self._extend_by_eps_bottom

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_left(self) -> bool:
        """
        Return whether to extend the left face of the cube by eps for a clear overlap.
        """
        return self._extend_by_eps_left

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_right(self) -> bool:
        """
        Return whether to extend the front face of the cube by eps for a clear overlap.
        """
        return self._extend_by_eps_right

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return Cuboid(size=Vector3(self.size, self.size, self.size),
                      center=self.center,
                      extend_by_eps_front=self.extend_by_eps_front,
                      extend_by_eps_back=self.extend_by_eps_back,
                      extend_by_eps_top=self.extend_by_eps_top,
                      extend_by_eps_bottom=self.extend_by_eps_bottom,
                      extend_by_eps_left=self.extend_by_eps_left,
                      extend_by_eps_right=self.extend_by_eps_right)

# ----------------------------------------------------------------------------------------------------------------------
