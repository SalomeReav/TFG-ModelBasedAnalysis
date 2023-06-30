from Node import Node


class Transition(Node):
    def __init__(self,Id):
        super().__init__(Id)
    
    
    def getIsTimed(self):
        return self.isTimed
    
    def setIsTimed(self, isTimed : bool):
        self.isTimed = isTimed

    def getSourceArcs(self):
        return self.sourceArcs

    def getTargetArcs(self):
        return self.targetArcs

    def setSourceArc(self, source):
        self.targetArcs.append(source)
    
   
    def setTargetArc(self, target):
        self.targetArcs.append(target)
    
    def getId(self):
        return self.Id