import pythreejs as three
from compas.scene import GeometryObject

from compas_notebook.conversions.geometry import circle_to_threejs

from .sceneobject import ThreeSceneObject


class ThreeCircleObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing circles."""

    def draw(self) -> list[three.Line]:
        """Draw the circle as a discretized polyline.

        Returns
        -------
        list[three.Line]
            List of pythreejs objects created.

        """
        geometry = circle_to_threejs(self.geometry)
        line = three.LineLoop(geometry, three.LineBasicMaterial(color=self.contrastcolor.hex))

        self._guids = [line]

        return self.guids
