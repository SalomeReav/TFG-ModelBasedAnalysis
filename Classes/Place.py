from Node import Node

class Place(Node):
    ''' Define a Place object with its value and mark '''
    def __init__(self, name, Id):
        super().__init__( Id)
        self.nameValue = name
        self.initialMarking = None
    
    def getInitialMarking(self):
        ''' Return the mark of the place node '''
        return self.initialMarking
    
    def setInitialMarking(self, mark: int):
        ''' Set the mark in the pace node '''
        self.initialMarking = mark
    
    def getSourceArcs(self):
        ''' Return the source arcs of the place node '''
        return self.sourceArcs

    def getTargetArcs(self):
        ''' Return the target arcs of the place node '''
        return self.targetArcs

    def setSourceArc(self, source):
        ''' Set the source arc of the place node '''
        self.sourceArcs.append(source)
    
   
    def setTargetArc(self, target):
        ''' Set the target arc of the place node '''
        self.targetArcs.append(target)
    
    def getId(self):
        ''' Return place node id '''
        return self.Id
