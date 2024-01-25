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
INTEGER_LITERAL = "IntegerLiteral"
STRING_LITERAL = "StringLiteral"
UNARY_OP = "UnaryOperator"
UNARY_OPEXPR = "UnaryExprOrTypeTraitExpr"

'''List for checked nodes and last ouput place for connect figures'''
CHECKED_NODES = {}
LAST_OUTPUT_ID = 1 
LAST_PARENT_ID = 0



def searchNodeById(id, net:PetriNet):
    for n in net.nodes:
        if  isinstance(n,Place) or isinstance(n,Transition):
            if n.getId() == id:
                return n 
    return None

def functionDecl(ast,node,net: PetriNet):
    principal = Place("input_main", "0")
    principal.setInitialMarking(1)
    net.nodes.append(principal)


    tranParm = Transition(node["id"])
    net.nodes.append(tranParm)

    arcM = Arc(0)
    arcM.setSourceNode(principal)
    arcM.setTargetNode(tranParm)
    net.arcs.append(arcM)

    global LAST_OUTPUT_ID
    output = Place("OutputMain", LAST_OUTPUT_ID)
    net.nodes.append(output)

    arcToOutput = Arc(0)
    arcToOutput.setSourceNode(tranParm)
    arcToOutput.setTargetNode(output)
    net.arcs.append(arcToOutput)

def parmDecl(ast,node,net:PetriNet):
    parm = Place(node["name"],node["id"])
    net.nodes.append(parm)

    parent = searchNodeById(node["parent"],net)
    arc= Arc(0)
    arc.setSourceNode(parent)
    arc.setTargetNode(parm)
    net.arcs.append(arc)

def declstmt(ast,node, net: PetriNet):

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
    
    '''in case it is a definition we put this node as last father'''
    if "inner" in ast[varDeclId]:
        global LAST_PARENT_ID
        LAST_PARENT_ID = node["id"]
     

def declExpr(node, net: PetriNet):
    global LAST_PARENT_ID
    source = searchNodeById(LAST_PARENT_ID,net)

    target = searchNodeById(node["referencedDecl"]["id"],net)  
    if target == None:
        #if the referenced variable does not exist yet create it and add to nodes list
        target = Place(node['referencedDecl']["name"], node['referencedDecl']["id"])
        net.nodes.append(target)
    
    arc = Arc(0)
    arc.setSourceNode(target)
    arc.setTargetNode(source)
    net.arcs.append(arc)

def integerLiteral(node,net:PetriNet):
    global LAST_PARENT_ID
    p = searchNodeById(LAST_PARENT_ID,net)
    lit = Place(node["kind"] + "_" + node["value"],node["id"])
    net.nodes.append(lit)
    if isinstance(p,Transition):


        arc = Arc(0)
        arc.setSourceNode(p)
        arc.setTargetNode(lit)
        net.arcs.append(arc)
    else:
        t = Transition(node["id"])
        net.nodes.append(t)
        
        arc = Arc(0)
        arc.setSourceNode(p)
        arc.setTargetNode(t)
        net.arcs.append(arc)

        arcFinal = Arc(0)
        arcFinal.setSourceNode(t)
        arcFinal.setTargetNode(lit)
        net.arcs.append(arcFinal)

def binaryOp( ast, node, net:PetriNet):

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

    global LAST_PARENT_ID
    LAST_PARENT_ID = node["id"]

    '''in case its parent is a declaration'''
    
    if ast[node["parent"]]["kind"]== DECL_TYPES:
        print("entro en arco de cl con bop")
        dcl = searchNodeById(node["parent"],net)
        link = Arc(0)
        link.setSourceNode(operator)
        link.setTargetNode(dcl)

        net.arcs.append(link)


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
    '''set the id of this node as Last parent'''

    global LAST_OUTPUT_ID
    p = searchNodeById(LAST_OUTPUT_ID,net)
    t_eval = Transition(node["id"])
    net.nodes.append(t_eval)
    
    global LAST_PARENT_ID
    LAST_PARENT_ID = node["id"]


    arc =Arc(0)
    arc.setSourceNode(p)
    arc.setTargetNode(t_eval)
    net.arcs.append(arc)


    LAST_OUTPUT_ID = LAST_OUTPUT_ID +1 
    output = Place("Output" + node["kind"], LAST_OUTPUT_ID)
    net.nodes.append(output)

    l = Arc(0)
    l.setSourceNode(t_eval)
    l.setTargetNode(output)
    net.arcs.append(l)

def compoundIfstmt(ast, node,net:PetriNet):

    if ast[node["parent"]]["kind"] == CONTROL_TYPES:

        '''if it is the second child we identify as the true branch'''
        if  ast[node["parent"]]["inner"][1] == node["id"]:
            print("entro en true branch del if")
            t_true = Transition("t_true")
            net.nodes.append(t_true)
            global LAST_OUTPUT_ID
            input = searchNodeById(LAST_OUTPUT_ID, net)

            arc = Arc(0)
            arc.setSourceNode(input)
            arc.setTargetNode(t_true)
            net.arcs.append(arc)

            LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1
            mid = Place("OuputTrueBranch", LAST_OUTPUT_ID)
            net.nodes.append(mid)
            
            l2=Arc(0)
            l2.setSourceNode(t_true)
            l2.setTargetNode(mid)
            net.arcs.append(l2)

            actionBlock = Transition(node["id"])
            net.nodes.append(actionBlock)

            a = Arc(0)
            a.setSourceNode(mid)
            a.setTargetNode(actionBlock)
            net.arcs.append(a)

            LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1
            output = Place("Output_Ifstmt", LAST_OUTPUT_ID)
            net.nodes.append(output)

            actToOutput = Arc(0)
            actToOutput.setSourceNode(actionBlock)
            actToOutput.setTargetNode(output)
            net.arcs.append(actToOutput)

            LAST_PARENT_ID = node["id"]
        elif len(ast[node["parent"]]["inner"]) > 2:
            print("entro en rama False del if")
            t_false = Transition("t_false")
            net.nodes.append(t_false)
            global LAST_OUTPUT_ID
            input = searchNodeById(LAST_OUTPUT_ID, net)

            arc = Arc(0)
            arc.setSourceNode(input)
            arc.setTargetNode(t_false)
            net.arcs.append(arc)

            LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1
            mid = Place("OuputTrueBranch", LAST_OUTPUT_ID)
            net.nodes.append(mid)
            
            l2=Arc(0)
            l2.setSourceNode(t_true)
            l2.setTargetNode(mid)
            net.arcs.append(l2)

            actionBlock = Transition(node["id"])
            net.nodes.append(actionBlock)

            a = Arc(0)
            a.setSourceNode(mid)
            a.setTargetNode(actionBlock)
            net.arcs.append(a)

            LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1
            output = Place("Output_Ifstmt", LAST_OUTPUT_ID)
            net.nodes.append(output)

            actToOutput = Arc(0)
            actToOutput.setSourceNode(actionBlock)
            actToOutput.setTargetNode(output)
            net.arcs.append(actToOutput)


def stringLiteral(node, net:PetriNet):
    s = Place(node["kind"] + node["value"], node["id"])
    net.nodes.append(s)

    global LAST_PARENT_ID
    p = searchNodeById(LAST_PARENT_ID,net)

    a = Arc(0)
    a.setSourceNode(p)
    a.setTargetNode(s)
    net.arcs.append(a)

    
  


#guardar nodos ya recorridos, dic
def classifyNodes(current_ast,node, net: PetriNet):
    global CHECKED_NODES
    if node["id"] not in CHECKED_NODES:
        CHECKED_NODES[node["id"]] = {"type": node["kind"]}
        c = node["kind"]
        if c == FUNC_DECL:
            functionDecl(current_ast,node,net)
        elif c == PARMVAR_DECL:
            parmDecl(current_ast,node,net)
        elif c == DECL_STMT:
            declstmt(current_ast, node,net)
        elif c == BINARY_OP:
            binaryOp(current_ast,node, net)
        elif c == DECL_REFER: 
            declExpr(node ,net)
        elif c == INTEGER_LITERAL: 
           integerLiteral(node, net)
        elif c == CONTROL_TYPES:
            ifStmt(current_ast,node,net)
        elif c == COMPOUND_STMT:
            compoundIfstmt(current_ast,node,net)
        elif c == STRING_LITERAL:
            stringLiteral(node,net)
        #lo que s epuede hacer en el compund es crear el enlace
        #o transicion 

