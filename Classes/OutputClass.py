from abc import ABC, abstractmethod

class Output(ABC):
    @abstractmethod
    def createOutputTransition():
        pass
    
    @abstractmethod
    def createOutputPlace():
        pass 
    
    @abstractmethod
    def createOutputArc():
        pass

class OutputPNML(Output):
    #falta implementación 
    def createOutputTransition():
        pass
    
    def createOutputPlace():
        pass

    def createOutputArc():
        pass