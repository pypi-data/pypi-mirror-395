from super_scad.scad.Context import Context
from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.private.PrivateRotate import PrivateRotate
from super_scad.type.Angle import Angle


class Rotate2D(ScadSingleChildParent):
    """
    Rotates its child about the z-axis. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#rotate.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 angle: float | None = None,
                 child: ScadWidget) -> None:
        """
        Object constructor.

        :param angle: The angle of rotation (around the z-axis).
        :param child: The widget to be rotated.
        """
        ScadSingleChildParent.__init__(self, child=child)

        self._angle: float | None = angle
        """
        The angle of rotation (around the z-axis).
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle(self) -> float:
        """
        Returns the angle of rotation (around the z-axis).
        """
        if self._angle is None:
            self._angle = 0.0

        return Angle.normalize(self._angle)

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return PrivateRotate(angle=self.angle, child=self.child)

# ----------------------------------------------------------------------------------------------------------------------
