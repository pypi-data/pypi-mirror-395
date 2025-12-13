from pathlib import Path
from typing import Any, Dict

from super_scad.private.PrivateOpenScadCommand import PrivateOpenScadCommand
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget


class Import(PrivateOpenScadCommand):
    """
    Widget for importing a file for use in the current OpenSCAD model. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Importing_Geometry#import.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 path: Path | str,
                 convexity: int | None = None,
                 layer: str | None = None):
        """
        Object constructor.

        :param path: The absolute path or the relative path from the target script to the file that will be imported.
        :param convexity: Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line 
                          through the child widget.
        :param layer: For DXF import only, specify a specific layer to import.
        """
        if isinstance(path, Path):
            path = str(path)

        PrivateOpenScadCommand.__init__(self, command='import', args=locals())

        self.__validate_arguments(locals())

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __validate_arguments(args: Dict[str, Any]) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.

        :param args: The arguments supplied to the constructor.
        """
        validator = ArgumentValidator(args)
        validator.validate_required({'path'})

        # We like to validate here whether the path goes to an exiting readable file, but we need the build context for
        # that. So, we test the existence of the file in the build method.

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_map(self) -> Dict[str, str]:
        """
        Returns the map from SuperSCAD arguments to OpenSCAD arguments.
        """
        return {'path': 'file'}

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def convexity(self) -> int | None:
        """
        Returns the number of "inward" curves, i.e., expected number of path crossings of an arbitrary line through the
        child widget.
        """
        return self._args.get('convexity')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def layer(self) -> str | None:
        """
        For DXF import only, returns the specific layer to import.
        """
        return self._args.get('layer')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def path(self) -> Path:
        """
        Returns the absolute path or the relative path from the target script to the file that will be imported.
        """
        return Path(self._args['path'])

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        path = self.path
        if not path.is_absolute():
            path = context.target_path.parent.joinpath(path)

        if not path.is_file():
            raise FileNotFoundError(f'File {path} does not exist.')

        return self

# ----------------------------------------------------------------------------------------------------------------------
