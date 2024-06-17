import xml.etree.ElementTree as ET
import json
from PetriNet import PetriNet 
import Mods
import sys


if __name__== "__main__":

    file = sys.argv[1]
    
    jsonGenerated = open(file)
    myjson = json.load(jsonGenerated)

    net = PetriNet()

    #comprobar por nodo 
    for source_file in myjson:
        current_ast =myjson[source_file]
        for id in current_ast:
            Mods.classify_nodes(current_ast,current_ast[id], net)

    #write xml for the petri net
    root = ET.Element("pnml")
    net.writeOuput(root)