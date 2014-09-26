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
from lexer.token import BaseOneLineComment
from lexer.token import Token

class OneLineComment(BaseOneLineComment):
    _pattern = r'#.*$'

class Tk_str(Token):
    _pattern = r'"([^"\\]|\\.)*"'

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

class Tk_num(Token):
    _pattern = r'[-]?([0-9]+)(\.[0-9]+)?'

class Tk_true(Token):
    _pattern = r'\btrue\b'

class Tk_false(Token):
    _pattern = r'\bfalse\b'

class Tk_bool(Token):
    _pattern = r'\bboolean\b'

class Tk_number(Token):
    _pattern = r'\bnumber\b'

class Tk_mat(Token):
    _pattern = r'\bmatrix\b'

class Tk_row(Token):
    _pattern = r'\brow\b'

class Tk_col(Token):
    _pattern = r'\bcol\b'

class Tk_not(Token):
    _pattern = r'\bnot\b'

class Tk_div(Token):
    _pattern = r'\bdiv\b'

class Tk_mod(Token):
    _pattern = r'\bmod\b'

class Tk_print(Token):
    _pattern = r'\bprint\b'

class Tk_use(Token):
    _pattern = r'\buse\b'

class Tk_in(Token):
    _pattern = r'\bin\b'

class Tk_end(Token):
    _pattern = r'\bend\b'

class Tk_set(Token):
    _pattern = r'\bset\b'

class Tk_read(Token):
    _pattern = r'\bread\b'

class Tk_if(Token):
    _pattern = r'\bif\b'

class Tk_then(Token):
    _pattern = r'\bthen\b'

class Tk_else(Token):
    _pattern = r'\belse\b'

class Tk_for(Token):
    _pattern = r'\bfor\b'

class Tk_do(Token):
    _pattern = r'\bdo\b'

class Tk_while(Token):
    _pattern = r'\bwhile\b'

class Tk_function(Token):
    _pattern = r'\bfunction\b'

class Tk_ret(Token):
    _pattern = r'\breturn\b'

class Tk_beg(Token):
    _pattern = r'\bbegin\b'

class Tk_prog(Token):
    _pattern = r'\bprogram\b'

class Tk_mplus(Token):
    _pattern = r'\.\+\.'

class Tk_mminus(Token):
    _pattern = r'\.\-\.'

class Tk_mtimes(Token):
    _pattern = r'\.\*\.'

class Tk_mrdiv(Token):
    _pattern = r'\./\.'

class Tk_mrmod(Token):
    _pattern = r'\.%\.'

class Tk_mdiv(Token):
    _pattern = r'\.div\.'

class Tk_mmod(Token):
    _pattern = r'\.mod\.'

class Tk_eq(Token):
    _pattern = r'=='

class Tk_neq(Token):
    _pattern = r'/='

class Tk_leq(Token):
    _pattern = r'<='

class Tk_geq(Token):
    _pattern = r'>='

class Tk_comma(Token):
    _pattern = r','
    
class Tk_colon(Token):
    _pattern = r':'

class Tk_scolon(Token):
    _pattern = r';'

class Tk_obrace(Token):
    _pattern = r'\{'

class Tk_cbrace(Token):
    _pattern = r'\}'

class Tk_oparen(Token):
    _pattern = r'\('

class Tk_cparen(Token):
    _pattern = r'\)'

class Tk_obrack(Token):
    _pattern = r'\['

class Tk_cbrack(Token):
    _pattern = r'\]'

class Tk_and(Token):
    _pattern = r'&'

class Tk_or(Token):
    _pattern = r'\|'

class Tk_asign(Token):
    _pattern = r'='

class Tk_great(Token):
    _pattern = r'>'

class Tk_less(Token):
    _pattern = r'<'

class Tk_plus(Token):
    _pattern = r'\+'

class Tk_minus(Token):
    _pattern = r'-'

class Tk_times(Token):
    _pattern = r'\*'

class Tk_rdiv(Token):
    _pattern = r'/'

class Tk_rmod(Token):
    _pattern = r'%'

class Tk_trans(Token):
    _pattern = r'\''

tokens = [
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
    Tk_asign,
    Tk_great,
    Tk_less,
    Tk_plus,
    Tk_times,
    Tk_rdiv,
    Tk_rmod,
    Tk_trans
]