import pythreejs as three
from compas.scene import GeometryObject

from compas_notebook.conversions.geometry import surface_to_threejs

from .sceneobject import ThreeSceneObject


class ThreeSurfaceObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing surfaces."""

    def draw(self) -> list[three.Object3D]:
        """Draw the surface as mesh with edges.

        Returns
        -------
        list[three.Object3D]
            List of pythreejs objects created.

        """
        self._guids = surface_to_threejs(self.geometry)

        return self.guids
