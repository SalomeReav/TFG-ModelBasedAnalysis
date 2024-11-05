import xml.etree.ElementTree as ET
import json
import sys
from PetriNet import PetriNet 
import Mods
from Variables import Variables



if __name__== "__main__":

    file = sys.argv[1]
    
    jsonGenerated = open(file)
    myjson = json.load(jsonGenerated)

    net = PetriNet()

    # launch clasify function for each readed node
    for source_file in myjson:
        current_ast =myjson[source_file]
        Variables.ID_GEN = Mods.generate_id_conec()
        for id in current_ast:
            Mods.classify_nodes(current_ast,current_ast[id], net)

    # write xml for the petri net
    root = ET.Element("pnml")
    net.writeOuput(root)