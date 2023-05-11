from abc import ABC, abstractmethod

class OutputFormat(ABC):
    '''Interface that returns xml for each type of petri net component'''
    @abstractmethod
    def writeTransition(self):
        pass
    
    @abstractmethod
    def writePlace(self,place):
        pass 
#rr    
    @abstractmethod
    def writeArc(self):
        pass

