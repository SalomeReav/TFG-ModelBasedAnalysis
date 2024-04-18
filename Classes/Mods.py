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
RETURN_STMT = "ReturnStmt"
CHARACTER_LITERAL = "CharacterLiteral"
WHILE_STMT = "WhileStmt"

'''List for checked nodes and last ouput place for connect figures'''
CHECKED_NODES = {}
LAST_OUTPUT_ID = 0 
LAST_PARENT_ID = 0



def searchNodeById(id, net:PetriNet):
    for n in net.nodes:
        if  isinstance(n,Place) or isinstance(n,Transition):
            if n.getId() == id:
                return n 
    return None

def functionDecl(ast,node,net: PetriNet):
    global LAST_OUTPUT_ID
    if ast[node["parent"]]["kind"] == "TranslationUnitDecl":
        input = Place("InputFunction", LAST_OUTPUT_ID)
        input.setInitialMarking(1)
        net.nodes.append(input)
    else:
        input = searchNodeById(LAST_OUTPUT_ID,net)
        
    tranParm = Transition(node["id"])
    net.nodes.append(tranParm)

    arcM = Arc(0)
    arcM.setSourceNode(input)
    arcM.setTargetNode(tranParm)
    net.arcs.append(arcM)

    
    LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1
    output = Place("OutputFunction", LAST_OUTPUT_ID)
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


    if node["referencedDecl"]["kind"] == FUNC_DECL:
        '''EN ESTE CASO VER SI PONER ARCO A DEFINICION DE LA FUNCION'''
        tDeclRef = Transition(node["id"])
        net.nodes.append(tDeclRef)
        
        global LAST_OUTPUT_ID
        input = searchNodeById(LAST_OUTPUT_ID,net)

        arc = Arc(0)
        arc.setSourceNode(input)
        arc.setTargetNode(tDeclRef)
        net.arcs.append(arc) 

        LAST_OUTPUT_ID = LAST_OUTPUT_ID +1 
        output = Place("OutputFuncReference", LAST_OUTPUT_ID)
        net.nodes.append(output)

        arc2 = Arc(0)
        arc2.setSourceNode(tDeclRef)
        arc2.setTargetNode(output)
        net.arcs.append(arc2)

        LAST_PARENT_ID = node["id"]
    else:
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
        arc.setSourceNode(lit)
        arc.setTargetNode(p)        
        net.arcs.append(arc)
         
    else: 
        '''REVISAR SI ES NECESARIO LO DE DISTINGUIR SI ES TRANSI O LUGAR, CREO QUE NO '''  
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
    '''in case its parent is an IF we need its own input'''

    if ast[node["parent"]]["kind"]== CONTROL_TYPES or WHILE_STMT:
        '''cambiar id, este de momento para probar'''
        input = Place("OutputToBO", 3 + LAST_OUTPUT_ID)
        arc = Arc(0)
        arc.setSourceNode(input)
        arc.setTargetNode(operator)

        net.nodes.append(operator)
        net.nodes.append(input)
        net.arcs.append(arc)

        padre = searchNodeById(node["parent"],net)

        arc = Arc(0)
        arc.setSourceNode(padre)
        arc.setTargetNode(input)
        net.arcs.append(arc)
    elif ast[node["parent"]]["kind"]== DECL_TYPES:
        '''in case its parent is a declaration'''
        dcl = searchNodeById(node["parent"],net)
        link = Arc(0)
        link.setSourceNode(operator)
        link.setTargetNode(dcl)
        '''NO ESTA CONECTADO EL ARCO AL MAIN PRINCIPAL'''

        net.arcs.append(link)

    else:
        
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
    net.nodes.append(operator)
    
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

    global LAST_PARENT_ID
    LAST_PARENT_ID = node["id"]

def ifStmt(ast, node, net: PetriNet):

    '''si este nodo if es un una rama de otro if principal, por ejemplo 
    en el caso de un ElseIf, es un if que consta dentro de la rama false de 
    otro if principal. Cuando esto ocurra lo que hay que hacer es enlazar el 
    if con el nodo ooutput del if principal'''
    if ast[node["parent"]]["kind"] == CONTROL_TYPES:

        idLastOuputParent = CHECKED_NODES[node["parent"]]["outputIf"] 
        p = searchNodeById(idLastOuputParent, net)
    else:
        global LAST_OUTPUT_ID
        p = searchNodeById(LAST_OUTPUT_ID,net)


    '''set the id of this node as Last parent'''
   
    t_eval = Transition(node["id"])
    net.nodes.append(t_eval)
    
    global LAST_PARENT_ID
    LAST_PARENT_ID = node["id"]


    arc =Arc(0)
    arc.setSourceNode(p)
    arc.setTargetNode(t_eval)
    net.arcs.append(arc)

    '''pensar como guardar el output porque la rama else la necesita.
    Idea primera es meter el id del output en la lista de cheked nodes como 
    hijo del nodo if principal. asi poder buscarlo cuando se llegue al else'''
    #borrar esto de arriba cuando se compruebe que es correcto lo que se intenta hacer

    LAST_OUTPUT_ID = LAST_OUTPUT_ID +1 
    output = Place("Output" + node["kind"], LAST_OUTPUT_ID)
    net.nodes.append(output)

    '''guardo en el nodo padre if, el id del ouput para luego en el nodo else
    buscar ese id y partir de ahi'''
    CHECKED_NODES[node["id"]]["outputIf"] = LAST_OUTPUT_ID

    l = Arc(0)
    l.setSourceNode(t_eval)
    l.setTargetNode(output)
    net.arcs.append(l)

def whileStmt(node, net: PetriNet):
    stmt = Transition(node["id"])
    net.nodes.append(stmt)
    global LAST_OUTPUT_ID, LAST_PARENT_ID

    input = searchNodeById(LAST_OUTPUT_ID,net)

    arc = Arc(0)
    arc.setSourceNode(input)
    arc.setTargetNode(stmt)
    net.arcs.append(arc)

    LAST_OUTPUT_ID = LAST_OUTPUT_ID +1
    output = Place("OutputWhile",LAST_OUTPUT_ID)
    net.nodes.append(output)
    c = Arc(0)
    c.setSourceNode(stmt)
    c.setTargetNode(output)
    net.arcs.append(c)

    LAST_PARENT_ID =  node["id"]



def compoundIfstmt(ast, node,net:PetriNet):
    global LAST_OUTPUT_ID

    if ast[node["parent"]]["kind"] == CONTROL_TYPES:

        '''if it is the second child we identify as the true branch'''
        if  ast[node["parent"]]["inner"][1] == node["id"]:

            t_true = Transition("t_true_"+ str(LAST_OUTPUT_ID))
            net.nodes.append(t_true)
            
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

            '''AQUI ESTA EL PROBLEMO PORQUE NO RESUELVO EL ACOITN BLOCK'''
            actionBlock = Transition(node["id"])
            net.nodes.append(actionBlock)

            a = Arc(0)
            a.setSourceNode(mid)
            a.setTargetNode(actionBlock)
            net.arcs.append(a)
            '''En caso de que sean if anidados cierra todo en un solo output'''
            abu = ast[node["parent"]]["parent"]
            if ast[abu]["kind"] == CONTROL_TYPES:
                ant = CHECKED_NODES[abu]["finalOutput"]
                output = searchNodeById(ant, net)

                '''guardo el lugar de cierre de ifs'''
                CHECKED_NODES[node["parent"]]["finalOutput"] = ant
            else:
                LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1
                output = Place("Output_If", LAST_OUTPUT_ID)
                net.nodes.append(output)

                '''guardo el lugar de cierre de ifs'''
                CHECKED_NODES[node["parent"]]["finalOutput"] = LAST_OUTPUT_ID


            global LAST_PARENT_ID
            LAST_PARENT_ID = node["id"]
        elif ast[node["parent"]]["hasElse"] == True:

            t_false = Transition("t_false_"+ str(LAST_OUTPUT_ID))
            net.nodes.append(t_false)
            idLastOuputParent = CHECKED_NODES[node["parent"]]["outputIf"] 
          
            input = searchNodeById(idLastOuputParent, net)

            arc = Arc(0)
            arc.setSourceNode(input)
            arc.setTargetNode(t_false)
            net.arcs.append(arc)
  

            LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1
            mid = Place("OuputTrueBranch", LAST_OUTPUT_ID)
            net.nodes.append(mid)
            
            l2=Arc(0)
            l2.setSourceNode(t_false)
            l2.setTargetNode(mid)
            net.arcs.append(l2)

            actionBlock = Transition(node["id"])
            net.nodes.append(actionBlock)

            a = Arc(0)
            a.setSourceNode(mid)
            a.setTargetNode(actionBlock)
            net.arcs.append(a)

  
            LAST_PARENT_ID = node["id"]
           

            idCloseOutput = CHECKED_NODES[node["parent"]]["finalOutput"]
            output = searchNodeById(idCloseOutput, net) 
    

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

def characterLiteral(node, net: PetriNet):
    s = Place(node["kind"] + chr(node["value"]), node["id"])
    net.nodes.append(s)

    global LAST_PARENT_ID
    p = searchNodeById(LAST_PARENT_ID,net)

    a = Arc(0)
    a.setSourceNode(p)
    a.setTargetNode(s)
    net.arcs.append(a)

def returnStmt(node, net: PetriNet):

    global LAST_OUTPUT_ID, LAST_PARENT_ID
    rtn = Transition(node['id'])
    net.nodes.append(rtn)
    entry = searchNodeById(LAST_OUTPUT_ID,net)

    arc = Arc(0)
    arc.setSourceNode(entry)
    arc.setTargetNode(rtn)
    net.arcs.append(arc)

    LAST_OUTPUT_ID = LAST_OUTPUT_ID +1
    ouput = Place("OutputRtn", LAST_OUTPUT_ID)
    net.nodes.append(ouput)

    arc2 = Arc(0)
    arc2.setSourceNode(rtn)
    arc2.setTargetNode(ouput)
    net.arcs.append(arc2)

    LAST_PARENT_ID = node["id"]



    


#guardar nodos ya recorridos, dic
def classifyNodes(current_ast,node, net: PetriNet):
    global CHECKED_NODES
    if node["id"] not in CHECKED_NODES:
        CHECKED_NODES[node["id"]] = {"type": node["kind"],"outputIf": None, "finalOutput":None}
        c = node["kind"]
        if c == FUNC_DECL:
            functionDecl(current_ast,node,net)
        elif c == PARMVAR_DECL:
            parmDecl(current_ast,node,net)
        elif c == DECL_STMT:
            declstmt(current_ast, node,net)
        elif c == BINARY_OP:
            binaryOp(current_ast,node, net)
        elif c == UNARY_OP:
            unaryOp(node,net)
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
        elif c ==  RETURN_STMT :
            returnStmt(node,net)
        elif c == CHARACTER_LITERAL:
            characterLiteral(node,net)
        elif c == WHILE_STMT:
            whileStmt(node,net)
        #lo que s epuede hacer en el compund es crear el enlace
        #o transicion 

