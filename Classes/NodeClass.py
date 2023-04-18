from abc import ABC, abstractmethod
from ArcClass import Arc 
from NodeClass import Node

class Node(ABC):
    def __init__(self):
        self.ID = None
        self.sourceNodes = [] 
        self.targetNodes= []
    
    @abstractmethod
    def getSourceArcs(self):
        return self.sourceNodes
    
    @abstractmethod
    def getTargetArcs(self):
        return self.targetNodes

    @abstractmethod
    def addSourceArc(self, source: Node):
        self.sourceNodes.append(source)
    
    @abstractmethod
    def addTargetArc(self, target: Node):
        self.targetNodes.append(target)