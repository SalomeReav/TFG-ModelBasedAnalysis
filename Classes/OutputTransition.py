from abc import ABC, abstractmethod
from TransitionClass import Transition

class OutputTransition(ABC):
    def __init__(self) -> None:
        ''' super initialization here ??? '''
        super().__init__()

    @abstractmethod
    def toStringTransition():
        #recieves a Transition class and then transform into a string 
        pass 



class TransitionPNML(OutputTransition):
    def __init__(self, transition: Transition):
        super().__init__()
        self.transition = transition