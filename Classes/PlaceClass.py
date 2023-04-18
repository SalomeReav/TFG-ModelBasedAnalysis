from NodeClass import Node

class Place(Node):
    def __init__(self):
        super().__init__()
        self.nameValue = None
        self.initialMarking = None
        self.outputPlace = None
    
    def getInitialMarking(self, mark: int):
        return self.initialMarking
    
    def addInitialMarking(self, mark: int):
        self.initialMarking = mark