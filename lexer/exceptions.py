#!/usr/bin/env python
# ------------------------------------------------------------
# exceptions.py
#
# Exceptions for the lexer
#
# Authors:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# Francisco Martinez, 09-10502, <frammnm@gmail.com>
# ------------------------------------------------------------

class TokensNotDefinedException(Exception):
    pass

class InputNotProvidedException(Exception):
    pass

class PatternNotDefinedException(Exception):
    pass