

class Arc():
    def __init__(self, value: int ):
        self.value = value
        self.targetNode = None
        self.sourceNode = None

    

    def getTargetNode(self):
        return self.targetNode
    

    def getsourceNode(self):
        return self.sourceNode
    
    def setTargetNode(self, target:Node):
        self.targetNode = target
    
    def setSourceNode(self, source: Node):
        self.sourceNode = source 
