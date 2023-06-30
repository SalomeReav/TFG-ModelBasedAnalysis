from OutputFormat import OutputFormat
import xml.etree.ElementTree as ET
from Place import Place
from Transition import Transition
from Arc import Arc
from Node import Node


class OutputPNML(OutputFormat):
    def writeTransition(self,tr: Transition, root: ET):
        transition = ET.SubElement(root,"transition",{"id":str(tr.getId())})


    def writePlace(self,pt: Place, root: ET):
        place = ET.SubElement(root,"place",{"id":str(pt.getId())})
        nameLabel = ET.SubElement(place,"name")
        nameValue = ET.SubElement(nameLabel,"value")
        nameValue.text = pt.nameValue



    def writeArc(self, arc: Arc, root: ET):
        source: Node 
        target: Node
        source = arc.getsourceNode()
        target= arc.getTargetNode() 

        arc = ET.SubElement(root,"arc",{"source":str(source.getId()),"target":str(target.getId())})

