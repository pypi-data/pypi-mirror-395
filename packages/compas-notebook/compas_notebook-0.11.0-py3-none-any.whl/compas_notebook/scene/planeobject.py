import pythreejs as three
from compas.scene import GeometryObject

from compas_notebook.conversions.geometry import plane_to_threejs

from .sceneobject import ThreeSceneObject


class ThreePlaneObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing planes as grids."""

    def draw(self) -> list[three.Object3D]:
        """Draw the plane as a grid.

        Returns
        -------
        list[three.Object3D]
            List of pythreejs objects created.

        """
        self._guids = plane_to_threejs(self.geometry)

        return self.guids
