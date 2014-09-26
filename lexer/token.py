#!/usr/bin/env python
# ------------------------------------------------------------
# token.py
#
# Base Token specification
#
# Authors:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# Francisco Martinez, 09-10502, <frammnm@gmail.com>
# ------------------------------------------------------------
from abc import ABCMeta, abstractmethod, abstractproperty
from exceptions import PatternNotDefinedException
import re

class Token:
    __metaclass__ = ABCMeta

    def __init__(self, pattern=None):
        if pattern is not None:
            self._pattern = pattern
        try:
            if self._pattern is not None:
                self._regex = re.compile(self._pattern)
        except AttributeError:
            pass
        self._column = -1
        self._end_pos = -1
        self._line = -1
        self._value = None

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "%s(value: '%s', line: %d, column: %d, to: %d)" % (
            self.__class__.__name__,
            self._value,
            self._line,
            self._column,
            self._end_pos
            )


    def match(self, line_no, col_no, inputString):
        try:
            matched = self._regex.match(inputString)
        except AttributeError:
            raise PatternNotDefinedException()
        if matched is None:
            return None
        else:
            self._line = line_no
            self._column = col_no + matched.start()
            self._end_pos = col_no + matched.end() - 1
            self._value = matched.group()
            return self

    def setValue(self, value):
        self._value = value

    def setColumn(self, col):
        self._column = col

    def setLine(self, line):
        self._line = line

    def setEndPos(self, end):
        self._end_pos = end

    def getEndPos(self):
        return self._end_pos

    def getSpan(self):
        return len(self._value)

class BaseOneLineComment:
    __metaclass__ = ABCMeta

    def __init__(self, pattern=None):
        if pattern is not None:
            self._pattern = pattern
        if self._pattern is not None:
            self._regex = re.compile(self._pattern)

    def stripOneLineComment(self, line):
        matched = self._regex.search(line)
        if matched is not None:
            line = line[:matched.start()]
        return line


class UnexpectedToken(Token):

    def isInit(self):
        return self._column > -1

    def addToValue(self, val):
        if self._value is None: self._value = ''
        self._value += val