import typing

if typing.TYPE_CHECKING:
    from compas_notebook.viewer import Viewer

from compas.geometry import Point


class Controller:
    def __init__(self, viewer: "Viewer"):
        self.viewer = viewer

    # =============================================================================
    # Load/Save
    # =============================================================================

    def load_scene(self) -> None:
        """Load a scene from file."""
        self.viewer.set_statustext("Loading scene...")

    def save_scene(self) -> None:
        """Save the scene to file."""
        self.viewer.set_statustext("Saving scene...")

    # =============================================================================
    # Zoom
    # =============================================================================

    def zoom_extents(self) -> None:
        """Zoom to the extents of the scene.

        Raises
        ------
        NotImplementedError
            If the value of ``self.viewer.viewport`` is anything other than ``{'perspective', 'top'}``

        Warnings
        --------
        This function is experimental.

        """
        width = self.viewer.config.view.width
        height = self.viewer.config.view.height

        self.viewer.set_statustext("Zoom extents...")
        xmin, ymin, zmin, xmax, ymax, zmax = self.scene_bounds()
        dx = xmax - xmin
        dy = ymax - ymin
        dz = zmax - zmin
        cx, cy, cz = (xmin + xmax) / 2, (ymin + ymax) / 2, (zmin + zmax) / 2
        d = max(dx, dy, dz)

        if self.viewer.viewport == "perspective":
            self.viewer.camera3.position = [cx, cy - 2 * d, cz + 0.5 * dz]
            self.viewer.controls3.target = [cx, cy, cz]

        elif self.viewer.viewport == "top":
            self.viewer.camera3.position = [cx, cy, cz + d]
            self.viewer.camera3.zoom = min(0.75 * width / d, 0.75 * height / d)
            self.viewer.controls3.target = [cx, cy, cz]

        else:
            raise NotImplementedError

    def zoom_in(self) -> None:
        """Zoom in.

        Zooming in is done by halving the distance between the target and the camera position.
        The camera position is a property of the camera itself.
        The target is controlled by ``three.OrbitControls``.

        So we basically compute the vector from the target location to the camera position,
        and then move the camera to ``target + direction * 0.5``.

        Note that you should not use the ``zoom`` attribute of the camera.
        Changing the camera zoom is more like changing the magnification.

        """
        self.viewer.set_statustext("Zoom in...")

        position = Point(*self.viewer.camera3.position)
        target = Point(*self.viewer.controls3.target)
        direction = position - target
        self.viewer.camera3.position = list(target + direction * 0.5)
        self.viewer.controls3.target = list(target)

    def zoom_out(self) -> None:
        """Zoom out.

        Zooming out is done by doubling the distance between the target and the camera position.
        The camera position is a property of the camera itself.
        The target is controlled by ``three.OrbitControls``.

        So we basically compute the vector from the target location to the camera position,
        and then move the camera to ``target + direction * 2.0``.

        Note that you should not use the ``zoom`` attribute of the camera.
        Changing the camera zoom is more like changing the magnification.

        """
        self.viewer.set_statustext("Zoom out...")

        position = Point(*self.viewer.camera3.position)
        target = Point(*self.viewer.controls3.target)
        direction = position - target
        self.viewer.camera3.position = list(target + direction * 2.0)
        self.viewer.controls3.target = list(target)

    # move this to the scene
    # add a BVH to the scene
    def scene_bounds(self):
        """Compute the axis-aligned bounding box of the scene."""
        xmin = ymin = zmin = +1e12
        xmax = ymax = zmax = -1e12
        for obj in self.viewer.scene.objects:
            if hasattr(obj, "mesh"):
                box = obj.mesh.aabb
            elif hasattr(obj, "geometry"):
                box = obj.geometry.aabb
            elif hasattr(obj, "brep"):
                box = obj.brep.aabb
            else:
                continue
            xmin = min(xmin, box.xmin)
            ymin = min(ymin, box.ymin)
            zmin = min(zmin, box.zmin)
            xmax = max(xmax, box.xmax)
            ymax = max(ymax, box.ymax)
            zmax = max(zmax, box.zmax)
        return xmin, ymin, zmin, xmax, ymax, zmax

    # =============================================================================
    # Show/Hide
    # =============================================================================

    def on_toggle_vertices(self, change):
        for obj in self.viewer.scene.objects:
            if hasattr(obj, "show_vertices"):
                obj.show_vertices = change["new"]
        self.viewer.update()
