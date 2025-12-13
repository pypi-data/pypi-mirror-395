import pythreejs as three
from compas.scene import GeometryObject

from compas_notebook.conversions import line_to_threejs

from .sceneobject import ThreeSceneObject


class ThreeLineObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing line."""

    def draw(self) -> list[three.Line]:
        """Draw the frame associated with the scene object.

        Returns
        -------
        list[three.Line]
            List of pythreejs objects created.

        """
        geometry = line_to_threejs(self.geometry)
        line = three.Line(geometry, three.LineBasicMaterial(color=self.contrastcolor.hex))

        self._guids = [line]

        return self.guids
