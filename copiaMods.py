from PetriNet import PetriNet 
from Place import Place  
from Transition import Transition 
from Arc import Arc 
import Node

'''Node's relevant names'''
FUNC_DECL = "FunctionDecl"
DECL_TYPES = "VarDecl"
CONTROL_TYPES = "IfStmt"
CALL_TYPES = "CallExpr"
BINARY_OP = "BinaryOperator"
COMPOUND_STMT = "CompoundStmt"
DECL_STMT = "DeclStmt"
DECL_REFER = "DeclRefExpr"
PARMVAR_DECL = "ParmVarDecl"
IMPLICIT_CAST = "ImplicitCastExpr"
UNARY_OP = "UnaryOperator"
UNARY_OPEXPR = "UnaryExprOrTypeTraitExpr"

'''List for checked nodes and last ouput place for connect figures'''
CHECKED_NODES = {}
LAST_OUTPUT_ID = 1 



def searchNodeById(id, net:PetriNet):
    for n in net.nodes:
        if  isinstance(n,Place) or isinstance(n,Transition):
            if n.getId() == id:
                return n 

def functionDecl(ast,node,net: PetriNet):
    principal = Place(node["name"], node["id"])
    principal.setInitialMarking(1)
    net.nodes.append(principal)


    tranParm = Transition("t_"+node["kind"])
    net.nodes.append(tranParm)

    arcM = Arc(0)
    arcM.setSourceNode(principal)
    arcM.setTargetNode(tranParm)
    net.arcs.append(arcM)

    global CHECKED_NODES
    for n in node["inner"]:
        if ast[n]["kind"] in PARMVAR_DECL:
            declNode = Place("ParmVarDecl_" + ast[n]["name"], ast[n]["id"])
            CHECKED_NODES[node["id"]] = {"type": node["kind"]}
            net.nodes.append(declNode)
            arcTran = Arc(0)
            arcTran.setSourceNode(tranParm)
            arcTran.setTargetNode(declNode)
            net.arcs.append(arcTran)

    global LAST_OUTPUT_ID
    output = Place("OutputMain", LAST_OUTPUT_ID)
    net.nodes.append(output)

    arcToOutput = Arc(0)
    arcToOutput.setSourceNode(tranParm)
    arcToOutput.setTargetNode(output)
    net.arcs.append(arcToOutput)


def declstmt(ast,node, net: PetriNet):
    '''common structure even if it's a declaration or definition'''
    varDeclId = node["inner"][0]

    tDcl = Transition(node["id"])
    net.nodes.append(tDcl)

    global LAST_OUTPUT_ID
    outputTotran = Arc(0)
    tOutput = searchNodeById(LAST_OUTPUT_ID, net)
    outputTotran.setSourceNode(tOutput)
    outputTotran.setTargetNode(tDcl)
    net.arcs.append(outputTotran)

    initialPlace = Place("varId_" + ast[varDeclId]["name"],varDeclId)
    net.nodes.append(initialPlace)

    union = Arc(0)
    union.setSourceNode(tDcl)
    union.setTargetNode(initialPlace)

    net.arcs.append(union)

    '''creation of ouput node for following structure'''
    LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1
    outputP = Place("Ouput" + node["kind"], LAST_OUTPUT_ID )
    net.nodes.append(outputP)

    arcToOuput = Arc(0)
    arcToOuput.setSourceNode(tDcl)
    arcToOuput.setTargetNode(outputP)
    net.arcs.append(arcToOuput)

    '''append varDecl id as checked node'''
    CHECKED_NODES[varDeclId] = {"type":ast[varDeclId]["kind"]}
    
    '''in case it is a definition we need to create the place of the assignation'''
    if "inner" in ast[varDeclId]:
        child = ast[varDeclId]["inner"][0]
        '''modify this kind check if it is not necessary to know it'''
        if ast[child]["kind"] == "IntegerLiteral":
            result = Place("var_" + child + "_" + ast[child]["value"], child)

            arcToResult = Arc(0)
            arcToResult.setSourceNode(tDcl)
            arcToResult.setTargetNode(result)

            net.nodes.append(result)
            net.arcs.append(arcToResult)

            CHECKED_NODES[child] = {"type":ast[child]["kind"]}
       
   

def binaryOp( node, net:PetriNet):

    operator = Transition(node["id"])

    global LAST_OUTPUT_ID
    input = searchNodeById(LAST_OUTPUT_ID,net)
    arc = Arc(0)
    arc.setSourceNode(input)
    arc.setTargetNode(operator)

    net.nodes.append(operator)
    net.arcs.append(arc)

    LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1 
    output = Place("Output" + node["kind"], LAST_OUTPUT_ID)
    net.nodes.append(output)

    link = Arc(0)
    link.setSourceNode(operator)
    link.setTargetNode(output)

    net.arcs.append(link)


def declExpr(node, net: PetriNet):  
    arc = Arc(0)
    source = searchNodeById(node["parent"],net)
    target = searchNodeById(node["referencedDecl"]["id"],net)

    arc.setSourceNode(source)
    arc.setTargetNode(target)

    net.arcs.append(arc)

def implicitCastExpr(ast, node, net:PetriNet):
    #Recorrer hasta encontrar el DeclRefExpresion guardando que el padre 
    # es el binary op, PORQUE NO HACE FALTA EL IMPLICIT Y ARRAYSUBDCRIPT 
    parentId = node["parent"]
    ch = node["inner"][0]

    global CHECKED_NODES
    while ast[ch]["kind"]  not in DECL_REFER:
        CHECKED_NODES[ch] = {"type": ast[ch]["kind"]}
        ch = ast[ch]["inner"][0]
        

    CHECKED_NODES[ch] = {"type": ast[ch]["kind"]}

    arc = Arc(0)
    source = searchNodeById(parentId,net)
    target = searchNodeById(ast[ch]["referencedDecl"]["id"],net)

    arc.setSourceNode(source)
    arc.setTargetNode(target)

    net.arcs.append(arc)

def unaryOp(node, net: PetriNet):
    tranOp = Transition(node["id"])

    net.nodes.append(tranOp)

    global LAST_OUTPUT_ID
    input = searchNodeById(LAST_OUTPUT_ID, net)

    arc = Arc(0)
    arc.setSourceNode(input)
    arc.setTargetNode(tranOp)

    net.arcs.append(arc)

    LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1
    output = Place("Output" + node["kind"], LAST_OUTPUT_ID)
    net.nodes.append(output)

    link = Arc(0)
    link.setSourceNode(tranOp)
    link.setTargetNode(output)

    net.arcs.append(link)

def ifStmt(current_ast, node, net: PetriNet):

    trueChild = node["inner"][1]

    '''TO DO parte de else gestion'''
    if "haselse" in current_ast[node]:
        falseChild = node["inner"][2]

    tEval = Transition(node["id"])
 
    net.nodes.append(tEval)

    global LAST_OUTPUT_ID
    input= searchNodeById(LAST_OUTPUT_ID,net)
    connect = Arc(0)
    connect.setSourceNode(input)
    connect.setTargetNode(tEval)
    net.arcs.append(connect)

    LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1
    inter = Place("Conexion Place", LAST_OUTPUT_ID)
    net.nodes.append(inter)

    '''conect teval with inter'''
    arc = Arc(0)
    arc.setSourceNode(tEval)
    arc.setTargetNode(inter)
    net.arcs.append(arc)


    tTrue = Transition(trueChild)
    net.nodes.append(tTrue)


    l = Arc(0)
    l.setSourceNode(inter)
    l.setTargetNode(tTrue)
    net.arcs.append(l)

    
    '''find action block'''
    global CHECKED_NODES
    while current_ast[ch]["kind"]  not in DECL_REFER:
        CHECKED_NODES[ch] = {"type": current_ast[ch]["kind"]}
        ch = current_ast[ch]["inner"][0]
        

    CHECKED_NODES[ch] = {"type": current_ast[ch]["kind"]}




#guardar nodos ya recorridos, dic
def classifyNodes(current_ast,node, net: PetriNet):
    global CHECKED_NODES
    if node["id"] not in CHECKED_NODES:
        CHECKED_NODES[node["id"]] = {"type": node["kind"]}
        c = node["kind"]
        if c == FUNC_DECL:
            functionDecl(current_ast,node,net)
        elif c == DECL_STMT:
            declstmt(current_ast, node,net)
        elif c == BINARY_OP:
            binaryOp(node, net)
        elif c == DECL_REFER: 
            declExpr(node ,net)
        elif c == IMPLICIT_CAST: 
            implicitCastExpr(current_ast, node, net)
        #lo que s epuede hacer en el compund es crear el enlace
        #o transicion 

