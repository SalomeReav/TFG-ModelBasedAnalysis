import random
import autopep8

from PetriNet import PetriNet 
from Place import Place  
from Transition import Transition 
from Arc import Arc 
from Variables import Variables
import Node 



'''List for checked nodes and last ouput place for connect figures'''
CHECKED_NODES = {}
LAST_OUTPUT_ID = 0 
LAST_PARENT_ID = 0


def search_node_by_id(id, net:PetriNet):
    for n in net.nodes:
        if  isinstance(n,Place) or isinstance(n,Transition):
            if n.getId() == id:
                return n 
    return None

def function_decl(ast,node,net: PetriNet):
    print("entro en func decl")
    global LAST_OUTPUT_ID,LAST_PARENT_ID

    #If node its the first function created we initialize the place mark
    if ast[node["parent"]]["kind"] == "TranslationUnitDecl":
        input_place = Place("input_placeFunction", LAST_OUTPUT_ID)
        input_place.setInitialMarking(1)
        net.nodes.append(input_place)
    else:
        input_place = search_node_by_id(LAST_OUTPUT_ID,net)
        
    transition_func = Transition(node["id"])
    net.nodes.append(transition_func)

    arc = Arc(0)
    arc.setSourceNode(input_place)
    arc.setTargetNode(transition_func)
    net.arcs.append(arc)

    #set arc for each node
    input_place.setSourceArc(arc)
    transition_func.setTargetArc(arc)


    LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1
    output = Place("OutputFunction", LAST_OUTPUT_ID)
    net.nodes.append(output)

    arc_trans_output = Arc(0)
    arc_trans_output.setSourceNode(transition_func)
    arc_trans_output.setTargetNode(output)
    net.arcs.append(arc_trans_output)

    transition_func.setSourceArc(arc_trans_output)
    output.setTargetArc(arc_trans_output)

    LAST_PARENT_ID = node["id"]

def parm_decl(ast,node,net:PetriNet):
    parameter = Place(node["name"],node["id"])
    net.nodes.append(parameter)

    parent_node = search_node_by_id(node["parent"],net)
    arc= Arc(0)
    arc.setSourceNode(parent_node)
    arc.setTargetNode(parameter)
    net.arcs.append(arc)

    parent_node.setSourceArc(arc)
    parameter.setTargetArc(arc)

    arc_parm_parent = Arc(0)
    arc_parm_parent.setSourceNode(parameter)
    arc_parm_parent.setTargetNode(parent_node)
    net.arcs.append(arc_parm_parent)

    parameter.setSourceArc(arc_parm_parent)
    parent_node.setTargetArc(arc_parm_parent)

def decl_stmt(ast,node, net: PetriNet):
    global LAST_OUTPUT_ID, LAST_PARENT_ID
    
    declare_node = Transition(node["id"])
    net.nodes.append(declare_node)

    input_place_place = search_node_by_id(LAST_OUTPUT_ID, net)

    arc_input_place_trans = Arc(0)    
    arc_input_place_trans.setSourceNode(input_place_place)
    arc_input_place_trans.setTargetNode(declare_node)
    net.arcs.append(arc_input_place_trans)

    input_place_place.setSourceArc(arc_input_place_trans)
    declare_node.setTargetArc(arc_input_place_trans)

    #creation of ouput node for following structure
    LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1
    output = Place("Ouput" + node["kind"], LAST_OUTPUT_ID )
    net.nodes.append(output)

    arc_tran_output = Arc(0)
    arc_tran_output.setSourceNode(declare_node)
    arc_tran_output.setTargetNode(output)
    net.arcs.append(arc_tran_output)

    declare_node.setSourceArc(arc_tran_output)
    output.setTargetArc(arc_tran_output)
    
    LAST_PARENT_ID = node["id"]
     
def var_dcl(node, net: PetriNet):
    global LAST_PARENT_ID

    variable = Place("varId_" + node["name"],node["id"])
    net.nodes.append(variable)

    parent = search_node_by_id(LAST_PARENT_ID,net)

    union = Arc(0)
    union.setSourceNode(parent)
    union.setTargetNode(variable)
    net.arcs.append(union)

    parent.setSourceArc(union)
    variable.setTargetArc(union)
    

def decl_expr(ast,node, net: PetriNet):
    global LAST_PARENT_ID,LAST_OUTPUT_ID

    if node["referencedDecl"]["kind"] == Variables.FUNC_DECL:
        '''EN ESTE CASO VER SI PONER ARCO A DEFINICION DE LA FUNCION'''
       
        ref_node_decl = Place("Reference",node["id"])
        net.nodes.append(ref_node_decl)
        
        '''AQUI HAY QUE DIFERENCIAR SI VIENE DE TRAN O PLACE, PARA CREAR SINO EL INPUT'''
        antecesor = ast[node["parent"]]["parent"]
        print(antecesor)
        anc_two = ast[antecesor]["parent"]
        anc_three = ast[anc_two]["parent"]
        print(anc_three)

        if ast[anc_three]["kind"] == Variables.BINARY_OP:
            input_place = search_node_by_id(anc_three,net)
            print("toy")
        else:

            input_place = search_node_by_id(LAST_PARENT_ID,net)
        

        arc_inp_ref = Arc(0)
        arc_inp_ref.setSourceNode(input_place)
        arc_inp_ref.setTargetNode(ref_node_decl)
        net.arcs.append(arc_inp_ref) 

        input_place.setSourceArc(arc_inp_ref)
        ref_node_decl.setTargetArc(arc_inp_ref)

        arc_ref_func = Arc(0)

        if node["referencedDecl"]["id"] in CHECKED_NODES:
            tran_refer = search_node_by_id(node["referencedDecl"]["id"],net)
            arc_ref_func.setSourceNode(ref_node_decl)
            arc_ref_func.setTargetNode(tran_refer)

            ref_node_decl.setSourceArc(arc_ref_func)
            tran_refer.setTargetArc(arc_ref_func)
        else:
            new_tran_func = Transition(node["referencedDecl"]["id"])
            net.nodes.append(new_tran_func)

            arc_ref_func.setSourceNode(ref_node_decl)
            arc_ref_func.setTargetNode(new_tran_func)

            ref_node_decl.setSourceArc(arc_ref_func)
            new_tran_func.setTargetArc(arc_ref_func)

            arc_new_conect = Arc(0)
            arc_new_conect.setSourceNode(new_tran_func)
            arc_new_conect.setTargetNode(ref_node_decl)
            net.arcs.append(arc_new_conect)

            new_tran_func.setSourceArc(arc_new_conect)
            ref_node_decl.setTargetArc(arc_new_conect)

            
        LAST_PARENT_ID = node["referencedDecl"]["id"]
        net.arcs.append(arc_ref_func)

    else:
        print("entro en declexpre")
        antecesor = ast[node["parent"]]["parent"]
        print(antecesor)
        anc_two = ast[antecesor]["parent"]
        anc_three = ast[anc_two]["parent"]
        print(anc_three)

        if ast[anc_three]["kind"] == Variables.BINARY_OP:
            target = search_node_by_id(anc_three,net)
            print("toy")
        else:

            target = search_node_by_id(LAST_PARENT_ID,net)
        
        source = search_node_by_id(node["referencedDecl"]["id"],net) 

        if source == None:
            #if the referenced variable does not exist yet create it and add to nodes list
            source = Place(node["referencedDecl"]["name"], node['referencedDecl']["id"])
            net.nodes.append(source)
        
        # arrow direction depends of type node
        arc_sour_targ = Arc(0)
        '''CONFIRMAR QUE ES NECESARIO HACER ESTA DIFERENCIA, NO QUE '''
        if node["referencedDecl"]["kind"] == Variables.DECL_TYPES:
            arc_sour_targ.setSourceNode(target)
            arc_sour_targ.setTargetNode(source)

            arc_targ_source = Arc(0)
            arc_targ_source.setSourceNode(source)
            arc_targ_source.setTargetNode(target)
            net.arcs.append(arc_targ_source)

            source.setSourceArc(arc_targ_source)
            target.setTargetArc(arc_targ_source)
            

            target.setSourceArc(arc_sour_targ)
            source.setTargetArc(arc_sour_targ)

        else:
            arc_sour_targ.setSourceNode(source)
            arc_sour_targ.setTargetNode(target)

            source.setSourceArc(arc_sour_targ)
            target.setTargetArc(arc_sour_targ)

        net.arcs.append(arc_sour_targ)

       

def literals(node,net:PetriNet):
    print("entro en integer")
    global LAST_PARENT_ID

    parent_node = search_node_by_id(LAST_PARENT_ID,net)

    literal = Place(node["kind"] + "_" + str(node["value"]),node["id"])
    net.nodes.append(literal)

    arc = Arc(0)
    arc.setSourceNode(parent_node)
    arc.setTargetNode(literal)
    net.arcs.append(arc)

    parent_node.setSourceArc(arc)
    literal.setTargetArc(arc)

    arc_lit_parent = Arc(0)
    arc_lit_parent.setSourceNode(literal)
    arc_lit_parent.setTargetNode(parent_node)        
    net.arcs.append(arc_lit_parent)

    literal.setSourceArc(arc_lit_parent)
    parent_node.setTargetArc(arc_lit_parent)
        

def binary_operator( ast, node, net:PetriNet):
    print("entro en primera parte ob")
    global LAST_OUTPUT_ID, LAST_PARENT_ID
    
    operator = Transition(node["id"])
   
    #in case its parent is an IF we need its own input_place
    if ast[node["parent"]]["kind"]== Variables.CONTROL_TYPES or  ast[node["parent"]]["kind"]== Variables.WHILE_STMT:
        print("en situacin de que padre sea if o while")
        
        out_tran_opb = Place("OutputToBO",random.randrange(1,100,1) + LAST_OUTPUT_ID)
        net.nodes.append(out_tran_opb)
        
        arc_to_opb = Arc(0)
        arc_to_opb.setSourceNode(out_tran_opb)
        arc_to_opb.setTargetNode(operator)
        net.arcs.append(arc_to_opb)

        out_tran_opb.setSourceArc(arc_to_opb)
        operator.setTargetArc(arc_to_opb)

        parent = search_node_by_id(node["parent"],net)

        arc_par_out = Arc(0)
        arc_par_out.setSourceNode(parent)
        arc_par_out.setTargetNode(out_tran_opb)
        net.arcs.append(arc_par_out)

        parent.setSourceArc(arc_par_out)
        out_tran_opb.setTargetArc(arc_par_out)

        '''PENDIENTE DE REVISAR PARA POSIBLE ELIMINACION'''
    elif ast[node["parent"]]["kind"]== Variables.DECL_TYPES:
        print("entro en ob zona de declstmt")
        '''in case its parent is a declaration'''
        dcl_parent = search_node_by_id(node["parent"],net)

        arc_par_dcl = Arc(0)
        arc_par_dcl.setSourceNode(operator)
        arc_par_dcl.setTargetNode(dcl_parent)
        '''NO ESTA CONECTADO EL ARCO AL MAIN PRINCIPAL'''
        net.arcs.append(arc_par_dcl)

        operator.setSourceArc(arc_par_dcl)
        dcl_parent.setTargetArc(arc_par_dcl)


    elif ast[node["parent"]]["kind"]== Variables.PAREN_EXPR:
        parent_node = search_node_by_id(LAST_PARENT_ID,net)

        out_par_ob = Place("ParenMidOB", LAST_OUTPUT_ID + random.randrange(1,1000,1))
        net.nodes.append(out_par_ob)

        arc_par_ob = Arc(0)
        arc_par_ob.setSourceNode(parent_node)
        arc_par_ob.setTargetNode(out_par_ob)
        net.arcs.append(arc_par_ob)

        parent_node.setSourceArc(arc_par_ob)
        out_par_ob.setTargetArc(arc_par_ob)

        arc_out_op =Arc(0)
        arc_out_op.setSourceNode(out_par_ob)
        arc_out_op.setTargetNode(operator)
        net.arcs.append(arc_out_op)

        out_par_ob.setSourceArc(arc_out_op)
        operator.setTargetArc(arc_out_op)

    elif ast[node["parent"]]["kind"]== Variables.DO_WHILE:
        
        in_mid = search_node_by_id(LAST_OUTPUT_ID,net)

        t_eval = Transition(node["id"])
        net.nodes.append(t_eval)

        arc_in_eval = Arc(0)
        arc_in_eval.setSourceNode(in_mid)
        arc_in_eval.setTargetNode(t_eval)
        net.arcs.append(arc_in_eval)

        in_mid.setSourceArc(arc_in_eval)
        t_eval.setTargetArc(arc_in_eval)

        '''Create two transitions black ones'''

        LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1 
        out_mid = Place("OutputFromEval",LAST_OUTPUT_ID)
        net.nodes.append(out_mid)

        arc_eval_mid = Arc(0)
        arc_eval_mid.setSourceNode(t_eval)
        arc_eval_mid.setTargetNode(out_mid)
        net.arcs.append(arc_eval_mid)

        t_eval.setSourceArc(arc_eval_mid)
        out_mid.setTargetArc(arc_eval_mid)

        t_end_do = Transition("t_end_do")
        net.nodes.append(t_end_do)

        arc_mid_end = Arc(0)
        arc_mid_end.setSourceNode(out_mid)
        arc_mid_end.setTargetNode(t_end_do)
        net.arcs.append(arc_mid_end)

        out_mid.setSourceArc(arc_mid_end)
        t_end_do.setTargetArc(arc_mid_end)

        t_do = Transition("t_do")
        net.nodes.append(t_do)

        arc_out_do = Arc(0)
        arc_out_do.setSourceNode(out_mid)
        arc_out_do.setTargetNode(t_do)
        net.arcs.append(arc_out_do)

        out_mid.setSourceArc(arc_out_do)
        t_do.setTargetArc(arc_out_do)

        '''arco de tdo to beggining'''

        node_parent = search_node_by_id(node["parent"],net)
    
        arc_target_parent = node_parent.getTargetArcs()
        print("estoy en ob de do while, en el gettargetarcs")

        if isinstance(arc_target_parent[0],Arc):
            node_source = arc_target_parent[0].getsourceNode()
            print("nodos de arco")
            print(node_source)
        
            arc_do_in = Arc(0)
            arc_do_in.setSourceNode(t_do)
            arc_do_in.setTargetNode(node_source)
            net.arcs.append(arc_do_in)

            t_do.setSourceArc(arc_do_in)

      

        #final ouput of all structure
        LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1 
        out_final_do = Place("FinalOuputDoWhile",LAST_OUTPUT_ID)
        net.nodes.append(out_final_do)

        arc_end_final = Arc(0)
        arc_end_final.setSourceNode(t_end_do)
        arc_end_final.setTargetNode(out_final_do)
        net.arcs.append(arc_end_final)

        t_end_do.setSourceArc(arc_end_final)
        out_final_do.setTargetArc(arc_end_final)


    else:
        
        input_place = search_node_by_id(LAST_OUTPUT_ID,net)
        arc_in_op = Arc(0)
        arc_in_op.setSourceNode(input_place)
        arc_in_op.setTargetNode(operator)
        net.arcs.append(arc_in_op)

        LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1 
        output_p = Place("Output" + node["kind"], LAST_OUTPUT_ID)
        net.nodes.append(output_p)

        arc_op_outp = Arc(0)
        arc_op_outp.setSourceNode(operator)
        arc_op_outp.setTargetNode(output_p)

        operator.setSourceArc(arc_op_outp)
        output_p.setTargetArc(arc_op_outp)

        net.arcs.append(arc_op_outp)
        print("salgo del ob delcompund")

    
    LAST_PARENT_ID = node["id"]
    net.nodes.append(operator)
    
def unary_operator(ast, node, net: PetriNet):
    global LAST_OUTPUT_ID, LAST_PARENT_ID

    #we use id of father's father
    antecesor= ast[node["parent"]]["parent"]
   
    tran_unary_op = Transition(node["id"])
    net.nodes.append(tran_unary_op)

    if ast[antecesor]["kind"] == Variables.WHILE_STMT:
        id_conector_place =  CHECKED_NODES[antecesor]["finalOutput"] 
        input_place_con = search_node_by_id(id_conector_place, net)

        output_tr = Place("Output" + node["kind"], LAST_OUTPUT_ID + random.randrange(1,1000,1))
    else:
        input_place_con = search_node_by_id(LAST_OUTPUT_ID, net)
        
        LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1
        output_tr = Place("Output" + node["kind"], LAST_OUTPUT_ID)
    
    arc_con_tran = Arc(0)
    arc_con_tran.setSourceNode(input_place_con)
    arc_con_tran.setTargetNode(tran_unary_op)
    net.arcs.append(arc_con_tran)

    input_place_con.setSourceArc(arc_con_tran)
    tran_unary_op.setTargetArc(arc_con_tran)
    
    net.nodes.append(output_tr)

    arc_tran_out = Arc(0)
    arc_tran_out.setSourceNode(tran_unary_op)
    arc_tran_out.setTargetNode(output_tr)
    net.arcs.append(arc_tran_out)

    tran_unary_op.setSourceArc(arc_tran_out)
    output_tr.setTargetArc(arc_tran_out)

    LAST_PARENT_ID = node["id"]

def if_stmt(ast, node, net: PetriNet):
    global LAST_PARENT_ID
    '''si este nodo if es un una rama de otro if principal, por ejemplo 
    en el caso de un ElseIf, es un if que consta dentro de la rama false de 
    otro if principal. Cuando esto ocurra lo que hay que hacer es enlazar el 
    if con el nodo ooutput del if principal'''
    if ast[node["parent"]]["kind"] == Variables.CONTROL_TYPES:

        id_last_out_parent = CHECKED_NODES[node["parent"]]["outputIf"] 
        out_parent = search_node_by_id(id_last_out_parent, net)
    else:
        global LAST_OUTPUT_ID
        out_parent = search_node_by_id(LAST_OUTPUT_ID,net)


    '''set the id of this node as Last parent'''
   
    t_eval = Transition(node["id"])
    net.nodes.append(t_eval)
    
    LAST_PARENT_ID = node["id"]

    arc_out_eval =Arc(0)
    arc_out_eval.setSourceNode(out_parent)
    arc_out_eval.setTargetNode(t_eval)
    net.arcs.append(arc_out_eval)

    out_parent.setSourceArc(arc_out_eval)
    t_eval.setTargetArc(arc_out_eval)

    LAST_OUTPUT_ID = LAST_OUTPUT_ID +1 
    output_mid_if = Place("Output" + node["kind"], LAST_OUTPUT_ID)
    net.nodes.append(output_mid_if)

    '''guardo en el nodo padre if, el id del ouput para luego en el nodo else
    buscar ese id y partir de ahi'''
    CHECKED_NODES[node["id"]]["outputIf"] = LAST_OUTPUT_ID

    arc_eval_out = Arc(0)
    arc_eval_out.setSourceNode(t_eval)
    arc_eval_out.setTargetNode(output_mid_if)
    net.arcs.append(arc_eval_out)

    t_eval.setSourceArc(arc_eval_out)
    output_mid_if.setTargetArc(arc_eval_out)

def while_stmt(node, net: PetriNet):
    global LAST_OUTPUT_ID, LAST_PARENT_ID

    tran_while = Transition(node["id"])
    net.nodes.append(tran_while)
    
    input_place = search_node_by_id(LAST_OUTPUT_ID,net)

    arc_in_tran = Arc(0)
    arc_in_tran.setSourceNode(input_place)
    arc_in_tran.setTargetNode(tran_while)
    net.arcs.append(arc_in_tran)

    input_place.setSourceArc(arc_in_tran)
    tran_while.setTargetArc(arc_in_tran)

    LAST_OUTPUT_ID = LAST_OUTPUT_ID +1
    out_mid= Place("OutputMidWhile",LAST_OUTPUT_ID)
    net.nodes.append(out_mid)

    CHECKED_NODES[node["id"]]["OutputIf"] = LAST_OUTPUT_ID


    arc_tran_mid = Arc(0)
    arc_tran_mid.setSourceNode(tran_while)
    arc_tran_mid.setTargetNode(out_mid)
    net.arcs.append(arc_tran_mid)

    tran_while.setSourceArc(arc_tran_mid)
    out_mid.setTargetArc(arc_tran_mid)

    t_end_while = Transition("t_end_while" + str(LAST_OUTPUT_ID + random.randrange(1,1000,1)))
    net.nodes.append(t_end_while)

    arc_mid_end = Arc(0)
    arc_mid_end.setSourceNode(out_mid)
    arc_mid_end.setTargetNode(t_end_while)
    net.arcs.append(arc_mid_end)

    out_mid.setSourceArc(arc_mid_end)
    t_end_while.setTargetArc(arc_mid_end)

    LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1 
    output_final = Place("finalOutputWhile", LAST_OUTPUT_ID)
    net.nodes.append(output_final)

    arc_end_final= Arc(0)
    arc_end_final.setSourceNode(t_end_while)
    arc_end_final.setTargetNode(output_final)
    net.arcs.append(arc_end_final)

    t_end_while.setSourceArc(arc_end_final)
    output_final.setTargetArc(arc_end_final)

    LAST_PARENT_ID =  node["id"]

def do_while(node,net:PetriNet):
    global LAST_OUTPUT_ID,LAST_PARENT_ID
    
    input_place = search_node_by_id(LAST_OUTPUT_ID,net)

    tran_do_while = Transition(node["id"])
    net.nodes.append(tran_do_while)

    arc_in_do = Arc(0)
    arc_in_do.setSourceNode(input_place)
    arc_in_do.setTargetNode(tran_do_while)
    net.arcs.append(arc_in_do)

    input_place.setSourceArc(arc_in_do)
    tran_do_while.setTargetArc(arc_in_do)
    
    LAST_OUTPUT_ID = LAST_OUTPUT_ID +1
    out_mid_do = Place("OutputMidDoWhile",LAST_OUTPUT_ID)  
    net.nodes.append(out_mid_do)

    arc_do_mid = Arc(0)
    arc_do_mid.setSourceNode(tran_do_while)
    arc_do_mid.setTargetNode(out_mid_do)
    net.arcs.append(arc_do_mid)

    tran_do_while.setSourceArc(arc_do_mid)
    out_mid_do.setTargetArc(arc_do_mid)
    
    LAST_PARENT_ID= node["id"]


def compound_control(ast, node,net:PetriNet):
    global LAST_OUTPUT_ID, LAST_PARENT_ID

    if ast[node["parent"]]["kind"] == Variables.CONTROL_TYPES:

        #if node is the second child of a ifstmt we identify it as the true branch
        if  ast[node["parent"]]["inner"][1] == node["id"]:

            t_true = Transition("t_true_"+ str(LAST_OUTPUT_ID))
            net.nodes.append(t_true)
            
            input_place = search_node_by_id(LAST_OUTPUT_ID, net)

            arc_in_true = Arc(0)
            arc_in_true.setSourceNode(input_place)
            arc_in_true.setTargetNode(t_true)
            net.arcs.append(arc_in_true)

            input_place.setSourceArc(arc_in_true)
            t_true.setTargetArc(arc_in_true)

            LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1
            out_mid_true = Place("OuputTrueBranch", LAST_OUTPUT_ID)
            net.nodes.append(out_mid_true)
            
            arc_true_mid=Arc(0)
            arc_true_mid.setSourceNode(t_true)
            arc_true_mid.setTargetNode(out_mid_true)
            net.arcs.append(arc_true_mid)

            t_true.setSourceArc(arc_true_mid)
            out_mid_true.setTargetArc(arc_true_mid)

            action_block = Transition(node["id"])
            net.nodes.append(action_block)

            arc_mid_act = Arc(0)
            arc_mid_act.setSourceNode(out_mid_true)
            arc_mid_act.setTargetNode(action_block)
            net.arcs.append(arc_mid_act)

            out_mid_true.setSourceArc(arc_mid_act)
            action_block.setTargetArc(arc_mid_act)

            '''En caso de que sean if anidados cierra todo en un solo output'''
            if_parent = ast[node["parent"]]["parent"]
            if ast[if_parent]["kind"] == Variables.CONTROL_TYPES:
                out_final = CHECKED_NODES[if_parent]["finalOutput"]
                output_if = search_node_by_id(out_final, net)

                '''guardo el lugar de cierre de ifs'''
                CHECKED_NODES[node["parent"]]["finalOutput"] = out_final
            else:
                LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1
                output_if = Place("Output_If", LAST_OUTPUT_ID)
                net.nodes.append(output_if)

                '''guardo el lugar de cierre de ifs'''
                CHECKED_NODES[node["parent"]]["finalOutput"] = LAST_OUTPUT_ID


            
            LAST_PARENT_ID = node["id"]
        elif ast[node["parent"]]["hasElse"] == True:

            t_false = Transition("t_false_"+ str(LAST_OUTPUT_ID))
            net.nodes.append(t_false)
            id_last_Out_Par = CHECKED_NODES[node["parent"]]["outputIf"] 
          
            input_out_par= search_node_by_id(id_last_Out_Par, net)

            arc_in_false = Arc(0)
            arc_in_false.setSourceNode(input_out_par)
            arc_in_false.setTargetNode(t_false)
            net.arcs.append(arc_in_false)

            input_out_par.setSourceArc(arc_in_false)
            t_false.setTargetArc(arc_in_false)

            LAST_OUTPUT_ID = LAST_OUTPUT_ID + 1
            out_false_mid = Place("OuputFalseBranch", LAST_OUTPUT_ID)
            net.nodes.append(out_false_mid)
            
            arc_false_out=Arc(0)
            arc_false_out.setSourceNode(t_false)
            arc_false_out.setTargetNode(out_false_mid)
            net.arcs.append(arc_false_out)

            t_false.setSourceArc(arc_false_out)
            out_false_mid.setTargetArc(arc_false_out)

            action_block = Transition(node["id"])
            net.nodes.append(action_block)

            arc_false_act = Arc(0)
            arc_false_act.setSourceNode(out_false_mid)
            arc_false_act.setTargetNode(action_block)
            net.arcs.append(arc_false_act)

            out_false_mid.setSourceArc(arc_false_act)
            action_block.setTargetArc(arc_false_act)
  
            LAST_PARENT_ID = node["id"]
           
            id_close_output = CHECKED_NODES[node["parent"]]["finalOutput"]
            output_if = search_node_by_id(id_close_output, net) 
    

        arc_act_out = Arc(0)
        arc_act_out.setSourceNode(action_block)
        arc_act_out.setTargetNode(output_if)
        net.arcs.append(arc_act_out)

        action_block.setSourceArc(arc_act_out)
        output_if.setTargetArc(arc_act_out)
    
    elif ast[node["parent"]]["kind"] == Variables.WHILE_STMT:
        
        in_out_par = CHECKED_NODES[node["parent"]]["OutputIf"]
        input_place = search_node_by_id(in_out_par,net)

        t_while = Transition("t_while" + str(LAST_OUTPUT_ID))
        net.nodes.append(t_while)

        arc_in_while = Arc(0)
        arc_in_while.setSourceNode(input_place)
        arc_in_while.setTargetNode(t_while)
        net.arcs.append(arc_in_while)

        input_place.setSourceArc(arc_in_while)
        t_while.setTargetArc(arc_in_while)

        '''output_fin = Place("OutputWhile_Action", LAST_OUTPUT_ID + random.randrange(1,1000,1))
        net.nodes.append(output_fin)

        arc_while_fin = Arc(0)
        arc_while_fin.setSourceNode(t_while)
        arc_while_fin.setTargetNode(output_fin)
        net.arcs.append(arc_while_fin)

        t_while.setSourceArc(arc_while_fin)
        output_fin.setTargetArc(arc_while_fin)

        action_block_while = Transition(node["id"])
        net.nodes.append(action_block_while)

        arc_out_act = Arc(0)
        arc_out_act.setSourceNode(output_fin)
        arc_out_act.setTargetNode(action_block_while)
        net.arcs.append(arc_out_act) 

        output_fin.setSourceArc(arc_out_act)
        action_block_while.setTargetArc(arc_out_act)'''

        id_aux = LAST_OUTPUT_ID + random.randrange(1,1000,1)
        out_aux = Place("midOutwhile", id_aux)
        net.nodes.append(out_aux)

        arc_act_aux = Arc(0)
        arc_act_aux.setSourceNode(t_while)
        arc_act_aux.setTargetNode(out_aux)
        net.arcs.append(arc_act_aux)

        t_while.setSourceArc(arc_act_aux)
        out_aux.setTargetArc(arc_act_aux)

        CHECKED_NODES[node["parent"]]["finalOutput"] = id_aux

        #LAST_PARENT_ID = node["id"]


def return_stmt(node, net: PetriNet):
    global LAST_OUTPUT_ID, LAST_PARENT_ID

    tran_rtn = Transition(node['id'])
    net.nodes.append(tran_rtn)

    input = search_node_by_id(LAST_OUTPUT_ID,net)

    arc_in_rtn = Arc(0)
    arc_in_rtn.setSourceNode(input)
    arc_in_rtn.setTargetNode(tran_rtn)
    net.arcs.append(arc_in_rtn)

    input.setSourceArc(arc_in_rtn)
    tran_rtn.setTargetArc(arc_in_rtn)

    LAST_OUTPUT_ID = LAST_OUTPUT_ID +1
    output_rtn = Place("OutputRtn", LAST_OUTPUT_ID)
    net.nodes.append(output_rtn)

    arc_rtn_out = Arc(0)
    arc_rtn_out.setSourceNode(tran_rtn)
    arc_rtn_out.setTargetNode(output_rtn)
    net.arcs.append(arc_rtn_out)

    tran_rtn.setSourceArc(arc_rtn_out)
    output_rtn.setTargetArc(arc_rtn_out)

    LAST_PARENT_ID = node["id"]


#guardar nodos ya recorridos, dic
def classify_nodes(current_ast,node, net: PetriNet):
    global CHECKED_NODES
    if node["id"] not in CHECKED_NODES:
        '''CAMBIAR AQUI EL NOMBRE DE LOS NODOS A GUARDAR PARA QUE SEA UNIVERSAL'''
        CHECKED_NODES[node["id"]] = {"type": node["kind"],"outputIf": None, "finalOutput":None}
        c = node["kind"]
        if c == Variables.FUNC_DECL:
            function_decl(current_ast,node,net)
        elif c == Variables.PARMVAR_DECL:
            parm_decl(current_ast,node,net)
        elif c == Variables.DECL_STMT:
            decl_stmt(current_ast, node,net)
        elif c == Variables.DECL_TYPES:
            var_dcl(node,net)
        elif c == Variables.BINARY_OP:
            binary_operator(current_ast,node, net)
        elif c == Variables.UNARY_OP:
            unary_operator(current_ast,node,net)
        elif c == Variables.DECL_REFER: 
            decl_expr(current_ast,node ,net)
        elif c == Variables.INTEGER_LITERAL: 
           literals(node, net)
        elif c == Variables.CONTROL_TYPES:
            if_stmt(current_ast,node,net)
        elif c == Variables.COMPOUND_STMT:
            compound_control(current_ast,node,net)
        elif c == Variables.STRING_LITERAL:
            literals(node,net)
        elif c ==  Variables.RETURN_STMT :
            return_stmt(node,net)
        elif c == Variables.CHARACTER_LITERAL:
            literals(node,net)
        elif c == Variables.WHILE_STMT:
            while_stmt(node,net)
        elif c == Variables.DO_WHILE:
            do_while(node,net)

