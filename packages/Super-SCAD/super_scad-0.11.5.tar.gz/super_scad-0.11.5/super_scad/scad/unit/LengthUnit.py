class LengthUnit:
    """
    Interface for units of length.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def id(self) -> int:
        """
        Returns the ID or enumeration value of this unit of length.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def meters(self) -> float:
        """
        Returns the length of one unit expressed in meters.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def symbol(self) -> str:
        """
        Returns the symbol for a unit of length.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
