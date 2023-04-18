from abc import ABC, abstractmethod
from PlaceClass import Place


class OutputPlace(ABC):

    @abstractmethod
    def toStringPlace():
        pass 



class PlacePNML(OutputPlace):
    def __init__(self, place: Place):
        super().__init__()
        self.place = place
    

