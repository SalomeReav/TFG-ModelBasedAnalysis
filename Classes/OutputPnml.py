from OutputFormat import OutputFormat
import xml.etree.ElementTree as ET
from Place import Place
from Transition import Transition
from Arc import Arc


class OutputPNML(OutputFormat):
    #falta implementación  de todo 
    def writeTransition(self,tr: Transition, root: ET):
        string = "transition id= \"" + tr.Id + "\" isTimed= \"" + str(tr.getIsTimed()) + "\""
        trans = ET.SubElement(root,string)
        #return trans
        #ET.dump(trans)

    def writePlace(self,pt: Place, root: ET):
        string = "place id= \"" + pt.Id + "\" name=\"" + pt.nameValue + "\" "
        place1 = ET.SubElement(root,string)
        #return place1
        #ET.dump(place1) 

    def writeArc(self, arc: Arc, root: ET):
        source = arc.getsourceNode()
        target= arc.getTargetNode() 
        string = "arc source= " + str(source) + " "
        arc1 = ET.SubElement(root,string)
        #return arc1
        #ET.dump(arc1)