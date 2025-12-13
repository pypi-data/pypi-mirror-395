import pythreejs as three
from compas.scene import GeometryObject

from compas_notebook.conversions import point_to_threejs

from .sceneobject import ThreeSceneObject


class ThreePointObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing point."""

    def draw(self):
        """Draw the point associated with the scene object.

        Returns
        -------
        list[three.Points]
            List of pythreejs objects created.

        """
        geometry = point_to_threejs(self.geometry)
        material = three.PointsMaterial(size=self.pointsize, color=self.color.hex)
        points = three.Points(geometry, material)

        self._guids = [points]
        return self.guids
