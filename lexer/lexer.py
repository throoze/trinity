#!/usr/bin/env python
# ------------------------------------------------------------
# lexer.py
#
# Lexer
#
# Authors:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# Francisco Martinez, 09-10502, <frammnm@gmail.com>
#
# Usage:
#
# ------------------------------------------------------------
from exceptions import TokensNotDefinedException, InputNotProvidedException
import inspect
import re

class Lexer():

    def __init__(self, module=None, inputString=None):
        if inputString is not None and inputString != '':
            self.inputString = inputString
        self.module = module

    def build(self):
        if self.module is None:
            raise TokensNotDefinedException()
        self.tokens = dict(inspect.getmembers(self.module, inspect.isclass))
        try:
            del self.tokens['Token']
        except KeyError:
            pass

    def lex(self, silent=False):
        if self.inputString is None or self.inputString == '':
            raise InputNotProvidedException()
        newline = re.compile(r'[\n\r]+')
        blankspace = re.compile(r'\s+')
        self.tokenList = []
        for line in newline.split(self.inputString):
            for piece in blankspace.split(line):
                self.tokenList += piece
        if not silent:
            for token in self.tokenList:
                print token
