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
from exceptions import (TokensNotDefinedException,
                        InputNotProvidedException)
from token import UnexpectedToken
import inspect
import pprint
import re

pp = pprint.PrettyPrinter(indent=4)

class Lexer():

    def __init__(self, module=None, inputString=None):
        if inputString is not None and inputString != '':
            self._inputString = inputString
        self._module = module

    def build(self):
        if self._module is None:
            raise TokensNotDefinedException()
        self._tokens = self._module.tokens
        self._oneLineComment = self._module.OneLineComment
        self._currentError = UnexpectedToken()
        # self._tokens = inspect.getmembers(self._module, inspect.isclass)
        # self._oneLineComment = dict(self._tokens)['OneLineComment']
        # for i, (k,v) in enumerate(self._tokens)
        #     if k in ['Token', 'BaseOneLineComment', 'OneLineComment']:
        #         try:
        #             del self._tokens[i]
        #         except KeyError:
        #             pass
        #pp.pprint(self._tokens)

    def lex(self, silent=False):
        if self._inputString is None or self._inputString == '':
            raise InputNotProvidedException()
        newline = re.compile(r'[\n\r]')
        self._found_tokens = []
        self._found_errors = []
        self._line_count = 1
        self._col_count = 1
        for line in newline.split(self._inputString):
            line = self._stripOneLineComment(line)
            print "line %d: '%s'" % (self._line_count, line)
            self._col_count = 1
            self._lexLine(line)
            self._line_count += 1
        if not silent:
            if len(self._found_errors) > 0:
                for error in self._found_errors:
                    print error
            else:
                for token in self._found_tokens:
                    print token

    def _stripOneLineComment(self, line):
        return self._oneLineComment().stripOneLineComment(line)

    def _lexLine(self, line):
        #print "line %d: '%s'" % (self._line_count, line)
        if line == '':
            if self._currentError.isInit():
                self._found_errors += [self._currentError]
                self._currentError = UnexpectedToken()
            return
        pattern = r'\s+'
        regex = re.compile(pattern)
        spaces = regex.match(line)
        if spaces is not None:
            if self._currentError.isInit():
                self._found_errors += [self._currentError]
                self._currentError = UnexpectedToken()
            line = line[spaces.end():]
            self._col_count = spaces.end()
            if line == '': return
        matched = False
        for tk in self._tokens:
            test_token = tk()
            token = test_token.match(
                self._line_count, self._col_count, line)
            if token is not None:
                matched = True
                self._col_count = token.getEndPos()-1
                self._found_tokens += [token]
                break
        if not matched:
            if self._currentError.isInit():
                self._currentError.addToValue(line[0])
                self._currentError.setEndPos(
                    self._currentError.getEndPos()+1)
            else:
                self._currentError.setLine(self._line_count)
                self._currentError.setColumn(self._col_count)
                self._currentError.setEndPos(self._col_count+1)
                self._currentError.addToValue(line[0])
            self._col_count += 1
            line = line[1:]
            self._lexLine(line)
        else:
            if self._currentError.isInit():
                self._found_errors += [self._currentError]
                self._currentError = UnexpectedToken()
            if len(line) > 0:
                self._lexLine(line[self._col_count:])




