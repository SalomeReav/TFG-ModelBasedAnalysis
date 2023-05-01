from NodeClass import Node


class Transition(Node):
    def __init__(self, is_timed: bool):
        super().__init__()
        self.isTimed = is_timed
    
    def getIsTimed(self):
        return self.isTimed
    
    def setIsTimed(self, isTimed : bool):
        self.isTimed = isTimed