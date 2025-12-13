import numpy
import pythreejs as three
from compas.colors import Color
from compas.geometry import Polygon
from compas.geometry import earclip_polygon
from compas.scene import MeshObject

from compas_notebook.scene import ThreeSceneObject


class ThreeMeshObject(ThreeSceneObject, MeshObject):
    """Scene object for drawing mesh."""

    def __init__(
        self,
        show_edges=True,
        vertexcolor=Color(0.0, 0.0, 0.0),
        edgecolor=Color(0.2, 0.2, 0.2),
        facecolor=Color(0.9, 0.9, 0.9),
        vertexsize=0.1,
        **kwargs,
    ):
        super().__init__(
            show_edges=show_edges,
            vertexcolor=vertexcolor,
            edgecolor=edgecolor,
            facecolor=facecolor,
            vertexsize=vertexsize,
            **kwargs,
        )

    def draw(self):
        """Draw the mesh associated with the scene object.

        Returns
        -------
        list[three.Mesh, three.LineSegments]
            List of pythreejs objects created.

        """
        self._guids = []

        vertices = list(self.mesh.vertices())
        faces = list(self.mesh.faces())
        edges = list(self.mesh.edges())

        if self.show_vertices:
            if self.show_vertices is not True:
                vertices = self.show_vertices
            self._guids.append(self.draw_vertices(vertices, self.vertexcolor))

        if self.show_edges:
            if self.show_edges is not True:
                edges = self.show_edges
            self._guids.append(self.draw_edges(edges, self.edgecolor))

        if self.show_faces:
            if self.show_faces is not True:
                faces = self.show_faces
            self._guids.append(self.draw_faces(faces, self.facecolor))

        return self.guids

    def draw_vertices(self, vertices, color):
        positions = [self.mesh.vertex_coordinates(vertex) for vertex in vertices]
        positions = numpy.array(positions, dtype=numpy.float32)
        colors = [color[i] for i in range(len(vertices))]
        colors = numpy.array(colors, dtype=numpy.float32)

        geometry = three.BufferGeometry(
            attributes={
                "position": three.BufferAttribute(positions, normalized=False),
                "color": three.BufferAttribute(colors, normalized=False, itemSize=3),
            }
        )
        material = three.PointsMaterial(
            size=self.vertexsize,
            vertexColors="VertexColors",
        )
        return three.Points(geometry, material)

    def draw_edges(self, edges, color):
        positions = []
        colors = []

        for u, v in edges:
            positions.append(self.mesh.vertex_coordinates(u))
            positions.append(self.mesh.vertex_coordinates(v))
            colors.append(color[u, v])
            colors.append(color[u, v])

        positions = numpy.array(positions, dtype=numpy.float32)
        colors = numpy.array(colors, dtype=numpy.float32)

        geometry = three.BufferGeometry(
            attributes={
                "position": three.BufferAttribute(positions, normalized=False),
                "color": three.BufferAttribute(colors, normalized=False, itemSize=3),
            }
        )
        material = three.LineBasicMaterial(vertexColors="VertexColors")
        return three.LineSegments(geometry, material)

    def draw_faces(self, faces, color):
        positions = []
        colors = []

        for face in faces:
            vertices = self.mesh.face_vertices(face)
            c = color[face]

            if len(vertices) == 3:
                positions.append(self.mesh.vertex_coordinates(vertices[0]))
                positions.append(self.mesh.vertex_coordinates(vertices[1]))
                positions.append(self.mesh.vertex_coordinates(vertices[2]))
                colors.append(c)
                colors.append(c)
                colors.append(c)
            elif len(vertices) == 4:
                positions.append(self.mesh.vertex_coordinates(vertices[0]))
                positions.append(self.mesh.vertex_coordinates(vertices[1]))
                positions.append(self.mesh.vertex_coordinates(vertices[2]))
                colors.append(c)
                colors.append(c)
                colors.append(c)
                positions.append(self.mesh.vertex_coordinates(vertices[0]))
                positions.append(self.mesh.vertex_coordinates(vertices[2]))
                positions.append(self.mesh.vertex_coordinates(vertices[3]))
                colors.append(c)
                colors.append(c)
                colors.append(c)
            else:
                polygon = Polygon([self.mesh.vertex_coordinates(v) for v in vertices])
                ears = earclip_polygon(polygon)
                for ear in ears:
                    positions.append(self.mesh.vertex_coordinates(vertices[ear[0]]))
                    positions.append(self.mesh.vertex_coordinates(vertices[ear[1]]))
                    positions.append(self.mesh.vertex_coordinates(vertices[ear[2]]))
                    colors.append(c)
                    colors.append(c)
                    colors.append(c)

        positions = numpy.array(positions, dtype=numpy.float32)
        colors = numpy.array(colors, dtype=numpy.float32)

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
