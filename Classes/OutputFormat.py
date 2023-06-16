from abc import ABC, abstractmethod

class OutputFormat(ABC):
    '''Interface that returns xml for each type of petri net component'''
    @abstractmethod
    def writeTransition(self,transition,root):
        pass
    
    @abstractmethod
    def writePlace(self,place,root):
        pass 
        
    @abstractmethod
    def writeArc(self,arc,root):
        pass

