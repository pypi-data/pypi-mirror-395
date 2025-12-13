import pythreejs as three
from compas.scene import GeometryObject

from .sceneobject import ThreeSceneObject


class ThreeConeObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing cone."""

    def draw(self):
        """Draw the cone associated with the scene object.

        Returns
        -------
        list[three.Mesh, three.LineSegments]
            List of pythreejs objects created.

        """
        geometry = three.CylinderGeometry(
            radiusTop=0,
            radiusBottom=self.geometry.radius,
            height=self.geometry.height,
            radialSegments=32,
        )
        transformation = self.y_to_z(self.geometry.transformation)

        self._guids = self.geometry_to_objects(
            geometry,
            self.color,
            transformation=transformation,
        )
        return self.guids
