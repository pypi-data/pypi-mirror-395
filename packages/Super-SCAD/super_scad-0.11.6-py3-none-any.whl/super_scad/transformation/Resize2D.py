from typing import Any, Dict, Tuple

from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.private.PrivateResize import PrivateResize
from super_scad.type.Vector2 import Vector2


class Resize2D(ScadSingleChildParent):
    """
    Modifies the size of the child widget to match the given width and depth. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#resize.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 new_size: Vector2 | None = None,
                 new_width: float | None = None,
                 new_depth: float | None = None,
                 auto: bool | Tuple[bool, bool] | None = None,
                 auto_width: bool | None = None,
                 auto_depth: bool | None = None,
                 convexity: int | None = None,
                 child: ScadWidget):
        """
        Object constructor.

        :param new_size: The new size along all two axes.
        :param new_width: The new width (the new size along the x-axis).
        :param new_depth: The new depth (the new size along the y-axis).
        :param auto: Whether to auto-scale any 0-dimensions to match.
        :param convexity: Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line 
                          through the child widget.
        :param child: The child widget to be resized.
        """
        ScadSingleChildParent.__init__(self, child=child)

        self._new_size: Vector2 | None = new_size
        """
        The new size along all two axes.
        """

        self._new_width: float | None = new_width
        """
        The new width (the new size along the x-axis).
        """

        self._new_depth: float | None = new_depth
        """
        The new depth (the new size along the y-axis).
        """

        self._auto: bool | Tuple[bool, bool] | None = auto
        """
        Whether to auto-scale any 0-dimensions to match.
        """

        self._auto_width: bool | None = auto_width
        """
        Whether to auto-scale any 0-dimensions to match.
        """

        self._auto_depth: bool | None = auto_depth
        """
        Whether to auto-scale any 0-dimensions to match.
        """

        self._convexity: int | None = convexity
        """
        The convexity of the child widget.
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
        validator.validate_exclusive({'new_size'}, {'new_width', 'new_depth'})
        validator.validate_exclusive({'auto'}, {'auto_width', 'auto_depth'})

        # Handle resizing beyond resolution.

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def new_size(self) -> Vector2:
        """
        Returns the new_size along all three axes.
        """
        if self._new_size is None:
            self._new_size = Vector2(self._new_width, self._new_depth)

        return self._new_size

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def new_width(self) -> float:
        """
        Returns new width (the new size along the x-axis).
        """
        if self._new_width is None:
            if self._new_size is not None:
                self._new_width = self._new_size.x
            else:
                self._new_width = 0.0

        return self._new_width

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def new_depth(self) -> float:
        """
        Returns the new depth (the new size along the y-axis).
        """
        if self._new_depth is None:
            if self._new_size is not None:
                self._new_depth = self._new_size.y
            else:
                self._new_depth = 0.0

        return self._new_depth

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def auto(self) -> Tuple[bool, bool]:
        """
        Returns whether to auto-scale the width and depth.
        """
        return self.auto_width, self.auto_depth

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def auto_width(self) -> bool:
        """
        Returns whether to auto-scale the width (the size along the x-axis).
        """
        if round(self.new_width, 4) == 0.0:  # xxx Use rounding in target units.
            if self._auto is not None:
                if isinstance(self._auto, tuple):
                    return self._auto[0]

                return self._auto

            if self._auto_width is not None:
                return self._auto_width

        return False

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def auto_depth(self) -> bool:
        """
        Returns whether to auto-scale the depth (the size along the y-axis).
        """
        if round(self.new_depth, 4) == 0.0:  # xxx Use rounding in target units.
            if self._auto is not None:
                if isinstance(self._auto, tuple):
                    return self._auto[1]

                return self._auto

            if self._auto_depth is not None:
                return self._auto_depth

        return False

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def convexity(self) -> int | None:
        """
        Returns the convexity.
        """
        return self._convexity

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return PrivateResize(new_size=self.new_size, auto=self.auto, convexity=self.convexity, child=self.child)

# ----------------------------------------------------------------------------------------------------------------------
