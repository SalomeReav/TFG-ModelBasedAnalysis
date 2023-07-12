from PetriNet import PetriNet 
from Place import Place  
from Transition import Transition 
from Arc import Arc 
import Node


FUNC_DECL = ["FunctionDecl"]
DECL_TYPES = ["VarDecl"]
CONTROL_TYPES = ["IfStmt"]
CALL_TYPES = ["CallExpr"]
BINARY_OP = ["BinaryOperator"]
COMPOUND_STMT = ["CompoundStmt"]
DECL_STMT = ["DeclStmt"]
DECL_REFER = ["DeclRefExpr"]
PARMVAR_DECL = ["ParmVarDecl"]
CHECKED_NODES = {}


def searchNodeById(id, net:PetriNet):
    for n in net.nodes:
        if  isinstance(n,Place) or isinstance(n,Transition):
            if n.getId() == id:
                return n 

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

        arcI = Arc(0)
        arcI.setSourceNode(initialPlace)
        arcI.setTargetNode(t_assig)

        arcAsig = Arc(0)
        arcAsig.setSourceNode(t_assig)
        arcAsig.setTargetNode(finalPlace)

        net.arcs.append(arcI)
        net.arcs.append(arcAsig)
    else:
         #its a variable declaration 
         #to do: add initial marking 
         initialPlace = Place("varId_" + ast[varDeclId]["name"],varDeclId)
         net.nodes.append(initialPlace)

         init = searchNodeById(ast[varDeclId]["parent"])

         union = Arc(0)
         union.setSourceNode(init)
         union.setTargetNode(initialPlace)

         net.arcs.append(union)
         



def binaryOp(ast, node, net:PetriNet):
    #comprobar si es un nodo ya existente el resultado ypor tanto
    #unirlo con el nodo. o si es un resultado como una suma donde hay que crear
    #el nodo 
    #AÑADIR EN NOMBRE QUE TIPO DE OP PARA MAS CLARIDAD 
    operator = Place("BinaryOP_" + node["opcode"], node["id"])
    p = searchNodeById(node["parent"], net)

    arc = Arc(0)
    arc.setSourceNode(p)
    arc.setTargetNode(operator)

    net.nodes.append(operator)
    net.nodes.append(p)
    net.arcs.append(arc)
    

def declExpr(ast, node, net: PetriNet):  
    #parent its a place so we create this kind as a transitoin 
    #and then we conecct it to the place whose being referenced 

    tDecl = Transition(node["id"])
    net.nodes.append(tDecl)

    parent = searchNodeById(node["parent"],net)

    union = Arc(0)
    union.setSourceNode(parent)
    union.setTargetNode(tDecl)
    net.arcs.append(union)

    referenced = searchNodeById(node["referencedDecl"]["id"], net)
    arcToReferenced = Arc(0)
    arcToReferenced.setSourceNode(tDecl)
    arcToReferenced.setTargetNode(referenced)
    net.arcs.append(arcToReferenced)

def implicitCastExpr(ast, node, net:PetriNet):
    #Recorrer hasta encontrar el DeclRefExpresion guardando que el padre 
    # es el binary op, PORQUE NO HACE FALTA EL IMPLICIT Y ARRAYSUBDCRIPT 
    parentId = node["parent"]
    segChild = node["inner"]
    terChild = ast[segChild]["inner"][0]
    fourthChild = ast[terChild]["inner"]

    tDecl = Transition(fourthChild)
    net.nodes.append(tDecl)

    p = searchNodeById(parentId, net)

    link = Arc(0)
    link.setSourceNode(p)
    link.setTargetNode(tDecl)
    net.arcs.append(link)

    referenced = searchNodeById(ast[fourthChild]["referencedDecl"]["id"], net)
    arc = Arc(0)
    arc.setSourceNode(tDecl)
    arc.setTargetNode(referenced)
    net.arcs.append(arc)

def functionDecl(ast,node,net: PetriNet):
    principal = Place(node["name"], node["id"])
    principal.setInitialMarking(1)
    net.nodes.append(principal)

    if node["name"] == "main":
        #PENSAR SI EL NOMBRE ES ADECUADO,  y si al reutilizarlo es mejor ponerlo 
        #en una variable global
        tranParm = Transition("t_declMainParams")
        net.nodes.append(tranParm)
        arcM = Arc(0)
        arcM.setSourceNode(principal)
        arcM.setTargetNode(tranParm)
        net.arcs.append(arcM)

        for n in node["inner"]:
            print("entro en inner de main")
            print(n)
            print(ast[n]["kind"])
            if ast[n]["kind"] in PARMVAR_DECL:
                print(ast[n]["kind"])
                declNode = Place("ParmVarDecl_" + ast[n]["name"], ast[n]["id"])
                CHECKED_NODES[node["id"]] = {"type": node["kind"]}
                net.nodes.append(declNode)
                arcTran = Arc(0)
                arcTran.setSourceNode(tranParm)
                arcTran.setTargetNode(declNode)
                net.arcs.append(arcTran)
    else:
        print("es un functiondecl pero no el main")


def compoundStmt(ast,node,net:PetriNet):
    compoundStart = Transition(node["id"])
    parent = searchNodeById(node["parent"],net)
    
    union = Arc(0)
    union.setSourceNode(parent)
    union.setTargetNode(compoundStart)


    net.nodes.append(compoundStart)
    net.nodes.append(parent)
    net.arcs.append(union)
    
#guardar nodos ya recorridos, dic
def classifyNodes(current_ast,node, net: PetriNet):
    if node["id"] not in CHECKED_NODES:
        CHECKED_NODES[node["id"]] = {"type": node["kind"]}
        c = node["kind"]
        if c in FUNC_DECL:
            functionDecl(current_ast,node,net)
        elif c in COMPOUND_STMT:
            compoundStmt(current_ast,node,net)
        elif c in DECL_STMT:
            declstmt(current_ast, node,net)
        elif c in BINARY_OP:
            binaryOp(current_ast,node, net)
        elif c in DECL_REFER: 
            pass #declExpr(current_ast,node ,net)
        #lo que s epuede hacer en el compund es crear el enlace
        #o transicion 

