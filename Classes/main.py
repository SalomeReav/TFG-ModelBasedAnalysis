from OutputPnmlClass import OutputPNML
import json

#node types of interest
DECL_TYPES = ["VarDecl"]


if __name__== "__main__":
    with open("curated_ast.json", "r") as j:
        myjson = json.load(j)
        print(myjson)
    

    #aux = prueba.createOutputTransition()
