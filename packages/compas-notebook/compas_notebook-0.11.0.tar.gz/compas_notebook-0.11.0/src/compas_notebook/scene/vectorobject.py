import pythreejs as three
from compas.scene import GeometryObject

from compas_notebook.conversions.geometry import vector_to_threejs

from .sceneobject import ThreeSceneObject


class ThreeVectorObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing vectors as arrows."""

    def draw(self) -> list[three.Object3D]:
        """Draw the vector as arrow (line + cone head).

        Returns
        -------
        list[three.Object3D]
            List of pythreejs objects created.

        """
        self._guids = vector_to_threejs(self.geometry)

        return self.guids
