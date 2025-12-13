import pythreejs as three
from compas.scene import GeometryObject

from .sceneobject import ThreeSceneObject


class ThreeTorusObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing torus."""

    def draw(self, u=128, v=32):
        """Draw the torus associated with the scene object.

        Parameters
        ----------
        u : int, optional
            The number of segments around the main axis.
        v : int, optional
            The number of segments around the pipe axis.

        Returns
        -------
        list[three.Mesh, three.LineSegments]
            List of pythreejs objects created.

        """
        geometry = three.TorusGeometry(
            radius=self.geometry.radius_axis,
            tube=self.geometry.radius_pipe,
            radialSegments=v,
            tubularSegments=u,
        )
        transformation = self.y_to_z(self.geometry.transformation)

        self._guids = self.geometry_to_objects(
            geometry,
            self.color,
            transformation=transformation,
        )
        return self.guids
