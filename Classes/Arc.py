

class Arc():
    ''' 
    Represents an arc in a graph with a value, source node and target node
    '''
    def __init__(self, value: int ):
        ''' Initialize an Arc with a value'''
        self.value = value
        self.targetNode = None
        self.sourceNode = None

    

    def getTargetNode(self):
        '''Return the target node of the arc'''
        return self.targetNode
    

    def getsourceNode(self):
        '''Return the source node of the arc'''
        return self.sourceNode
    
    def setTargetNode(self, target):
        '''Set the target node of the arc'''
        self.targetNode = target
    
    def setSourceNode(self, source):
        '''Set the source node of the arc'''
        self.sourceNode = source 
