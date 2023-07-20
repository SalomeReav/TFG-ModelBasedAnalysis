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
        n = ET.SubElement(root,"net")
        for node in self.nodes:
            if isinstance(node,Place):
                output.writePlace(node,n)
            if isinstance(node,Transition):
                output.writeTransition(node,n)
        
        for arcs in self.arcs:
            output.writeArc(arcs,n)
        
        ET.indent(root)
        et=ET.ElementTree(root)
        et.write("ficheroPrueba.xml", xml_declaration=True, encoding= "UTF-8")







