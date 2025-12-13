import pythreejs as three
from compas.scene import GeometryObject

from .sceneobject import ThreeSceneObject


class ThreeCylinderObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing cylinder."""

    def draw(self):
        """Draw the cylinder associated with the scene object.

        Returns
        -------
        list[three.Mesh, three.LineSegments]
            List of pythreejs objects created.

        """
        geometry = three.CylinderGeometry(
            radiusTop=self.geometry.radius,
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
