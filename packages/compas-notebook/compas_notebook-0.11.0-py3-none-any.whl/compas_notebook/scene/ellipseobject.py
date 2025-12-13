import pythreejs as three
from compas.scene import GeometryObject

from compas_notebook.conversions.geometry import ellipse_to_threejs

from .sceneobject import ThreeSceneObject


class ThreeEllipseObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing ellipses."""

    def draw(self) -> list[three.Line]:
        """Draw the ellipse as a discretized polyline.

        Returns
        -------
        list[three.Line]
            List of pythreejs objects created.

        """
        geometry = ellipse_to_threejs(self.geometry)
        line = three.LineLoop(geometry, three.LineBasicMaterial(color=self.contrastcolor.hex))

        self._guids = [line]

        return self.guids
