import ipywidgets as widgets
import pythreejs as three
from compas.colors import Color
from compas.scene import Scene
from IPython.display import display as ipydisplay

from .config import Config
from .controller import Controller
from .scene import NotebookScene


class Viewer:
    """Viewer for COMPAS geometry in Jupyter notebooks.

    Parameters
    ----------
    config : :class:`Config`, optional
        A configuration object.
    configpath : path-like or str, optional
        The path to a configuration file.
    scene : :class:`Scene`, optional
        A COMPAS scene, with context set to "Notebook".
    controller : :class:`Controller`, optional
        A custom action controller.

    Examples
    --------
    This example is meant to be run from within a Jupyter notebook.

    >>> import compas
    >>> from compas.datastructures import Mesh
    >>> from compas_notebook.viewer import Viewer
    >>> mesh = Mesh.from_obj(compas.get("tubemesh.obj"))
    >>> viewer = Viewer()
    >>> viewer.scene.add(mesh)  # doctest: +SKIP
    >>> viewer.show()  # doctest: +SKIP

    """

    def __init__(
        self,
        config: Config = None,
        controller: Controller = None,
    ):
        self._scene = None
        self.config = config or Config()
        self.controller = controller or Controller(viewer=self)

        # move this to a UI class
        self.toolbar = None
        self.main = None
        self.statusbar = None
        self.statustext = None

    # =============================================================================
    # System methods
    # =============================================================================

    @property
    def scene(self):
        if self._scene is None:
            self._scene = NotebookScene()
        return self._scene

    @scene.setter
    def scene(self, scene: Scene) -> None:
        scene = scene or NotebookScene()
        self._scene: NotebookScene = NotebookScene.__from_data__(scene.__data__)

    def show(self) -> None:
        """Display the viewer in the notebook."""
        self.init_webgl()
        self.init_ui()

        self.scene.draw()
        for o in self.scene.objects:
            for o3 in o.guids:
                self.scene3.add(o3)

        ipydisplay(self.ui)

    # this could be handled better,
    # by only removing and re-adding objects that have changed.
    # in any case, visibility should just be updateable...
    def update(self) -> None:
        """Update an existing viewer instance."""
        for child in self.scene3.children:
            self.scene3.remove(child)

        self.scene3.children = []

        if self.config.view.show_grid:
            self.scene3.add(self.grid3)
        if self.config.view.show_axes:
            self.scene3.add(self.axes3)

        self.scene.draw()

        for o in self.scene.objects:
            for o3 in o.guids:
                self.scene3.add(o3)

    # =============================================================================
    # WebGL
    # =============================================================================

    def init_webgl(self):
        width = self.config.view.width
        height = self.config.view.height
        aspect = width / height

        self.scene3 = three.Scene(background=self.config.view.background.hex)

        if self.config.view.show_grid:
            self.grid3 = three.GridHelper(
                size=20,
                divisions=20,
                colorCenterLine=Color.grey().hex,
                colorGrid=Color.grey().lightened(50).hex,
            )
            self.grid3.rotateX(3.14159 / 2)
            self.scene3.add(self.grid3)

        if self.config.view.show_axes:
            self.axes3 = three.AxesHelper(size=0.5)
            self.scene3.add(self.axes3)

        # camera and controls

        if self.config.view.viewport == "top":
            self.camera3 = three.OrthographicCamera(
                width / -2,
                width / 2,
                height / 2,
                height / -2,
                self.config.view.camera.near,
                self.config.view.camera.far,
            )
            self.camera3.position = self.config.view.camera.position
            self.camera3.zoom = 1

            self.controls3 = three.OrbitControls(controlling=self.camera3)
            self.controls3.enableRotate = False
            self.controls3.maxDistance = self.config.view.camera.far
            self.controls3.minDistance = self.config.view.camera.near

        elif self.config.view.viewport == "perspective":
            self.camera3 = three.PerspectiveCamera()
            self.camera3.position = self.config.view.camera.position
            self.camera3.up = self.config.view.camera.up
            self.camera3.aspect = aspect
            self.camera3.near = self.config.view.camera.near
            self.camera3.far = self.config.view.camera.far
            self.camera3.fov = self.config.view.camera.fov

            self.controls3 = three.OrbitControls(controlling=self.camera3)
            self.controls3.maxDistance = self.config.view.camera.far
            self.controls3.minDistance = self.config.view.camera.near
            self.controls3.target = self.config.view.camera.target

            self.camera3.zoom = 1
            self.camera3.lookAt(self.config.view.camera.target)

        else:
            raise NotImplementedError

        # renderer

        self.renderer3 = three.Renderer(
            scene=self.scene3,
            camera=self.camera3,
            controls=[self.controls3],
            width=width,
            height=height,
            antialias=True,
        )

    # =============================================================================
    # UI
    # =============================================================================

    def init_ui(self) -> None:
        """Initialize the user interface."""
        self.ui = widgets.VBox()
        self.ui.layout.width = "auto"
        children = []

        height = self.config.view.height

        if self.config.ui.show_toolbar:
            self.toolbar = self.make_toolbar()
            children.append(self.toolbar)
            height += 64

        self.main = self.make_main()
        children.append(self.main)

        if self.config.ui.show_statusbar:
            self.statusbar = self.make_statusbar()
            children.append(self.statusbar)
            height += 48

        self.ui.layout.height = f"{height + 4}px"
        self.ui.children = children

    def make_main(self) -> widgets.HBox:
        """Initialize the main section of the user interface."""
        children = []

        if self.config.ui.sidebar.show:
            sidebar = self.make_sidebar()
            children.append(sidebar)

        view3d = self.make_view3d()
        children.append(view3d)

        main = widgets.HBox()
        main.layout.width = "auto"
        main.layout.height = f"{self.config.view.height + 4}px"
        main.children = children
        return main

    def make_sidebar(self) -> widgets.GridBox:
        """"""
        items = self.config.ui.sidebar.items
        item_layout = widgets.Layout(
            width="100%",
            margin="0px",
            padding="0px",
            display="block",
        )

        sidebar = widgets.GridBox()
        sidebar.layout.width = "240px"
        sidebar.layout.grid_template_rows = "32px 1fr"
        sidebar.layout.height = f"{self.config.view.height + 4}px"
        sidebar.layout.align_content = "flex-start"
        sidebar.layout.align_items = "flex-start"
        sidebar.layout.justify_content = "flex-start"
        sidebar.layout.justify_items = "flex-start"
        sidebar.layout.overflow = "hidden"
        sidebar.layout.padding = "0px"
        sidebar.layout.margin = "0px"

        children = []

        if items:
            for item in items:
                if item["type"] == "checkbox":

                    def action(x):
                        f = getattr(self.controller, item["action"])
                        f(x)

                    checkbox = widgets.Checkbox(value=item["value"], description=item["text"], layout=item_layout)
                    checkbox.observe(action, names="value")
                    children.append(checkbox)

        sidebar.children = children
        return sidebar

    def make_view3d(self) -> widgets.Box:
        """"""
        view3d = widgets.Box()
        view3d.layout.width = "auto"
        view3d.layout.height = f"{self.config.view.height + 4}px"
        view3d.children = [self.renderer3]
        return view3d

    def make_statusbar(self) -> widgets.HBox:
        """Initialize the status bar.

        Returns
        -------
        ipywidgets.HBox

        """
        statustext = widgets.Text(value="", placeholder="...", description="", disabled=True)
        statustext.layout.width = "100%"
        statustext.layout.height = "32px"
        statustext.layout.padding = "0px 0px 0px 0px"
        statustext.layout.margin = "0px 0px 0px 0px"
        statustext.style.background = "#eeeeee"

        self.statustext = statustext

        statusbar = widgets.HBox()
        statusbar.layout.display = "flex"
        statusbar.layout.flex_flow = "row"
        statusbar.layout.align_items = "flex-start"
        statusbar.layout.width = "auto"
        statusbar.layout.height = "48px"
        statusbar.layout.padding = "0px 0px 0px 0px"
        statusbar.layout.margin = "0px 0px 0px 0px"
        statusbar.children = [statustext]

        return statusbar

    def make_toolbar(self) -> widgets.HBox:
        """Initialize the toolbar.

        Returns
        -------
        ipywidgets.HBox

        """
        buttons = []

        # load_scene_button = widgets.Button(
        #     icon="folder-open",
        #     tooltip="Load scene",
        #     layout=widgets.Layout(width="48px", height="32px"),
        # )
        # load_scene_button.on_click(lambda x: self.controller.load_scene())
        # buttons.append(load_scene_button)

        # save_scene_button = widgets.Button(
        #     icon="save",
        #     tooltip="Load scene",
        #     layout=widgets.Layout(width="48px", height="32px"),
        # )
        # save_scene_button.on_click(lambda x: self.controller.save_scene())
        # buttons.append(save_scene_button)

        zoom_in_button = widgets.Button(
            icon="search-plus",
            tooltip="Zoom in",
            layout=widgets.Layout(width="48px", height="32px"),
        )
        zoom_in_button.on_click(lambda x: self.controller.zoom_in())
        buttons.append(zoom_in_button)

        zoom_out_button = widgets.Button(
            icon="search-minus",
            tooltip="Zoom out",
            layout=widgets.Layout(width="48px", height="32px"),
        )
        zoom_out_button.on_click(lambda x: self.controller.zoom_out())
        buttons.append(zoom_out_button)

        toolbar = widgets.HBox()
        toolbar.layout.display = "flex"
        toolbar.layout.flex_flow = "row"
        toolbar.layout.align_items = "center"
        toolbar.layout.width = "auto"
        toolbar.layout.height = "48px"
        toolbar.layout.padding = "0px 0px 0px 0px"
        toolbar.layout.margin = "0px 0px 16px 0px"
        toolbar.children = buttons

        return toolbar

    # =============================================================================
    # Actions
    # =============================================================================

    def set_statustext(self, text: str) -> None:
        """Set the text of the status bar."""
        if self.statustext:
            self.statustext.value = text
