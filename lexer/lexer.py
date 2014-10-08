#!/usr/bin/env python
# ------------------------------------------------------------
# lexer.py
#
# Lexer class
#
# Authors:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# Francisco Martinez, 09-10502, <frammnm@gmail.com>
# ------------------------------------------------------------
from exceptions import (TokensNotDefinedException,
                        InputNotProvidedException,
                        LexicographicalError)
from token import UnexpectedToken
import re

class Lexer():

    _SUCCESS = 0

    def __init__(self, module=None, inputString=None, debug=False, save_comments=False):
        self.reset(module, inputString, debug, save_comments)

    def reset(self, module=None, inputString=None, debug=False, save_comments=False):
        if inputString is not None and inputString != '':
            self._inputString = inputString
        self._module = module
        self._debug = debug
        self._save_comments = save_comments
        if module is not None:
            self.build()

    def build(self):
        if self._module is None:
            raise TokensNotDefinedException()
        self._token_list     = self._module.tokens
        self._currentError   = UnexpectedToken()
        self._found_tokens   = []
        if self._save_comments:
            self._found_comments = []
        self._found_errors   = []
        self._line_count     = 1
        self._col_count      = 1
        self._lexed          = False

    def input(self, inputString=None):
        if inputString is not None and inputString != '':
            self._inputString = inputString
        return self.lex(silent=True)

    def token(self):
        try:
            return self.grabToken()
        except StopIteration:
            return None

    def grabToken(self):
        if not self._lexed:
            self.lex()
        for token in self._found_tokens:
            token.makePLYable()
            yield token

    def lex(self, silent=False):
        if self._module is None:
            raise TokensNotDefinedException()
        if self._inputString is None or self._inputString == '':
            raise InputNotProvidedException()
        newline = re.compile(r'[\n\r]')
        for line in newline.split(self._inputString):
            self._col_count = 1
            self._lexLine(line)
            if self._debug: print "=============================================\n"
            self._line_count += 1
        if len(self._found_errors) > 0:
            raise LexicographicalError(self._found_errors)
        if not silent:
            for token in self._found_tokens:
                    print token
        self._lexed = True
        return self._SUCCESS

    def _finishError(self):
        if self._currentError.isInit():
            self._found_errors += [self._currentError]
            self._currentError = None
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
        for tk in self._token_list:
            test_token = tk()
            token = test_token.match(
                self._line_count, self._col_count, line)
            if token is not None:
                matched = True
                next_start = token.getSpan()
                self._col_count = token.getEndPos() + 1
                if token.isComment():
                    if self._save_comments:
                        self._found_comments += [token]
                else:
                    self._found_tokens += [token]
                if self._debug: print "token: (%s), _col_count: %s" % (token, self._col_count)
                break
        if not matched:
            self._updateError(line)
        else:
            self._finishError()
            if len(line) > 0:
                self._lexLine(line[next_start:])