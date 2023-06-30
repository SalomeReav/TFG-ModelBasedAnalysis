from Node import Node

class Place(Node):
    def __init__(self, name, Id):
        super().__init__( Id)
        self.nameValue = name
        self.initialMarking = None
    
    def getInitialMarking(self):
        return self.initialMarking
    
    def setInitialMarking(self, mark: int):
        self.initialMarking = mark
    
    def getSourceArcs(self):
        return self.sourceArcs

    def getTargetArcs(self):
        return self.targetArcs

    def setSourceArc(self, source):
        self.sourceArcs.append(source)
    
   
    def setTargetArc(self, target):
        self.targetArcs.append(target)
    
    def getId(self):
        return self.Id
