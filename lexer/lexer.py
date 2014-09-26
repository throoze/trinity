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

    def __init__(self, module=None, inputString=None, debug=False):
        if inputString is not None and inputString != '':
            self._inputString = inputString
        self._module = module
        self._debug = debug

    def build(self):
        if self._module is None:
            raise TokensNotDefinedException()
        self._tokens = self._module.tokens
        self._oneLineComment = self._module.OneLineComment
        self._currentError = UnexpectedToken()
        self._found_tokens = []
        self._found_errors = []
        self._line_count = 1
        self._col_count = 1

    def lex(self, silent=False):
        if self._inputString is None or self._inputString == '':
            raise InputNotProvidedException()
        newline = re.compile(r'[\n\r]')
        for line in newline.split(self._inputString):
            line = self._stripOneLineComment(line)
            self._col_count = 1
            self._lexLine(line)
            if self._debug: print "=============================================\n"
            self._line_count += 1
        if not silent:
            if len(self._found_errors) > 0:
                for error in self._found_errors:
                    print error
            else:
                for token in self._found_tokens:
                    print token
        return len(self._found_errors) == 0

    def _stripOneLineComment(self, line):
        return self._oneLineComment().stripOneLineComment(line)

    def _finishError(self):
        if self._currentError.isInit():
            self._found_errors += [self._currentError]
            self._currentError = UnexpectedToken()

    def _updateError(self, line):
        if self._currentError.isInit():
            self._currentError.addToValue(line[0])
            self._currentError.setEndPos(
                self._currentError.getEndPos() + 1
                )
        else:
            self._currentError.setLine(self._line_count)
            self._currentError.setColumn(self._col_count)
            self._currentError.setEndPos(self._col_count+1)
            self._currentError.addToValue(line[0])
        self._col_count += 1
        line = line[1:]
        self._lexLine(line)



    def _lexLine(self, line):
        if self._debug: print "line %02d: '%s'" % (self._line_count, line)
        if line == '':
            self._finishError()
            return
        pattern = r'\s+'
        regex = re.compile(pattern)
        spaces = regex.match(line)
        if spaces is not None:
            self._finishError()
            line = line[spaces.end():]
            self._col_count = self._col_count + spaces.end()
            if self._debug: print "whitespace: ('%s'), _col_count: %s" % (spaces.group(), self._col_count)
            if line == '': return
        matched = False
        next_start = 0
        for tk in self._tokens:
            test_token = tk()
            token = test_token.match(
                self._line_count, self._col_count, line)
            if token is not None:
                matched = True
                next_start = token.getSpan()
                self._col_count = token.getEndPos() + 1
                self._found_tokens += [token]
                if self._debug: print "token: (%s), _col_count: %s" % (token, self._col_count)
                break
        if not matched:
            self._updateError(line)
        else:
            self._finishError()
            if len(line) > 0:
                self._lexLine(line[next_start:])




