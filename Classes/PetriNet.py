from abc import ABC, abstractmethod
from OutputPnml import OutputPNML
from Place import Place
from Transition import Transition
import xml.etree.ElementTree as ET
#añadir las clases de node  y arc para poder poner las
#funciones que añadan esos nodos en nodes o arcs dependiendo.
#no me cuadra porque en la composicion petrinet deberia usar objetos de
#la clase node o arc, y estan declarados en el mismo fichero por lo que no 
#necesutan importar. pero en este caso no puedo poner las 3 clases en el mismo 
#fichero. o si? ?¿?¿


class PetriNet:
    def __init__(self):
        self.nodes = []
        self.arcs = []
    
    def writeOuput(self,root):
        output = OutputPNML()
        xml = []
    
        for arcs in self.arcs:
            output.writeArc(arcs,root)
        for node in self.nodes:
            if isinstance(node,Place):
                output.writePlace(node,root)
            if isinstance(node,Transition):
                output.writeTransition(node,root)
        
        ET.dump(root)
        
    








