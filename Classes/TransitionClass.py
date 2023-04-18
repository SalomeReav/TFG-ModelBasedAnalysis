from NodeClass import Node


class Transition(Node):
    def __init__(self, is_timed=False):
        super().__init__()
        self.isTimed = is_timed
        self.outputTransition = None
    
    def getIsTimed(self):
        return self.is_timed
    
    def addIsTimed(self, isTimed : bool):
        self.isTimed = isTimed