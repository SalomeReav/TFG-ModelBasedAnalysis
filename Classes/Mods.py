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



def declstmt(ast,node, net: PetriNet):
    '''check if is a declaration or a definition'''
    varDeclId = node["inner"][0]
    if "inner" in ast[varDeclId]:
        #its a variable definition 
        initialPlace = Place("initialValue"+ ast[varDeclId]["name"],varDeclId)
        #comprobar transicion 
        t_assig = Transition("t_assig")
        finalPlace = Place("VarID",ast[varDeclId]["inner"][0])
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
         #its a variable declaration 
         #to do: add initial marking 
         initialPlace = Place("varId_" + ast[varDeclId]["name"],varDeclId)
         net.nodes.append(initialPlace)

def binaryOp(node, net:PetriNet):
    tOp = Transition(node["id"])
    leftChild= node["inner"][0]
    rightChild= node["inner"][1]

    op1= Place("op_1_"+ leftChild,leftChild)
    op2= Place("op_2_"+ rightChild,rightChild)
    result= Place("result_var_"+leftChild+","+rightChild,"" )

    net.nodes.append(op1)
    net.nodes.append(op2)
    net.nodes.append(result)

    net.nodes.append(tOp)

    arcP1toTran = Arc(None)
    arcP1toTran.setSourceNode(op1)
    arcP1toTran.setTargetNode(tOp)
    net.arcs.append(arcP1toTran)
    
    arcP2toTran = Arc(None)
    arcP2toTran.setSourceNode(op2)
    arcP2toTran.setTargetNode(tOp)
    net.arcs.append(arcP2toTran)

    tOp.setSourceArc(tOp)
    tOp.setTargetArc(op1)
    tOp.setTargetArc(op2)
    #COMPROBAR EL USO DE ESTAS FUNCIONES Y COMO SACARLO EN EL PNML

    arcTtoResult = Arc(None)
    arcTtoResult.setSourceNode(tOp)
    arcTtoResult.setTargetNode(result)
    net.arcs.append(arcTtoResult)


def classifyNodes(ast, net: PetriNet):
    for source_file in ast:
        current_ast =ast[source_file]
        for c in NODES_INTEREST:
            if current_ast[c]["kind"] in DECL_STMT:
                declstmt(current_ast, current_ast[c],net)
            if current_ast[c]["kind"] in BINARY_OP:
                binaryOp(current_ast[c], net)

