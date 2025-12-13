from super_scad.private.PrivateSingleChildOpenScadCommand import PrivateSingleChildOpenScadCommand
from super_scad.scad.Context import Context
from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.scad.ScadWidget import ScadWidget


class Modify(ScadSingleChildParent):
    """
    Class for applying modifier characters. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Modifier_Characters#Disable_Modifier
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 disable: bool = False,
                 show_only: bool = False,
                 highlight: bool = False,
                 transparent: bool = False,
                 child: ScadWidget):
        """
        Object constructor.

        :param disable: Whether the child widget is ignored.
        :param show_only: Whether to ignore the rest of the design and use this child widget as design root.
        :param highlight: Whether the child widget is used as usual in the rendering process but also draw it
                          unmodified in transparent pink.
        :param transparent: Whether this child widget is used as usual in the rendering process but draw it in
                            transparent gray (all transformations are still applied to the nodes in this tree).
        :param child: The child widget.
        """
        ScadSingleChildParent.__init__(self, child=child)

        self._disable: bool = disable
        """
        Whether the child widget is ignored.
        """

        self._show_only: bool = show_only
        """
        Whether to ignore the rest of the design and use this child widget as design root.
        """

        self._highlight: bool = highlight
        """
        Whether the child widget is used as usual in the rendering process but also draw it unmodified in transparent
        pink.
        """

        self._transparent: bool = transparent
        """
        Whether this child widget is used as usual in the rendering process but draw it in transparent gray (all 
        transformations are still applied to the nodes in this tree).
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def disable(self) -> bool:
        """
        Returns whether this SuperSCAD widget is ignored.
        """
        return self._disable

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def show_only(self) -> bool:
        """
        Returns whether to ignore the rest of the design and use this SuperSCAD widget as design root.
        """
        return self._show_only

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def highlight(self) -> bool:
        """
        Returns whether this SuperSCAD widget is used as usual in the rendering process but also draw it unmodified in
        transparent pink.
        """
        return self._highlight

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def transparent(self) -> bool:
        """
        Returns whether this SuperSCAD widget is used as usual in the rendering process but draw it in transparent gray
        (all transformations are still applied to the nodes in this tree).
        """
        return self._transparent

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        modifiers = ('*' if self.disable else '') + \
                    ('!' if self.show_only else '') + \
                    ('#' if self.highlight else '') + \
                    ('%' if self.transparent else '')

        if modifiers == '':
            return self.child

        return PrivateSingleChildOpenScadCommand(command=modifiers + 'union', args={}, child=self.child)

# ----------------------------------------------------------------------------------------------------------------------
