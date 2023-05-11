from Node import Node


class Transition(Node):
    def __init__(self, is_timed: bool, Id):
        super().__init__(self,Id)
        self.isTimed = is_timed
    
    def getIsTimed(self):
        return self.isTimed
    
    def setIsTimed(self, isTimed : bool):
        self.isTimed = isTimed