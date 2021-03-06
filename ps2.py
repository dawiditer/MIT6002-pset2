# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from typing import List, Tuple, Optional, Set, cast
from graph import Digraph, Node, WeightedEdge, Edge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
# - Nodes represent the buidlings
# - Edges represent the connection between two buildings
# - Distances are represented as the weights of the edges
#   as the tuple (total distance, distance outdoors)
#


# Problem 2b: Implementing load_map
def load_map(map_filename) -> Digraph:
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """
    mit_map: Digraph = Digraph()
    
    with open(map_filename) as f:
        for line in f:
            edge_details: List[str] = line.split(" ")

            src: Node = Node(edge_details[0])
            dest: Node = Node(edge_details[1])
            total_distance: int = int(edge_details[2])
            outdoor_distance: int = int(edge_details[3])
            
            edge: WeightedEdge = WeightedEdge(src,
                                              dest, 
                                              total_distance, 
                                              outdoor_distance)

            if not mit_map.has_node(src):
                mit_map.add_node(src)
            if not mit_map.has_node(dest):
                mit_map.add_node(dest)
                
            mit_map.add_edge(edge)

    print("Loading map from file...")
    return mit_map
    
# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
##def test_load_map():
##    test_map = load_map("test_load_map.txt")
##        
##    assert test_map
##    print(test_map)
##    
##test_load_map()


#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
# - Objective Function: Minimize the total distance travelled between
#   2 buildings
# - Constraint: Total outdoor distance travelled
#   should be less than or equal to the specified value
#

def printPath(path: List[Node]) -> str:
    """Assumes path is a list of nodes"""
    result: str = ''
    for i in range(len(path)):
        result = result + str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result

#TODO: Follow the spec
    
# Problem 3b: Implement get_best_path
def get_best_path(digraph: Digraph, 
                  start: str, 
                  end: str, 
#                  path: List[List[str], int, int], #this is what was suppposed to be
                  path: List[str],
                  max_dist_outdoors: int, 
                  total_dist: int = 0, 
                  best_dist: int = 0,
                  best_path: List[str] = []
                  ) -> Optional[Tuple[List[str], int]]:
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        total_dist: int
            Total distance travelled by a single path.
            If path == best_path then total_dist == best_dist
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    startNode: Node = Node(start)
    endNode: Node = Node(end)
    
    if not (digraph.has_node(startNode) and digraph.has_node(endNode)):
        raise ValueError("Invalid start and/or end nodes")

    path = path + [start]
    if start == end:
        return path, total_dist

    #To be considered
##    if max_dist_outdoors <= 0:
##        return None
    
    if max_dist_outdoors >= 0:
        for edge in digraph.get_edges_for_node(startNode):
            w_edge = cast(WeightedEdge, edge)
            child_node: Node = w_edge.get_destination()
            child = child_node.get_name()
            outdoor_dist: int = w_edge.get_outdoor_distance()
            dist_travelled: int = w_edge.get_total_distance()
            
            if (child not in path and outdoor_dist <= max_dist_outdoors):
                if best_dist == 0 or (total_dist < best_dist and len(path) <= len(best_path)):
                    #This evaluates to the best path. Only enter here for the best
                    #path
                    newPathDist = get_best_path(digraph, child, end, path,
                                                max_dist_outdoors - outdoor_dist,
                                                total_dist + dist_travelled,
                                                best_dist, best_path)

                    if newPathDist != None:
                        newPathDist = cast(Tuple[List[str], int], newPathDist)
                        if (best_dist and newPathDist[1] < best_dist) or not best_dist:
                            best_path, best_dist = newPathDist


    return None if not best_path else (best_path, best_dist)



                   

# Problem 3c: Implement directed_dfs
def directed_dfs(digraph: Digraph, 
                 start: str, 
                 end: str, 
                 max_total_dist: int, 
                 max_dist_outdoors: int) -> Optional[List[str]]:
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    try:
        result: Optional[Tuple[List[str], int]] = get_best_path(digraph, 
                                                      start, 
                                                      end, 
                                                      [],
                                                      max_dist_outdoors,
                                                      0, 0, [])
        best_path = cast(Tuple[List[str], int], result)
        
        shortest_path: List[str]
        dist_travelled: int
        
        shortest_path, dist_travelled = best_path
        
        if dist_travelled > max_total_dist:
            raise ValueError
        
        return shortest_path
    except TypeError:
        raise ValueError




def directed_cyclic_bfs(digraph: Digraph, 
                        start: str, 
                        end: str, 
                        max_total_dist: int, 
                        max_dist_outdoors: int) -> Optional[List[str]]:
    #([path], total_path_distance, total_path_outdoor_distance)
    initPath: Tuple[List[str], int, int] = ([start], 0, 0)#Caution: 0 is a dangerous integer to work with
    queue: List[Tuple[List[str], int, int]] = [initPath]
    bestDist: int = 0
    bestPath: Optional[List[str]] = None
    
    while len(queue) != 0:
        pathDetails: Tuple[List[str], int, int] = queue.pop(0)
        
        currentPath: List[str]
        totalPathDist: int
        totalOutdoorDist: int
        
        currentPath, totalPathDist, totalOutdoorDist = pathDetails
        lastNode: Node = Node(currentPath[-1])
##        print("current path:", printPath(currentPath))
        
        #if the length of the currentPath is greater than the best path
        #it means the search went down one level, so no need to keep searching
        if bestPath and len(bestPath) < len(currentPath):
            break
        
        if totalPathDist > max_total_dist or totalOutdoorDist > max_dist_outdoors:
            continue
        
        if lastNode.get_name() == end:#shortest path not necessarily best path, ie has to be shortest and best dist
            if not bestDist or totalPathDist < bestDist:#set once or change if found better
                bestDist = totalPathDist
                bestPath = currentPath[:]
##                print("found")  
                #we continue the search along the same level/generation
                #because the next path might contain a shorter distance
                
        #continue DOWN the search only if we havent found the bestPath
        if not bestPath: 
            for edge in digraph.get_edges_for_node(lastNode):
                w_edge = cast(WeightedEdge, edge)
                childNode: Node = w_edge.get_destination()
                newPath: List[str] = currentPath + [childNode.get_name()]
                newPathDist: int = totalPathDist + w_edge.get_total_distance()
                newOutDist: int = totalOutdoorDist + w_edge.get_outdoor_distance()

                newPathDetails: Tuple[List[str], int, int] = \
                        (newPath, newPathDist, newOutDist)
                        
                if childNode not in currentPath:#if kid points back a generation, discard
                    if newPathDist <= max_total_dist and \
                       newOutDist <= max_dist_outdoors:
                        queue.append(newPathDetails)
    return bestPath



# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST: int = 99999

    def setUp(self) -> None:
        self.graph: Digraph = load_map("mit_map.txt")

    def test_load_map_basic(self) -> None:
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges: List[Edge] = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        set_all_edges: Set[Edge] = set(all_edges)
        self.assertEqual(len(set_all_edges), 129)

    def _print_path_description(self, 
                                start: str, 
                                end: str, 
                                total_dist: int, 
                                outdoor_dist: int):
        constraint: str = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath: List[str],
                   total_dist: int = LARGE_DIST,
                   outdoor_dist: int = LARGE_DIST) -> None:
        start: str
        end: str
        
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start: str,
                              end: str,
                              total_dist: int = LARGE_DIST,
                              outdoor_dist: int = LARGE_DIST) -> None:
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self) -> None:
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self) -> None:
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self) -> None:
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self) -> None:
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self) -> None:
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self) -> None:
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self) -> None:
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self) -> None:
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
##    digraph = load_map("sample.txt")
    digraph: Digraph = load_map("mit_map.txt")
    unittest.main()
#    
#    start: Node = Node("1")
#    end: Node = Node("32")
#    best_path_bfs: List[str] = directed_cyclic_bfs(digraph, start, end, 99999, 99999)
#    best_path_dfs: List[str] = directed_dfs(digraph, start, end, 99999, 99999)
#    print("Best Path by BFS:", best_path_bfs)
#    print("Best Path by DFS:", best_path_dfs)
##    print()
