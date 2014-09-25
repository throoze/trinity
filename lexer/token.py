#!/usr/bin/env python
# ------------------------------------------------------------
# token.py
#
# BaseToken specification
#
# Authors:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# Francisco Martinez, 09-10502, <frammnm@gmail.com>
#
# Usage:
#
# ------------------------------------------------------------
from abc import ABCMeta, abstractmethod, abstractproperty

class Token:
    __metaclass__ = ABCMeta

    @abstractmethod
    def say_something(self): pass


class Tk_comment(Token):
    pattern = r'^\#.*$'

class Tk_ID(Token):
    pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'

class Tk_number(Token):
    pattern = r'^[+-]?([0-9]*(\.?)[0-9]*)'

class Tk_mplus(Token):
    pattern = r'\.\+\.'

class Tk_mminus(Token):
    pattern = r'\.\-\.'

class Tk_mtimes(Token):
    pattern = r'\.\*\.'

class Tk_mrdiv(Token):
    pattern = r'\.\/\.'

class Tk_mrmod(Token):
    pattern = r'\.\%\.'

class Tk_mdiv(Token):
    pattern = r'\.div\.'

class Tk_mmod(Token):
    pattern = r'\.\mod\.'

class Tk_eq(Token):
    pattern = r'\=\='

class Tk_neq(Token):
    pattern = r'\/\='

class Tk_leq(Token):
    pattern = r'\<\='

class Tk_geq(Token):
    pattern = r'\>\='

class Tk_quote(Token):
    pattern = r'\"'

class Tk_esc(Token):
    pattern = r'\\'

class Tk_comma(Token):
    pattern = r'\,'
    
class Tk_colon(Token):
    pattern = r'\:'

class Tk_scolon(Token):
    pattern = r'\;'

class Tk_obrace(Token):
    pattern = r'\{'

class Tk_cbrace(Token):
    pattern = r'\}'

class Tk_lparen(Token):
    pattern = r'\('

class Tk_rparen(Token):
    pattern = r'\)'

class Tk_obrack(Token):
    pattern = r'\['

class Tk_cbrack(Token):
    pattern = r'\]'

class Tk_and(Token):
    pattern = r'\&'

class Tk_or(Token):
    pattern = r'\|'

class Tk_asign(Token):
    pattern = r'\='

class Tk_great(Token):
    pattern = r'\>'

class Tk_less(Token):
    pattern = r'\<'

class Tk_plus(Token):
    pattern = r'\+'

class Tk_minus(Token):
    pattern = r'\-'

class Tk_times(Token):
    pattern = r'\*'

class Tk_rdiv(Token):
    pattern = r'\/'

class Tk_rmod(Token):
    pattern = r'\%'

class Tk_trans(Token):
    pattern = r'\''

   
