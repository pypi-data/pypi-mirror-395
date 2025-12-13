from abc import ABC
from typing import List

from super_scad.scad.ScadWidget import ScadWidget


class ScadMultiChildParent(ScadWidget, ABC):
    """
    Abstract widget for creating SuperSCAD widgets that have multiple children.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, children: List[ScadWidget]):
        """
        Object constructor.

        :param children: The child SuperSCAD widgets of this multi-child parent.
        """
        ScadWidget.__init__(self)

        self.__children: List[ScadWidget] = children
        """
        The child OpenSCAD widgets of this multi-child parent.
        """

        for key, child in enumerate(self.children):
            assert isinstance(child, ScadWidget), f"Child {key} is of type: {child.__class__}"

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def children(self) -> List[ScadWidget]:
        """
        Returns the children of this multi-child parent.
        """
        return self.__children

# ----------------------------------------------------------------------------------------------------------------------
