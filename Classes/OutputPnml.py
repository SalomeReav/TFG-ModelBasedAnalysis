from OutputFormat import OutputFormat
import xml.etree.ElementTree as ET
from Place import Place
from Transition import Transition
from Arc import Arc
from Node import Node
import random


XPOSITION = 329.0
YPOSITION = 134.0

XPOSTRANSICION = 342.0
YPOSTRANSICION = 100.0

class OutputPNML(OutputFormat):
    def writeTransition(self,tr: Transition, root: ET):
        global XPOSTRANSICION 
        global YPOSTRANSICION
        transition = ET.SubElement(root,"transition",{"id":str(tr.getId())})
        graph = ET.SubElement(transition,"graphics")
        pos = ET.SubElement(graph,"position")
        pos.set("x", str(XPOSTRANSICION))
        pos.set("y", str(YPOSTRANSICION))

        XPOSTRANSICION = XPOSTRANSICION + 50
        YPOSTRANSICION = YPOSTRANSICION + 50

        nameLabel = ET.SubElement(transition,"name")
        nameValue = ET.SubElement(nameLabel,"value")
        nameValue.text = "T"
        offset = ET.SubElement(nameLabel, "graphics")
        offset.set("x", "-5.0")
        offset.set("y","35.0")

    def writePlace(self,pt: Place, root: ET):
        global XPOSITION
        global YPOSITION
        place = ET.SubElement(root,"place",{"id":str(pt.getId())})
        graph = ET.SubElement(place,"graphics")
        pos = ET.SubElement(graph,"position")
        pos.set("x",str(XPOSITION))
        pos.set("y",str(YPOSITION))
        XPOSITION = XPOSITION + (35 * random.randint(0,2))
        YPOSITION = YPOSITION + (35 * random.randint(0,2))
        nameLabel = ET.SubElement(place,"name")
        nameValue = ET.SubElement(nameLabel,"value")
        nameValue.text = pt.nameValue
        offset = ET.SubElement(nameLabel, "graphics")
        offset.set("x", "-5.0")
        offset.set("y","35.0")



    def writeArc(self, arc: Arc, root: ET):
        source: Node 
        target: Node
        source = arc.getsourceNode()
        target= arc.getTargetNode() 
        print("dentro de write arc")
        print(source.getId())
        print(target.getId())
        arc1 = ET.SubElement(root,"arc")
        arc1.set("id",str(source.getId()) + " TO " + str(target.getId()))
        arc1.set("source",str(source.getId()) )
        arc1.set("target",str(target.getId()) )
        
        
        

