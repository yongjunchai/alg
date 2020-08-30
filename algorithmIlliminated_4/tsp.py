import sys
from utils.utils import *


class TSP:
    def __init__(self, graph: Graph):
        # edges of the shortest tour
        self.edges = dict()
        self.tourLength = sys.maxsize
        self.graph = graph
        self.totalTours = 0

    def solve(self, start: str):
        startNode: Node = self.graph.nodes.get(start)
        edges: dict = startNode.outflowEdges
        nodesVisited = set()
        edgesVisited = dict()
        nodesVisited.add(start)
        for name, length in edges.items():
            target = self.graph.nodes.get(name)
            nodesVisited.add(target.name)
            edge = Edge(start, name, length)
            edgesVisited[edge.getEdgeKey()] = edge
            self.travel(start, target, nodesVisited, edgesVisited)
            nodesVisited.remove(target.name)
            edgesVisited.pop(edge.getEdgeKey())
        assert len(edgesVisited) == 0
        assert len(nodesVisited) == 1

    def dumpTour(self, edges: list):
        print("[%d] tour length: %d" % (self.totalTours, self.calculateEdgesLength(edges)))
        for edge in edges:
            print(edge.srcNodeName + " --> " + edge.targetNodeName + "  :  " + str(edge.edgeLength))

    def calculateEdgesLength(self, edges: list):
        totalLength = 0
        for edge in edges:
            totalLength += edge.edgeLength
        return totalLength

    def travel(self, start: str, curNode: Node, nodesVisited: set, edgesVisited: dict):
        # if all nodes visited, then the tour is done
        # check whether the current tour is the shortest tour
        if len(nodesVisited) == len(self.graph.nodes):
            for name, length in curNode.outflowEdges.items():
                if name == start:
                    edge = Edge(curNode.name, start, length)
                    edgesVisited[edge.getEdgeKey()] = edge
                    totalLength = self.calculateEdgesLength(edgesVisited.values())
                    if totalLength < self.tourLength:
                        self.tourLength = totalLength
                        self.edges = copy.deepcopy(edgesVisited)
                    self.totalTours += 1
                    self.dumpTour(edgesVisited.values())
                    edgesVisited.pop(edge.getEdgeKey())
                    return
            assert False
            return

        edges: dict = curNode.outflowEdges
        for name, length in edges.items():
            if name in nodesVisited:
                continue
            targetNode = self.graph.nodes.get(name)
            nodesVisited.add(name)
            edge = Edge(curNode.name, name, length)
            edgesVisited[edge.getEdgeKey()] = edge
            self.travel(start, targetNode, nodesVisited, edgesVisited)
            nodesVisited.remove(targetNode.name)
            edgesVisited.pop(edge.getEdgeKey())


