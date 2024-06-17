#Node's relevant names

class Variables:
    '''structure variables'''
    INPUT = 0
    OUTOPUT = 0
    ID_GEN = {}
    CHECKED_NODES = {}

    '''node type variables'''
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
    PAREN_EXPR = "ParenExpr"
    DO_WHILE = "DoStmt"