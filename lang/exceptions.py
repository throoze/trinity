#!/usr/bin/env python
# ------------------------------------------------------------
# exceptions.py
#
# Exceptions for the Trinity Language
#
# Authors:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# Francisco Martinez, 09-10502, <frammnm@gmail.com>
# ------------------------------------------------------------

class TrinityException(Exception):

    def __init__(self, error, *args, **kwargs):
        super(TrinityException, self).__init__(args,kwargs)
        self._error = error

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()

class TrinitySyntaxError(TrinityException):

    def __unicode__(self):
        string = "TrinitySyntaxError: %s" % self._error
        return string

class TrinityScopeError(TrinityException):

    def __unicode__(self):
        string = "TrinityScopeError: %s" % self._error
        return string

class TrinityTypeError(TrinityException):
    
    def __unicode__(self):
        string = "TrinityTypeError : %s" % self._error
        return string

class TrinityMatrixDimensionError(TrinityException):

    def __unicode__(self):
        string = "TrinityMatrixDimensionError : %s" % self._error
        return string

class TrinityMatrixDimensionAccessError(TrinityException):

    def __unicode__(self):
        string = "TrinityMatrixDimensionAccessError : %s" % self._error
        return string


class TrinityZeroDivisionError(TrinityException):
    
    def __unicode__(self):
        string = "TrinityZeroDivisionError : %s" % self._error
        return string 