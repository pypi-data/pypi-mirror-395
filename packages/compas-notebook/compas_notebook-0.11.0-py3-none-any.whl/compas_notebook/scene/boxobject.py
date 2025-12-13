from compas.scene import GeometryObject

from compas_notebook.conversions import box_to_threejs

from .sceneobject import ThreeSceneObject


class ThreeBoxObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing box shapes."""

    def draw(self):
        """Draw the box associated with the scene object.

        Returns
        -------
        list[three.Mesh, three.LineSegments]
            List of pythreejs objects created.

        """
        geometry = box_to_threejs(self.geometry)
        transformation = self.y_to_z(self.geometry.transformation)

        self._guids = self.geometry_to_objects(
            geometry,
            self.color,
            transformation=transformation,
        )

        return self.guids
