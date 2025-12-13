import pythreejs as three
from compas.datastructures import Mesh
from compas.scene import GeometryObject

from compas_notebook.conversions import vertices_and_edges_to_threejs
from compas_notebook.conversions import vertices_and_faces_to_threejs

from .sceneobject import ThreeSceneObject


class ThreeCapsuleObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing capsule."""

    def draw(self):
        """Draw the capsule associated with the scene object.

        Returns
        -------
        list[three.Mesh, three.LineSegments]
            List of pythreejs objects created.

        """
        mesh = Mesh.from_shape(self.geometry)
        vertices, faces = mesh.to_vertices_and_faces()
        edges = list(mesh.edges())

        geometry = vertices_and_faces_to_threejs(vertices, faces)
        mesh = three.Mesh(geometry, three.MeshBasicMaterial(color=self.color.hex, side="DoubleSide"))

        geometry = vertices_and_edges_to_threejs(vertices, edges)
        line = three.LineSegments(geometry, three.LineBasicMaterial(color=self.contrastcolor.hex))

        self._guids = [mesh, line]

        return self.guids
