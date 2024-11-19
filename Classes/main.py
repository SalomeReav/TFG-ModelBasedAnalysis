import xml.etree.ElementTree as ET
import json
import sys
import os 
import time
from PetriNet import PetriNet 
import Mods
from Variables import Variables



def main():
    inicio_gen = time.time()
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <json_file>")
        sys.exit(1)

    file = sys.argv[1]

    try:
        jsonGenerated = open(file)
        myjson = json.load(jsonGenerated)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)

    net = PetriNet()

    # Read each node of the AST and run Classify function 
    for source_file in myjson:
        current_ast = myjson[source_file]
        Variables.ID_GEN = Mods.generate_id_conec()
        for id in current_ast:
            Mods.classify_nodes(current_ast,current_ast[id], net)

    # write petri net to an XML file
    root = ET.Element("pnml")
    name_file = os.path.splitext(os.path.basename(file))[0]
    net.writeOuput(root,str(name_file) +"_PetriNet.pnml")

    fin_gen = time.time()
    tiempo_gen = fin_gen - inicio_gen

    print(f"Tiempo de ejecución global:{tiempo_gen: .4f} segundos")


if __name__== "__main__":
    main()
    
    


    