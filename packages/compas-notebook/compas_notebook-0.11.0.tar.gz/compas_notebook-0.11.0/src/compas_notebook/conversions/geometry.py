import math

import numpy
import pythreejs as three
from compas.geometry import Box
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
from compas.geometry import Polyline
from compas.geometry import Sphere
from compas.geometry import Surface
from compas.geometry import Torus
from compas.geometry import Vector

from compas_notebook.conversions.meshes import vertices_and_edges_to_threejs
from compas_notebook.conversions.meshes import vertices_and_faces_to_threejs
from compas_notebook.geometry import Dot


def line_to_threejs(line: Line) -> three.BufferGeometry:
    """Convert a COMPAS line to PyThreeJS.

    Parameters
    ----------
    line : :class:`compas.geometry.Line`
        The line to convert.

    Returns
    -------
    :class:`three.BufferGeometry`

    """
    vertices = numpy.array([line.start, line.end], dtype=numpy.float32)
    geometry = three.BufferGeometry(attributes={"position": three.BufferAttribute(vertices, normalized=False)})
    return geometry


def frame_to_threejs(frame: Frame) -> list[three.BufferGeometry]:
    """Convert a COMPAS frame to PyThreeJS.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`
        The frame to convert.

    Returns
    -------
    list[three.BufferGeometry]

    """

    # create lines for each axis
    _x_line = Line(frame.point, frame.point + frame.xaxis)
    _y_line = Line.from_point_and_vector(frame.point, frame.yaxis)
    _z_line = Line.from_point_and_vector(frame.point, frame.zaxis)

    # convert lines to threejs vertex buffers
    xline_verts = line_to_threejs(_x_line)
    yline_verts = line_to_threejs(_y_line)
    zline_verts = line_to_threejs(_z_line)

    # convert from vertex buffers to line objects
    xline_lines = three.Line(xline_verts, three.LineBasicMaterial(color="red"))
    yline_lines = three.Line(yline_verts, three.LineBasicMaterial(color="green"))
    zline_lines = three.Line(zline_verts, three.LineBasicMaterial(color="blue"))

    result = [xline_lines, yline_lines, zline_lines]
    return result


def point_to_threejs(point: Point) -> three.SphereGeometry:
    """Convert a COMPAS point to PyThreeJS.

    Parameters
    ----------
    point : :class:`compas.geometry.Point`
        The point to convert.

    Returns
    -------
    :class:`three.BufferGeometry`

    Examples
    --------
    >>> from compas.geometry import Point
    >>> point = Point(1, 2, 3)
    >>> point_to_threejs(point)  # doctest: +ELLIPSIS
    BufferGeometry(...)

    """
    vertices = numpy.array([point], dtype=numpy.float32)
    geometry = three.BufferGeometry(attributes={"position": three.BufferAttribute(vertices, normalized=False)})
    return geometry


def pointcloud_to_threejs(pointcloud: Pointcloud) -> three.SphereGeometry:
    """Convert a COMPAS point to PyThreeJS.

    Parameters
    ----------
    pointcloud : :class:`compas.geometry.Pointcloud`
        The pointcloud to convert.

    Returns
    -------
    :class:`three.BufferGeometry`

    Examples
    --------
    >>>

    """
    vertices = numpy.array(pointcloud.points, dtype=numpy.float32)
    geometry = three.BufferGeometry(attributes={"position": three.BufferAttribute(vertices, normalized=False)})
    return geometry


def polyline_to_threejs(polyline: Polyline) -> three.BufferGeometry:
    """Convert a COMPAS polyline to PyThreeJS.

    Parameters
    ----------
    polyline : :class:`compas.geometry.Polyline`
        The polyline to convert.

    Returns
    -------
    :class:`three.BufferGeometry`

    """
    vertices = numpy.array(polyline.points, dtype=numpy.float32)
    geometry = three.BufferGeometry(attributes={"position": three.BufferAttribute(vertices, normalized=False)})
    return geometry


def circle_to_threejs(circle: Circle, max_angle: float = 5.0) -> three.BufferGeometry:
    """Convert a COMPAS circle to PyThreeJS.

    Parameters
    ----------
    circle : :class:`compas.geometry.Circle`
        The circle to convert.
    max_angle : float, optional
        Maximum angle in degrees between segments.

    Returns
    -------
    :class:`three.BufferGeometry`

    """

    n = max(8, int(math.ceil(360.0 / max_angle)))
    polyline = circle.to_polyline(n=n)
    vertices = numpy.array(polyline.points, dtype=numpy.float32)
    geometry = three.BufferGeometry(attributes={"position": three.BufferAttribute(vertices, normalized=False)})
    return geometry


def ellipse_to_threejs(ellipse: Ellipse, max_angle: float = 5.0) -> three.BufferGeometry:
    """Convert a COMPAS ellipse to PyThreeJS.

    Parameters
    ----------
    ellipse : :class:`compas.geometry.Ellipse`
        The ellipse to convert.
    max_angle : float, optional
        Maximum angle in degrees between segments.

    Returns
    -------
    :class:`three.BufferGeometry`

    """
    n = max(8, int(math.ceil(360.0 / max_angle)))
    polyline = ellipse.to_polyline(n=n)
    vertices = numpy.array(polyline.points, dtype=numpy.float32)
    geometry = three.BufferGeometry(attributes={"position": three.BufferAttribute(vertices, normalized=False)})
    return geometry


def vector_to_threejs(vector: Vector, scale: float = 1.0) -> list[three.Object3D]:
    """Convert a COMPAS vector to PyThreeJS as arrow.

    Parameters
    ----------
    vector : :class:`compas.geometry.Vector`
        The vector to convert.
    scale : float, optional
        Scale factor for vector length.

    Returns
    -------
    list[three.Object3D]
        Line and cone representing the arrow.

    """
    # Line from origin to vector * scale
    line = Line([0, 0, 0], vector * scale)
    line_geom = line_to_threejs(line)
    line_obj = three.Line(line_geom, three.LineBasicMaterial(color="blue"))

    # Cone head at tip (10% of length, positioned at end)
    length = vector.length * scale
    cone_height = length * 0.1
    cone_radius = cone_height * 0.3

    # Position cone at vector tip
    cone_geom = three.CylinderGeometry(
        radiusTop=0,
        radiusBottom=cone_radius,
        height=cone_height,
        radialSegments=8,
    )
    cone_obj = three.Mesh(cone_geom, three.MeshBasicMaterial(color="blue"))

    # Compute cone position and rotation
    # Cone should point in vector direction
    tip = vector * scale
    cone_obj.position = (tip.x, tip.y, tip.z)

    # Align cone with vector direction
    # Three.js cylinder default is Y-up, need to rotate to align with vector
    normalized = vector.unitized()
    cone_obj.quaternion = _vector_to_quaternion(normalized)

    return [line_obj, cone_obj]


def _vector_to_quaternion(vector):
    """Helper to compute quaternion for aligning Y-axis with vector."""
    import math

    # Default direction is Y-up [0, 1, 0]
    y_axis = Vector(0, 1, 0)

    # Compute rotation axis (cross product)
    axis = y_axis.cross(vector)

    # Compute rotation angle
    angle = math.acos(max(-1, min(1, y_axis.dot(vector))))

    if axis.length < 1e-10:
        # Vector is parallel or anti-parallel to Y-axis
        if vector.y > 0:
            return (0, 0, 0, 1)  # No rotation
        else:
            return (0, 0, 1, 0)  # 180 degree rotation around Z

    # Normalize axis
    axis = axis.unitized()

    # Convert axis-angle to quaternion
    half_angle = angle / 2
    s = math.sin(half_angle)
    return (axis.x * s, axis.y * s, axis.z * s, math.cos(half_angle))


def plane_to_threejs(plane: Plane, size: float = 1.0, grid: int = 10) -> list[three.Object3D]:
    """Convert a COMPAS plane to PyThreeJS as grid.

    Parameters
    ----------
    plane : :class:`compas.geometry.Plane`
        The plane to convert.
    size : float, optional
        Size of the grid visualization.
    grid : int, optional
        Number of grid lines in each direction.

    Returns
    -------
    list[three.Object3D]
        Grid lines in the plane.

    """
    objects = []

    # Get frame from plane to have xaxis and yaxis
    frame = Frame.from_plane(plane)

    # Create grid lines along xaxis and yaxis directions
    step = size / grid
    half = size / 2

    # Lines parallel to xaxis
    for i in range(grid + 1):
        offset = -half + i * step
        start = frame.point + frame.yaxis * offset - frame.xaxis * half
        end = frame.point + frame.yaxis * offset + frame.xaxis * half
        line = Line(start, end)
        line_geom = line_to_threejs(line)
        line_obj = three.Line(line_geom, three.LineBasicMaterial(color="lightgray"))
        objects.append(line_obj)

    # Lines parallel to yaxis
    for i in range(grid + 1):
        offset = -half + i * step
        start = frame.point + frame.xaxis * offset - frame.yaxis * half
        end = frame.point + frame.xaxis * offset + frame.yaxis * half
        line = Line(start, end)
        line_geom = line_to_threejs(line)
        line_obj = three.Line(line_geom, three.LineBasicMaterial(color="lightgray"))
        objects.append(line_obj)

    return objects


def curve_to_threejs(curve: Curve, resolution: int = 100) -> three.BufferGeometry:
    """Convert a COMPAS curve to PyThreeJS.

    Parameters
    ----------
    curve : :class:`compas.geometry.Curve`
        The curve to convert.
    resolution : int, optional
        Number of points for discretization.

    Returns
    -------
    :class:`three.BufferGeometry`

    """
    polyline = curve.to_polyline(n=resolution)
    vertices = numpy.array(polyline.points, dtype=numpy.float32)
    geometry = three.BufferGeometry(attributes={"position": three.BufferAttribute(vertices, normalized=False)})
    return geometry


def surface_to_threejs(surface: Surface, resolution_u: int = 20, resolution_v: int = 20):
    """Convert a COMPAS surface to PyThreeJS.

    Parameters
    ----------
    surface : :class:`compas.geometry.Surface`
        The surface to convert.
    resolution_u : int, optional
        Number of divisions in U direction.
    resolution_v : int, optional
        Number of divisions in V direction.

    Returns
    -------
    tuple[three.Mesh, three.LineSegments]
        Mesh and edge visualization.

    """
    vertices, faces = surface.to_vertices_and_faces(nu=resolution_u, nv=resolution_v)

    # Create faces
    faces_geom = vertices_and_faces_to_threejs(vertices, faces)
    mesh = three.Mesh(faces_geom, three.MeshBasicMaterial(color="lightblue", side="DoubleSide"))

    # Create edges
    edges = []
    for face in faces:
        n = len(face)
        for i in range(n):
            edge = (face[i], face[(i + 1) % n])
            # Add edge if not duplicate
            if (edge[1], edge[0]) not in edges:
                edges.append(edge)

    edges_geom = vertices_and_edges_to_threejs(vertices, edges)
    lines = three.LineSegments(edges_geom, three.LineBasicMaterial(color="black"))

    return [mesh, lines]


# =============================================================================
# Shapes
# =============================================================================


def box_to_threejs(box: Box) -> three.BoxGeometry:
    """Convert a COMPAS box to PyThreeJS.

    Parameters
    ----------
    box : :class:`compas.geometry.Box`
        The box to convert.

    Returns
    -------
    :class:`three.BoxGeometry`

    Examples
    --------
    >>> from compas.geometry import Box
    >>> box = Box.from_width_height_depth(1, 2, 3)
    >>> box_to_threejs(box)  # doctest: +ELLIPSIS
    BoxGeometry(...)

    """
    return three.BoxGeometry(width=box.width, height=box.height, depth=box.depth)


def cone_to_threejs(cone: Cone) -> three.CylinderGeometry:
    """Convert a COMPAS cone to PyThreeJS.

    Parameters
    ----------
    cone : :class:`compas.geometry.Cone`
        The cone to convert.

    Returns
    -------
    :class:`three.CylinderGeometry`

    Examples
    --------
    >>> from compas.geometry import Cone
    >>> cone = Cone(radius=1, height=2)
    >>> cone_to_threejs(cone)  # doctest: +ELLIPSIS
    CylinderGeometry(...)

    """
    return three.CylinderGeometry(
        radiusTop=0,
        radiusBottom=cone.radius,
        height=cone.height,
        radialSegments=32,
    )


def cylinder_to_threejs(cylinder: Cylinder) -> three.CylinderGeometry:
    """Convert a COMPAS cylinder to PyThreeJS.

    Parameters
    ----------
    cylinder : :class:`compas.geometry.Cylinder`
        The cylinder to convert.

    Returns
    -------
    :class:`three.CylinderGeometry`

    Examples
    --------
    >>> from compas.geometry import Cylinder
    >>> cylinder = Cylinder(radius=1, height=2)
    >>> cylinder_to_threejs(cylinder)  # doctest: +ELLIPSIS
    CylinderGeometry(...)

    """
    return three.CylinderGeometry(
        radiusTop=cylinder.radius,
        radiusBottom=cylinder.radius,
        height=cylinder.height,
        radialSegments=32,
    )


def sphere_to_threejs(sphere: Sphere) -> three.SphereGeometry:
    """Convert a COMPAS sphere to PyThreeJS.

    Parameters
    ----------
    sphere : :class:`compas.geometry.Sphere`
        The sphere to convert.

    Returns
    -------
    :class:`three.SphereGeometry`

    Examples
    --------
    >>> from compas.geometry import Sphere
    >>> sphere = Sphere(radius=1)
    >>> sphere_to_threejs(sphere)  # doctest: +ELLIPSIS
    SphereGeometry(...)

    """
    return three.SphereGeometry(radius=sphere.radius, widthSegments=32, heightSegments=32)


def torus_to_threejs(torus: Torus) -> three.TorusGeometry:
    """Convert a COMPAS torus to a PyThreeJS torus geometry.

    Parameters
    ----------
    torus : :class:`compas.geometry.Torus`
        The torus to convert.

    Returns
    -------
    :class:`three.TorusGeometry`
        The PyThreeJS torus geometry.

    Examples
    --------
    >>> from compas.geometry import Torus
    >>> torus = Torus(radius_axis=1, radius_pipe=0.2)
    >>> torus_to_threejs(torus)  # doctest: +ELLIPSIS
    TorusGeometry(...)

    """
    return three.TorusGeometry(
        radius=torus.radius_axis,
        tube=torus.radius_pipe,
        radialSegments=64,
        tubularSegments=32,
    )


def dot_to_threejs(dot: Dot, fontsize: int = 48, color: str = "white") -> three.Sprite:
    """Convert a COMPAS Dot to PyThreeJS Sprite.

    The sprite maintains constant screen size regardless of zoom level.

    Parameters
    ----------
    dot : :class:`compas_notebook.geometry.Dot`
        The dot to convert.
    fontsize : int, optional
        Font size for the text texture.
    color : str, optional
        Text color.

    Returns
    -------
    :class:`three.Sprite`
        A sprite with text texture positioned at the dot location.

    """
    texture = three.TextTexture(string=dot.text, size=fontsize, color=color, squareTexture=False)
    material = three.SpriteMaterial(map=texture, sizeAttenuation=False, transparent=True)
    sprite = three.Sprite(material=material)
    sprite.position = [dot.point.x, dot.point.y, dot.point.z]
    # scale based on text length - roughly 0.6 width per character
    aspect = len(dot.text) * 0.6
    scale = 0.025
    sprite.scale = [scale * aspect, scale, 1]
    return sprite
