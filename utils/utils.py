from collections import deque
from inspect import currentframe, getframeinfo
import copy

import time

current_milli_time = lambda: int(round(time.time() * 1000))

class Utils:
    @staticmethod
    def createArray_internal(dimensions: list, index: int, root, defaultVal = None):
        if index >= len(dimensions):
            return
        if root is None:
            assert(False)
        items = dimensions[index]
        isLastDimension = (len(dimensions) - 1) == index
        for i in range(items):
            value = None
            if not isLastDimension:
                value = []
            else:
                if defaultVal is not None:
                    value = copy.deepcopy(defaultVal)
            root.append(value)
            Utils.createArray_internal(dimensions, index + 1, value, defaultVal)
        return root

    @staticmethod
    def createArray(dimensions: list, defaultVal = None):
        return Utils.createArray_internal(dimensions, 0, [], defaultVal)

    @staticmethod
    def getValue(arr: list, indices: list):
        cur = arr
        for i in indices:
            cur = cur[i]
        return cur

    @staticmethod
    def updateValue(arr: list, indices: list, value):
        """
        apply the value to all the remaining dimensions
        for example indices = [3, 2]
        if arr[3][2] is a not list, then set value as it values
        if arr[3][2] is list, and have more remaining dimensions, set value as the values of all the remaining dimensions
        :param arr:
        :param indices:
        :param value:
        :return:
        """
        cur = arr
        i = len(indices) - 1
        for j in range(len(indices)):
            if j == i:
                if type(cur[indices[j]]) is list:
                    Utils.updateSlot(cur[indices[j]], value)
                else:
                    cur[indices[j]] = value
            else:
                cur = cur[indices[j]]

    @staticmethod
    def updateSlot(slot: list, value):
        for i in range(len(slot)):
            if type(slot[i]) is list:
                Utils.updateSlot(slot[i], value)
            else:
               slot[i] = value

    @staticmethod
    def dumpMatrix(m, rows, columns, fn=lambda a: a):
        for i in range(0, rows):
            for j in range(0, columns):
                value = fn(m[rows - 1 - i][j])
                if value is None:
                    value = "-"
                print("%5s" % value, end="")
            print("")


class Node:
    def __init__(self, nodeName: str):
        self.name = nodeName
        self.inflowEdges: dict = dict()
        self.outflowEdges: dict = dict()
        self.visited: bool = False
        self.topoOrderVal: int = None
        self.numScc: int = None
        self.predecessor: Node = None
        self.dist: int = None

    def addInflowEdge(self, inflowNodeName: str, edgeLength: int):
        """
        only keep the shorted edge from the same node
        :param inflowNodeName:
        :param edgeLength:
        :return:
        """
        existingEdgeLen = self.inflowEdges.get(inflowNodeName)
        if existingEdgeLen is not None:
            if existingEdgeLen < edgeLength:
                return
        self.inflowEdges[inflowNodeName] = edgeLength

    def addOutflowEdge(self, outflowNodeName: str, edgeLength: int):
        existingEdgeLen = self.outflowEdges.get(outflowNodeName)
        if existingEdgeLen is not None:
            if existingEdgeLen < edgeLength:
                return
        self.outflowEdges[outflowNodeName] = edgeLength

class Edge:
    def __init__(self, srcNodeName: str, targetNodeName: str, edgeLength: int):
        self.srcNodeName = srcNodeName
        self.targetNodeName = targetNodeName
        self.edgeLength = edgeLength


class Graph:
    def __init__(self, edges: list):
        self.nodes = dict()
        for edge in edges:
            targetNode = self.nodes.get(edge.targetNodeName)
            if targetNode is None:
                targetNode = Node(edge.targetNodeName)
                self.nodes[edge.targetNodeName] = targetNode
            targetNode.addInflowEdge(edge.srcNodeName, edge.edgeLength)

            srcNode = self.nodes.get(edge.srcNodeName)
            if srcNode is None:
                srcNode = Node(edge.srcNodeName)
                self.nodes[edge.srcNodeName] = srcNode
            srcNode.addOutflowEdge(edge.targetNodeName, edge.edgeLength)


class Solution:
    def __init__(self, length, inflowNodeName):
        self.length = length
        self.inflowNodeName = inflowNodeName


class Path:
    def __init__(self):
        self.length = 0
        self.path = deque()


def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno
