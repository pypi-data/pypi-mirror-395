import pythreejs as three
from compas.geometry import earclip_polygon
from compas.itertools import pairwise
from compas.scene import GeometryObject

from compas_notebook.conversions import vertices_and_edges_to_threejs
from compas_notebook.conversions import vertices_and_faces_to_threejs

from .sceneobject import ThreeSceneObject


class ThreePolygonObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing polygons."""

    def draw(self):
        """Draw the polygon associated with the scene object.

        Returns
        -------
        list[three.Mesh, three.LineSegments]
            List of pythreejs objects created.

        """
        n = len(self.geometry.points)
        vertices = self.geometry.points
        triangles = earclip_polygon(self.geometry)
        edges = list(pairwise(range(len(vertices)))) + [(n - 1, 0)]

        geometry = vertices_and_faces_to_threejs(vertices, triangles)
        mesh = three.Mesh(geometry, three.MeshBasicMaterial(color=self.color.hex, side="DoubleSide"))

        geometry = vertices_and_edges_to_threejs(vertices, edges)
        line = three.LineSegments(geometry, three.LineBasicMaterial(color=self.contrastcolor.hex))

        self._guids = [mesh, line]
        return self.guids
