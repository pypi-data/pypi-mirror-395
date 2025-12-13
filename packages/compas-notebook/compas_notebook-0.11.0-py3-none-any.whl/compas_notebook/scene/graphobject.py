import pythreejs as three
from compas.colors import Color
from compas.scene import GraphObject

from compas_notebook.conversions import nodes_and_edges_to_threejs
from compas_notebook.conversions import nodes_to_threejs
from compas_notebook.scene import ThreeSceneObject


class ThreeGraphObject(ThreeSceneObject, GraphObject):
    """Scene object for drawing graph."""

    def __init__(
        self,
        nodesize=0.1,
        nodecolor=Color(0.0, 0.0, 0.0),
        edgecolor=Color(0.2, 0.2, 0.2),
        **kwargs,
    ):
        super().__init__(
            nodesize=nodesize,
            nodecolor=nodecolor,
            edgecolor=edgecolor,
            **kwargs,
        )

    def draw(self):
        """Draw the graph associated with the scene object.

        Returns
        -------
        list[three.LineSegments, three.Points]
            List of pythreejs objects created.

        """
        guids = []

        nodes, edges = self.graph.to_nodes_and_edges()

        if self.show_nodes:
            if self.show_nodes is not True:
                nodes = self.show_nodes

            geometry = nodes_to_threejs(nodes)
            points = three.Points(geometry, three.PointsMaterial(size=self.nodesize, color=self.contrastcolor.hex))
            guids.append(points)

        if self.show_edges:
            if self.show_edges is not True:
                edges = self.show_edges

            geometry = nodes_and_edges_to_threejs(nodes, edges)
            line = three.LineSegments(geometry, three.LineBasicMaterial(color=self.contrastcolor.hex))
            guids.append(line)

        self._guids = guids
        return self.guids
