from abc import ABC, abstractmethod


class OutputArc(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def writeArc():
        pass 

class ArcPNML(OutputArc):
    def __init__(self, arc):
        self.arc = arc