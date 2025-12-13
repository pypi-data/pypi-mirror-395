from typing import Dict, Set

from super_scad.private.PrivateSingleChildOpenScadCommand import PrivateSingleChildOpenScadCommand
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type.Vector2 import Vector2


class PrivateLinearExtrude(PrivateSingleChildOpenScadCommand):
    """
    Linear Extrusion is an operation that takes a 2D object as input and generates a 3D object as a result. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#linear_extrude.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 height: float,
                 center: bool = False,
                 convexity: int | None = None,
                 twist: float = 0.0,
                 scale: float | Vector2 = 1.0,
                 slices: int | None = None,
                 segments: int | None = None,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 child: ScadWidget):
        """
        Object constructor.

        :param height: The height of the extruded object.
        :param center: Whether the cylinder is centered along the z-as.
        :param convexity: Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line 
                          through the child widget.
        :param twist: The number of degrees through which the shape is extruded. Setting the parameter twist = 360
                      extrudes through one revolution. The twist direction follows the left-hand rule.
        :param scale: Scales the 2D shape by this value over the height of the extrusion.
        :param slices: Defines the number of intermediate points along the Z axis of the extrusion. Its default
                       increases with the value of twist. Explicitly setting slices may improve the output refinement.
        :param segments: Adds vertices (points) to the extruded polygon resulting in smoother twisted geometries.
                         Segments need to be a multiple of the polygon's fragments to have an effect (6 or 9... for a
                         circle($fn=3), 8,12... for a square()).
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        """
        PrivateSingleChildOpenScadCommand.__init__(self, command='linear_extrude', args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_map(self) -> Dict[str, str]:
        """
        Returns the map from SuperSCAD arguments to OpenSCAD arguments.
        """
        return {'fa': '$fa', 'fs': '$fs', 'fn': '$fn'}

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_angles(self) -> Set[str]:
        """
        Returns the set with arguments that are angles.
        """
        return {'$fa', 'twist'}

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_lengths(self) -> Set[str]:
        """
        Returns the set with arguments that are lengths.
        """
        return {'height', '$fs'}

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_scales(self) -> Set[str]:
        """
        Returns the set with arguments that are scales and factors.
        """
        return {'scale'}

# ----------------------------------------------------------------------------------------------------------------------
