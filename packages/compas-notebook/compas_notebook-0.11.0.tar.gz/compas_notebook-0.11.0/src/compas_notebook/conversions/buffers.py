from typing import Union

import numpy as np
import pythreejs as three
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Polygon
from compas.geometry import Shape
from compas.geometry import earclip_polygon


class MeshShape:
    def __init__(self, mesh: Mesh):
        self.mesh = mesh
        self._vertices = None
        self._edges = None
        self._faces = None

    @property
    def vertices(self):
        if not self._vertices:
            self._vertices = self.mesh.vertices_attributes("xyz")
        return self._vertices

    @property
    def edges(self):
        if not self._edges:
            self._edges = list(self.mesh.edges())
        return self._edges

    @property
    def faces(self):
        if not self._faces:
            self._faces = [self.mesh.face_vertices(face) for face in self.mesh.faces()]
        return self._faces


def shapes_to_edgesbuffer(
    shapes: list[Mesh, Shape],
    color: Color,
) -> three.LineSegments:
    """Convert the combined edges of a collection of shapes to one line segment buffer.

    Parameters
    ----------
    shapes : list[:class:`compas.datastructures.Mesh`, :class:`compas.geometry.Shape`]
        The shape collection.
    color : :class:`compas.colors.Color`
        The color of the edges.

    Returns
    -------
    pythreejs.LineSegments

    """
    positions = []
    colors = []

    for shape in shapes:
        buffer = shape_to_edgesbuffer(shape, color)
        positions += buffer[0]
        colors += buffer[1]

    positions = np.array(positions, dtype=np.float32)
    colors = np.array(colors, dtype=np.float32)

    geometry = three.BufferGeometry(
        attributes={
            "position": three.BufferAttribute(positions, normalized=False),
            "color": three.BufferAttribute(colors, normalized=False, itemSize=3),
        }
    )

    material = three.LineBasicMaterial(vertexColors="VertexColors")

    return three.LineSegments(geometry, material)


def shapes_to_facesbuffer(
    shapes: list[Mesh],
    color: Color,
) -> three.Mesh:
    """Convert the combined faces of a collection of shapes to one mesh buffer.

    Parameters
    ----------
    shapes : list[:class:`compas.datastructures.Mesh`, :class:`compas.geometry.Shape`]
        The shape collection.
    color : :class:`compas.colors.Color`
        The color of the faces.

    Returns
    -------
    pythreejs.Mesh

    """
    positions = []
    colors = []

    for shape in shapes:
        buffer = shape_to_facesbuffer(shape, color)
        positions += buffer[0]
        colors += buffer[1]

    positions = np.array(positions, dtype=np.float32)
    colors = np.array(colors, dtype=np.float32)

    geometry = three.BufferGeometry(
        attributes={
            "position": three.BufferAttribute(positions, normalized=False),
            "color": three.BufferAttribute(colors, normalized=False, itemSize=3),
        }
    )

    material = three.MeshBasicMaterial(
        side="DoubleSide",
        vertexColors="VertexColors",
    )

    return three.Mesh(geometry, material)


def shape_to_edgesbuffer(shape: Union[Mesh, Shape], color: Color) -> tuple[list[list[float]], list[Color]]:
    positions = []
    colors = []

    if isinstance(shape, Mesh):
        shape = MeshShape(shape)

    for u, v in shape.edges:
        positions.append(shape.vertices[u])
        positions.append(shape.vertices[v])
        colors.append(color)
        colors.append(color)

    return positions, colors


def shape_to_facesbuffer(shape: Union[Mesh, Shape], color: Color) -> tuple[list[list[float]], list[Color]]:
    positions = []
    colors = []

    if isinstance(shape, Mesh):
        shape = MeshShape(shape)

    for face in shape.faces:
        if len(face) == 3:
            positions.append(shape.vertices[face[0]])
            positions.append(shape.vertices[face[1]])
            positions.append(shape.vertices[face[2]])
            colors.append(color)
            colors.append(color)
            colors.append(color)

        elif len(face) == 4:
            positions.append(shape.vertices[face[0]])
            positions.append(shape.vertices[face[1]])
            positions.append(shape.vertices[face[2]])
            colors.append(color)
            colors.append(color)
            colors.append(color)
            positions.append(shape.vertices[face[0]])
            positions.append(shape.vertices[face[2]])
            positions.append(shape.vertices[face[3]])
            colors.append(color)
            colors.append(color)
            colors.append(color)

        else:
            ears = earclip_polygon(Polygon([shape.vertices[v] for v in face]))
            for ear in ears:
                positions.append(shape.vertices[ear[0]])
                positions.append(shape.vertices[ear[1]])
                positions.append(shape.vertices[ear[2]])
                colors.append(color)
                colors.append(color)
                colors.append(color)

    return positions, colors
