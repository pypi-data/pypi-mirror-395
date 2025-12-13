from compas.colors import Color
from compas.data import Data

from compas_notebook.conversions import shapes_to_edgesbuffer
from compas_notebook.conversions import shapes_to_facesbuffer

from .sceneobject import SceneObject


class Group(Data):
    """A group of compas.data.Data items."""

    def __init__(self, items: list[Data] = None):
        super().__init__()
        self.items = items or []

    @property
    def __data__(self):
        return {"items": self.items}


class ThreeGroupObject(SceneObject):
    """A group of scene objects."""

    item: Group

    def __init__(self, item=None, **kwargs):
        super().__init__(item=Group(item), **kwargs)
        self.show = True
        self.is_selected = False
        self.opacity = 1.0
        self.bounding_box = None

    @property
    def items(self) -> list:
        return self.item.items

    def init(self, *args, **kwargs):
        pass

    def draw(self, *args, **kwargs):
        self._guids = []
        edgesbuffer = shapes_to_edgesbuffer(self.items, Color(0.2, 0.2, 0.2))
        facesbuffer = shapes_to_facesbuffer(self.items, self.color)
        self._guids.append(edgesbuffer)
        self._guids.append(facesbuffer)
        return self._guids

    def draw_instance(self, *args, **kwargs):
        pass
