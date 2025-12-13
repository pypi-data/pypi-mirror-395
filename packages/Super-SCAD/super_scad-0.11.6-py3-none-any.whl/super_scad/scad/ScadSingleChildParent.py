from abc import ABC

from super_scad.scad.ScadWidget import ScadWidget


class ScadSingleChildParent(ScadWidget, ABC):
    """
    Abstract parent widget for SuperSCAD widgets that have a single-child.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, child: ScadWidget):
        """
        Object constructor.

        :param child: The child SuperSCAD widget of this single-child parent.
        """
        ScadWidget.__init__(self)

        self.__child = child
        """
        The child OpenSCAD widget of this single-child parent.
        """

        assert isinstance(child, ScadWidget), f"Child is of type: {child.__class__}"

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def child(self) -> ScadWidget:
        """
        Returns the child of this single-child parent.
        """
        return self.__child

# ----------------------------------------------------------------------------------------------------------------------
