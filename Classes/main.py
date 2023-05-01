from OutputPnmlClass import OutputPNML
import json

#node types of interest
#ECL_TYPES = ["VarDecl"]


#f __name__== "__main__":

j = open('curated_ast.json')
myjson = json.load(j)
print(myjson)
    

    #aux = prueba.createOutputTransition()
