from abc import ABC, abstractmethod
import Arc as arc

class Node(ABC):
    def __init__(self, Id ):
        self.Id = Id
        self.sourceArcs = [] 
        self.targetArcs= []
    
    @abstractmethod
    def getSourceArcs(self):
        return self.sourceArcs
    
    @abstractmethod
    def getTargetArcs(self):
        return self.targetArcs

    @abstractmethod
    def setSourceArc(self, source: arc.Arc):
        self.sourceArcs.append(source)
    
    @abstractmethod
    def setTargetArc(self, target: arc.Arc):
        self.targetArcs.append(target)
    
    @abstractmethod
    def getId(self):
        return self.Id
