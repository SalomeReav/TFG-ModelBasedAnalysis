from Node import Node


class Transition(Node):
    ''' Define a transition node in the graph with it ID'''
    def __init__(self,Id):
        super().__init__(Id)
    
    
    def getIsTimed(self):
        ''' Return if the Transition its timed'''
        return self.isTimed
    
    def setIsTimed(self, isTimed : bool):
        ''' Set if the Transition its timed'''
        self.isTimed = isTimed

    def getSourceArcs(self):
        ''' Return source arcs of the transition '''
        return self.sourceArcs

    def getTargetArcs(self):
        ''' Return target arcs of the transition '''
        return self.targetArcs

    def setSourceArc(self, source):
        ''' Add a source arc to the transition '''
        self.sourceArcs.append(source)
    
   
    def setTargetArc(self, target):
        ''' Add a target arc to the transition '''
        self.targetArcs.append(target)
    
    def getId(self):
        ''' Return the transition id '''
        return self.Id