# ruff: noqa: F401
"""This package provides scene object plugins for visualising COMPAS objects in Jupyter Notebooks using three.
When working in a notebook, :class:`compas.scene.SceneObject`
will automatically use the corresponding PyThreeJS scene object for each COMPAS object type.

"""

from compas.plugins import plugin
from compas.scene import register

from compas.geometry import Box
from compas.geometry import Brep
from compas.geometry import Capsule
from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Curve
from compas.geometry import Cylinder
from compas.geometry import Ellipse
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Pointcloud
from compas.geometry import Polygon
from compas.geometry import Polyhedron
from compas.geometry import Polyline
from compas.geometry import Sphere
from compas.geometry import Surface
from compas.geometry import Torus
from compas.geometry import Vector

from compas_notebook.geometry import Dot

from compas.datastructures import Graph
from compas.datastructures import Mesh

from .scene import NotebookScene

from .sceneobject import ThreeSceneObject

from .boxobject import ThreeBoxObject
from .brepobject import ThreeBrepObject
from .capsuleobject import ThreeCapsuleObject
from .circleobject import ThreeCircleObject
from .coneobject import ThreeConeObject
from .curveobject import ThreeCurveObject
from .cylinderobject import ThreeCylinderObject
from .dotobject import ThreeDotObject
from .ellipseobject import ThreeEllipseObject
from .frameobject import ThreeFrameObject
from .groupobject import ThreeGroupObject
from .lineobject import ThreeLineObject
from .planeobject import ThreePlaneObject
from .pointobject import ThreePointObject
from .pointcloudobject import ThreePointcloudObject
from .polygonobject import ThreePolygonObject
from .polyhedronobject import ThreePolyhedronObject
from .polylineobject import ThreePolylineObject
from .sphereobject import ThreeSphereObject
from .surfaceobject import ThreeSurfaceObject
from .torusobject import ThreeTorusObject
from .vectorobject import ThreeVectorObject

from .graphobject import ThreeGraphObject
from .meshobject import ThreeMeshObject


@plugin(category="drawing-utils", pluggable_name="clear", requires=["pythreejs"])
def clear_pythreejs(guids=None):
    pass


@plugin(category="drawing-utils", pluggable_name="redraw", requires=["pythreejs"])
def redraw_pythreejs():
    pass


@plugin(
    category="drawing-utils",
    pluggable_name="after_draw",
    requires=["pythreejs"],
)
def after_draw(sceneobjects):
    pass


@plugin(category="factories", requires=["pythreejs"])
def register_scene_objects():
    register(Box, ThreeBoxObject, context="Notebook")
    register(Brep, ThreeBrepObject, context="Notebook")
    register(Capsule, ThreeCapsuleObject, context="Notebook")
    register(Circle, ThreeCircleObject, context="Notebook")
    register(Cone, ThreeConeObject, context="Notebook")
    register(Curve, ThreeCurveObject, context="Notebook")
    register(Cylinder, ThreeCylinderObject, context="Notebook")
    register(Dot, ThreeDotObject, context="Notebook")
    register(Ellipse, ThreeEllipseObject, context="Notebook")
    register(Frame, ThreeFrameObject, context="Notebook")
    register(Graph, ThreeGraphObject, context="Notebook")
    register(Line, ThreeLineObject, context="Notebook")
    register(Mesh, ThreeMeshObject, context="Notebook")
    register(Plane, ThreePlaneObject, context="Notebook")
    register(Point, ThreePointObject, context="Notebook")
    register(Pointcloud, ThreePointcloudObject, context="Notebook")
    register(Polygon, ThreePolygonObject, context="Notebook")
    register(Polyhedron, ThreePolyhedronObject, context="Notebook")
    register(Polyline, ThreePolylineObject, context="Notebook")
    register(Sphere, ThreeSphereObject, context="Notebook")
    register(Surface, ThreeSurfaceObject, context="Notebook")
    register(Torus, ThreeTorusObject, context="Notebook")
    register(Vector, ThreeVectorObject, context="Notebook")
    register(list, ThreeGroupObject, context="Notebook")
