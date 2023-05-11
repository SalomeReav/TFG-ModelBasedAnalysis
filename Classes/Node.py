from abc import ABC, abstractmethod
import Arc as arc

class Node(ABC):
    def __init__(self, Id ):
        self.Id = Id
        self.sourceNodes = [] 
        self.targetNodes= []
    
    @abstractmethod
    def getSourceArcs(self):
        return self.sourceNodes
    
    @abstractmethod
    def getTargetArcs(self):
        return self.targetNodes

    @abstractmethod
    def setSourceArc(self, source: arc.Arc):
        self.sourceNodes.append(source)
    
    @abstractmethod
    def setTargetArc(self, target: arc.Arc):
        self.targetNodes.append(target)
