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


##########################################################
######### Reglas de asociatividad y precedencia ##########
##########################################################

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
################################ Grammar rules #################################
################################################################################
start = 'Trinity'

#Gramatic Definitions
def p_Trinity(p):
    '''
    Trinity : FuncDefinitions Tk_prog Statements Tk_end Tk_scolon
    '''

def p_FuncDefinitions(p):
    '''
    FuncDefinitions : FuncDefinitions FuncDefinition
                    | lambda
    '''

def p_FuncDefinition(p):
    '''
    FuncDefinition : Tk_function Tk_ID Tk_oparen FormalParams Tk_cparen Tk_ret Type FunctionBody
    '''

def p_FunctionBody(p):
    '''
    FunctionBody : Tk_beg Statements Tk_end Tk_scolon
    '''

def p_FormalParams(p):
    '''
    FormalParams : FParamList
                 | lambda
    '''

def p_FParamList(p):
    '''
    FParamList : FormalParam
               | FParamList Tk_comma FormalParam
    '''

def p_FormalParam(p):
    '''
    FormalParam : Type Tk_ID
    '''

def p_Type(p):
    '''
    Type : Tk_bool
         | Tk_number
         | Tk_mat Tk_oparen Tk_num Tk_comma Tk_num Tk_cparen
         | Tk_row Tk_oparen Tk_num Tk_cparen
         | Tk_col Tk_oparen Tk_num Tk_cparen
    '''

def p_Statements(p):
    '''
    Statements : Statements Statement
               | lambda
    '''

def p_Statement(p):
    '''
    Statement : SimpleStatement
              | ComplexStatement
    '''

def p_SimpleStatement(p):
    '''
    SimpleStatement : Print
                    | Read
                    | Assignment
                    | Return
    '''

def p_Print(p):
    '''
    Print : Tk_print PrintableList Tk_scolon
    '''

def p_PrintableList(p):
    '''
    PrintableList : Printable
                  | PrintableList Tk_comma Printable
    '''

def p_Printable(p):
    '''
    Printable : Expression
              | Tk_str
    '''

def p_Read(p):
    '''
    Read : Tk_read Tk_ID Tk_scolon
    '''

def p_Assignment(p):
    '''
    Assignment : Tk_set LeftSide Tk_assign Expression Tk_scolon
    '''

def p_LeftSide(p):
    '''
    LeftSide : Tk_ID
             | Tk_ID Tk_obrack Tk_num Tk_cbrack
             | Tk_ID Tk_obrack Tk_num Tk_comma Tk_num Tk_cbrack
    '''

def p_Return(p):
    '''
    Return : Tk_ret Expression Tk_scolon
    '''

def p_ComplexStatement(p):
    '''
    ComplexStatement : If
                     | For
                     | While
                     | Block
    '''

def p_If(p):
    '''
    If : Tk_if Expression Tk_then Statements Tk_else Statements Tk_end Tk_scolon
       | Tk_if Expression Tk_then Statements Tk_end Tk_scolon
    '''

def p_For(p):
    '''
    For : Tk_for Tk_ID Tk_in Expression Tk_do Statements Tk_end Tk_scolon
    '''

def p_While(p):
    '''
    While : Tk_while Expression Tk_do Statements Tk_end Tk_scolon
    '''

def p_Block(p):
    '''
    Block : Tk_use VariableDeclarations Tk_in Statements Tk_end Tk_scolon
    '''

def p_VariableDeclarations(p):
    '''
    VariableDeclarations : VariableDeclaration
                         | VariableDeclarations VariableDeclaration
    '''

def p_VariableDeclaration(p):
    '''
    VariableDeclaration : Type Tk_ID Tk_scolon
                        | Type Tk_ID Tk_assign Expression Tk_scolon
    '''

def p_Expression(p):
    '''
    Expression : Tk_oparen Expression Tk_cparen
               | UnaryOperatorExpression
               | Expression BinaryOperator Expression
               | LeftSide
               | FunctionCall
               | Literal
    '''

def p_UnaryOperatorExpression(p):
    '''
    UnaryOperatorExpression : Tk_minus Expression %prec UMINUS
                            | Matrix Tk_trans
                            | Tk_ID Tk_trans
                            | Tk_not Expression
    '''

def p_Literal(p):
    '''
    Literal : Matrix
            | Tk_true
            | Tk_false
            | Tk_num
    '''

def p_Matrix(p):
    '''
    Matrix : Tk_obrace RowList Tk_cbrace
    '''

def p_RowList(p):
    '''
    RowList : Row
            | RowList Tk_colon Row
    '''

def p_Row(p):
    '''
    Row : Tk_num
        | Row Tk_comma Tk_num
    '''
    # TODO: Check if it's a number or an expression

def p_FunctionCall(p):
    '''
    FunctionCall : Tk_ID Tk_oparen Arguments Tk_cparen
    '''

def p_Arguments(p):
    '''
    Arguments : ArgList
              | lambda
    '''

def p_ArgList(p):
    '''
    ArgList : Expression
            | ArgList Tk_comma Expression
    '''

def p_BinaryOperator(p):
    '''
    BinaryOperator : ArithmeticBinaryOperator
                   | BooleanBinaryOperator
    '''

def p_ArithmeticBinaryOperator(p):
    '''
    ArithmeticBinaryOperator : OverloadedBinaryOperator
                             | ScalarBinaryOperator
                             | CrossedBinaryOperator
    '''

def p_OverloadedBinaryOperator(p):
    '''
    OverloadedBinaryOperator : Tk_plus
                             | Tk_minus
                             | Tk_times
    '''

def p_ScalarBinaryOperator(p):
    '''
    ScalarBinaryOperator : Tk_div
                         | Tk_mod
                         | Tk_rdiv
                         | Tk_rmod
    '''

def p_CrossedBinaryOperator(p):
    '''
    CrossedBinaryOperator : Tk_mplus
                          | Tk_mminus
                          | Tk_mtimes
                          | Tk_mdiv
                          | Tk_mmod
                          | Tk_mrdiv
                          | Tk_mrmod
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

# Error handling
def p_error(p):
    if p is None:
        print "There was a SyntaxError. Unexpected End Of File (EOF)."
    else:
        print "There was a SyntaxError. Unexpected token in %s." % p

################################################################################
############################ End of Grammar rules ##############################
################################################################################
