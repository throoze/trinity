#!/usr/bin/env python
# ------------------------------------------------------------
# ast.py
#
# Trinity language Abstract Syntactic Tree (AST) specification
#
# Authors:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# Francisco Martinez, 09-10502, <frammnm@gmail.com>
# ------------------------------------------------------------


class Trinity():

    def __init__(self, functions, statements):
        self._functions  = functions
        self._statements = statements


class FunctionDefinition():

    def __init__(self, name, params, return_type, statements):
        self._name       = name
        self._params     = params
        self._type       = return_type
        self._statements = statements


class FormalParameter():

    def __init__(self, data_type, name):
        self._type = data_type
        self._name = name

class List():

    def __init__(self, wrapped_list, trailing_elem=None):
        if isinstance(wrapped_list, List) and isinstance(trailing_elem, List):
            self._list = wrapped_list.asList() + trailing_elem.asList()
        elif isinstance(wrapped_list, list) and isinstance(trailing_elem, list):
            self._list = wrapped_list + trailing_elem
        if trailing_elem not None:
            if isinstance(wrapped_list, List):
                self._list += wrapped_list.asList()
            elif isinstance(wrapped_list, list):
                self._list = wrapped_list

    def asList(self):
        return self._list

class Type():
    pass

class BooleanType(Type):
    pass


class NumberType(Type):
    pass


class MatrixType(Type):

    def __init__(self, r, c):
        self._rows = r
        self._cols = c


class ColumnVectorType(MatrixType):

    def __init__(self, r):
        super(ColumnVectorType, self).__init__(r,1)


class RowVectorType(MatrixType):

    def __init__(self, c):
        super(RowVectorType, self).__init__(1,c)


class Statement():
    pass


class PrintStatement(Statement):

    def __init__(self, printables):
        self._printables = printables


class Printable():
    pass


class Literal():
    pass


class StringLiteral(Literal,Printable):

    def __init__(self, value):
        self._value = value


class ReadStatement(Statement):

    def __init__(self, variable):
        self._variable = variable


class AssignmentStatement(Statement):

    def __init__(self, lvalue, rvalue):
        self._lvalue = lvalue
        self._rvalue = rvalue


class Expression(Printable):
    pass


class Variable(Expression):
    
    def __init__(self, identifier):
        self._id = identifier


class VectorAccessedVariable(Variable):

    def __init__(self, identifier, component):
        super(VectorAccessedVariable, self).__init__(identifier)
        self._component = component


class MatrixAccessedVariable(Variable):

    def __init__(self, identifier, row, col):
        super(MatrixAccessedVariable, self).__init__(identifier)
        self._row = row
        self._col = col


class ReturnStatement(Statement):

    def __init__(self, expression):
        self._expression = expression


class DiscardedExpression(Statement):

    def __init__(self, expression):
        self._expression = expression


class IfThenStatement(Statement):

    def __init__(self, condition, statements):
        self._condition = condition
        self._statements = statements


class IfThenElseStatement(IfThenStatement):

    def __init__(self, condition, statements, alt_statements):
        super(IfThenElseStatement, self).__init__(condition, statements)
        self._alt_statements = alt_statements


class ForStatement(Statement):

    def __init__(self, item, iterable, statements):
        self._item = item
        self._iterable = iterable
        self._statements = statements


class WhileStatement(Statement):

    def __init__(self, condition, statements):
        self._condition = condition
        self._statements = statements


class BlockStatement(Statement):

    def __init__(self, declared_vars, statements):
        self._declared_vars = declared_vars
        self._statements = statements


class VariableDeclaration():

    def __init__(self, data_type, identifier):
        self._type = data_type
        self._id = identifier


class VariableDeclarationAssign(VariableDeclaration):

    def __init__(self, data_type, identifier, rvalue):
        super(VariableDeclarationAssign, self).__init__(identifier)
        self._rvalue = rvalue


class BinaryExpression(Expression):

    def __init__(self, left, op, right):
        self._left = left
        self._function = op
        self._right = right


class TrueLiteral(Literal, Expression):
    pass


class FalseLiteral(Literal, Expression):
    pass
        

class NumberLiteral(Literal, Expression):

    def __init__(self, value):
        self._value = value


class MatrixLiteral(Literal, Expression):

    def __init__(self, matrix):
        self._matrix = matrix


class FunctionCall(Expression):

    def __init__(self, identifier, args):
        self._id = identifier
        self._arguments = args

class Sum(BinaryExpression):

    def __init__(self, left, right):
        super(Sum, self).__init__(left, lambda x,y: x + y, right)

class Substraction(BinaryExpression):

    def __init__(self, left, right):
        super(Sum, self).__init__(left, lambda x,y: x - y, right)

class Times(BinaryExpression):

    def __init__(self, left, right):
        super(Sum, self).__init__(left, lambda x,y: x * y, right)