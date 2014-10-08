#!/usr/bin/env python
# ------------------------------------------------------------
# tokens.py
#
# Trinity language token specifications
#
# Authors:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# Francisco Martinez, 09-10502, <frammnm@gmail.com>
# ------------------------------------------------------------
from lexer.token import OneLineComment, Token

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

tokens = [
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