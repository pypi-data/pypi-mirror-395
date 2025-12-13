import re
from typing import Any, List, Tuple

from super_scad.scad import Length
from super_scad.scad.Context import Context
from super_scad.scad.Unit import Unit
from super_scad.type import Vector2, Vector3
from super_scad.type.Color import Color


class Formatter:
    """
    A utility class for formatting and rounding arguments of OpenSCAD commands and variables.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def format(context: Context,
               argument: Any,
               is_angle: bool = False,
               is_length: bool = False,
               is_scale: bool = False,
               unit: Unit | None = None) -> str:
        """
        Returns an argument of the OpenSCAD command.

        :param context: The build context.
        :param argument: The argument of OpenSCAD command.
        :param is_scale: Whether the argument or variable is a scale.
        :param is_length: Whether the argument or variable is a length.
        :param is_angle: Whether the argument or variable is an angle.
        :param unit: The unit of length. Mandatory when the argument or variable is a length.
        """
        if is_length and (isinstance(argument, float) or isinstance(argument, int)):
            argument = Length.convert(float(argument), unit, context.get_unit_length_final())
            argument = str(round(argument, context.length_digits))
            if argument == '-0.0':
                argument = '0.0'
            return argument

        if is_angle and (isinstance(argument, float) or isinstance(argument, int)):
            argument = str(round(float(argument), context.angle_digits))
            if argument == '-0.0':
                argument = '0.0'
            return argument

        if is_scale and (isinstance(argument, float) or isinstance(argument, int)):
            argument = str(round(float(argument), context.scale_digits))
            if argument == '-0.0':
                argument = '0.0'
            return argument

        if isinstance(argument, Vector2):
            return "[{}, {}]".format(Formatter.format(context, argument.x, is_angle, is_length, is_scale, unit),
                                     Formatter.format(context, argument.y, is_angle, is_length, is_scale, unit))

        if isinstance(argument, Vector3):
            return "[{}, {}, {}]".format(
                    Formatter.format(context, argument.x, is_angle, is_length, is_scale, unit),
                    Formatter.format(context, argument.y, is_angle, is_length, is_scale, unit),
                    Formatter.format(context, argument.z, is_angle, is_length, is_scale, unit))

        if isinstance(argument, bool):
            return str(argument).lower()

        if isinstance(argument, str):
            return '"{}"'.format(re.sub(r'([\\\"])', r'\\\1', argument))

        if isinstance(argument, int):
            return str(argument)

        if isinstance(argument, float):
            return str(argument)

        if isinstance(argument, List) or isinstance(argument, Tuple):
            parts = [Formatter.format(context, element, is_angle, is_length, is_scale, unit) for element in argument]

            return '[{}]'.format(', '.join(parts))

        if isinstance(argument, Color):
            return str(argument)

        raise ValueError(f'Can not format argument or variable of type {argument.__class__}.')

# ----------------------------------------------------------------------------------------------------------------------
