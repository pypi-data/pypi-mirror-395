from compas.scene import GeometryObject

from compas_notebook.conversions.geometry import frame_to_threejs

from .sceneobject import ThreeSceneObject


class ThreeFrameObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing frames"""

    def draw(self):
        """Draw the frame associated with the scene object as a set of lines: x-axis in red, y-axis in green, z-axis in blue.

        Returns
        -------
        list[three.Line]
            List of pythreejs objects created.

        """

        self._guids = frame_to_threejs(self.geometry)

        return self.guids
