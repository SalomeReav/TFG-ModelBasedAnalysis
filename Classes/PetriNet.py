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
        token = ET.SubElement(n,"token")
        token.set("id", "Default")
        token.set("red", "0")
        token.set("green", "0")
        token.set("blue", "0")
        
        for node in self.nodes:
            if isinstance(node,Place):
                output.writePlace(node,n)
            if isinstance(node,Transition):
                output.writeTransition(node,n)
        
        for arcs in self.arcs:
            output.writeArc(arcs,n)
        
        ET.indent(root,level= 2 )
        et=ET.ElementTree(root)
        
        newName = 'ficheroPruebaNuevo.pnml'
        out= open(newName,'wb')
        out.write(b'<?xml version="1.0" encoding="UTF-8" standalone = "yes"?>\n')
        et.write(out, encoding= 'UTF-8', xml_declaration= False)
        out.close()

    






