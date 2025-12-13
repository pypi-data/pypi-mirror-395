from compas.colors import Color
from compas.scene import GeometryObject
from compas.scene.descriptors.color import ColorAttribute

from compas_notebook.conversions import dot_to_threejs

from .sceneobject import ThreeSceneObject


class ThreeDotObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing a dot (text at a point)."""

    color = ColorAttribute(default=Color.black())

    def __init__(self, fontsize=256, **kwargs):
        super().__init__(**kwargs)
        self.fontsize = fontsize

    def draw(self):
        """Draw the dot associated with the scene object.

        Returns
        -------
        list[three.Sprite]
            List of pythreejs objects created.

        """
        sprite = dot_to_threejs(self.geometry, fontsize=self.fontsize, color=self.color.hex)
        self._guids = [sprite]
        return self.guids
