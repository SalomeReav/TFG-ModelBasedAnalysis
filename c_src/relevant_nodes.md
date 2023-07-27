# Implicit casting
https://clang.llvm.org/doxygen/classclang_1_1ImplicitCastExpr.html#details
- "type": destiny type (?, not sure)
- "inner": expression or value that's being casted
- "valueCategory": "prvalue" (?);-- could be useful?
- "castKind": "LValueToRValue"/"FunctionToPointerDecay"/"NoOp" (?);-- could be useful?

# Accessing array indexes (Array subscripting)
https://clang.llvm.org/doxygen/classclang_1_1ArraySubscriptExpr.html
- "kind": "ArraySubscriptExpr"
- "type": element's type
- "valueCategory": "lvalue" (?);-- could be useful?
- "inner": first entry for the array that's being accessed + second entry for the index itself (regardless of its type (literal or expression))

# Referencing declared variables, functions, enums, etc... 
https://clang.llvm.org/doxygen/classclang_1_1DeclRefExpr.html
- "kind": "DeclRefExpr"
- "referencedDecl": dictionary containing entries about the referenced variable, function, etc... like the
	 "id", 
	 "kind", 
	 "name", and 
	 "type" of the referenced node.
- "type": (?);-- could be useful
- "valueCategory": "lvalue" (?);-- could be useful?

# Literals 
## IntegerLiteral
https://clang.llvm.org/doxygen/classclang_1_1IntegerLiteral.html
- "kind": "IntegerLiteral"
- "value": its value (it's a literal)
- "type": its type (always int?)
- "valueCategory": "prvalue" (?);-- could be useful?
## CharLiteral

## StringLiteral
https://clang.llvm.org/doxygen/classclang_1_1StringLiteral.html
- "kind": "StringLiteral"
- "value": its value
- "type": "char [5]" (example)
- "valueCategory": "lvalue" (?);-- could be useful?

# Function declaration or definition
https://clang.llvm.org/doxygen/classclang_1_1FunctionDecl.html
- "kind": "FunctionDecl"
- "inner": one entry per parameter + one entry for the body

# Function Parameter
https://clang.llvm.org/doxygen/classclang_1_1ParmVarDecl.html
- "kind": "ParmVarDecl"
- "mangledName": "argc"
- "type": dictionary with one or more entries specifying its type

# Compound stmt
https://clang.llvm.org/doxygen/classclang_1_1CompoundStmt.html
- "kind": "CompoundStmt",
- "inner": one entry per each group of related nodes

# Declaration (of some data type)
https://clang.llvm.org/doxygen/classclang_1_1Decl.html
- "kind": "DeclStmt"
- "inner": next node, specifying what is being declared
	
# Variable declaration or definition
https://clang.llvm.org/doxygen/classclang_1_1VarDecl.html
- "kind": "VarDecl",
- "type": type of the variable
- "mangledName": name of the variable,
- "inner": node corresponding to the expression on the right side o the '='
- "isUSed": true;-- could be useful
- "init": initialization style;-- could be useful

# If statement
https://clang.llvm.org/doxygen/classclang_1_1IfStmt.html
- "kind": "IfStmt"
- "hasElse": true
- "inner": 3 entries: 1st for the expression, 2nd of the if block and 3rd for the else block.

# Unary Operator  Represents the unary-expression's 
(except sizeof and alignof), the postinc/postdec operators from postfix-expression, and various extensions
https://clang.llvm.org/doxygen/classclang_1_1UnaryOperator.html
- "kind": "UnaryOperator",
- "opcode": "!", the operator itself
- "type": {} --could be useful
- "valueCategory": "prvalue", --could be useful
- "isPostfix": false, --could be useful
- "canOverflow": false
- "inner": expression

# CallExpr represents a function call
https://clang.llvm.org/doxygen/classclang_1_1CallExpr.html
- "kind": "CallExpr"
- "type": return type of the expression
- "valueCategory": "prvalue" --could be useful
- "inner": one entry for the function being called + one entry for each parameter

# RetrunStmt represents the return instruction 
https://clang.llvm.org/doxygen/classclang_1_1ReturnStmt.html
- "kind": "ReturnStmt"
- "inner": the expression that's actually returned

# ParenExpr represents a parethesized expression
https://clang.llvm.org/doxygen/classclang_1_1ParenExpr.html
- "kind": "ParenExpr",
- "valueCategory": "prvalue"
- "inner": expression between parenthesis


# OpaqueValueExpr (?) An expression referring to an opaque object of a fixed type and value class.
https://clang.llvm.org/doxygen/classclang_1_1OpaqueValueExpr.html#details
- "kind": "OpaqueValueExpr",
- "type": "qualType": "_Bool"
- "valueCategory": "prvalue"