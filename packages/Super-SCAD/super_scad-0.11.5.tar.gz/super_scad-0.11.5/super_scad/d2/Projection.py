from super_scad.d2.private.PrivateProjection import PrivateProjection
from super_scad.scad.Context import Context
from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Translate3D import Translate3D


class Projection(ScadSingleChildParent):
    """
    Creates 2D drawings from 3D models. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#3D_to_2D_Projection.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 cut: bool = False,
                 z: float = 0.0,
                 child: ScadWidget):
        """
        Object constructor.

        :param cut: Whether to cut the 3D model.
        :param z: The height where the 3D model will be cut. Defaults to 0.0.
        :param child: The widget with the 3D model.
        """
        ScadSingleChildParent.__init__(self, child=child)

        self._cut: bool = cut
        """
        Whether to cut the 3D model.
        """

        self._z: float | None = z
        """
        The height where the 3D model will be cut. Defaults to 0.0.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def cut(self) -> bool:
        """
        Returns whether to cut the 3D model.
        """
        return self._cut

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def z(self) -> float | None:
        """
        Returns the height where the 3D model will be cut.
        """
        if not self.cut:
            return None

        return self._z

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        if self.z is None:
            child = self.child
        else:
            child = Translate3D(z=-self.z, child=self.child)

        return PrivateProjection(cut=self.cut, child=child)

# ----------------------------------------------------------------------------------------------------------------------
