from OutputPnml import OutputPNML
from PetriNet import PetriNet 
from Place import Place  
from Transition import Transition 
from Arc import Arc 
import json

#node types of interest
DECL_TYPES = ["VarDecl"]
CONTROL_TYPES = ["IfStmt"]
CALL_TYPES = ["CallExpr"]
TYPES_OF_INTEREST = DECL_TYPES + CONTROL_TYPES + CALL_TYPES 

if __name__== "__main__":

    paint = OutputPNML()

    j = open('curated_ast.json')
    myjson = json.load(j)

    for key in myjson:
        for value in myjson[key]:
            for type in myjson[key][value]:
                if "kind" in type:
                    if  myjson[key][value][type] in DECL_TYPES:
                        nameValue= myjson[key][value][type]
                        Id= myjson[key][value]["id"]
                        #cambiar
                        principalNet = PetriNet()
                        placeAux = Place(nameValue,Id)
                        principalNet.nodes = placeAux 
                        paint.writePlace(principalNet.nodes)

                   


    #aux = prueba.createOutputTransition()
