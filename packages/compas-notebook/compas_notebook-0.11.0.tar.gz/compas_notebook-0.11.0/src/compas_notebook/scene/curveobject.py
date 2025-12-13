import pythreejs as three
from compas.scene import GeometryObject

from compas_notebook.conversions.geometry import curve_to_threejs

from .sceneobject import ThreeSceneObject


class ThreeCurveObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing curves."""

    def draw(self) -> list[three.Line]:
        """Draw the curve as discretized polyline.

        Returns
        -------
        list[three.Line]
            List of pythreejs objects created.

        """
        geometry = curve_to_threejs(self.geometry)
        line = three.Line(geometry, three.LineBasicMaterial(color=self.contrastcolor.hex))

        self._guids = [line]

        return self.guids
