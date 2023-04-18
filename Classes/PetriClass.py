from abc import ABC, abstractmethod
from NodeClass import Node
from ArcClass import Arc
#separara cada clase en su propio fichero, poner la misma notacion y cuando revibe alguna clase especificalro
class PetriNet:
    def __init__(self):
        self.nodes = []
        self.arcs = []
    
    def addNode(self, node: Node):
        self.nodes.append(node)
    
    def addArc(self, arc: Arc):
        self.arcs.append(arc)










