# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

import unittest
from typing import List, Set, Dict, Any
#
# A set of data structures to represent graphs
#

##Immutable ADT
class Node(object):
    """Represents a node in the graph"""
    def __init__(self, name: str) -> None:
        self.name: str = str(name)

    def get_name(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Node):
            return False
        return self.name == other.name

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        # This function is necessary so that Nodes can be used as
        # keys in a dictionary, even though Nodes are mutable
        return self.name.__hash__()

##Immutable
##Keep note of dynamic binding, ie, deleting a node should delete an edge
class Edge(object):
    """Represents an edge in the dictionary. Includes a source and
    a destination."""
    def __init__(self, src: Node, dest: Node) -> None:
        self.src: Node = src
        self.dest: Node = dest

    def get_source(self) -> Node:
        return self.src

    def get_destination(self) -> Node:
        return self.dest

    def __str__(self) -> str:
        return '{}->{}'.format(self.src, self.dest)


class WeightedEdge(Edge):
    def __init__(self, 
                 src: Node, 
                 dest: Node, 
                 total_distance: int, 
                 outdoor_distance: int) -> None:
        Edge.__init__(self, src, dest)
        self.total_distance: int = total_distance
        self.outdoor_distance: int = outdoor_distance

        #self._check_rep()
        
    def _check_rep(self) -> None:
        assert self.total_distance >= self.outdoor_distance

    def get_total_distance(self) -> int:
        return self.total_distance
    
    def get_outdoor_distance(self) -> int:
        return self.outdoor_distance

    def __str__(self) -> str:
        return Edge.__str__(self) +\
               ' ({}, {})'.format(self.total_distance, self.outdoor_distance)

#Uses Adjacency List representation
class Digraph(object):
    """Represents a directed graph of Node and Edge objects"""
    def __init__(self) -> None:
        self.nodes: Set[Node] = set([])
        self.edges: Dict[Node, List[Edge]] = {}

    def __str__(self) -> str:
        edge_strings: List[str] = []
        for edges in self.edges.values():
            for edge in edges:
                edge_strings.append(str(edge))
        edge_strings = sorted(edge_strings)  # sort alphabetically
        return '\n'.join(edge_strings)  # concat edge_strs with "\n"s between them

    def get_edges_for_node(self, node: Node) -> List[Edge]:
        return self.edges[node]

    def has_node(self, node: Node) -> bool:
        return node in self.nodes

    def add_node(self, node: Node) -> None:
        """Adds a Node object to the Digraph. Raises a ValueError if it is
        already in the graph."""

        if self.has_node(node):
            raise ValueError("Node already in graph")
        
        self.nodes.add(node)
        self.edges[node] = []

    def add_edge(self, edge: Edge) -> None:
        """Adds an Edge or WeightedEdge instance to the Digraph. Raises a
        ValueError if either of the nodes associated with the edge is not
        in the  graph."""
        source: Node = edge.get_source()
        dest: Node = edge.get_destination()
        
        if not (self.has_node(source) and self.has_node(dest)):
            raise ValueError("Either or both of the nodes are not in this graph")

        self.edges[source].append(edge)


# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class TestGraph(unittest.TestCase):

    def setUp(self):
        self.g: Digraph = Digraph()
        self.na: Node = Node('a')
        self.nb: Node = Node('b')
        self.nc: Node = Node('c')
        self.g.add_node(self.na)
        self.g.add_node(self.nb)
        self.g.add_node(self.nc)
        self.e1: WeightedEdge = WeightedEdge(self.na, self.nb, 15, 10)
        self.e2: WeightedEdge = WeightedEdge(self.na, self.nc, 14, 6)
        self.e3: WeightedEdge = WeightedEdge(self.nb, self.nc, 3, 1)
        self.g.add_edge(self.e1)
        self.g.add_edge(self.e2)
        self.g.add_edge(self.e3)

    def test_weighted_edge_str(self):
        self.assertEqual(str(self.e1), "a->b (15, 10)")
        self.assertEqual(str(self.e2), "a->c (14, 6)")
        self.assertEqual(str(self.e3), "b->c (3, 1)")

    def test_weighted_edge_total_distance(self):
        self.assertEqual(self.e1.get_total_distance(), 15)
        self.assertEqual(self.e2.get_total_distance(), 14)
        self.assertEqual(self.e3.get_total_distance(), 3)

    def test_weighted_edge_outdoor_distance(self):
        self.assertEqual(self.e1.get_outdoor_distance(), 10)
        self.assertEqual(self.e2.get_outdoor_distance(), 6)
        self.assertEqual(self.e3.get_outdoor_distance(), 1)

    def test_add_edge_to_nonexistent_node_raises(self):
        node_not_in_graph: Node = Node('q')
        no_src: WeightedEdge = WeightedEdge(self.nb, node_not_in_graph, 5, 5)
        no_dest: WeightedEdge = WeightedEdge(node_not_in_graph, self.na, 5, 5)

        with self.assertRaises(ValueError):
            self.g.add_edge(no_src)
        with self.assertRaises(ValueError):
            self.g.add_edge(no_dest)

    def test_add_existing_node_raises(self):
        with self.assertRaises(ValueError):
            self.g.add_node(self.na)

    def test_graph_str(self):
        expected = "a->b (15, 10)\na->c (14, 6)\nb->c (3, 1)"
        self.assertEqual(str(self.g), expected)


if __name__ == "__main__":
    unittest.main()
