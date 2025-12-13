from typing import List

from super_scad.scad.Unit import Unit
from super_scad.scad.unit.AngstromUnit import AngstromUnit
from super_scad.scad.unit.AstronomicalUnit import AstronomicalUnit
from super_scad.scad.unit.AttoparsecUnit import AttoparsecUnit
from super_scad.scad.unit.CentimeterUnit import CentimeterUnit
from super_scad.scad.unit.DecimeterUnit import DecimeterUnit
from super_scad.scad.unit.FootUnit import FootUnit
from super_scad.scad.unit.InchUnit import InchUnit
from super_scad.scad.unit.KilometerUnit import KilometerUnit
from super_scad.scad.unit.LengthUnit import LengthUnit
from super_scad.scad.unit.LightYearUnit import LightYearUnit
from super_scad.scad.unit.LiUnit import LiUnit
from super_scad.scad.unit.MeterUnit import MeterUnit
from super_scad.scad.unit.MicrometerUnit import MicrometerUnit
from super_scad.scad.unit.MileUnit import MileUnit
from super_scad.scad.unit.MillimeterUnit import MillimeterUnit
from super_scad.scad.unit.ParsecUnit import ParsecUnit
from super_scad.scad.unit.RoyalCubitUnit import RoyalCubitUnit
from super_scad.scad.unit.ThouUnit import ThouUnit
from super_scad.scad.unit.YardUnit import YardUnit


class Length:
    """
    Utility class for converting lengths between different units of length.
    """
    # ------------------------------------------------------------------------------------------------------------------
    __ratio: List[List[float] | None] = []
    """
    The ratios of all unit of lengths.
    """

    __units: List = [AngstromUnit,
                     AstronomicalUnit,
                     AttoparsecUnit,
                     CentimeterUnit,
                     DecimeterUnit,
                     FootUnit,
                     InchUnit,
                     KilometerUnit,
                     LightYearUnit,
                     LiUnit,
                     MeterUnit,
                     MicrometerUnit,
                     MileUnit,
                     MillimeterUnit,
                     ParsecUnit,
                     RoyalCubitUnit,
                     ThouUnit,
                     YardUnit]
    """
    All unit of unit of lengths known to SuperSCAD.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def init_ratios() -> None:
        """
        Initializes the ratios of lengths.
        """
        max_value = max(unit.value for unit in Unit)
        for i in range(max_value + 1):
            for j in range(max_value + 1):
                if j == 0:
                    Length.__ratio.append([])
                Length.__ratio[i].append(None)

        for unit_from_class in Length.__units:
            unit_from = unit_from_class()
            id_from = unit_from.id()
            for unit_to_class in Length.__units:
                unit_to = unit_to_class()
                id_to = unit_to.id()
                Length.__ratio[id_from][id_to] = unit_from.meters() / unit_to.meters()

        # One special case. A length that is free of any scale can be converted to a length that is free of any scale
        # only.
        Length.__ratio[Unit.FREE.value][Unit.FREE.value] = 1.0

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def convert(length: float, from_unit: Unit, to_unit: Unit) -> float:
        """
        Converts a length from one unit to another.

        @param length: The length to convert.
        @param from_unit: The unit to convert from.
        @param to_unit: The unit to convert to.
        """
        try:
            return length * Length.__ratio[from_unit.value][to_unit.value]
        except Exception:
            raise ValueError(f'Cannot convert length {length} from {from_unit.name} to {to_unit.name}.')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def length_unit(unit: Unit) -> LengthUnit:
        """
        Returns the length unit object of a unit of length.

        :param unit: The unit of length.
        """
        if unit == Unit.UM:
            return MicrometerUnit()

        if unit == Unit.MM:
            return MillimeterUnit()

        if unit == Unit.CM:
            return CentimeterUnit()

        if unit == Unit.DM:
            return DecimeterUnit()

        if unit == Unit.M:
            return MeterUnit()

        if unit == Unit.KM:
            return KilometerUnit()

        if unit == Unit.THOU:
            return ThouUnit()

        if unit == Unit.INCH:
            return InchUnit()

        if unit == Unit.FOOT:
            return FootUnit()

        if unit == Unit.YARD:
            return YardUnit()

        if unit == Unit.MILE:
            return MileUnit()

        if unit == Unit.LI:
            return LiUnit()

        if unit == Unit.ROYAL_CUBIT:
            return RoyalCubitUnit()

        if unit == Unit.ANGSTROM:
            return AngstromUnit()

        if unit == Unit.ASTRONOMICAL_UNIT:
            return AstronomicalUnit()

        if unit == Unit.LIGHT_YEAR:
            return LightYearUnit()

        if unit == Unit.PARSEC:
            return ParsecUnit()

        if unit == Unit.ATTOPARSEC:
            return AttoparsecUnit()

        raise ValueError(f'Unsupported unit {unit}.')

# ----------------------------------------------------------------------------------------------------------------------
