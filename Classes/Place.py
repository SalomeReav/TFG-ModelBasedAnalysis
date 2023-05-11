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
        return self.sourceNodes

    def getTargetArcs(self):
        return self.targetNodes

    def setSourceArc(self, source):
        self.sourceNodes.append(source)
    
   
    def setTargetArc(self, target):
        self.targetNodes.append(target)
