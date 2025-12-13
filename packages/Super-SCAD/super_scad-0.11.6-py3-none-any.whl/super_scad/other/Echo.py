from typing import Dict

from super_scad.private.PrivateOpenScadCommand import PrivateOpenScadCommand


class Echo(PrivateOpenScadCommand):
    """
    The echo() module prints the contents to the compilation window (aka Console). See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#Echo_module.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, message: str | None = None, **kwargs):
        """
        Object constructor.
        """
        args = {'message': message}
        args.update(kwargs)
        PrivateOpenScadCommand.__init__(self, command='echo', args=args)

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_map(self) -> Dict[str, str | None]:
        """
        Returns the map from SuperSCAD arguments to OpenSCAD arguments.
        """
        return {'message': None}

# ----------------------------------------------------------------------------------------------------------------------
