from compas.scene import GeometryObject

from compas_notebook.conversions import sphere_to_threejs

from .sceneobject import ThreeSceneObject


class ThreeSphereObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing sphere."""

    def draw(self):
        """Draw the sphere associated with the scene object.

        Returns
        -------
        list[three.Mesh, three.LineSegments]
            List of pythreejs objects created.

        """
        geometry = sphere_to_threejs(self.geometry)
        transformation = self.y_to_z(self.geometry.transformation)

        self._guids = self.geometry_to_objects(
            geometry,
            self.color,
            transformation=transformation,
        )
        return self.guids
