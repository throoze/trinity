#!/usr/bin/env python
# ------------------------------------------------------------
# sym_table.py
#
# Trinity language symbol table. Represents a context and
# ensures the proper checking of names scope.
#
# Authors:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# Francisco Martinez, 09-10502, <frammnm@gmail.com>
# ------------------------------------------------------------
from exception import TrinityScopeError


class Type(object):
    """
    Represents one of the Trinity language basic data types
    """
    pass
        

class Boolean(Type):
    """Represents the Boolean type"""
    pass
        

class Number(Type):
    """Represents the Number type"""
    pass

class Matrix(Type):
    """Represents the Matrix type"""
    pass

class SymTable(object):
    """
    Trinity language symbol table. Represents a context and
    ensures the proper checking of names scope.
    """

    def __init__(self):
        self._head = {}
        self._tail = []

    def addName(self, name, type_class, token):
        """
        Adds a new name to the most inmediate scope
        """
        if name in self._head:
            message = ""
            message  += "Line: %d, Column: %d. " % (token.getLine(), token.getColumn()))
            message += "Variable or function '%s' is already defined." % name
            raise TrinityScopeError(message)
        self._head[name] = type_class

    def lookup(self, name, token):
        """
        Looks for a given name in the most inmediate scope. If it is not found,
        looks in the next one until it finds it or, raise an exception if it
        doesn't find it in any scope.
        """
        if name in self._head:
            return self._head[name]
        else:
            for context in self._tail:
                if name in context:
                    return context[name]
        message = ""
        message += "Line: %d, Column: %d. " % (token.getLine(), token.getColumn()))
        message += "Variable of function '%s' not defined in this scope" % name
        raise TrinityScopeError(message)

    def pop(self):
        """
        Removes the most inmediate scope
        """
        ret = self._head
        self._head = self._tail[0]
        self._tail = self._tail[1:]

    def push(self):
        """
        Creates a new empty scope in the SymTable.
        """
        self._tail.insert(0, self._head)
        self._head = {}

    def printScope(self, name):
        """
        Prints the most inmediate scope
        TODO: Fix this
        """
        print "Scope %s" % name
        print self._head