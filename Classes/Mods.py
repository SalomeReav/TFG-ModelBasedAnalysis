import random
import autopep8

from PetriNet import PetriNet 
from Place import Place  
from Transition import Transition 
from Arc import Arc 
from Variables import Variables
from Node import Node 


def generate_id_conec(max_id=1000):
    '''
    Generate IDs for names from 0 to max_id
    Args:
        max_id (int): The maximum Id to generate
    Yields:
        int: next ID in the sequence
    '''
    for id in range(max_id + 1):
        yield id

def search_node_by_id(id:int, net:PetriNet):
    '''
    Return a Place or Transition object by its id. 
    '''
    for n in net.nodes:
        if  isinstance(n,Place) or isinstance(n,Transition):
            if n.getId() == id:
                return n 
    return None

def create_arc(first_node:Node,second_node:Node,net: PetriNet):
    '''
    Create an Arc object,connect the parameters node and append all to the net 
    Args:
        first_node: source node 
        second_node: target node
        net: net which its being writted
        num: cardinality of the arc 
    '''

    try:
        if not isinstance(first_node,Node):
            raise TypeError("first_node must be a Node object")
        if not isinstance(second_node,Node):
            raise TypeError("second_node must be a Node object")
    except TypeError as e:
        print(e)
      

    arc = Arc(1)
    arc.setSourceNode(first_node)
    arc.setTargetNode(second_node)
    net.arcs.append(arc)

def create_sec_tran(net: PetriNet):
    '''
    Create black transition which its union place and arcs
    '''
    tran_black = Transition("t_sec_black" + str(next(Variables.ID_GEN)))
    net.nodes.append(tran_black)

    nex_out = Place("out_con",next(Variables.ID_GEN))
    net.nodes.append(nex_out)
    create_arc(Variables.CURRENT_OUTPUT,tran_black,net)
    create_arc(tran_black,nex_out,net)

    Variables.CURRENT_OUTPUT = nex_out

def verify_object(eval_node:Node,first_node:Node,net:PetriNet):
    '''
    Check the type of an object and create its determinate arcs and places.
    For control type structures where transitions of decision need to be link 
    with the reference node. 
    Parameters:
        eval_node: referenced node of an evaluation
        fisrt_node: node which has to be link with node eval
        net: petri net that is being drawing
        num: cardinality of arcs
    '''

    try:
        if not isinstance(first_node,Node):
            raise TypeError("first_node must be a Node object")
        if not isinstance(eval_node,Node):
            raise TypeError("eval_node must be a Node object")
    except TypeError as e:
        print(e)

    if isinstance(eval_node, Transition):
        out_ax_t = Place("out_mid_ref", next(Variables.ID_GEN))
        out_ax_t.setInitialMarking(1)
        net.nodes.append(out_ax_t)
        # its a bidirectional arc
        create_arc(first_node,out_ax_t,net)
        create_arc(out_ax_t,eval_node,net)
        create_arc(out_ax_t,first_node,net)
        create_arc(eval_node,out_ax_t,net)
    else:
        create_arc(first_node,eval_node,net)
        create_arc(eval_node,first_node,net)

def final_conect(ast,node, net:PetriNet):
    '''
    Process final conections of a previous main node based on its type
    '''
    if node["parent"] == Variables.MAIN_COMPOUND:
        end_node = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["output_node"],net)
        repeat_node = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["input_node"],net) 

        
        main_parent_kind = ast[Variables.ID_MAIN_PARENT]["kind"]
        if main_parent_kind == Variables.WHILE_STMT or main_parent_kind == Variables.FOR_STMT:
            # connect to the repeat node to mark the loop
            create_arc(Variables.LAST_PARENT, repeat_node,net)
            Variables.CURRENT_OUTPUT = end_node
        elif main_parent_kind == Variables.IF_STMT and len(ast[Variables.ID_MAIN_PARENT]["inner"]) > 2:
            if Variables.CURRENT_COMPOUND == ast[Variables.ID_MAIN_PARENT]["inner"][2]:
                print("dentro de cierre de false")
                # Close the false branch of an if with the end node created in the true branch before
                create_arc(Variables.LAST_PARENT, end_node,net)
                Variables.CURRENT_OUTPUT = end_node
        elif main_parent_kind == Variables.DO_WHILE:
            # Create a transition for the end of the do-while loop
            t_end_do = Transition("t_end_do" + str(next(Variables.ID_GEN)))
            net.nodes.append(t_end_do)

            ref_node = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["referenced_node"],net)
            create_arc(Variables.CURRENT_OUTPUT,t_end_do,net)
            create_arc(t_end_do,ref_node,net)

            # Create a transition for the start of the do-while loop
            t_do = Transition("t_do" + str(next(Variables.ID_GEN)))
            net.nodes.append(t_do)
            create_arc(Variables.CURRENT_OUTPUT,t_do,net)
            create_arc(t_do,ref_node,net)

            # Link default transitions to the evaluation node referenced
            verify_object(ref_node,t_end_do,net)
            verify_object(ref_node,t_do,net)

            input_node = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["input_node"],net)
            create_arc(t_do,input_node,net)

            output_do = Place("output_do",next(Variables.ID_GEN))
            net.nodes.append(output_do)
            create_arc(t_end_do,output_do,net)
            Variables.CURRENT_OUTPUT = output_do    

def func_struct_decl(ast,node,net: PetriNet):
    '''
    Process function and struct/union/class nodes
    '''
    # Determine if this is the first function in the TranslationUnitDecl
    if ast[node["parent"]]["inner"][0] == node["id"]:
        # If node its the first function created we initialize the place mark in its input
        input_place = Place("input_placeFunction", next(Variables.ID_GEN) )
        input_place.setInitialMarking(1)
        net.nodes.append(input_place)
    else:
        # If the node is not the first function created we link the model with the previous output
        input_place = Variables.CURRENT_OUTPUT

    Variables.CHECKED_NODES[node["id"]]["input_node"] = input_place.getId()

    # create elements and append them to the net    
    transition_func = Transition(node["id"])
    net.nodes.append(transition_func)
    create_arc(input_place,transition_func,net)
    output = Place("OutputInter", next(Variables.ID_GEN))
    net.nodes.append(output)
    create_arc(transition_func,output,net)

    # save information for the current structure 
    Variables.CHECKED_NODES[node["id"]]["output_node"] = output.getId() 
    Variables.CURRENT_OUTPUT = output
    Variables.LAST_PARENT= transition_func
    Variables.ID_MAIN_PARENT = node["id"]

def parm_field_decl(ast,node,net:PetriNet):
    '''
    Process of function paremeters and fields of struct/union/class
    '''
    parameter = Place(node["name"],node["id"])
    parameter.setInitialMarking(1)
    net.nodes.append(parameter)
    create_arc(Variables.LAST_PARENT,parameter,net)
    create_arc(parameter,Variables.LAST_PARENT,net)

def decl_stmt(ast,node, net: PetriNet):
    '''
    Process nodes of function or variables declarations
    '''
    final_conect(ast,node,net)
    # if belongs to the main compound or the current means its a secuencial stmt, not a inner like in a condition
    if node["parent"] in {Variables.MAIN_COMPOUND, Variables.CURRENT_COMPOUND} :
        create_sec_tran(net)

    # create a transition node for the declaration 
    declare_node = Transition(node["id"])
    net.nodes.append(declare_node)
    input_place_place = Variables.CURRENT_OUTPUT
    Variables.CHECKED_NODES[node["id"]]["input_node"] = input_place_place.getId()
    create_arc(input_place_place,declare_node,net)

    # create output node for following structure
    output = Place("Output" + node["kind"], next(Variables.ID_GEN) )
    net.nodes.append(output)
    Variables.CURRENT_OUTPUT = output
    create_arc(declare_node,output,net)
    Variables.CHECKED_NODES[node["id"]]["output_node"] = output.getId()
    
    Variables.LAST_PARENT = declare_node
    Variables.ID_MAIN_PARENT = node["id"]
       
def var_dcl(node, net: PetriNet):
    '''
    Process variables declared in DeclStmt
    ''' 
    variable = Place("varId_" + node["name"],node["id"])
    variable.setInitialMarking(1)
    net.nodes.append(variable)
    create_arc(Variables.LAST_PARENT,variable,net)

def decl_expr(ast,node, net: PetriNet):
    '''
    Process the Referenced nodes to functions or variables
    '''
    final_conect(ast,node,net)
    node_referenced = search_node_by_id(node["referencedDecl"]["id"],net)
    if node["referencedDecl"]["kind"] == Variables.FUNC_DECL:
       # in case the node is not created in the red(f.e printf)
        if node_referenced == None:
            node_referenced = Transition(node["referencedDecl"]["id"])
            net.nodes.append(node_referenced)
        else:
            # create a reference transition to mark the call of the function on the net 
            node_referenced = Transition(node["id"])
            net.nodes.append(node_referenced)

            out_aux = Place("out_refer", next(Variables.ID_GEN))
            net.nodes.append(out_aux)
            create_arc(node_referenced,out_aux,net)
            node_referenced2 = search_node_by_id(node["referencedDecl"]["id"],net)
            create_arc(out_aux,node_referenced2,net)

        if node["parent"] in {Variables.MAIN_COMPOUND,Variables.CURRENT_COMPOUND} :
            create_sec_tran(net)
        #if ast[Variables.LAST_PARENT.getId()]["kind"] not in Variables.CONTROL_TYPES:
            # in all the cases out of a control type the reference is a secuencial instruction
            # inside a condition of a control type the reference is a inside instruction 
        #    create_sec_tran(net)   

        create_arc(Variables.CURRENT_OUTPUT,node_referenced,net)
        mid_aux = Place("out_mid_x", next(Variables.ID_GEN))
        net.nodes.append(mid_aux)
        create_arc(node_referenced,mid_aux,net)

        Variables.CURRENT_OUTPUT = mid_aux
        Variables.LAST_PARENT = node_referenced    

    else:
        # in case its a variable, it always going to be delacre before so we do not need to
        # divide in two cases
        check = ast[Variables.ID_MAIN_PARENT]["inner"][0]
        if ast[node["parent"]]["kind"] == Variables.BINARY_OP:
            # this is the case when its the variable where the binary is going to save a value ( a = b)
            par_node = search_node_by_id(node["parent"],net)
            create_arc(par_node,node_referenced,net)
        
        elif ast[check]["kind"] not in Variables.OPERATORS and ast[Variables.ID_MAIN_PARENT]["kind"] in Variables.CONTROL_TYPES:
            # Case of control type condition f.e if (a) 
            tran_refer = Transition(node["id"])
            net.nodes.append(tran_refer)

            create_arc(Variables.CURRENT_OUTPUT,tran_refer,net)
            mid_out = Place("midIF", next(Variables.ID_GEN))
            net.nodes.append(mid_out)
            create_arc(tran_refer,mid_out,net)

            Variables.CURRENT_OUTPUT = mid_out

            # link with referenced node 
            create_arc(node_referenced, tran_refer,net)
        else:
            create_arc(node_referenced,Variables.LAST_PARENT,net)

    # save the reference for cases where multiple structures belongs to a condition of a control type
    # and its need only one for conections
    if Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["referenced_node"] == None:
        Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["referenced_node"] = node["referencedDecl"]["id"]

def literals(ast,node,net:PetriNet):
    '''
    Process nodes of integers, strings and characters
    '''
    final_conect(ast,node,net)
    literal = Place(node["kind"] + "_" + str(node["value"]),node["id"])
    literal.setInitialMarking(1)
    net.nodes.append(literal)
    create_arc(Variables.LAST_PARENT,literal,net)
    create_arc(literal,Variables.LAST_PARENT,net)
       
def operators( ast, node, net:PetriNet):
    '''
    Process binary and unary operators
    ''' 
    predecesor = ast[Variables.CURRENT_COMPOUND]["parent"]
    parent_kind = ast[node["parent"]]["kind"]
    
    if ast[Variables.ID_MAIN_PARENT]["kind"] != Variables.FOR_STMT or ast[predecesor]["kind"] == Variables.FOR_STMT:
        operator = Transition(node["id"])
        if parent_kind in Variables.CONTROL_TYPES:
            # its a operator inside the contorl condition
            create_sec_tran(net)
            create_arc(Variables.CURRENT_OUTPUT,operator,net)

            Variables.CHECKED_NODES[node["parent"]]["input_node"] = Variables.CURRENT_OUTPUT.getId()
            out_mid= Place("OutputInter",next(Variables.ID_GEN))
            net.nodes.append(out_mid)
            create_arc(operator,out_mid,net)

            Variables.CHECKED_NODES[node["parent"]]["referenced_node"] = node["id"]
        
            Variables.ID_MAIN_PARENT = node["parent"]
            Variables.CURRENT_OUTPUT = out_mid

            # parent for verification but no for drawing the net
            par_temp = Transition(node["parent"])
            Variables.LAST_PARENT = par_temp

        elif parent_kind == Variables.DECL_TYPES:
            # its an operator that saves the value in a "vardecl"
            nex_node = Place("nex_ob",next(Variables.ID_GEN))
            net.nodes.append(nex_node)
            create_arc(nex_node,Variables.LAST_PARENT,net)
            create_arc(operator,nex_node,net)

        elif parent_kind == Variables.DO_WHILE:
            # its the condition of a do while
            create_arc(Variables.CURRENT_OUTPUT,operator,net)
            out_op = Place("out_eval", next(Variables.ID_GEN))
            net.nodes.append(out_op)
            create_arc(operator,out_op,net)

            Variables.CURRENT_OUTPUT = out_op
            Variables.ID_MAIN_PARENT = node["parent"]   
        else:
            # default case for a normal use of an operator
            final_conect(ast,node,net)
            if node["parent"] in {Variables.MAIN_COMPOUND,Variables.CURRENT_COMPOUND} :
                create_sec_tran(net)
        
            Variables.CHECKED_NODES[node["id"]]["input_node"] = Variables.CURRENT_OUTPUT.getId()
            create_arc(Variables.CURRENT_OUTPUT,operator,net)

            output_p = Place("Output" + node["kind"],next(Variables.ID_GEN))
            net.nodes.append(output_p)
            Variables.CURRENT_OUTPUT = output_p
            Variables.CHECKED_NODES[node["id"]]["output_node"] == output_p.getId()

            create_arc(operator,output_p,net)

        Variables.LAST_PARENT = operator
        net.nodes.append(operator)

def for_loop(ast,node,net:PetriNet):
    '''
    Reset the current output for the output node of the previous For stmt
    '''
    final_conect(ast,node,net)
    # reset current compound for compound of for 
    Variables.CURRENT_COMPOUND = Variables.MAIN_COMPOUND
    if ast[Variables.ID_MAIN_PARENT]["kind"] == Variables.FOR_STMT:
        # save previous out for cases where the for is inside other for 
        prev_out = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["output_node"],net)
        Variables.CURRENT_OUTPUT = prev_out

    Variables.ID_MAIN_PARENT = node["id"]

'''
Function that manage the true or false branch of an If structure.
Create its respective transitions and arcs to complete the pattern. 
'''
def control_if_treatment(ast,node,net:PetriNet):
        Variables.ID_MAIN_PARENT = node["parent"]
        # if node is the second child of a ifstmt we identify it as the true branch
        if  ast[node["parent"]]["inner"][1] == node["id"]:
            # create a transition for the true branch
            t_true = Transition("t_true_"+ str(next(Variables.ID_GEN)))
            net.nodes.append(t_true)
            Variables.CHECKED_NODES[node["parent"]]["middle_output"] = Variables.CURRENT_OUTPUT.getId()
            create_arc(Variables.CURRENT_OUTPUT,t_true,net)

            '''node referenced of the eval stmt'''
            eval_node = search_node_by_id( Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["referenced_node"],net)

            # if the referenced node is a transition we need a place to link it 
            verify_object(eval_node,t_true,net)

            out_mid_true = Place("OuputTrueBranch", next(Variables.ID_GEN))
            net.nodes.append(out_mid_true)

            Variables.CURRENT_OUTPUT = out_mid_true            
            create_arc(t_true,out_mid_true,net)


        elif "hasElse" in ast[Variables.ID_MAIN_PARENT] and ast[Variables.ID_MAIN_PARENT]["inner"][2] == node["id"]:
            # it's the false branch of an if 
            # Create false transition 
            t_false = Transition("t_false_"+ str(next(Variables.ID_GEN)))
            net.nodes.append(t_false)
            Variables.CHECKED_NODES[node["parent"]]["output_node"] = Variables.CURRENT_OUTPUT.getId()
          
            # obtain mid place created in the true branch 
            # the false node has to begin in the same node 
            input_mid= search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["middle_output"], net)
            create_arc(input_mid,t_false,net)

            # retrive evaluation node referenced before
            eval_node = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["referenced_node"],net)
            verify_object(eval_node,t_false,net)
            
            out_false_mid = Place("OuputFalseBranch", next(Variables.ID_GEN))
            net.nodes.append(out_false_mid)
            create_arc(t_false,out_false_mid,net)

            Variables.CURRENT_OUTPUT = out_false_mid

def compound_control(ast, node,net:PetriNet):
    '''
    Manage all cases in base of which node belongs the compound. 
    The compound represents the action block of a structure
    '''
    parent_kind = ast[node["parent"]]["kind"] 
    if parent_kind == Variables.FUNC_DECL:
        # it's the main compound of the function
        Variables.MAIN_COMPOUND = node["id"]
    Variables.CURRENT_COMPOUND = node["id"]

    # parent for verification but no for drawing the net
    par_temp = Transition(node["id"])

    Variables.LAST_PARENT = par_temp
    
    if parent_kind == Variables.IF_STMT:
        control_if_treatment(ast,node,net)
    
    elif parent_kind == Variables.WHILE_STMT:
        # complete structure of a while stmt 
        in_out_par = Variables.CURRENT_OUTPUT

        # Create while transition 
        t_while = Transition("t_while" + str(next(Variables.ID_GEN)))
        net.nodes.append(t_while)
        create_arc(in_out_par,t_while,net)

        
        out_aux = Place("midOutwhile", next(Variables.ID_GEN))
        net.nodes.append(out_aux)

        Variables.CURRENT_OUTPUT = out_aux
        create_arc(t_while,out_aux,net)

        # Create end while transition 
        t_end_while = Transition("t_end_while" + str(next(Variables.ID_GEN)))
        net.nodes.append(t_end_while)
        create_arc(in_out_par,t_end_while,net)
        
        # retrieve evaluatoin node and connect to prevoius  transitions
        node_eval = search_node_by_id( Variables.CHECKED_NODES[node["parent"]]["referenced_node"],net)
        verify_object(node_eval,t_while,net)
        verify_object(node_eval,t_end_while,net)
        
        output_final = Place("finalOutputWhile", next(Variables.ID_GEN))
        net.nodes.append(output_final)
        create_arc(t_end_while,output_final,net)
        Variables.CHECKED_NODES[node["parent"]]["output_node"] = output_final.getId()

    elif parent_kind == Variables.DO_WHILE:
        # save information for do while pattern 
        Variables.CHECKED_NODES[node["parent"]]["input_node"] = Variables.CURRENT_OUTPUT.getId()
        Variables.ID_MAIN_PARENT = node["parent"]

    elif parent_kind == Variables.FOR_STMT:
        Variables.ID_MAIN_PARENT = node["parent"]    

        # create default transition of continuity 
        t_eval_con = Transition("t_eval_continues_" + str(next(Variables.ID_GEN)))
        net.nodes.append(t_eval_con)
        Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["input_node"] = Variables.CURRENT_OUTPUT.getId()
        create_arc(Variables.CURRENT_OUTPUT,t_eval_con,net)

        out_eval = Place("out_eval_", next(Variables.ID_GEN))
        net.nodes.append(out_eval)

        create_arc(t_eval_con,out_eval,net)
        Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["middle_output"] = out_eval.getId()

        cond_for = Place("for_cond",next(Variables.ID_GEN))
        net.nodes.append(cond_for)

        create_arc(t_eval_con,cond_for,net)
        create_arc(cond_for,t_eval_con,net)

        # Create end transition of the FOR structure
        t_end_for = Transition("t_end_for" + str(next(Variables.ID_GEN)))
        net.nodes.append(t_end_for)
        create_arc(cond_for,t_end_for,net)

        out_for_loop = Place("out_for",next(Variables.ID_GEN))
        net.nodes.append(out_for_loop)
       
        create_arc(t_end_for,out_for_loop,net)

        # Save information for current state
        Variables.CURRENT_OUTPUT = out_eval
        Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["output_node"] = out_for_loop.getId()

def return_stmt(ast,node, net: PetriNet):
    '''
    Process return type nodes
    '''
    final_conect(ast,node,net)
    if node["parent"] in {Variables.MAIN_COMPOUND,Variables.CURRENT_COMPOUND} :
        create_sec_tran(net)

    input = Variables.CURRENT_OUTPUT
    Variables.CHECKED_NODES[node["id"]]["input_node"] = input.getId()

    # Create a transition for the return stmt
    tran_rtn = Transition(node['id'])
    net.nodes.append(tran_rtn)
    create_arc(input,tran_rtn,net)

    # Create an output place for the return stmt
    output_rtn = Place("OutputRtn", next(Variables.ID_GEN))
    net.nodes.append(output_rtn)
    create_arc(tran_rtn,output_rtn,net)

    # Update global variables
    Variables.LAST_PARENT = tran_rtn
    Variables.CURRENT_OUTPUT = output_rtn
    Variables.CHECKED_NODES[node["id"]]["output_node"] = output_rtn.getId()



def classify_nodes(current_ast,node, net: PetriNet):
    '''
    Save checked nodes and launch the respective function
    Args:
        current_ast: the current abstract syntax tree
        node: the current node being processed
        net: the current PetriNet being constructed
    '''

    try:
        if not isinstance(current_ast,dict):
            raise TypeError("First argument, current_ast, has to be a dictionary")
        if not isinstance(node,dict):
            raise TypeError("Second argument, node, has to be a dictionary")
        if not isinstance(net,PetriNet):
            raise TypeError("Third argument, net, has to be a PetriNet object")
    except TypeError as e:
        print(e)

    if node["id"] not in Variables.CHECKED_NODES:
        Variables.CHECKED_NODES[node["id"]] = {"input_node": None, "output_node": None, "middle_output": None, "node_relev":None, "referenced_node": None}
        c = node["kind"]
        if c in Variables.FUNC_STRUCTS:
            func_struct_decl(current_ast,node,net)
        elif c in Variables.VAR_FUNC:
            parm_field_decl(current_ast,node,net)
        elif c == Variables.DECL_STMT:
            decl_stmt(current_ast, node,net)
        elif c == Variables.DECL_TYPES:
            var_dcl(node,net)
        elif c in Variables.OPERATORS:
            operators(current_ast,node, net)
        elif c == Variables.DECL_REFER: 
            decl_expr(current_ast,node ,net)
        elif c in Variables.LITERALS: 
           literals(current_ast,node, net)
        elif c == Variables.COMPOUND_STMT:
            compound_control(current_ast,node,net)
        elif c ==  Variables.RETURN_STMT :
            return_stmt(current_ast,node,net)
        elif c == Variables.FOR_STMT:
            for_loop(current_ast,node,net)
        elif c in Variables.CONTROL_TYPES:
            Variables.ID_MAIN_PARENT = node["id"]

