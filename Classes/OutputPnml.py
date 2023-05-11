from OutputFormat import OutputFormat
import xml.etree.ElementTree as ET
from Node import Node 
from PetriNet import PetriNet
from Place import Place


class OutputPNML(OutputFormat):
    #falta implementación  de todo 
    def writeTransition(self):
        pass
         

    def writePlace(self,pt: Place):
        string = "place id= \"" + pt.Id + "\" name=\"" + pt.nameValue + "\" "
        place1 = ET.Element(string)
        ET.dump(place1) 

    def writeArc(self):
        pass
