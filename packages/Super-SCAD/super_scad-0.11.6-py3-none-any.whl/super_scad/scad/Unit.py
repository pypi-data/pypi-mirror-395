from enum import auto, Enum, STRICT


class Unit(Enum, boundary=STRICT):
    """
    Enumeration of all known units of lengths in SuperSCAD.
    """

    # ------------------------------------------------------------------------------------------------------------------
    FREE = auto()
    """
    Free of any scale.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Metric units.

    UM = auto()
    """
    Micrometers.
    """

    MM = auto()
    """
    Millimeters.
    """

    CM = auto()
    """
    Centimeters.
    """

    DM = auto()
    """
    Decimeters.
    """

    M = auto()
    """
    Meters.
    """

    KM = auto()
    """
    Kilometers.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Imperial units.

    THOU = auto()
    """
    Thous. One thou is one thousand of an inch. See https://en.wikipedia.org/wiki/Thousandth_of_an_inch.
    """

    INCH = auto()
    """
    Inches. One inch is defined as 25.4mm. See https://en.wikipedia.org/wiki/Inch.
    """

    FOOT = auto()
    """
    Feet. One foot is 12 inch. See https://en.wikipedia.org/wiki/Foot_(unit).
    """

    YARD = auto()
    """
    Yards. One yard is 3 feet. See https://en.wikipedia.org/wiki/Yard.
    """

    MILE = auto()
    """
    Miles. One mile is 5280 feet. See https://en.wikipedia.org/wiki/Mile.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Chinese units.

    LI = auto()
    """
    Li, a.k.a. Chinese mile. One li is 500 meters. See https://en.wikipedia.org/wiki/Li_(unit).
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Ancient Egyptian units.

    ROYAL_CUBIT = auto()
    """
    Royal cubit. See https://en.wikipedia.org/wiki/Cubit#Ancient_Egyptian_royal_cubit.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Pysics units.

    ANGSTROM = auto()
    """
    Angstroms. One ångström is 10e−10m. See https://en.wikipedia.org/wiki/Angstrom.
    """

    ASTRONOMICAL_UNIT = auto()
    """
    Astronomical units. One Astronomical unit 149 597 870 700 m. See https://en.wikipedia.org/wiki/Astronomical_unit.
    """

    LIGHT_YEAR = auto()
    """
    Light-years. The distance that light travels in a vacuum in one Julian year. See
    https://en.wikipedia.org/wiki/Light-year.
    """

    PARSEC = auto()
    """
    Parsecs. One parsec is 30 856 775 814 913 673 m. See https://en.wikipedia.org/wiki/Parsec.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Humorous units.

    ATTOPARSEC = auto()
    """
    Attoparsecs. One attoparsec 1e-18 parsec. See 
    https://en.wikipedia.org/wiki/List_of_humorous_units_of_measurement#Attoparsec.
    """

# ----------------------------------------------------------------------------------------------------------------------
