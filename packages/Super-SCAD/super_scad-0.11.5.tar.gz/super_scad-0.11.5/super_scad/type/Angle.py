import math


class Angle:
    """
    Utility class for angles.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def normalize(angle: float, norm: float = 360.0) -> float:
        """
        Returns the normalized angle of an angle. A normalized angle is between 0.0 and the norm (360.0 degrees by
        default).

        :param angle: The angle to be normalized.
        :param norm: The norm value.
        """
        angle = math.fmod(angle, norm)
        if angle < 0.0:
            angle = math.fmod(angle + norm, norm)

        return angle

# ----------------------------------------------------------------------------------------------------------------------
