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
from exceptions import TrinityScopeError


class Type(object):
    """
    Represents one of the Trinity language basic data types
    """
    pass
        

class Boolean(Type):
    """Represents the Boolean type"""
    def __str__(self):
        return "Boolean"
        

class Number(Type):
    """Represents the Number type"""
    def __str__(self):
        return "Number"


class Matrix(Type):
    """Represents the Matrix type"""

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def __str__(self):
        return "Matrix(%d,%d)" % (self.rows, self.cols)


class Function(Type):
    """Represents the Function type"""

    def __init__(self, args_types, return_type):
        self.n_args = len(args_types)
        self.args_types = args_types
        self.return_type = return_type

    def __str__(self):
        return "Function(%d)" % self.n_args


class SymTable(object):
    """
    Trinity language symbol table. Represents a context and
    ensures the proper checking of names scope.
    """
    SPACE="    " 

    def __init__(self, father=None, scope={}, in_function=None,belongsto=None ):
        """
        Params:
            scope  :
                type : dictionary
                        keys   : names of functions or variables.
                        values : type class of the functions or variables.
            father :
                type: SymTable father of this SymTable.
        """
        self._scope = scope
        self._children = []
        if father is not None: father._birth(self)
        self._father = father
        if in_function is None:
            self._in_function = father.isInFunction()
        else:
            self._in_function = in_function
        self._belong= belongsto 

    def isInFunction(self):
        return self._in_function

    def addName(self, name, type_class, position):
        """
        Adds a new name to the most inmediate scope
        """
        if name in self._scope:
            error = ""
            error += "In line %d, column %d, " % position
            error += "variable or function '%s' is already defined." % name
            raise TrinityScopeError(error)
        self._scope[name] = type_class

    def _birth(self, child):
        """
        Creates the reference from the father to its children
        """
        self._children.append(child)

    def lookup(self, name, position):
        """
        Looks for a given name in the most inmediate scope. If it is not found,
        looks in the next one until it finds it or, raise an exception if it
        doesn't find it in any scope.
        """
        if name in self._scope: return self._scope[name]
        elif self._father is not None: return self._father.lookup(name)
        else:
            error = ""
            error += "In line %d, column %d, " % position
            error += "variable of function '%s' not defined in this scope" % name
            raise TrinityScopeError(error)

    def __str__(self):
        return self.printDic(1)

    
    def printDic(self, indent):
        string = indent*SPACE + "New context of %d : \n" % (self._belong) 
        for x in  self._scope :
            string += indent*" "+ x + " : " +  self._scope[x].printAST(indent)+"\n"
        for child in self._children : 
            child.printDic(indent +1 )
