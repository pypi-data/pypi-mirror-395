import typing
from abc import ABC, abstractmethod

from super_scad.scad.Context import Context
from super_scad.scad.Unit import Unit

ScadWidget = typing.NewType('ScadWidget', None)


class ScadWidget(ABC):
    """
    Abstract parent widget for all SuperSCAD widgets.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """

        self.__unit: Unit = Context.get_unit_length_current()
        """
        The unit of length of the Context of this OpenSCAD widget.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def unit(self) -> Unit:
        """
        Returns unit of length of the Context of this OpenSCAD widget.
        """
        return self.__unit

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
