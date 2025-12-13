from compas.scene import Scene


class NotebookScene(Scene):
    def __init__(self, name: str = "NotebookScene", context: str = "Notebook"):
        super().__init__(name=name, context=context)
