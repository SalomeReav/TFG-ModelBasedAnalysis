from abc import ABC, abstractmethod

class OutputFormat(ABC):
    def __init__(self):
        pass
    '''Interface that returns xml for each type of petri net component'''
    @abstractmethod
    def createTransition(self):
        pass
    
    @abstractmethod
    def createPlace(self):
        pass 
#rr    
    @abstractmethod
    def createArc(self):
        pass

