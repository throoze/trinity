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
from exceptions import *


class Type(object):
    """
    Represents one of the Trinity language basic data types
    """
    def __init__(self, position=None):
        self._position = position

    def getPosition(self):
        return self._position


class String(Type):
    """
    Represents the String literal type
    """

    def __init__(self, position=None):
        super(String, self).__init__(position)

    def __str__(self):
        return "String"

    def compare(self, other):
        return type(self) is type(other)
        

class Boolean(Type):
    """Represents the Boolean type"""

    def __init__(self, position=None):
        super(Boolean, self).__init__(position)

    def __str__(self):
        return "Boolean"

    def compare(self, other):
        return type(self) is type(other)
        

class Number(Type):
    """Represents the Number type"""

    def __init__(self, position=None):
        super(Number, self).__init__(position)

    def __str__(self):
        return "Number"

    def compare(self, other):
        return type(self) is type(other)


class Matrix(Type):
    """Represents the Matrix type"""

    def __init__(self, rows, cols, position=None):
        super(Matrix, self).__init__(position)
        self.rows = rows
        self.cols = cols

    def __str__(self):
        return "Matrix(%d,%d)" % (self.rows, self.cols)

    def compare(self, other):
        ok = type(self) is type(other)
        if ok:
            ok = self.rows == other.rows and self.cols == other.cols
            if not ok : 
                error = "Trying to compare diferent sized matrices " 
                raise TrinityMatrixDimensionError(error)
        return ok


class Function(Type):
    """Represents the Function type"""

    def __init__(self, args_types, return_type, position=None):
        super(Function, self).__init__(position)
        self.n_args = len(args_types)
        self.args_types = args_types
        self.return_type = return_type

    def __str__(self):
        return "Function(%d)" % self.n_args

    def compare(self, other):
        ok = type(self) is type(other)
        if ok:
            ok = ok and self.n_args == other.n_args
            ok = ok and self.return_type.compare(other.return_type)
            ok = ok and len(self.args_types) == len(args_types)
        for i in range(len(self.args_types)):
            ok = ok and self.args_types[i].compare(other.args_types[i])
        return ok


class SymTable(object):
    """
    Trinity language symbol table. Represents a context and
    ensures the proper checking of names scope.
    """
    SPACE="    " 

    def __init__(self, father=None, scope={}, in_function=None, function_type=None, belongs_to=None ):
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
            if father is not None:
                self._in_function = father.isInFunction()
            else:
                self._in_function = in_function
        else:
            self._in_function = in_function
        if self._in_function is True:

            if function_type is None:
                if father is not None:
                    self._function_type = father.getFunctionType()
                else:
                    self._function_type = function_type
            else:
                self._function_type = function_type
        else:
            self._function_type = None
        self._belong= belongs_to

    def getFunctionType(self):
        return self._function_type

    def isInFunction(self):
        return self._in_function

    def addName(self, name, type_class, position, value=None):
        """
        Adds a new name to the most inmediate scope
        """
        if name in self._scope:
            error = ""
            error += "In line %d, column %d, " % position
            error += "variable or function '%s' is already defined." % name
            raise TrinityScopeError(error)
        self._scope[name] = (type_class, value)

    def _birth(self, child):
        """
        Creates the reference from the father to its children
        """
        self._children.append(child)

    def lookup(self, name, position):
        """
        Looks for a given name in the most inmediate scope. If it is not found,
        looks in the next one until it finds it or, raise an exception if it
        doesn't find it in any scope. Returns the type associated with the given
        name.
        """
        if name in self._scope: return (self._scope[name])[0]
        elif self._father is not None: return self._father.lookup(name,position)
        else:
            error = ""
            error += "In line %d, column %d, " % position
            error += "variable or function '%s' not defined in this scope" % name.printAST(0)
            raise TrinityScopeError(error)

    def getValue(self, name, position):
        """
        Looks for a given name in the most inmediate scope. If it is not found,
        looks in the next one until it finds it or, raise an exception if it
        doesn't find it in any scope. Returns the value associated with the
        given name.
        """
        if name in self._scope: return (self._scope[name])[1]
        elif self._father is not None: return self._father.lookup(name)
        else:
            error = ""
            error += "In line %d, column %d, " % position
            error += "variable or function '%s' not defined in this scope" % name.printAST(0)
            raise TrinityScopeError(error)

    def __str__(self):
        return self.printDic(1)

    
    def printDic(self, indent):
        string = indent*self.SPACE + "New context of :" 
        for x in  self._scope :
            string += indent*" "+ x + " : " +  ((self._scope[x])[0]).__str__()+"\n"
        for child in self._children : 
            string += child.printDic(indent +1 )
        return string 
