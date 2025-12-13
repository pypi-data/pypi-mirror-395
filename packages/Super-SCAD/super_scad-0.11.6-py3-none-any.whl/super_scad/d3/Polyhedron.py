from typing import Dict, Iterable, List, Tuple

from super_scad.boolean.Union import Union
from super_scad.d3.Cylinder import Cylinder
from super_scad.d3.private.PrivatePolyhedron import PrivatePolyhedron
from super_scad.d3.Sphere import Sphere
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Paint import Paint
from super_scad.transformation.Translate3D import Translate3D
from super_scad.type.Color import Color
from super_scad.type.Vector3 import Vector3


# ----------------------------------------------------------------------------------------------------------------------

class Node:
    """
    A node of a polyhedron.
    """

    next_node_id: int = 0
    """
    The next node ID.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, point: Vector3):
        """
        Object constructor.

        :param point: The rounded position of the node.
        """

        self.point: Vector3 = point
        """
        The rounded position of this node.
        """

        self.node_id: int = Node.next_node_id
        """
        The ID of this node as implicitly implied by the invoker.
        """

        Node.next_node_id += 1


# ----------------------------------------------------------------------------------------------------------------------
class Polyhedron(ScadWidget):
    """
    Widget for creating polyhedrons. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Primitive_Solids#polyhedron.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 faces: List[List[Vector3] | Tuple[Vector3, ...]],
                 highlight_faces: int | List[int] | None = None,
                 highlight_nodes: int | List[int] = None,
                 highlight_diameter: float | None = None,
                 convexity: int | None = None,
                 validate: bool = False,
                 highlight_issues: bool = False):
        """
        Object constructor.

        :param faces: The faces that collectively enclose the solid.
        :param highlight_faces: The ID of the faces to highlight. Each node of the face is marked, the first point
                                is colored red, the second orange, the third green, and all other points are color
                                black.
        :param highlight_nodes: The IDs of the nodes to highlight.
        :param highlight_diameter: The diameter of the spheres that highlight the nodes of the faces.
        :param convexity: Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line
                          the polyhedron.
        :param validate: Whether to validate polyhedron.
        :param highlight_issues: Whether to highlight all issues found by the validation. This will override
                                 highlight_faces and highlight_nodes.

        Each face consists of three or more nodes. Faces may be defined in any order, but the nodes of each face must be
        ordered correctly, must be ordered in clockwise direction when looking at each face from the outside inwards.
        Define enough faces to fully enclose the solid, with no overlap. If nodes that describe a single face are not
        on the same plane, the face is by OpenSCAD automatically split into triangles as needed.
        """
        ScadWidget.__init__(self)

        self._faces: List[List[Vector3] | Tuple[Vector3, ...]] = faces
        """
        The faces that collectively enclose the solid.
        """

        self._highlight_faces: int | List[int] | None = highlight_faces
        """
        The ID of the faces to highlight. Each node of the face is marked, the first point
        """

        self._highlight_nodes: int | List[int] = highlight_nodes
        """
        The IDs of the nodes to highlight.
        """

        self._highlight_diameter: float | None = highlight_diameter
        """
        The diameter of the spheres that highlight the nodes of the faces.
        """

        self._convexity: int | None = convexity
        """
        Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line the polyhedron.
        """

        self._validate: bool = validate
        """
        Whether to validate the polyhedron.
        """

        self._highlight_issues: bool = highlight_issues

        self.__nodes: Dict[int, Node] = {}
        """
        Look up table from the memory address of a position of a node to the node.
        """

        self.__faces: List[List[Node]] = []
        """
        The faces of the polyhedron.
        """

        self.__is_ready: bool = False
        """
        Whether the real faces and the real nodes have been computed. 
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def highlight_faces(self) -> List[int]:
        """
        Returns the IDs of the faces to highlight
        """
        if not isinstance(self._highlight_faces, list):
            if self._highlight_faces is None:
                self._highlight_faces = []

            elif isinstance(self._highlight_faces, int):
                self._highlight_faces = [self._highlight_faces]

        return self._highlight_faces

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def highlight_nodes(self) -> List[int]:
        """
        Returns the IDs of the nodes to highlight
        """
        if not isinstance(self._highlight_nodes, list):
            if self._highlight_nodes is None:
                self._highlight_nodes = []
            elif isinstance(self._highlight_nodes, int):
                self._highlight_nodes = [self._highlight_nodes]

        return self._highlight_nodes

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def highlight_diameter(self) -> float | None:
        """
        Returns the diameter of the spheres that highlight the nodes.
        """
        return self._highlight_diameter

    # ------------------------------------------------------------------------------------------------------------------
    def __real_highlight_diameter(self, context: Context) -> float:
        """
        Returns the real diameter of the spheres that highlight the nodes.
        """
        diameter = self.highlight_diameter
        if diameter is not None:
            return max(diameter, 5.0 * context.resolution)

        face = self._faces[self.highlight_faces[0]]

        total_distance = 0.0
        prev_point = None
        for point in face:
            if prev_point is not None:
                total_distance += (point - prev_point).length
            prev_point = point

        if prev_point is not None:
            total_distance += (face[0] - prev_point).length

        average_distance = total_distance / (len(face) + 1)
        diameter = 0.1 * average_distance

        return round(max(diameter, 5.0 * context.resolution), context.length_digits)

    # ------------------------------------------------------------------------------------------------------------------
    def nodes(self, context: Context) -> List[Vector3]:
        """
        Returns the nodes of the polyhedron.
        """
        self.__prepare_data(context)

        return [node.point for node in self.__nodes.values()]

    # ------------------------------------------------------------------------------------------------------------------
    def faces(self, context: Context) -> List[List[int]]:
        """
        Returns the real faces of the polyhedron.
        """
        self.__prepare_data(context)

        return [[node.node_id for node in face] for face in self.__faces]

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def convexity(self) -> int | None:
        """
        Returns the number of "inward" curves, i.e., expected number of path crossings of an arbitrary line through the
        child widget.
        """
        return self._convexity

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def validate(self) -> bool:
        """
        Returns whether to validate polyhedron.
        """
        return self._validate

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def highlight_issues(self) -> bool:
        """
        Returns whether to highlight all issues found by the validation.
        """
        return self._highlight_issues

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __create_face_marker_nodes(points: Iterable[Vector3], is_real_face: bool, diameter: float) -> List[ScadWidget]:
        """
        Creates markers of the nodes of a face.

        :param points: The face, given as an iterable over its nodes given as points.
        :param is_real_face: Whether the face is a real face.
        :param diameter: The diameter of the markers.
        """
        markers = []
        for node_id, node in enumerate(points):
            if is_real_face:
                if node_id == 0:
                    color = Color('red')
                elif node_id == 1:
                    color = Color('orange')
                elif node_id == 2:
                    color = Color('green')
                else:
                    color = Color('black')
            else:
                color = Color('pink')

            marker = Paint(color=color,
                           child=Translate3D(vector=node,
                                             child=Sphere(diameter=diameter, fn=16)))
            markers.append(marker)

        return markers

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __create_face_marker_edges(points: Iterable[Vector3],
                                   is_real_face: bool,
                                   diameter: float,
                                   context: Context) -> List[ScadWidget]:
        """
        Creates markers of the edges of a face.

        :param points: The face, given as an iterable over its nodes given as points.
        :param is_real_face: Whether the face is a real face.
        :param diameter: The diameter of cylinders on the edges.
        :param context: The build context.
        """
        if is_real_face:
            color = Color('black')
        else:
            color = Color('pink')

        edges = []
        prev_point = None
        first_point = None
        for point in points:
            if prev_point is None:
                first_point = point
            else:
                if (point - prev_point).length >= context.resolution:
                    edge = Paint(color=color,
                                 child=Cylinder(start_point=prev_point,
                                                end_point=point,
                                                diameter=diameter,
                                                fn=16))
                    edges.append(edge)

            prev_point = point

        if prev_point is not None and first_point is not None:
            if (first_point - prev_point).length >= context.resolution:
                edge = Paint(color=color,
                             child=Cylinder(start_point=prev_point,
                                            end_point=first_point,
                                            diameter=diameter))
                edges.append(edge)

        return edges

    # ------------------------------------------------------------------------------------------------------------------
    def __create_markers(self, context: Context) -> List[ScadWidget]:
        """
        Create markers to faces and points.

        :param context: The build context.
        """
        markers = self.__create_markers_faces(context)
        markers += self.__create_markers_node(context)

        return markers

    # ------------------------------------------------------------------------------------------------------------------
    def __create_markers_faces(self, context: Context) -> List[ScadWidget]:
        """
        Create markers to highlight a face.

        :param context: The build context.
        """
        diameter_node = self.__real_highlight_diameter(context)
        diameter_edge = 0.2 * diameter_node
        markers = []

        for face_id in self.highlight_faces:
            if 0 <= face_id < len(self.__faces):
                face = self.__faces[face_id]

                points = [node.point for node in face]
                markers += self.__create_face_marker_nodes(points, True, diameter_node)
                markers += self.__create_face_marker_edges(points, True, diameter_edge, context)

                node_ids = ', '.join(str(node.node_id) for node in face)
                print(f'Note: Highlighting face {face_id}: [{node_ids}].')
                for node in face:
                    print(f'      Node {node.node_id}: {node.point}.')
            else:
                print(f'Warning: Face {face_id} not found.')

        return markers

    # ------------------------------------------------------------------------------------------------------------------
    def __create_markers_node(self, context: Context) -> List[ScadWidget]:
        """
        Create markers to highlight a node.

        :param context: The build context.
        """
        diameter_node = self.__real_highlight_diameter(context)
        markers = []

        map_node_id_to_node = {}
        for node in self.__nodes.values():
            map_node_id_to_node[node.node_id] = node

        for node_id in self.highlight_nodes:
            if node_id in map_node_id_to_node:
                point = map_node_id_to_node[node_id].point
                markers.append(Paint(color=Color('blue'),
                                     child=Translate3D(vector=point,
                                                       child=Sphere(diameter=diameter_node, fn=16))))

                print(f'Note: Highlighting node {node_id}: {point}.')
            else:
                print(f'Warning: Node {node_id} not found.')

        return markers

    # ------------------------------------------------------------------------------------------------------------------
    def __prepare_data(self, context):
        """
        Prepares the data as expected by OpenSCAD polyhedron.

        @param context: The build context.
        """
        if not self.__is_ready:
            Node.next_node_id = 0
            digits = context.length_digits

            for points in self._faces:
                face = []
                for point in points:
                    node = self.__nodes.get(id(point))
                    if node is None:
                        point_rounded = Vector3(round(point.x, digits),
                                                round(point.y, digits),
                                                round(point.z, digits))
                        node = Node(point_rounded)
                        self.__nodes[id(point)] = node
                    face.append(node)
                self.__faces.append(face)

            self.__is_ready = True

    # ------------------------------------------------------------------------------------------------------------------
    def __validate_line_segments(self) -> None:
        """
        Validates that all line segments are connected to exactly two faces.
        """
        line_segment_to_faces_map: Dict[Tuple[int, int], List[int]] = {}
        for face_id, face in enumerate(self.__faces):
            length = len(face)
            for index in range(length):
                node_id1 = face[index].node_id
                node_id2 = face[(index + 1) % length].node_id
                line_segment = (min(node_id1, node_id2), max(node_id1, node_id2))
                if line_segment in line_segment_to_faces_map:
                    line_segment_to_faces_map[line_segment].append(face_id)
                else:
                    line_segment_to_faces_map[line_segment] = [face_id]

        for line_segment, original_face_ids in line_segment_to_faces_map.items():
            if len(original_face_ids) != 2:
                face_ids = ', '.join(str(original_face_id) for original_face_id in original_face_ids)

                if len(original_face_ids) > 2:
                    print(f'Warning: Line segment {line_segment} is part of one face only.')
                    print(f'         Add highlight_nodes=[{line_segment}] to locate this line segment.')
                    print(f'         Add highlight_faces=[{face_ids}] to locate the face.')

                elif len(original_face_ids) < 2:
                    numer_of_faces = len(original_face_ids)
                    print(f'Warning: Line segment {line_segment} is part of {numer_of_faces} faces.')
                    print(f'         Add highlight_nodes=[{line_segment}] to locate this line segment.')
                    print(f'         Add highlight_faces=[{face_ids}] to locate the faces.')

                if self.highlight_issues:
                    self._highlight_nodes.append(line_segment[0])
                    self._highlight_nodes.append(line_segment[1])

    # ------------------------------------------------------------------------------------------------------------------
    def __validate_faces1(self) -> None:
        """
        Validates that faces have three or more nodes.
        """
        for face_id, face in enumerate(self.__faces):
            length = len(face)
            if length < 3:
                print(f'Warning: Face has less than three nodes.')
                print(f'         Add highlight_faces=[{face_id}] to locate the face.')

                if self.highlight_issues:
                    self._highlight_faces.append(face_id)

    # ------------------------------------------------------------------------------------------------------------------
    def __validate_faces2(self) -> None:
        """
        Validates that the nodes of all faces are ordered in clockwise direction.
        """
        # For now, press F12.
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def __validate(self) -> None:
        """
        Validates the polyhedron.
        """
        if self.highlight_issues:
            self._highlight_faces = []
            self._highlight_nodes = []

        self.__validate_line_segments()
        self.__validate_faces1()
        self.__validate_faces2()

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        self.__prepare_data(context)
        if self.validate:
            self.__validate()

        polyhedron = PrivatePolyhedron(points=self.nodes(context),
                                       faces=self.faces(context),
                                       convexity=self.convexity)

        if not self.highlight_faces and not self.highlight_nodes:
            return polyhedron

        markers = self.__create_markers(context)

        return Union(children=[polyhedron] + markers)

# ----------------------------------------------------------------------------------------------------------------------
