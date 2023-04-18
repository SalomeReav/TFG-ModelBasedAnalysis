from abc import ABC, abstractmethod
from NodeClass import Node

class Arc():
    def __init__(self):
        self.value = None
        self.targetNode = Node
        self.sourceNode = Node
        self.OutputArc = None
    

    def getTargetNode(self):
        return self.targetNode
    

    def getsourceNode(self):
        return self.sourceNode
    
    def addTargetNode(self, target:Node):
        self.targetNode = target
    
    def addSourceNode(self, source: Node):
        self.sourceNode = source 