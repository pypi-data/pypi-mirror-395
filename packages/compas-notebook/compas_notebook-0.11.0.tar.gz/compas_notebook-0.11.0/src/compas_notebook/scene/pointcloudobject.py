import pythreejs as three
from compas.scene import GeometryObject

from compas_notebook.conversions import pointcloud_to_threejs

from .sceneobject import ThreeSceneObject


class ThreePointcloudObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing pointcloud."""

    def draw(self):
        """Draw the pointcloud associated with the scene object.

        Returns
        -------
        list[three.Points]
            List of pythreejs objects created.

        """
        geometry = pointcloud_to_threejs(self.geometry)
        material = three.PointsMaterial(size=self.pointsize, color=self.color.hex)
        pointclouds = three.Points(geometry, material)

        self._guids = [pointclouds]
        return self.guids
