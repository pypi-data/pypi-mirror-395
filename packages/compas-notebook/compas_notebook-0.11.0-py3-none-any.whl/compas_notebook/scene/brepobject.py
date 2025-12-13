import pythreejs as three
from compas.geometry import Brep
from compas.scene import GeometryObject

from compas_notebook.conversions import polyline_to_threejs
from compas_notebook.conversions import vertices_and_faces_to_threejs
from compas_notebook.scene import ThreeSceneObject


class ThreeBrepObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing a Brep."""

    geometry: Brep

    def draw(self):
        """Draw the Brep associated with the scene object.

        Returns
        -------
        list[three.Mesh, three.LineSegments]
            List of pythreejs objects created.

        """
        mesh, polylines = self.geometry.to_viewmesh()
        vertices, faces = mesh.to_vertices_and_faces()

        geometry = vertices_and_faces_to_threejs(vertices, faces)
        mesh = three.Mesh(geometry, three.MeshBasicMaterial(color=self.color.hex, side="DoubleSide"))

        guids = [mesh]

        for polyline in polylines:
            geometry = polyline_to_threejs(polyline)
            line = three.LineSegments(geometry, three.LineBasicMaterial(color=self.contrastcolor.hex))
            guids.append(line)

        self._guids = guids
        return self.guids
