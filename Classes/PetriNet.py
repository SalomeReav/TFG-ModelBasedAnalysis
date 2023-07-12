from abc import ABC, abstractmethod
from OutputPnml import OutputPNML
from Place import Place
from Transition import Transition
import xml.etree.ElementTree as ET
import Node



class PetriNet:
    def __init__(self):
        self.nodes = []
        self.arcs = []
    
    def writeOuput(self,root):
        output = OutputPNML()
    
        for arcs in self.arcs:
            output.writeArc(arcs,root)
        for node in self.nodes:
            if isinstance(node,Place):
                output.writePlace(node,root)
            if isinstance(node,Transition):
                output.writeTransition(node,root)
        
        ET.indent(root)
        et=ET.ElementTree(root)
        et.write("ficheroPrueba", xml_declaration=True)







