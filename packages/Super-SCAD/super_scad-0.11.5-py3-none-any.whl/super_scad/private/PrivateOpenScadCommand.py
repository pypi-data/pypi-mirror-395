from typing import Any, Dict, Set

from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.util.Formatter import Formatter


class PrivateOpenScadCommand(ScadWidget):
    """
    Widget for creating OpenSCAD commands.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, command: str, args: Dict[str, Any]):
        """
        Object constructor.

        :param command: The name of the OpenSCAD command.
        :param args: The arguments of the OpenSCAD command.
        """
        ScadWidget.__init__(self)

        self._command: str = command
        """
        The name of the OpenSCAD command.
        """

        self._args: Dict[str, Any] = {}
        """
        The arguments of this OpenSCAD widget.
        """

        if args is not None:
            for key, value in args.items():
                if value is not None and value != self and key not in ('child', 'children'):
                    self._args[key] = value

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return self

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def command(self) -> str:
        """
        Returns the name of the OpenSCAD command.
        """
        return self._command

    # ------------------------------------------------------------------------------------------------------------------
    def generate_args(self, context: Context) -> str:
        """
        Returns the arguments of the OpenSCAD command.
        """
        argument_map = self._argument_map()
        argument_angles = self._argument_angles()
        argument_lengths = self._argument_lengths()
        argument_scales = self._argument_scales()

        args_as_str = '('
        first = True
        for key, value in self._args.items():
            if not first:
                args_as_str += ', '
            else:
                first = False

            real_name = argument_map.get(key, key)
            if real_name in argument_angles:
                real_value = Formatter.format(context, value, is_angle=True)
            elif real_name in argument_lengths:
                real_value = Formatter.format(context, value, is_length=True, unit=self.unit)
            elif real_name in argument_scales:
                real_value = Formatter.format(context, value, is_scale=True)
            else:
                real_value = Formatter.format(context, value)

            if real_name is None:
                args_as_str += '{}'.format(real_value)
            else:
                args_as_str += '{} = {}'.format(real_name, real_value)
        args_as_str += ')'

        return args_as_str

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_map(self) -> Dict[str, str | None]:
        """
        Returns the map from SuperSCAD arguments to OpenSCAD arguments.
        """
        return {}

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_angles(self) -> Set[str]:
        """
        Returns the set with arguments that are angles.
        """
        return set()

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_lengths(self) -> Set[str]:
        """
        Returns the set with arguments that are lengths.
        """
        return set()

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_scales(self) -> Set[str]:
        """
        Returns the set with arguments that are scales and factors.
        """
        return set()

# ----------------------------------------------------------------------------------------------------------------------
