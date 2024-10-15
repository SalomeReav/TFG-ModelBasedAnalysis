import random
import autopep8

from PetriNet import PetriNet 
from Place import Place  
from Transition import Transition 
from Arc import Arc 
from Variables import Variables
import Node 


'''generate next id for conector places'''
def generate_id_conec():
    id = 0
    while True:
        yield id
        id += 1
        if id > 1000:
            break


def search_node_by_id(id, net:PetriNet):
    for n in net.nodes:
        if  isinstance(n,Place) or isinstance(n,Transition):
            if n.getId() == id:
                return n 
    return None

def create_arc(first_node,second_node,net: PetriNet,num):
    arc = Arc(num)
    arc.setSourceNode(first_node)
    arc.setTargetNode(second_node)
    net.arcs.append(arc)
    
def create_sec_tran(net: PetriNet):
    tran_black = Transition("t_sec_black" + str(next(Variables.ID_GEN)))
    net.nodes.append(tran_black)

    nex_out = Place("out_con",next(Variables.ID_GEN))
    net.nodes.append(nex_out)

    create_arc(Variables.CURRENT_OUTPUT,tran_black,net,0)

    create_arc(tran_black,nex_out,net,0)

    Variables.CURRENT_OUTPUT = nex_out


def function_decl(ast,node,net: PetriNet):
    print("entro en func decl")
  
    #If node its the first function created we initialize the place mark
    if ast[node["parent"]]["inner"][0] == node["id"]:
        
        input_place = Place("input_placeFunction", next(Variables.ID_GEN) )
        input_place.setInitialMarking(1)
        net.nodes.append(input_place)
    else:
        #PARTE DELICADA REVISAR CONCATENACION DE ESTOS OBJETOS. 
        #sirve solo con currento output o se necesita el output
        input_place = Variables.CURRENT_OUTPUT

    Variables.CHECKED_NODES[node["id"]]["input_node"] = input_place.getId()
        
    transition_func = Transition(node["id"])
    net.nodes.append(transition_func)

    create_arc(input_place,transition_func,net,0)

    output = Place("OutputInter", next(Variables.ID_GEN))
    net.nodes.append(output)

    Variables.CHECKED_NODES[node["id"]]["output_node"] = output.getId()
    create_arc(transition_func,output,net,0)

    Variables.CURRENT_OUTPUT = output

    Variables.LAST_PARENT= transition_func
    Variables.ID_MAIN_PARENT = node["id"]


def parm_decl(ast,node,net:PetriNet):
    parameter = Place(node["name"],node["id"])
    net.nodes.append(parameter)

    create_arc(Variables.LAST_PARENT,parameter,net,0)

    create_arc(parameter,Variables.LAST_PARENT,net,0)


def decl_stmt(ast,node, net: PetriNet):

    if node["parent"] == Variables.MAIN_COMPOUND:
        if ast[Variables.ID_MAIN_PARENT]["kind"] == Variables.WHILE_STMT:
            repeat = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["input_node"],net)
            end = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["output_node"],net)
            create_arc(Variables.LAST_PARENT, repeat,net,0)
            Variables.CURRENT_OUTPUT = end
        elif ast[Variables.ID_MAIN_PARENT]["kind"] == Variables.IF_STMT and len(ast[Variables.ID_MAIN_PARENT]["inner"]) > 2:
            if Variables.CURRENT_COMPOUND == ast[Variables.ID_MAIN_PARENT]["inner"][2]:
                #false branch
                end = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["output_node"],net)
                print("dentro de uo,en if")
                print(end)
                create_arc(Variables.LAST_PARENT, end,net,0)
                Variables.CURRENT_OUTPUT = end
    
    if node["parent"] == Variables.MAIN_COMPOUND or node["parent"] == Variables.CURRENT_COMPOUND :
        create_sec_tran(net)

    declare_node = Transition(node["id"])
    net.nodes.append(declare_node)

    input_place_place = Variables.CURRENT_OUTPUT
    Variables.CHECKED_NODES[node["id"]]["input_node"] = input_place_place.getId()

    create_arc(input_place_place,declare_node,net,0)

    #creation of ouput node for following structure

    output = Place("Output" + node["kind"], next(Variables.ID_GEN) )
    net.nodes.append(output)
    Variables.CURRENT_OUTPUT = output

    Variables.CHECKED_NODES[node["id"]]["output_node"] = output.getId()

    create_arc(declare_node,output,net,0)
    
    Variables.LAST_PARENT = declare_node
    Variables.ID_MAIN_PARENT = node["id"]

    
     
def var_dcl(node, net: PetriNet):

    variable = Place("varId_" + node["name"],node["id"])
    net.nodes.append(variable)

    create_arc(Variables.LAST_PARENT,variable,net,0)


def decl_expr(ast,node, net: PetriNet):
    #PENSAR SI UNIFICAR EL CREAR EL OUTPUT, EN CASO DE QUE YA EXISTA NO CREARLO 
    #ASI ME AHORRO ESE CODIGO EN LAS TRES PARETES SIGUIENTES DE LA CREACION DEL OUPUT POTQUE SI TE FIJA
    #SE REPITE EN LOS TRES CASOS 
    print("entro EN DEcl exprerefe")
    node_referenced = search_node_by_id(node["referencedDecl"]["id"],net)
    if node["referencedDecl"]["kind"] == Variables.FUNC_DECL:
       #in case the node is not created in the red(f.e printf)
        if node_referenced == None:
            node_referenced = Transition(node["referencedDecl"]["id"])
            net.nodes.append(node_referenced)
        else:
            node_referenced = Transition(node["id"])
            net.nodes.append(node_referenced)

            out_aux = Place("out_refer", next(Variables.ID_GEN))
            net.nodes.append(out_aux)

            create_arc(node_referenced,out_aux,net,0)

            node_referenced2 = search_node_by_id(node["referencedDecl"]["id"],net)
            create_arc(out_aux,node_referenced2,net,0)


        if ast[Variables.LAST_PARENT.getId()]["kind"] not in Variables.CONTROL_TYPES:
            #case of reference inside of a control type compound 
            #decido que en el caso de funciones referenciadas, no se concatenaran una dentro de otra
            #asi que siempre seran instrucciones secuenciales respecto a lo anterior. 
            create_sec_tran(net)   

        create_arc(Variables.CURRENT_OUTPUT,node_referenced,net,0)
    
        mid_aux = Place("out_mid_x", next(Variables.ID_GEN))
        net.nodes.append(mid_aux)

        create_arc(node_referenced,mid_aux,net,0)

        Variables.CURRENT_OUTPUT = mid_aux

        Variables.LAST_PARENT = node_referenced    

    else:
        '''esto es porque si se da el caso, significa que es un = y que este primer hijo Refer
        es la variable donde se guarda, entonces el arco es en direccion de salida desde 
        el ob'''
        #in case its a variable, it always going to be delacre before so we do not need to
        #divide in two cases
        check = ast[Variables.ID_MAIN_PARENT]["inner"][0]
        if ast[node["parent"]]["kind"] == Variables.BINARY_OP:
            #this is the case when its the variable where the binary is going to save a value ( a = b)
            par_node = search_node_by_id(node["parent"],net)
            create_arc(par_node,node_referenced,net,0)
            print("en decl expr de var")
            print(Variables.ID_MAIN_PARENT)
        
        elif ast[check]["kind"] not in Variables.OPERATORS and ast[Variables.ID_MAIN_PARENT]["kind"] in Variables.CONTROL_TYPES:
            print("ESTOY EN DECL EXPR DE CONTROL TYPES")
            print(Variables.ID_MAIN_PARENT)
            #its the csondition of the control type f.e if (a) 
            tran_refer = Transition(node["id"])
            net.nodes.append(tran_refer)

            create_arc(Variables.CURRENT_OUTPUT,tran_refer,net,0)
            mid_out = Place("midIF", next(Variables.ID_GEN))
            net.nodes.append(mid_out)
            create_arc(tran_refer,mid_out,net,0)

            Variables.CURRENT_OUTPUT = mid_out

            #link with referenced node 
            create_arc(node_referenced, tran_refer,net,0)
        else:
            print("ARCO NROMAL REFEREncia")
            create_arc(node_referenced,Variables.LAST_PARENT,net,0)

    #para el caso en que la condicion son muchos ob, o cualquier instruccion que use como referencia
    # la primera esrtructura para los nodos referencia de los cnotrol type    
    if Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["referenced_node"] == None:
        Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["referenced_node"] = node["referencedDecl"]["id"]


def literals(node,net:PetriNet):

    print("entro en literal")
    literal = Place(node["kind"] + "_" + str(node["value"]),node["id"])
    net.nodes.append(literal)

    create_arc(Variables.LAST_PARENT,literal,net,0)

    create_arc(literal,Variables.LAST_PARENT,net,0)

        
def operators( ast, node, net:PetriNet):
    print("entro en primera parte ob")
    
    operator = Transition(node["id"])
    #aqui se puede poner compronnacion con variable control types ya que hemos quitadop el do while del array, osea ponerr if node[] in control types
    if ast[node["parent"]]["kind"]== Variables.WHILE_STMT or ast[node["parent"]]["kind"]== Variables.IF_STMT:  
        print("en situacin de que padre sea if o while")
        create_sec_tran(net)
        create_arc(Variables.CURRENT_OUTPUT,operator,net,0)

        Variables.CHECKED_NODES[node["parent"]]["input_node"] = Variables.CURRENT_OUTPUT.getId()
        id_next = next(Variables.ID_GEN)
        out_mid= Place("OutputInter",id_next)
        net.nodes.append(out_mid)

        create_arc(operator,out_mid,net,0)

        Variables.CHECKED_NODES[node["parent"]]["referenced_node"] = node["id"]
    
        Variables.ID_MAIN_PARENT = node["parent"]
        Variables.CURRENT_OUTPUT = out_mid

            #parent for verification but no for drawing the net
        par_temp = Transition(node["parent"])
            #unificar esto dentro del bo de while asi me quito una funcinoaqui
            #en ob de wile e if juntas las dos cosas para hcaer solo un if 
        Variables.LAST_PARENT = par_temp
        print(Variables.LAST_PARENT)


    elif ast[node["parent"]]["kind"]== Variables.DECL_TYPES:
        print("entro en ob zona de declstmt")
        '''in case its parent is a declaration'''

        nex_node = Place("nex_ob",next(Variables.ID_GEN))
        net.nodes.append(nex_node)
        
        create_arc(nex_node,Variables.LAST_PARENT,net,0)

        create_arc(operator,nex_node,net,0)


    elif ast[node["parent"]]["kind"] == Variables.DO_WHILE:
        print("entro en ob zona de do while")

        create_arc(Variables.CURRENT_OUTPUT,operator,net,0)

        out_op = Place("out_eval", next(Variables.ID_GEN))
        net.nodes.append(out_op)
        #Variables.CHECKED_NODES[node["parent"]]["referenced_node"] = node["id"]

        create_arc(operator,out_op,net,0)

        Variables.CURRENT_OUTPUT = out_op

        Variables.ID_MAIN_PARENT = node["parent"]

    else:
        if node["parent"] == Variables.MAIN_COMPOUND:
            if ast[Variables.ID_MAIN_PARENT]["kind"] == Variables.WHILE_STMT:
                repeat = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["input_node"],net)
                end = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["output_node"],net)
                create_arc(Variables.LAST_PARENT, repeat,net,0)
                Variables.CURRENT_OUTPUT = end
            elif ast[Variables.ID_MAIN_PARENT]["kind"] == Variables.IF_STMT and len(ast[Variables.ID_MAIN_PARENT]["inner"]) > 2:
                if Variables.CURRENT_COMPOUND == ast[Variables.ID_MAIN_PARENT]["inner"][2]:
                    #false branch
                    end = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["output_node"],net)
                    print("dentro de uo,en if")
                    print(end)
                    create_arc(Variables.LAST_PARENT, end,net,0)
                    Variables.CURRENT_OUTPUT = end

        
        if node["parent"] == Variables.MAIN_COMPOUND or node["parent"] == Variables.CURRENT_COMPOUND :
            create_sec_tran(net)
    
        Variables.CHECKED_NODES[node["id"]]["input_node"] = Variables.CURRENT_OUTPUT.getId()
        create_arc(Variables.CURRENT_OUTPUT,operator,net,0)

        output_p = Place("Output" + node["kind"],next(Variables.ID_GEN))
        net.nodes.append(output_p)
        Variables.CURRENT_OUTPUT = output_p
        Variables.CHECKED_NODES[node["id"]]["output_node"] == output_p.getId()

        create_arc(operator,output_p,net,0)
        print("salgo del ob delcompund")

        if ast[Variables.ID_MAIN_PARENT]["kind"] == Variables.DO_WHILE and node["parent"] == Variables.MAIN_COMPOUND:
            t_end_do = Transition("t_end_do" + str(next(Variables.ID_GEN)))
            net.nodes.append(t_end_do)

            ref_node = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["referenced_node"],net)
            create_arc(Variables.CURRENT_OUTPUT,t_end_do,net,0)
            create_arc(t_end_do,ref_node,net,0)

            t_do = Transition("t_do" + str(next(Variables.ID_GEN)))
            net.nodes.append(t_do)
            
            create_arc(Variables.CURRENT_OUTPUT,t_do,net,0)
            create_arc(t_do,ref_node,net,1)

            input_node = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["input_node"],net)
            create_arc(t_do,input_node,net,0)

            output_do = Place("output_do",next(Variables.ID_GEN))
            net.nodes.append(output_do)

            create_arc(t_end_do,output_do,net,0)
            Variables.CURRENT_OUTPUT = output_do    

    
    Variables.LAST_PARENT = operator
    net.nodes.append(operator)

def compound_control(ast, node,net:PetriNet):

    if ast[node["parent"]]["kind"] == Variables.FUNC_DECL:
        #its the main compound of the function
        Variables.MAIN_COMPOUND = node["id"]
        Variables.CURRENT_COMPOUND = node["id"]
    else:    
        Variables.CURRENT_COMPOUND = node["id"]
    
    #parent for verification but no for drawing the net
    par_temp = Transition(node["id"])

    Variables.LAST_PARENT = par_temp
    if ast[node["parent"]]["kind"] == Variables.IF_STMT:
        print("DENTRO DE CMPND DE IF")

        #if node is the second child of a ifstmt we identify it as the true branch
        if  ast[node["parent"]]["inner"][1] == node["id"]:

            t_true = Transition("t_true_"+ str(next(Variables.ID_GEN)))
            net.nodes.append(t_true)
            
            Variables.CHECKED_NODES[node["parent"]]["middle_output"] = Variables.CURRENT_OUTPUT.getId()
            
            create_arc(Variables.CURRENT_OUTPUT,t_true,net,0)

            '''node referenced of the eval stmt'''
            eval_node = search_node_by_id( Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["referenced_node"],net)

            if isinstance(eval_node, Transition):
                out_ax_t = Place("out_mid_t_ref", next(Variables.ID_GEN))
                net.nodes.append(out_ax_t)
                create_arc(t_true,out_ax_t,net,0)

                create_arc(out_ax_t,eval_node,net,0)
            else:
                 create_arc(t_true,eval_node,net,0)

            out_mid_true = Place("OuputTrueBranch", next(Variables.ID_GEN))
            net.nodes.append(out_mid_true)

            Variables.CURRENT_OUTPUT = out_mid_true
            print(out_mid_true)
            
            create_arc(t_true,out_mid_true,net,0)

        elif "hasElse" in ast[Variables.ID_MAIN_PARENT] and ast[Variables.ID_MAIN_PARENT]["inner"][2] == node["id"]:
            #its the false branch of an if 

            t_false = Transition("t_false_"+ str(next(Variables.ID_GEN)))
            net.nodes.append(t_false)
           
            Variables.CHECKED_NODES[node["parent"]]["output_node"] = Variables.CURRENT_OUTPUT.getId()
          
            input_mid= search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["middle_output"], net)
            print("dentro de nodo false de if")
            print(input_mid)
            print(Variables.ID_MAIN_PARENT)
            create_arc(input_mid,t_false,net,0)

            eval_node = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["referenced_node"],net)
            #in case its a transittion we cannot link a tr with a tr, so we need a intermedate place 
            if isinstance(eval_node, Transition):
                out_ax_t = Place("out_mid_t_ref", next(Variables.ID_GEN))
                net.nodes.append(out_ax_t)
                create_arc(t_false,out_ax_t,net,0)

                create_arc(out_ax_t,eval_node,net,0)
            else:
                 create_arc(t_false,eval_node,net,0)
            out_false_mid = Place("OuputFalseBranch", next(Variables.ID_GEN))
            net.nodes.append(out_false_mid)
            
            create_arc(t_false,out_false_mid,net,0)

            Variables.CURRENT_OUTPUT = out_false_mid
    
    elif ast[node["parent"]]["kind"] == Variables.WHILE_STMT:
        
        in_out_par = Variables.CURRENT_OUTPUT
        print(in_out_par)

        t_while = Transition("t_while" + str(next(Variables.ID_GEN)))
        net.nodes.append(t_while)

        create_arc(in_out_par,t_while,net,0)

        node_eval = search_node_by_id( Variables.CHECKED_NODES[node["parent"]]["referenced_node"],net)


        out_aux = Place("midOutwhile", next(Variables.ID_GEN))
        net.nodes.append(out_aux)

        Variables.CURRENT_OUTPUT = out_aux

        create_arc(t_while,out_aux,net,0)

        t_end_while = Transition("t_end_while" + str(next(Variables.ID_GEN)))
        net.nodes.append(t_end_while)

        create_arc(in_out_par,t_end_while,net,0)
        
        if isinstance(node_eval, Transition):
                out_ax_t = Place("out_mid_wh_ref", next(Variables.ID_GEN))
                net.nodes.append(out_ax_t)
                create_arc(t_while,out_ax_t,net,0)
                create_arc(t_end_while,out_ax_t,net,0)

                create_arc(out_ax_t,node_eval,net,0)
                create_arc(out_ax_t,node_eval,net,0)
        else:
                create_arc(t_while,node_eval,net,0)
        
        output_final = Place("finalOutputWhile", next(Variables.ID_GEN))
        net.nodes.append(output_final)

        Variables.CHECKED_NODES[node["parent"]]["output_node"] = output_final.getId()

        create_arc(t_end_while,output_final,net,0)
    elif ast[node["parent"]]["kind"] == Variables.DO_WHILE:
        print("estoy dentro de compound do while")
        Variables.CHECKED_NODES[node["parent"]]["input_node"] = Variables.CURRENT_OUTPUT.getId()
        
        Variables.ID_MAIN_PARENT = node["parent"]


       


def return_stmt(ast,node, net: PetriNet):
    print("DENTRO DE RETURN")

    if node["parent"] == Variables.MAIN_COMPOUND:
        if ast[Variables.ID_MAIN_PARENT]["kind"] == Variables.WHILE_STMT:
            repeat = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["input_node"],net)
            end = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["output_node"],net)
            create_arc(Variables.LAST_PARENT, repeat,net,0)
            Variables.CURRENT_OUTPUT = end
        elif ast[Variables.ID_MAIN_PARENT]["kind"] == Variables.IF_STMT and len(ast[Variables.ID_MAIN_PARENT]["inner"]) > 2:
            if Variables.CURRENT_COMPOUND == ast[Variables.ID_MAIN_PARENT]["inner"][2]:
                #false branch
                end = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["output_node"],net)
                print("dentro de uo,en if")
                print(end)
                create_arc(Variables.LAST_PARENT, end,net,0)
                Variables.CURRENT_OUTPUT = end
        elif ast[Variables.ID_MAIN_PARENT]["kind"] == Variables.DO_WHILE:
            t_end_do = Transition("t_end_do" + str(next(Variables.ID_GEN)))
            net.nodes.append(t_end_do)

            ref_node = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["referenced_node"],net)
            create_arc(Variables.CURRENT_OUTPUT,t_end_do,net,0)

            if isinstance(ref_node, Transition):
                out_ax_t = Place("out_mid_t_ref", next(Variables.ID_GEN))
                net.nodes.append(out_ax_t)
                create_arc(t_end_do,out_ax_t,net,0)

                create_arc(out_ax_t,ref_node,net,0)
            else:
                 create_arc(t_end_do,ref_node,net,0)

            t_do = Transition("t_do" + str(next(Variables.ID_GEN)))
            net.nodes.append(t_do)
            
            create_arc(Variables.CURRENT_OUTPUT,t_do,net,0)

            if isinstance(ref_node, Transition):
                out_ax_t = Place("out_mid_t_ref", next(Variables.ID_GEN))
                net.nodes.append(out_ax_t)
                create_arc(t_do,out_ax_t,net,0)

                create_arc(out_ax_t,ref_node,net,1)
            else:
                 create_arc(t_do,ref_node,net,1)


            input_node = search_node_by_id(Variables.CHECKED_NODES[Variables.ID_MAIN_PARENT]["input_node"],net)
            create_arc(t_do,input_node,net,0)

            output_do = Place("output_do",next(Variables.ID_GEN))
            net.nodes.append(output_do)

            create_arc(t_end_do,output_do,net,0)
            Variables.CURRENT_OUTPUT = output_do



    if node["parent"] == Variables.MAIN_COMPOUND or node["parent"] == Variables.CURRENT_COMPOUND :
        create_sec_tran(net)


    input = Variables.CURRENT_OUTPUT

    Variables.CHECKED_NODES[node["id"]]["input_node"] = input.getId()

    tran_rtn = Transition(node['id'])
    net.nodes.append(tran_rtn)

    create_arc(input,tran_rtn,net,0)

    output_rtn = Place("OutputRtn", next(Variables.ID_GEN))
    net.nodes.append(output_rtn)

    create_arc(tran_rtn,output_rtn,net,0)

    Variables.LAST_PARENT = tran_rtn
    Variables.CURRENT_OUTPUT = output_rtn

    Variables.CHECKED_NODES[node["id"]]["output_node"] = output_rtn.getId()


#guardar nodos ya recorridos, dic
def classify_nodes(current_ast,node, net: PetriNet):
    #initialize ids for general place conectors
    if node["id"] not in Variables.CHECKED_NODES:
        '''CAMBIAR AQUI EL NOMBRE DE LOS NODOS A GUARDAR PARA QUE SEA UNIVERSAL'''
        Variables.CHECKED_NODES[node["id"]] = {"input_node": None, "output_node": None, "middle_output": None, "node_relev":None, "referenced_node": None}
        c = node["kind"]
        if c == Variables.FUNC_DECL:
            function_decl(current_ast,node,net)
        elif c == Variables.PARMVAR_DECL:
            parm_decl(current_ast,node,net)
        elif c == Variables.DECL_STMT:
            decl_stmt(current_ast, node,net)
        elif c == Variables.DECL_TYPES:
            var_dcl(node,net)
        elif c in Variables.OPERATORS:
            operators(current_ast,node, net)
        elif c == Variables.DECL_REFER: 
            decl_expr(current_ast,node ,net)
        elif c in Variables.LITERALS: 
           literals(node, net)
        elif c == Variables.COMPOUND_STMT:
            compound_control(current_ast,node,net)
        elif c ==  Variables.RETURN_STMT :
            return_stmt(current_ast,node,net)

