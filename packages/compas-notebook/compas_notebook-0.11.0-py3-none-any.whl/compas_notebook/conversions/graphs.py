import numpy
import pythreejs as three


def nodes_and_edges_to_threejs(nodes, edges) -> three.BufferGeometry:
    """Convert nodes and edges to a PyThreeJS geometry.

    Parameters
    ----------
    nodes : list
        List of nodes.
    edges : list
        List of edges.

    Returns
    -------
    :class:`three.BufferGeometry`
        The PyThreeJS geometry.

    """
    nodes = numpy.array(nodes, dtype=numpy.float32)
    edges = numpy.array(edges, dtype=numpy.uint32).ravel()

    geometry = three.BufferGeometry(
        attributes={
            "position": three.BufferAttribute(nodes, normalized=False),
            "index": three.BufferAttribute(edges, normalized=False, itemSize=2),
        }
    )

    return geometry


def nodes_to_threejs(nodes) -> three.BufferGeometry:
    """Convert nodes to a PyThreeJS geometry.

    Parameters
    ----------
    nodes : list
        List of nodes.

    Returns
    -------
    :class:`three.BufferGeometry`
        The PyThreeJS geometry.

    """
    nodes = numpy.array(nodes, dtype=numpy.float32)
    geometry = three.BufferGeometry(attributes={"position": three.BufferAttribute(nodes, normalized=False)})
    return geometry
