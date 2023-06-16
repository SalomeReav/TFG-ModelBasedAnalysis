from Node import Node


class Transition(Node):
    def __init__(self,Id):
        super().__init__(Id)
    
    
    def getIsTimed(self):
        return self.isTimed
    
    def setIsTimed(self, isTimed : bool):
        self.isTimed = isTimed

    def getSourceArcs(self):
        return self.sourceNodes

    def getTargetArcs(self):
        return self.targetNodes

    def setSourceArc(self, source):
        self.sourceNodes.append(source)
    
   
    def setTargetArc(self, target):
        self.targetNodes.append(target)
    
    def getId(self):
        return self.Id