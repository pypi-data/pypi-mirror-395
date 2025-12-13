import pythreejs as three
from compas.scene import GeometryObject

from compas_notebook.conversions import vertices_and_edges_to_threejs
from compas_notebook.conversions import vertices_and_faces_to_threejs

from .sceneobject import ThreeSceneObject


class ThreePolyhedronObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing polyhedron."""

    def draw(self):
        """Draw the polyhedron associated with the scene object.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`compas.colors.Color`, optional
            The RGB color of the polyhedron.

        Returns
        -------
        list[three.Mesh, three.LineSegments]
            List of pythreejs objects created.

        """
        vertices = self.geometry.vertices
        faces = self.geometry.faces
        edges = self.geometry.edges

        geometry = vertices_and_faces_to_threejs(vertices, faces)
        mesh = three.Mesh(geometry, three.MeshBasicMaterial(color=self.color.hex, side="DoubleSide"))

        geometry = vertices_and_edges_to_threejs(vertices, edges)
        line = three.LineSegments(geometry, three.LineBasicMaterial(color=self.contrastcolor.hex))

        guids = [mesh, line]

        self._guids = guids
        return self.guids
