from abc import ABC, abstractmethod
import Arc as arc

class Node(ABC):
    ''' Represents a Node with it ID, source arcs and target arcs'''
    def __init__(self, Id ):
        self.Id = Id
        self.sourceArcs = [] 
        self.targetArcs= []
    
    @abstractmethod
    def getSourceArcs(self):
        '''Return source arcs'''
        return self.sourceArcs
    
    @abstractmethod
    def getTargetArcs(self):
        '''Return target arcs'''
        return self.targetArcs

    @abstractmethod
    def setSourceArc(self, source: arc.Arc):
        '''Append to the list of source arcs a Node'''
        self.sourceArcs.append(source)
    
    @abstractmethod
    def setTargetArc(self, target: arc.Arc):
        '''Append to the list of target arcs a Node'''
        self.targetArcs.append(target)
    
    @abstractmethod
    def getId(self):
        '''Return the ID of the Node'''
        return self.Id
