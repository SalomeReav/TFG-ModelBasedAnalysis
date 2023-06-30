import xml.etree.ElementTree as ET
import json
from PetriNet import PetriNet 
import Mods

#node types of interest
DECL_TYPES = ["VarDecl"]
CONTROL_TYPES = ["IfStmt"]
CALL_TYPES = ["CallExpr"]
BINARY_OP = ["BinaryOperator"]
COMPOUND_STMT = ["CompoundStmt"]
DECL_STMT = ["DeclStmt"]




if __name__== "__main__":

    j = open('curated_astAssig.json')
    myjson = json.load(j)

    net = PetriNet()

    '''Find childs Id of the CompoundStmt'''
    Mods.findIdCompound(myjson)
    Mods.classifyNodes(myjson, net)
    root = ET.Element("net")
    root.set("id","n1")
    net.writeOuput(root)