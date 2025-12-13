import math

from super_scad.scad.Context import Context


class Radius2Sides4n:
    """
    A utility class for converting a radius to sides with a multiple of 4 vertices.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def r2sides(context: Context, radius: float) -> int:
        """
        Replicates the OpenSCAD logic to calculate the number of sides from the radius.

        :param context: The build context.
        :param radius: The radius of the circle.
        """
        if context.fn > 0:
            return max(context.fn, 3)

        return int(math.ceil(max(min(360.0 / context.fa, radius * 2.0 * math.pi / context.fs), 5.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def r2sides4n(context: Context, radius: float) -> int:
        """
        Rounds up the number of sides to a multiple of 4 to ensure points land on all axes.

        :param context: The build context.
        :param radius: The radius of the circle.
        """
        return int(math.floor((Radius2Sides4n.r2sides(context, radius) + 3) / 4) * 4)

# ----------------------------------------------------------------------------------------------------------------------
