from abc import ABC, abstractmethod

class OutputFormat(ABC):
    '''This class define an interface for writting transitions, places
        and arcs in a specific format
    '''
    @abstractmethod
    def writeTransition(self,transition,root):
        '''Write a transitoin to the output format'''
        pass
    
    @abstractmethod
    def writePlace(self,place,root):
        '''Write a place to the output format'''
        pass 
        
    @abstractmethod
    def writeArc(self,arc,root):
        '''Write an arc to the output format'''
        pass

