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
    ''' Write transitions, places and arcs in PNML format. 
        Depends of OutputFormat class
    '''
    def writeTransition(self,tr: Transition, root: ET):
        '''Write a transition in pnml format with every level nedeed'''
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
        nameValue.text = str(tr.getId())
        offset = ET.SubElement(nameLabel, "graphics")
        offset.set("x", "-5.0")
        offset.set("y","35.0")

    def writePlace(self,pt: Place, root: ET):
        '''Write a place in pnml format with every level needed'''
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
        mark = ET.SubElement(place,"initialMarking")
        gr = ET.SubElement(mark,"graphics")
        off = ET.SubElement(gr,"offset")
        off.set("x","0.0")
        off.set("y","0.0")
        val = ET.SubElement(mark,"value")
        
        if pt.getInitialMarking() == 1: val.text = str(pt.getInitialMarking())


    def writeArc(self, arc: Arc, root: ET):
        '''Write an arc in pnml format with every level needed'''
        source: Node 
        target: Node
        source = arc.getsourceNode()
        target= arc.getTargetNode() 

        arc1 = ET.SubElement(root,"arc")
        arc1.set("id",str(source.getId()) + " TO " + str(target.getId()))
        arc1.set("source",str(source.getId()) )
        arc1.set("target",str(target.getId()) )
        typ = ET.SubElement(arc1,"type")
        typ.set("value","normal")
        ins = ET.SubElement(arc1,"inscription")
        val = ET.SubElement(ins,"value")
        val.text = str(arc.value)
        
        
        

