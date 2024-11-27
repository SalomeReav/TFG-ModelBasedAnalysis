from abc import ABC, abstractmethod
from OutputPnml import OutputPNML
from Place import Place
from Transition import Transition
import xml.etree.ElementTree as ET
import os
import Node




class PetriNet:
    def __init__(self):
        '''Initialize a Petri class nodes with its list of nodes and arcs'''
        self.nodes = []
        self.arcs = []
    
    def writeOuput(self,root,file_name):
        output = OutputPNML()

        # Create level token of the pnml file
        n = ET.SubElement(root,"net")
        token = ET.SubElement(n,"token")
        token.set("id", "Default")
        token.set("red", "0")
        token.set("green", "0")
        token.set("blue", "0")
        
        # Call writting functions for each place or transition respectively
        for node in self.nodes:
            if isinstance(node,Place):
                output.writePlace(node,n)
            if isinstance(node,Transition):
                output.writeTransition(node,n)
        
        # Caal write arc function for each arc in the petri net
        for arcs in self.arcs:
            output.writeArc(arcs,n)
        
        ET.indent(root,level= 2)
        et=ET.ElementTree(root)
        
        try:
            # create and open the file in write mode for write de pnml structure
            output_path = os.path.join(r"..\output_files",file_name)
            with open(output_path,'wb') as out:
                out.write(b'<?xml version="1.0" encoding="UTF-8" standalone = "yes"?>\n')
                et.write(out, encoding= 'UTF-8', xml_declaration= False)
        except IOError as e:
            print("Erroral abrir archivo: ", e)

    






