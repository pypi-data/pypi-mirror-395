import inspect
import os
from pathlib import Path

from super_scad.scad import Length
from super_scad.scad.BOM import BOM
from super_scad.scad.ScadCodeStore import ScadCodeStore
from super_scad.scad.Unit import Unit
from super_scad.type import Vector3


class Context:
    """
    The context for generating OpenSCAD from SuperSCAD.
    """

    # ------------------------------------------------------------------------------------------------------------------
    DEFAULT_FA: float = 12.0
    """
    OpenSCAD default value for $fa.
    """

    DEFAULT_FS: float = 2.0
    """
    OpenSCAD default value for $fs.
    """

    DEFAULT_FN: int = 0
    """
    OpenSCAD default value for $fn.
    """

    DEFAULT_VIEWPORT_ROTATION: Vector3 = Vector3(55.0, 0.0, 25)
    """
    The default viewport rotation.
    """

    DEFAULT_VIEWPORT_TRANSLATION: Vector3 = Vector3.origin
    """
    The default viewport translation.
    """

    DEFAULT_VIEWPORT_DISTANCE: float = 140.0
    """
    The default FOV (Field Of View).
    """

    DEFAULT_VIEWPORT_FIELD_OF_VIEW: float = 22.5
    """
    The default FOV (Field Of View).
    """

    __unit_length_current: Unit = Unit.FREE
    """
    The current unit of length.
    """

    __unit_length_final: Unit = Unit.FREE
    """
    The unit of length used in the generated OpenSCAD code.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 unit_length_final: Unit = Unit.MM,
                 fa: float = DEFAULT_FA,
                 fs: float = DEFAULT_FS,
                 fn: int = DEFAULT_FN,
                 vpr: Vector3 = DEFAULT_VIEWPORT_ROTATION,
                 vpt: Vector3 = DEFAULT_VIEWPORT_TRANSLATION,
                 vpd: float = DEFAULT_VIEWPORT_DISTANCE,
                 vpf: float = DEFAULT_VIEWPORT_FIELD_OF_VIEW,
                 eps: float = 1E-2,
                 delta: float = 1e-5,
                 angle_digits: int = 4,
                 length_digits: int = 4,
                 scale_digits: int = 4):
        """
        Object constructor.

        :param unit_length_final: The unit of length used in the generated OpenSCAD code.
        :param fa: The minimum angle (in degrees) of each fragment. Known in OpenSCAD as $fa,
                   see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$fa.
        :param fs: The minimum circumferential length of each fragment. Known in OpenSCAD as $fs,
                   see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$fs.
        :param fn: The number of fragments in 360 degrees. Values of 3 or more override $fa and $fs. Known in OpenSCAD
                   as $fn, see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$fn.
        :param vpr: The viewport rotation,
                    see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$vpr.
        :param vpt: The viewport translation,
                    see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$vpt.
        :param vpf: The FOV (Field of View) of the view,
                    see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$vpf.
        :param vpd: The camera distance,
                    see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$vpd.
        :param eps: Epsilon value for clear overlap.
        :param delta: The minimum distance between nodes, vertices and line segments for reliable computation of the
                      separation between line segments and nodes.
        :param angle_digits: The number of decimal places of an angle in the generated OpenSCAD code.
        :param length_digits: The number of decimal places of a length in the generated OpenSCAD code.
        :param scale_digits:  The number of decimal places of a scale or factor in the generated OpenSCAD code.
        """
        self.__project_home: Path = Path(os.getcwd()).resolve()
        """
        The home folder of the current project. 
        """

        self.__target_path: Path | None = None
        """
        The path to the OpenSCAD script that currently been generated.
        """

        self.__code_store: ScadCodeStore = ScadCodeStore()
        """
        The place were we store the generated OpenSCAD code.
        """

        self.__fa: float = fa
        """
        The minimum angle (in degrees) of each fragment. 
        Known in OpenSCAD as $fa, see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$fa.
        """

        self.__fs: float = fs
        """
        The minimum circumferential length of each fragment.
        Known in OpenSCAD as $fs, see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$fs.
        """

        self.__fn: int = fn
        """
        The number of fragments in 360 degrees. Values of 3 or more override $fa and $fs.
        Known in OpenSCAD as $fn, see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$fn.
        """

        self.__vpt: Vector3 = vpt
        """
        The viewport rotation.
        """

        self.__vpr: Vector3 = vpr
        """
        The viewport translation.
        """

        self.__vpd: float = vpd
        """
        The camera distance.
        """

        self.__vpf: float = vpf
        """
        The FOV (Field of View) of the view.
        """

        self.__eps: float = eps
        """
        Epsilon value for clear overlap.
        """

        self.__delta: float = delta
        """
        The minimum distance between nodes, vertices and line segments for reliable computation of the separation 
        between line segments and nodes.
        """

        self.__unit_length_final: Unit = unit_length_final
        """
        The unit of length.
        """

        self.__angle_digits = angle_digits
        """
        The number of decimal places of an angle in the generated OpenSCAD code.
        """

        self.__length_digits = length_digits
        """
        The number of decimal places of a length in the generated OpenSCAD code.
        """

        self.__scale_digits = scale_digits
        """
        The number of decimal places of a scale or factor in the generated OpenSCAD code.
        """

        self.__bom: BOM = BOM()
        """
        The Bill of materials.
        """

        Context.set_unit_length_current(unit_length_final)
        Context.__set_unit_length_final(unit_length_final)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def project_home(self) -> Path:
        """
        Returns the current project's home directory.
        """
        return self.__project_home

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def target_path(self) -> Path | None:
        """
        Returns the path to the OpenSCAD script that currently been generated.
        """
        return self.__target_path

    # ------------------------------------------------------------------------------------------------------------------
    @target_path.setter
    def target_path(self, target_path: str) -> None:
        """
        Set the path to the OpenSCAD script that currently been generated.
        """
        self.__target_path = Path(os.path.realpath(target_path))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle_digits(self) -> int:
        """
        Returns the number of decimal places of an angle in the generated OpenSCAD code.
        """
        return self.__angle_digits

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def length_digits(self) -> int:
        """
        Returns the number of decimal places of a length in the generated OpenSCAD code.
        """
        return self.__length_digits

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def scale_digits(self) -> int:
        """
        Returns the number of decimal places of a scale or factor in the generated OpenSCAD code.
        """
        return self.__scale_digits

    # ------------------------------------------------------------------------------------------------------------------
    def resolve_path(self, path: Path | str) -> Path:
        """
        Resolve a path relative from the caller script to a path relative to the project home.

        :param Path path: The path to resolve.
        """
        caller = Path(inspect.stack()[1].filename)
        absolute_path = Path(caller.parent.joinpath(path).resolve())

        if os.path.commonprefix([absolute_path, self.__project_home]) == str(self.__project_home):
            # works with python >=3.12 return absolute_path.relative_to(self.target_path.parent, walk_up=True)
            return Path(os.path.relpath(absolute_path, self.target_path.parent))

        return absolute_path

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def code_store(self) -> ScadCodeStore:
        """
        Returns code store.
        """
        return self.__code_store

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def eps(self) -> float:
        """
        Returns the epsilon value for clear overlap.
        """
        return Length.convert(self.__eps, self.__unit_length_final, self.__unit_length_current)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def delta(self) -> float:
        """
        Returns the minimum distance between nodes, vertices and line segments for reliable computation of the
        separation between line segments and nodes.
        """
        return Length.convert(self.__delta, self.__unit_length_final, self.__unit_length_current)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def resolution(self) -> float:
        """
        Returns the resolution of lengths in generated OpenSCAD code.
        """
        return 10.0 ** -self.__length_digits

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fa(self) -> float:
        """
        Returns the minimum angle (in degrees) of each fragment.
        Known in OpenSCAD as $fa, see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$fa.
        """
        return self.__fa

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fs(self) -> float:
        """
        Returns the minimum circumferential length of each fragment.
        Known in OpenSCAD as $fs, see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$fs.
        """
        return Length.convert(self.__fs, self.__unit_length_final, self.__unit_length_current)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn(self) -> int:
        """
        Returns the number of fragments in 360 degrees. Values of three or more override $fa and $fs.
        Known in OpenSCAD as $fn, see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$fn.
        """
        return self.__fn

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def vpr(self) -> Vector3:
        """
        Returns the viewport rotation,
        see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$vpr.
        """
        return Vector3(Length.convert(self.__vpr.x, self.__unit_length_final, self.__unit_length_current),
                       Length.convert(self.__vpr.y, self.__unit_length_final, self.__unit_length_current),
                       Length.convert(self.__vpr.z, self.__unit_length_final, self.__unit_length_current))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def vpt(self) -> Vector3:
        """
        Returns the viewport translation,
        see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$vpt.
        """
        return Vector3(Length.convert(self.__vpt.x, self.__unit_length_final, self.__unit_length_current),
                       Length.convert(self.__vpt.y, self.__unit_length_final, self.__unit_length_current),
                       Length.convert(self.__vpt.z, self.__unit_length_final, self.__unit_length_current))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def vpf(self) -> float:
        """
        Returns the FOV (Field of View) of the view,
        see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$vpf.
        """
        return self.__vpf

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def vpd(self) -> float:
        """
        Returns the camera distance,
        see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$vpd.
        """
        return Length.convert(self.__vpd, self.__unit_length_final, self.__unit_length_current)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bom(self) -> BOM:
        """
        Returns the BOM (Bill of Materials).
        """
        return self.__bom

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __set_unit_length_final(__unit_length_final: Unit) -> None:
        """
        Sets the unit of length used in the generated OpenSCAD code.
        """
        Context.__unit_length_final = __unit_length_final

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_unit_length_final() -> Unit:
        """
        Returns the unit of length used in the generated OpenSCAD code.
        """
        return Context.__unit_length_final

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def set_unit_length_current(unit_length_current: Unit) -> None:
        """
        Sets the current unit of length.

        :param unit_length_current: The new current unit of length.
        """
        Context.__unit_length_current = unit_length_current

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_unit_length_current() -> Unit:
        """
        Returns the current unit of length.
        """
        return Context.__unit_length_current

# ----------------------------------------------------------------------------------------------------------------------
