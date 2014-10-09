#!/usr/bin/env python
# ------------------------------------------------------------
# specs.py
#
# Trinity language token specifications
#
# Authors:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# Francisco Martinez, 09-10502, <frammnm@gmail.com>
# ------------------------------------------------------------
from lexer.token import OneLineComment, Token
from ast import *

################################################################################
############################# Tokens specification #############################
################################################################################

class Tk_Comment(OneLineComment):
    _pattern = r'#.*$'
    _name = 'Comment'

class Tk_str(Token):
    _pattern = r'"([^"\\]|\\.)*"'
    _name = 'String'

    def __init__(self, pattern=None):
        super(Tk_str, self).__init__(pattern=pattern)
        self._shows_value = True

    def match(self, line_no, col_no, inputString):
        ret = super(Tk_str, self).match(line_no, col_no, inputString)
        if ret is not None:
            ret._value = ret._value[1:len(ret._value)-1]
        return ret

    def getSpan(self):
        if self._value is not None:
            return len(self._value) + 2
        else:
            return 0

class Tk_ID(Token):
    _pattern = r'[a-zA-Z][a-zA-Z0-9_]*'
    _name = 'Id'

    def __init__(self, pattern=None):
        super(Tk_ID, self).__init__(pattern=pattern)
        self._shows_value = True

class Tk_num(Token):
    _pattern = r'[-]?([0-9]+)(\.[0-9]+)?'
    _name = 'Number'

    def __init__(self, pattern=None):
        super(Tk_num, self).__init__(pattern=pattern)
        self._shows_value = True

    def match(self, line_no, col_no, inputString):
        ret = super(Tk_num, self).match(line_no, col_no, inputString)
        if ret is not None:
            self._shown_value = float(self._value) if '.' in self._value else int(self._value)
        return ret

class Tk_true(Token):
    _pattern = r'\btrue\b'
    _name = 'True'

class Tk_false(Token):
    _pattern = r'\bfalse\b'
    _name = 'False'

class Tk_bool(Token):
    _pattern = r'\bboolean\b'
    _name = 'Reserved word \'boolean\''


class Tk_number(Token):
    _pattern = r'\bnumber\b'
    _name = 'Reserved word \'number\''

class Tk_mat(Token):
    _pattern = r'\bmatrix\b'
    _name = 'Reserved word \'matrix\''

class Tk_row(Token):
    _pattern = r'\brow\b'
    _name = 'Reserved word \'row\''

class Tk_col(Token):
    _pattern = r'\bcol\b'
    _name = 'Reserved word \'col\''

class Tk_not(Token):
    _pattern = r'\bnot\b'
    _name = 'Reserved word \'not\''

class Tk_div(Token):
    _pattern = r'\bdiv\b'
    _name = '\'div\' operator'

class Tk_mod(Token):
    _pattern = r'\bmod\b'
    _name = '\'mod\' operator'

class Tk_print(Token):
    _pattern = r'\bprint\b'
    _name = 'Reserved word \'print\''

class Tk_use(Token):
    _pattern = r'\buse\b'
    _name = 'Reserved word \'use\''

class Tk_in(Token):
    _pattern = r'\bin\b'
    _name = 'Reserved word \'in\''

class Tk_end(Token):
    _pattern = r'\bend\b'
    _name = 'Reserved word \'end\''

class Tk_set(Token):
    _pattern = r'\bset\b'
    _name = 'Reserved word \'set\''

class Tk_read(Token):
    _pattern = r'\bread\b'
    _name = 'Reserved word \'read\''

class Tk_if(Token):
    _pattern = r'\bif\b'
    _name = 'Reserved word \'if\''

class Tk_then(Token):
    _pattern = r'\bthen\b'
    _name = 'Reserved word \'then\''

class Tk_else(Token):
    _pattern = r'\belse\b'
    _name = 'Reserved word \'else\''

class Tk_for(Token):
    _pattern = r'\bfor\b'
    _name = 'Reserved word \'for\''

class Tk_do(Token):
    _pattern = r'\bdo\b'
    _name = 'Reserved word \'do\''

class Tk_while(Token):
    _pattern = r'\bwhile\b'
    _name = 'Reserved word \'while\''

class Tk_function(Token):
    _pattern = r'\bfunction\b'
    _name = 'Reserved word \'function\''

class Tk_ret(Token):
    _pattern = r'\breturn\b'
    _name = 'Reserved word \'return\''

class Tk_beg(Token):
    _pattern = r'\bbegin\b'
    _name = 'Reserved word \'begin\''

class Tk_prog(Token):
    _pattern = r'\bprogram\b'
    _name = 'Reserved word \'program\''

class Tk_mplus(Token):
    _pattern = r'\.\+\.'
    _name = '.+. operator'

class Tk_mminus(Token):
    _pattern = r'\.-\.'
    _name = '.-. operator'

class Tk_mtimes(Token):
    _pattern = r'\.\*\.'
    _name = '.*. operator'

class Tk_mrdiv(Token):
    _pattern = r'\./\.'
    _name = './. operator'

class Tk_mrmod(Token):
    _pattern = r'\.%\.'
    _name = '.%. operator'

class Tk_mdiv(Token):
    _pattern = r'\.div\.'
    _name = '.div. operator'

class Tk_mmod(Token):
    _pattern = r'\.mod\.'
    _name = '.mod. operator'

class Tk_eq(Token):
    _pattern = r'=='
    _name = 'Equivalence'

class Tk_neq(Token):
    _pattern = r'/='
    _name = 'Inequivalence'

class Tk_leq(Token):
    _pattern = r'<='
    _name = 'Less or equal than'

class Tk_geq(Token):
    _pattern = r'>='
    _name = 'Greater or equal than'

class Tk_comma(Token):
    _pattern = r','
    _name = 'Comma'
    
class Tk_colon(Token):
    _pattern = r':'
    _name = 'Colon'

class Tk_scolon(Token):
    _pattern = r';'
    _name = 'Semicolon'

class Tk_obrace(Token):
    _pattern = r'\{'
    _name = 'Opening brace {'

class Tk_cbrace(Token):
    _pattern = r'\}'
    _name = 'Closing brace }'

class Tk_oparen(Token):
    _pattern = r'\('
    _name = 'Opening parenthesis ('

class Tk_cparen(Token):
    _pattern = r'\)'
    _name = 'Closing parenthesis )'

class Tk_obrack(Token):
    _pattern = r'\['
    _name = 'Opening bracket ['

class Tk_cbrack(Token):
    _pattern = r'\]'
    _name = 'Closing bracket ]'

class Tk_and(Token):
    _pattern = r'&'
    _name = 'Ampersand'

class Tk_or(Token):
    _pattern = r'\|'
    _name = 'Pipe'

class Tk_assign(Token):
    _pattern = r'='
    _name = 'Assign'

class Tk_great(Token):
    _pattern = r'>'
    _name = 'Greater than'

class Tk_less(Token):
    _pattern = r'<'
    _name = 'Less than'

class Tk_plus(Token):
    _pattern = r'\+'
    _name = 'Plus'

class Tk_minus(Token):
    _pattern = r'-'
    _name = 'Minus'

class Tk_times(Token):
    _pattern = r'\*'
    _name = 'Times'

class Tk_rdiv(Token):
    _pattern = r'/'
    _name = 'Into'

class Tk_rmod(Token):
    _pattern = r'%'
    _name = '% operator'

class Tk_trans(Token):
    _pattern = r'\''
    _name = 'Transpose'

token_classes = [
    Tk_Comment,
    Tk_str,
    Tk_true,
    Tk_false,
    Tk_bool,
    Tk_number,
    Tk_mat,
    Tk_row,
    Tk_col,
    Tk_not,
    Tk_div,
    Tk_mod,
    Tk_print,
    Tk_use,
    Tk_in,
    Tk_end,
    Tk_set,
    Tk_read,
    Tk_if,
    Tk_then,
    Tk_else,
    Tk_for,
    Tk_do,
    Tk_while,
    Tk_function,
    Tk_ret,
    Tk_beg,
    Tk_prog,
    Tk_ID,
    Tk_minus,
    Tk_num,
    Tk_mplus,
    Tk_mminus,
    Tk_mtimes,
    Tk_mrdiv,
    Tk_mrmod,
    Tk_mdiv,
    Tk_mmod,
    Tk_eq,
    Tk_neq,
    Tk_leq,
    Tk_geq,
    Tk_comma,
    Tk_colon,
    Tk_scolon,
    Tk_obrace,
    Tk_cbrace,
    Tk_oparen,
    Tk_cparen,
    Tk_obrack,
    Tk_cbrack,
    Tk_and,
    Tk_or,
    Tk_assign,
    Tk_great,
    Tk_less,
    Tk_plus,
    Tk_times,
    Tk_rdiv,
    Tk_rmod,
    Tk_trans
]

tokens = [ token().__class__.__name__ for token in token_classes[1:] ]
################################################################################
######################### End of Tokens specification ##########################
################################################################################


################################################################################
###################### Precedence and associative rules ########################
################################################################################

precedence = (
    ('left', 'Tk_plus', 'Tk_minus',
             'Tk_mplus', 'Tk_mminus'
             ),
    ('left', 'Tk_times', 'Tk_rdiv', 'Tk_rmod', 'Tk_div', 'Tk_mod',
             'Tk_mtimes', 'Tk_mrdiv', 'Tk_mrmod', 'Tk_mdiv', 'Tk_mmod'
             ),
    ('left', 'Tk_trans'),
    ('nonassoc', 'Tk_eq', 'Tk_neq', 'Tk_geq', 'Tk_leq', 'Tk_great', 'Tk_less'),
    ('left', 'Tk_or'),
    ('left', 'Tk_and'),
    ('right', 'UMINUS'),
    ('right', 'Tk_not')
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
    p[0] = Trinity(p[1],p[3])

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
    p[0] = FunctionDefinition(p[2], p[4], p[7], p[8])

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
    p[0] = [p[1]]

def p_FParamList_list(p):
    '''
    FParamList : FParamList Tk_comma FormalParam
    '''
    p[0] = p[1] + [p[3]]

def p_FormalParam(p):
    '''
    FormalParam : Type Tk_ID
    '''
    p[0] = FormalParameter(p[1], p[2])

def p_Type_bool(p):
    '''
    Type : Tk_bool
    '''
    p[0] = BooleanType()

def p_Type_number(p):
    '''
    Type : Tk_number
    '''
    p[0] = NumberType()

def p_Type_2d(p):
    '''
    Type : Tk_mat Tk_oparen Tk_num Tk_comma Tk_num Tk_cparen
    '''
    p[0] = MatrixType(p[3],p[5])

def p_Type_row(p):
    '''
    Type : Tk_row Tk_oparen Tk_num Tk_cparen
    '''
    p[0] = RowVectorType(p[3])

def p_Type_col(p):
    '''
    Type : Tk_col Tk_oparen Tk_num Tk_cparen
    '''
    p[0] = ColumnVectorType(p[3])

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
    p[0] = PrintStatement(p[2])

def p_PrintableList_list(p):
    '''
    PrintableList : PrintableList Tk_comma Printable
    '''
    p[0] = p[1] + [p[3]]

def p_PrintableList_elem(p):
    '''
    PrintableList : Printable
    '''
    p[0] = p[1]

def p_Printable_expression(p):
    '''
    Printable : Expression
    '''
    p[0] = p[1]

def p_Printable_string(p):
    '''
    Printable : Tk_str
    '''
    p[0] = StringLiteral(p[1])

def p_Read(p):
    '''
    Read : Tk_read Tk_ID Tk_scolon
    '''
    p[0] = ReadStatement(p[2])

def p_Assignment(p):
    '''
    Assignment : Tk_set LeftValue Tk_assign Expression Tk_scolon
    '''
    p[0] = AssignmentStatement(p[2], p[4])

def p_LeftValue_simple(p):
    '''
    LeftValue : Tk_ID
    '''
    p[0] = Variable(p[1])

def p_LeftValue_vector_access(p):
    '''
    LeftValue : Tk_ID Tk_obrack Tk_num Tk_cbrack
    '''
    p[0] = VectorAccessedVariable(p[1], p[3])

def p_LeftValue_matrix_access(p):
    '''
    LeftValue : Tk_ID Tk_obrack Tk_num Tk_comma Tk_num Tk_cbrack
    '''
    p[0] = MatrixAccessedVariable(p[1], p[3], p[5])

def p_Return(p):
    '''
    Return : Tk_ret Expression Tk_scolon
    '''
    p[0] = ReturnStatement(p[2])

def p_DiscardedExpression(p):
    '''
    DiscardedExpression : Expression Tk_scolon
    '''
    p[0] = DiscardedExpression(p[1])

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
    p[0] = IfThenStatement(p[2], p[4])

def p_If_else(p):
    '''
    If : Tk_if Expression Tk_then Statements Tk_else Statements Tk_end Tk_scolon
    '''
    p[0] = IfThenElseStatement(p[2], p[4], p[6])


def p_For(p):
    '''
    For : Tk_for Tk_ID Tk_in Expression Tk_do Statements Tk_end Tk_scolon
    '''
    p[0] = ForStatement(p[2], p[4], p[6])

def p_While(p):
    '''
    While : Tk_while Expression Tk_do Statements Tk_end Tk_scolon
    '''
    p[0] = WhileStatement(p[2], p[4])

def p_Block(p):
    '''
    Block : Tk_use VariableDeclarations Tk_in Statements Tk_end Tk_scolon
    '''
    p[0] = BlockStatement(p[2], p[4])

def p_VariableDeclarations_list(p):
    '''
    VariableDeclarations : VariableDeclarations VariableDeclaration
    '''
    p[0] = p[1] + [p[2]]

def p_VariableDeclarations_elem(p):
    '''
    VariableDeclarations : VariableDeclaration
    '''
    p[0] = p[1]

def p_VariableDeclaration(p):
    '''
    VariableDeclaration : Type Tk_ID Tk_scolon
    '''
    p[0] = VariableDeclaration(p[1], p[2])

def p_VariableDeclaration_assign(p):
    '''
    VariableDeclaration : Type Tk_ID Tk_assign Expression Tk_scolon
    '''
    p[0] = VariableDeclarationAssign(p[1], p[2], p[4])

def p_Expression(p):
    '''
    Expression : UnaryOperatorExpression
               | Expression BinaryOperator Expression
               | LeftValue
               | FunctionCall
               | Literal
    '''
    p[0] = p[1]

def p_Expression_strict(p):
    '''
    Expression : Tk_oparen Expression Tk_cparen
    '''
    p[0] = p[2]

def p_BinaryExpression(p):
    '''
    Expression : Expression BinaryOperator Expression
    '''
    p[0] = BinaryExpression(p[1], p[2], p[3])

def p_UnaryOperatorExpression(p):
    '''
    UnaryOperatorExpression : Tk_minus Expression %prec UMINUS
                            | Matrix Tk_trans
                            | Tk_ID Tk_trans
                            | Tk_not Expression
    '''

def p_Literal_matrix(p):
    '''
    Literal : Matrix
    '''
    p[0] = p[1]

def p_Literal_true(p):
    '''
    Literal : Tk_true
    '''
    p[0] = TrueLiteral()

def p_Literal_false(p):
    '''
    Literal : Tk_false
    '''
    p[0] = FalseLiteral()

def p_Literal_num(p):
    '''
    Literal : Matrix
            | Tk_true
            | Tk_false
            | Tk_num
    '''
    p[0] = NumberLiteral(p[1])

def p_Matrix(p):
    '''
    Matrix : Tk_obrace RowList Tk_cbrace
    '''
    p[0] = Matrix(p[2])

def p_RowList_list(p):
    '''
    RowList : RowList Tk_colon Row
    '''
    p[0] = p[1] +[p[3]]

def p_RowList_row(p):
    '''
    RowList : Row
    '''
    p[0] = p[1]

def p_Row_exp(p):
    '''
    Row : Tk_num
    '''
    # TODO: Check if it's a number or an expression
    p[0] = NumberLiteral(p[1])

def p_Row(p):
    '''
    Row : Row Tk_comma Tk_num
    '''
    # TODO: Check if it's a number or an expression
    p[0] = p[1] + [NumberLiteral(p[3])]

def p_FunctionCall(p):
    '''
    FunctionCall : Tk_ID Tk_oparen Arguments Tk_cparen
    '''
    p[0] = FunctionCall(p[1], p[3])

def p_Arguments(p):
    '''
    Arguments : ArgList
              | lambda
    '''
    p[0] = p[1]

def p_ArgList_list(p):
    '''
    ArgList : ArgList Tk_comma Expression
    '''
    p[0] = p[1] + [p[3]]

def p_ArgList_item(p):
    '''
    ArgList : Expression
    '''
    p[0] = p[1]

def p_BinaryOperator(p):
    '''
    BinaryOperator : ArithmeticBinaryOperator
                   | BooleanBinaryOperator
    '''
    p[0] = p[1]

def p_ArithmeticBinaryOperator(p):
    '''
    ArithmeticBinaryOperator : OverloadedBinaryOperator
                             | ScalarBinaryOperator
                             | CrossedBinaryOperator
    '''
    p[0] = p[1]

def p_OverloadedBinaryOperator_plus(p):
    '''
    OverloadedBinaryOperator : Tk_plus
    '''

def p_OverloadedBinaryOperator_minus(p):
    '''
    OverloadedBinaryOperator : Tk_minus
    '''

def p_OverloadedBinaryOperator_times(p):
    '''
    OverloadedBinaryOperator : Tk_times
    '''

def p_ScalarBinaryOperator_div(p):
    '''
    ScalarBinaryOperator : Tk_div
    '''

def p_ScalarBinaryOperator_mod(p):
    '''
    ScalarBinaryOperator : Tk_mod
    '''

def p_ScalarBinaryOperator_rdiv(p):
    '''
    ScalarBinaryOperator : Tk_rdiv
    '''

def p_ScalarBinaryOperator_rmod(p):
    '''
    ScalarBinaryOperator : Tk_rmod
    '''

def p_CrossedBinaryOperator_mplus(p):
    '''
    CrossedBinaryOperator : Tk_mplus
    '''

def p_CrossedBinaryOperator_mminus(p):
    '''
    CrossedBinaryOperator : Tk_mminus
    '''

def p_CrossedBinaryOperator_mtimes(p):
    '''
    CrossedBinaryOperator : Tk_mtimes
    '''

def p_CrossedBinaryOperator_mdiv(p):
    '''
    CrossedBinaryOperator : Tk_mdiv
    '''

def p_CrossedBinaryOperator_mmod(p):
    '''
    CrossedBinaryOperator : Tk_mmod
    '''

def p_CrossedBinaryOperator_mrdiv(p):
    '''
    CrossedBinaryOperator : Tk_mrdiv
    '''

def p_CrossedBinaryOperator_mrmod(p):
    '''
    CrossedBinaryOperator : Tk_mrmod
    '''

def p_BooleanBinaryOperator(p):
    '''
    BooleanBinaryOperator : Tk_eq
                          | Tk_neq
                          | Tk_leq
                          | Tk_geq
                          | Tk_great
                          | Tk_less
                          | Tk_and
                          | Tk_or
    '''

def p_lambda(p):
    '''
    lambda : 
    '''
    p[0] = []

# Error handling
def p_error(p):
    if p is None:
        print "There was a SyntaxError. Unexpected End Of File (EOF)."
    else:
        print "There was a SyntaxError. Unexpected token in %s." % p

################################################################################
############################ End of Grammar rules ##############################
################################################################################
