import pythreejs as three
from compas.scene import GeometryObject

from compas_notebook.conversions import polyline_to_threejs

from .sceneobject import ThreeSceneObject


class ThreePolylineObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing polyline."""

    def draw(self):
        """Draw the polyline associated with the scene object.

        Returns
        -------
        list[three.Line]
            List of pythreejs objects created.

        """
        geometry = polyline_to_threejs(self.geometry)
        polyline = three.Line(geometry, three.LineBasicMaterial(color=self.contrastcolor.hex))

        guids = [polyline]

        self._guids = guids
        return self.guids
