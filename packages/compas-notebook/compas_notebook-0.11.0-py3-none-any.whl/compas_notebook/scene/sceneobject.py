from typing import Tuple

import numpy
import pythreejs as three
from compas.colors import Color
from compas.geometry import Rotation
from compas.geometry import Transformation
from compas.scene import SceneObject
from compas.scene.descriptors.color import ColorAttribute

Rx = Rotation.from_axis_and_angle([1, 0, 0], 3.14159 / 2)


class ThreeSceneObject(SceneObject):
    """Base class for all PyThreeJS scene objects."""

    color = ColorAttribute(default=Color(0.2, 0.2, 0.2))

    def y_to_z(self, transformation: Transformation) -> Transformation:
        """Convert a transformation from COMPAS to the ThreeJS coordinate system.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`
            The transformation to convert.

        Returns
        -------
        :class:`compas.geometry.Transformation`
            The converted transformation.

        """
        return transformation * Rx

    def geometry_to_objects(
        self,
        geometry: three.BufferGeometry,
        color: Color,
        contrastcolor: Color = None,
        transformation: Transformation = None,
    ) -> Tuple[three.Mesh, three.LineSegments]:
        """Convert a PyThreeJS geometry to a list of PyThreeJS objects.

        Parameters
        ----------
        geometry : :class:`three.Geometry`
            The PyThreeJS geometry to convert.
        color : rgb1 | rgb255 | :class:`compas.colors.Color`
            The RGB color of the geometry.
        contrastcolor : rgb1 | rgb255 | :class:`compas.colors.Color`, optional
            The RGB color of the edges.
        transformation : :class:`compas.geometry.Transformation`, optional
            The transformation to apply to the geometry.

        Returns
        -------
        tuple[three.Mesh, three.LineSegments]
            List of PyThreeJS objects created.

        """
        if not contrastcolor:
            contrastcolor = self.contrastcolor

        edges = three.EdgesGeometry(geometry)
        mesh = three.Mesh(geometry, three.MeshBasicMaterial(color=color.hex, side="DoubleSide"))
        line = three.LineSegments(edges, three.LineBasicMaterial(color=contrastcolor.hex))

        if transformation:
            matrix = numpy.array(transformation.matrix, dtype=numpy.float32).transpose().ravel().tolist()
            mesh.matrix = matrix
            line.matrix = matrix
            mesh.matrixAutoUpdate = False
            line.matrixAutoUpdate = False

        return mesh, line
