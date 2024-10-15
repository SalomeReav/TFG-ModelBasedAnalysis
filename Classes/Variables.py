from Place import Place
from Transition import Transition

class Variables:
    '''structure variables'''

    CURRENT_OUTPUT = Place
    LAST_PARENT = Transition
    ID_MAIN_PARENT = None
    CURRENT_COMPOUND = None
    MAIN_COMPOUND = None
    ID_GEN = {}
    CHECKED_NODES = {}

    '''node type variables'''
    FUNC_DECL = "FunctionDecl"
    DECL_TYPES = "VarDecl"
    IF_STMT = "IfStmt"
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
    PAREN_EXPR = "ParenExpr"
    DO_WHILE = "DoStmt"
    LITERALS = {INTEGER_LITERAL,STRING_LITERAL,CHARACTER_LITERAL}
    OPERATORS = {BINARY_OP,UNARY_OP,UNARY_OPEXPR}
    CONTROL_TYPES = {IF_STMT,WHILE_STMT}