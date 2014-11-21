#!/usr/bin/env python
# ------------------------------------------------------------
# syntactic_specs.py
#
# Trinity language syntactic specifications. Every grammar,
# precedence and associativity rule for Trinity are specified
# here.
#
# Authors:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# Francisco Martinez, 09-10502, <frammnm@gmail.com>
# ------------------------------------------------------------
from exceptions import TrinitySyntaxError

from lexical_specs import token_classes

from ast import *

##########
## List of tokens to be used by ply.yacc
tokens = [ token().__class__.__name__ for token in token_classes[1:] ]
##########

################################################################################
###################### Precedence and associative rules ########################
################################################################################

precedence = (
    
    ('left', 'Tk_or'),
    ('left', 'Tk_and'),
    ('nonassoc', 'Tk_eq', 'Tk_neq', 'Tk_geq', 'Tk_leq', 'Tk_great', 'Tk_less'),
     ('right', 'Tk_not'),
    ('left', 'Tk_plus', 'Tk_minus',
             'Tk_mplus', 'Tk_mminus'
             ),
    ('left', 'Tk_times', 'Tk_rdiv', 'Tk_rmod', 'Tk_div', 'Tk_mod',
             'Tk_mtimes', 'Tk_mrdiv', 'Tk_mrmod', 'Tk_mdiv', 'Tk_mmod'
             ),
   
    ('right', 'UMINUS'),
    ('left', 'Tk_trans')

   )

################################################################################
################### End of Precedence and associative rules ####################
################################################################################

################################################################################
################################ Grammar rules #################################
################################################################################
start = 'Trinity'

#Gramatic Definitions
def p_Trinity(p):
    '''
    Trinity : FuncDefinitions Tk_prog Statements Tk_end Tk_scolon
    '''
    p[0] = Trinity((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_FuncDefinitions_list(p):
    '''
    FuncDefinitions : FuncDefinitions FuncDefinition
    '''
    p[0] = p[1] + [p[2]]

def p_FuncDefinitions_lambda(p):
    '''
    FuncDefinitions : lambda
    '''
    p[0] = p[1]


def p_FuncDefinition(p):
    '''
    FuncDefinition : Tk_function Tk_ID Tk_oparen FormalParams Tk_cparen Tk_ret Type FunctionBody
    '''
    p[0] = FunctionDefinition((p.lineno(0), p.lexpos(0)),p[2], p[4], p[7], p[8])

def p_FunctionBody(p):
    '''
    FunctionBody : Tk_beg Statements Tk_end Tk_scolon
    '''
    p[0] = p[2]

def p_FormalParams(p):
    '''
    FormalParams : FParamList
                 | lambda
    '''
    p[0] = p[1]

def p_FParamList_param(p):
    '''
    FParamList : FormalParam
    '''
    p[0] = p[1]

def p_FParamList_list(p):
    '''
    FParamList : FParamList Tk_comma FormalParam
    '''
    p[0] = p[1] + p[3]

def p_FormalParam(p):
    '''
    FormalParam : Type Tk_ID
    '''
    p[0] = [FormalParameter((p.lineno(0), p.lexpos(0)), p[1], p[2])]

def p_Type_bool(p):
    '''
    Type : Tk_bool
    '''
    p[0] = BooleanType((p.lineno(0), p.lexpos(0)))

def p_Type_number(p):
    '''
    Type : Tk_number
    '''
    p[0] = NumberType((p.lineno(0), p.lexpos(0)))

def p_Type_2d(p):
    '''
    Type : Tk_mat Tk_oparen Tk_num Tk_comma Tk_num Tk_cparen
    '''
    p[0] = MatrixType((p.lineno(0), p.lexpos(0)), p[3],p[5])

def p_Type_row(p):
    '''
    Type : Tk_row Tk_oparen Tk_num Tk_cparen
    '''
    p[0] = RowVectorType((p.lineno(0), p.lexpos(0)), p[3])

def p_Type_col(p):
    '''
    Type : Tk_col Tk_oparen Tk_num Tk_cparen
    '''
    p[0] = ColumnVectorType((p.lineno(0), p.lexpos(0)), p[3])

def p_Statements_list(p):
    '''
    Statements : Statements Statement
    '''
    p[0] = p[1] + [p[2]]

def p_Statements_lambda(p):
    '''
    Statements : lambda
    '''
    p[0] = p[1]

def p_Statement(p):
    '''
    Statement : SimpleStatement
              | ComplexStatement
    '''
    p[0] = p[1]

def p_SimpleStatement(p):
    '''
    SimpleStatement : Print
                    | Read
                    | Assignment
                    | Return
                    | DiscardedExpression
    '''
    p[0] = p[1]

def p_Print(p):
    '''
    Print : Tk_print PrintableList Tk_scolon
    '''
    p[0] = PrintStatement((p.lineno(0), p.lexpos(0)), p[2])

def p_PrintableList_list(p):
    '''
    PrintableList : PrintableList Tk_comma Printable
    '''
    p[0] = p[1] + [p[3]]

def p_PrintableList_elem(p):
    '''
    PrintableList : Printable
    '''
    p[0] = [p[1]]

def p_Printable_expression(p):
    '''
    Printable : Expression
    '''
    p[0] = p[1]

def p_Printable_string(p):
    '''
    Printable : Tk_str
    '''
    p[0] = StringLiteral((p.lineno(0), p.lexpos(0)), p[1])

def p_Read(p):
    '''
    Read : Tk_read Tk_ID Tk_scolon
    '''
    p[0] = ReadStatement((p.lineno(0), p.lexpos(0)), Variable((p.lineno(2), p.lexpos(2)), p[2]))

def p_Assignment(p):
    '''
    Assignment : Tk_set LeftValue Tk_assign Expression Tk_scolon
    '''
    p[0] = AssignmentStatement((p.lineno(0), p.lexpos(0)), p[2], p[4])

def p_LeftValue_simple(p):
    '''
    LeftValue : Tk_ID
    '''
    p[0] = Variable((p.lineno(0), p.lexpos(0)), p[1])

def p_LeftValue_vector_access(p):
    '''
    LeftValue : Tk_ID Tk_obrack Expression Tk_cbrack
    '''
    p[0] = ProjectedVariable((p.lineno(0), p.lexpos(0)), Variable((p.lineno(1), p.lexpos(1)), p[1]), p[3])

def p_LeftValue_matrix_access(p):
    '''
    LeftValue : Tk_ID Tk_obrack Expression Tk_comma Expression Tk_cbrack
    '''
    p[0] = ProjectedVariable((p.lineno(0), p.lexpos(0)), Variable((p.lineno(1), p.lexpos(1)), p[1]), p[3], p[5])

def p_Return(p):
    '''
    Return : Tk_ret Expression Tk_scolon
    '''
    p[0] = ReturnStatement((p.lineno(0), p.lexpos(0)), p[2])

def p_DiscardedExpression(p):
    '''
    DiscardedExpression : Expression Tk_scolon
    '''
    p[0] = DiscardedExpression((p.lineno(0), p.lexpos(0)), p[1])

def p_ComplexStatement(p):
    '''
    ComplexStatement : If
                     | For
                     | While
                     | Block
    '''
    p[0] = p[1]

def p_If(p):
    '''
    If : Tk_if Expression Tk_then Statements Tk_end Tk_scolon
    '''
    p[0] = IfStatement((p.lineno(0), p.lexpos(0)), p[2], p[4])

def p_If_else(p):
    '''
    If : Tk_if Expression Tk_then Statements Tk_else Statements Tk_end Tk_scolon
    '''
    p[0] = IfStatement((p.lineno(0), p.lexpos(0)), p[2], p[4], p[6])


def p_For(p):
    '''
    For : Tk_for Tk_ID Tk_in Expression Tk_do Statements Tk_end Tk_scolon
    '''
    p[0] = ForStatement((p.lineno(0), p.lexpos(0)), p[2], p[4], p[6])

def p_While(p):
    '''
    While : Tk_while Expression Tk_do Statements Tk_end Tk_scolon
    '''
    p[0] = WhileStatement((p.lineno(0), p.lexpos(0)), p[2], p[4])

def p_Block(p):
    '''
    Block : Tk_use VariableDeclarations Tk_in Statements Tk_end Tk_scolon
    '''
    p[0] = BlockStatement((p.lineno(0), p.lexpos(0)), p[2], p[4])

def p_VariableDeclarations_list(p):
    '''
    VariableDeclarations : VariableDeclarations VariableDeclaration
    '''
    p[0] = p[1] + [p[2]]

def p_VariableDeclarations_elem(p):
    '''
    VariableDeclarations : lambda
    '''
    p[0] = p[1]

def p_VariableDeclaration(p):
    '''
    VariableDeclaration : Type Tk_ID Tk_scolon
    '''
    p[0] = VariableDeclaration((p.lineno(0), p.lexpos(0)), p[1], p[2])

def p_VariableDeclaration_assign(p):
    '''
    VariableDeclaration : Type Tk_ID Tk_assign Expression Tk_scolon
    '''
    p[0] = VariableDeclarationAssign((p.lineno(0), p.lexpos(0)), p[1], p[2], p[4])

def p_Expression(p):
    '''
    Expression : UnaryOperatorExpression
               | BinaryExpression
               | LeftValue
               | FunctionCall
               | Literal
               | ProjectedMatrix
    '''
    p[0] = p[1]

def p_Expression_strict(p):
    '''
    Expression : Tk_oparen Expression Tk_cparen
    '''
    p[0] = p[2]

def p_ProjectedMatrix_2D(p):
    '''
    ProjectedMatrix : Expression Tk_obrack  Expression Tk_comma Expression Tk_cbrack
    '''
    p[0] = ProjectedMatrix((p.lineno(0), p.lexpos(0)), p[1],p[3],p[5])

def p_ProjectedMatrix_1D(p):
    '''
    ProjectedMatrix : Expression Tk_obrack  Expression  Tk_cbrack
    '''
    p[0] = ProjectedVector((p.lineno(0), p.lexpos(0)), p[1],p[3])

def p_UnaryOperatorExpression_minus(p):
    '''
    UnaryOperatorExpression : Tk_minus Expression %prec UMINUS
    '''
    p[0] = UnaryMinus((p.lineno(0), p.lexpos(0)), p[2])

def p_UnaryOperatorExpression_trans(p):
    '''
    UnaryOperatorExpression : Matrix Tk_trans
                            
    '''
    p[0] = Transpose((p.lineno(0), p.lexpos(0)), p[1])

def p_UnaryOperatorExpression_trans_id(p):
    '''
    UnaryOperatorExpression : Expression Tk_trans
                            
    '''
    p[0] = Transpose((p.lineno(0), p.lexpos(0)), p[1])


def p_UnaryOperatorExpression_not(p):
    '''
    UnaryOperatorExpression : Tk_not Expression
    '''
    p[0] = Not((p.lineno(0), p.lexpos(0)), p[2])

def p_BinaryExpression_plus(p):
    '''
    BinaryExpression : Expression Tk_plus Expression
    '''
    p[0] = Sum((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_minus(p):
    '''
    BinaryExpression : Expression Tk_minus Expression
    '''
    p[0] = Subtraction((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_times(p):
    '''
    BinaryExpression : Expression Tk_times Expression
    '''
    p[0] = Times((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_div(p):
    '''
    BinaryExpression : Expression Tk_div Expression
    '''
    p[0] = Division((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_mod(p):
    '''
    BinaryExpression : Expression Tk_mod Expression
    '''
    p[0] = Modulus((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_rdiv(p):
    '''
    BinaryExpression : Expression Tk_rdiv Expression
    '''
    p[0] = RealDivision((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_rmod(p):
    '''
    BinaryExpression : Expression Tk_rmod Expression
    '''
    p[0] = RealModulus((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_mplus(p):
    '''
    BinaryExpression : Expression Tk_mplus Expression
    '''
    p[0] = MatrixSum((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_mminus(p):
    '''
    BinaryExpression : Expression Tk_mminus Expression
    '''
    p[0] = MatrixSubtraction((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_mtimes(p):
    '''
    BinaryExpression : Expression Tk_mtimes Expression
    '''
    p[0] = MatrixTimes((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_mdiv(p):
    '''
    BinaryExpression : Expression Tk_mdiv Expression
    '''
    p[0] = MatrixDivision((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_mmod(p):
    '''
    BinaryExpression : Expression Tk_mmod Expression
    '''
    p[0] = MatrixModulus((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_mrdiv(p):
    '''
    BinaryExpression : Expression Tk_mrdiv Expression
    '''
    p[0] = MatrixRealDivision((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_mrmod(p):
    '''
    BinaryExpression : Expression Tk_mrmod Expression
    '''
    p[0] = MatrixRealModulus((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_eq(p):
    '''
    BinaryExpression : Expression Tk_eq Expression
    '''
    p[0] = Equivalence((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_neq(p):
    '''
    BinaryExpression : Expression Tk_neq Expression
    '''
    p[0] = NotEquivalence((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_geq(p):
    '''
    BinaryExpression : Expression Tk_geq Expression
    '''
    p[0] = GreaterOrEqual((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_leq(p):
    '''
    BinaryExpression : Expression Tk_leq Expression
    '''
    p[0] = LessOrEqual((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_great(p):
    '''
    BinaryExpression : Expression Tk_great Expression
    '''
    p[0] = Greater((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_less(p):
    '''
    BinaryExpression : Expression Tk_less Expression
    '''
    p[0] = Less((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_and(p):
    '''
    BinaryExpression : Expression Tk_and Expression
    '''
    p[0] = And((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_BinaryExpression_or(p):
    '''
    BinaryExpression : Expression Tk_or Expression
    '''
    p[0] = Or((p.lineno(0), p.lexpos(0)), p[1], p[3])


def p_Literal_matrix(p):
    '''
    Literal : Matrix
    '''
    p[0] = p[1]

def p_Literal_true(p):
    '''
    Literal : Tk_true
    '''
    p[0] = TrueLiteral((p.lineno(0), p.lexpos(0)))

def p_Literal_false(p):
    '''
    Literal : Tk_false
    '''
    p[0] = FalseLiteral((p.lineno(0), p.lexpos(0)))

def p_Literal_num(p):
    '''
    Literal : Tk_num
    '''
    p[0] = NumberLiteral((p.lineno(0), p.lexpos(0)), p[1])

def p_Matrix(p):
    '''
    Matrix : Tk_obrace RowList Tk_cbrace
    '''
    p[0] = MatrixLiteral((p.lineno(0), p.lexpos(0)), p[2])

def p_RowList_row(p):
    '''
    RowList : Row
    '''
    p[0] = [p[1]]

def p_RowList_list(p):
    '''
    RowList : RowList Tk_colon Row
    '''
    p[0] = p[1] + [p[3]]

def p_Row_exp(p):
    '''
    Row : Expression
    '''
    p[0] = [p[1]]

def p_Row(p):
    '''
    Row : Row Tk_comma Expression
    '''
    p[0] = p[1] + [p[3]]

def p_FunctionCall(p):
    '''
    FunctionCall : Tk_ID Tk_oparen Arguments Tk_cparen
    '''
    p[0] = FunctionCall((p.lineno(0), p.lexpos(0)), p[1], p[3])

def p_Arguments(p):
    '''
    Arguments : ArgList
              | lambda
    '''
    p[0] = p[1]

def p_ArgList_item(p):
    '''
    ArgList : Expression
    '''
    p[0] = [p[1]]

def p_ArgList_list(p):
    '''
    ArgList : ArgList Tk_comma Expression
    '''    
    p[0] = p[1].append(p[3])


def p_lambda(p):
    '''
    lambda : 
    '''
    p[0] = []

################################################################################
############################ End of Grammar rules ##############################
################################################################################

# Error handling
def p_error(p):
    error = ""
    if p is None:
        error = "Unexpected End Of File (EOF)."
    else:
        error = "Unexpected token in %s." % p
    raise TrinitySyntaxError(error)
