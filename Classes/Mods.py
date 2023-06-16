from OutputPnml import OutputPNML
from PetriNet import PetriNet 
from Place import Place  
from Transition import Transition 
from Arc import Arc 
import xml.etree.ElementTree as ET
import json


DECL_TYPES = ["VarDecl"]
CONTROL_TYPES = ["IfStmt"]
CALL_TYPES = ["CallExpr"]
BINARY_OP = ["BinaryOperator"]
COMPOUND_STMT = ["CompoundStmt"]
DECL_STMT = ["DeclStmt"]
NODES_INTEREST = []

'''returns a list with ids of each node of the structure'''
def findIdCompound(ast):
    for key in ast:
        for value in ast[key]:
            astKey = ast[key][value]
            for type in astKey:
                if  astKey[type] in COMPOUND_STMT:
                    for id in astKey["inner"]:
                        NODES_INTEREST.append(id)


'''search a child with its id, and save labels' data of kind and childs' id
    in case the node has them. The function returns an array where the 
    structure id: [0] kind's name, [1] id inner child [...] if has more inners'''
def searchId(ast, childId):
    i = 0
    att=[]
    for key in ast:
        for value in ast[key]:
            astKey = ast[key][value]
            if astKey["id"] == childId:
                att.append(astKey["kind"])
                if "inner" in astKey:
                    for desc in astKey["inner"]:
                        i = i +1 
                        att.append(desc)
                return att 
                

    

def declstmt(ast, child, net: PetriNet):
    '''check if is a declaration or a definition'''
    varDeclAtt = searchId(ast,child) #obtain labels of VarDecl
    l = len(varDeclAtt)
    if l > 2 :
        initialPlace = Place("initialValue",child)
        t_assig = Transition("t1")
        finalPlace = Place("VarID",varDeclAtt[1])
        net.nodes.append(t_assig)
        net.nodes.append(finalPlace)
        net.nodes.append(initialPlace)
        print(net.nodes)

        arcI = Arc(None)
        arcI.setSourceNode(initialPlace)
        arcI.setTargetNode(t_assig)

        arcAsig = Arc(None)
        arcAsig.setSourceNode(t_assig)
        arcAsig.setTargetNode(finalPlace)

        net.arcs.append(arcI)
        net.arcs.append(arcAsig)
    else:
         initialPlace = Place("varId",child)
         net.nodes.append(initialPlace)


def classifyNodes(ast, net: PetriNet):
    for c in NODES_INTEREST:
        info = searchId(ast,c)
        if info[0] in DECL_STMT:
            declstmt(ast,info[1], net)
