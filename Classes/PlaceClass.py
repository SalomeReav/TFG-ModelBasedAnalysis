from NodeClass import Node

class Place(Node):
    def __init__(self, name):
        super().__init__()
        self.nameValue = name
        self.initialMarking = None
    
    def getInitialMarking(self):
        return self.initialMarking
    
    def setInitialMarking(self, mark: int):
        self.initialMarking = mark