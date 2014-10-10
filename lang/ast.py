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


class Trinity(object):

    def __init__(self, functions, statements):
        self._functions  = functions
        self._statements = statements


class FunctionDefinition(object):

    def __init__(self, name, params, return_type, statements):
        self._name       = name
        self._params     = params
        self._type       = return_type
        self._statements = statements


class FormalParameter(object):

    def __init__(self, data_type, name):
        self._type = data_type
        self._name = name


class Type(object):
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


class Statement(object):
    pass


class PrintStatement(Statement):

    def __init__(self, printables):
        self._printables = printables


class Printable(object):
    pass


class Literal(object):
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


class ProjectedMatrix(Expression):

    def __init__(self, matrix, row, col):
        self._row = row
        self._col = col

class ProjectedVector(ProjectedMatrix):

    def __init__(self, matrix, component):
        super(ProjectedVector, self).__init__(matrix,None,None)
        self._component = component



class ProjectedVariable(Expression):

    def __init__(self, matrix, row, col=None):
        if col is None :
            self._component=row
        else:
            self._row = row
            self._col = col


class ReturnStatement(Statement):

    def __init__(self, expression):
        self._expression = expression


class DiscardedExpression(Statement):

    def __init__(self, expression):
        self._expression = expression


class IfStatement(Statement):

    def __init__(self, condition, statements,alt_statements=None):
        self._condition = condition
        self._statements = statements




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


class VariableDeclaration(object):

    def __init__(self, data_type, identifier):
        self._type = data_type
        self._id = identifier


class VariableDeclarationAssign(VariableDeclaration):

    def __init__(self, data_type, identifier, rvalue):
        super(VariableDeclarationAssign, self).__init__(identifier)
        self._rvalue = rvalue


class BinaryExpression(Expression):

    def __init__(self, left, op, right):
        super(BinaryExpression, self).__init__()
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

class Subtraction(BinaryExpression):

    def __init__(self, left, right):
        super(Subtraction, self).__init__(left, lambda x,y: x - y, right)

class Times(BinaryExpression):

    def __init__(self, left, right):
        super(Times, self).__init__(left, lambda x,y: x * y, right)

class Division(BinaryExpression):

    def __init__(self, left, right):
        super(Division, self).__init__(left, lambda x,y: x // y, right)


class Modulus(BinaryExpression):
    
    def __init__(self, left, right):
        super(Modulus, self).__init__(left, lambda x,y: x % y, right)

class RealDivision(BinaryExpression):

    def __init__(self, left, right):
        super(RealDivision, self).__init__(left, lambda x,y: x / y, right)


class RealModulus(BinaryExpression):
    
    def __init__(self, left, right):
        super(RealModulus, self).__init__(left, lambda x,y: x % y, right)


class MatrixSum(BinaryExpression):

    def __init__(self, left, right):
        super(MatrixSum, self).__init__(left, None, right)


class MatrixSubtraction(BinaryExpression):

    def __init__(self, left, right):
        super(MatrixSubtraction, self).__init__(left, None, right)


class MatrixTimes(BinaryExpression):

    def __init__(self, left, right):
        super(MatrixTimes, self).__init__(left, None, right)


class MatrixDivision(BinaryExpression):

    def __init__(self, left, right):
        super(MatrixDivision, self).__init__(left, None, right)


class MatrixModulus(BinaryExpression):

    def __init__(self, left, right):
        super(MatrixModulus, self).__init__(left, None, right)


class MatrixRealDivision(BinaryExpression):

    def __init__(self, left, right):
        super(MatrixRealDivision, self).__init__(left, None, right)


class MatrixRealModulus(BinaryExpression):

    def __init__(self, left, right):
        super(MatrixRealModulus, self).__init__(left, None, right)


class Equivalence(BinaryExpression):

    def __init__(self, left, right):
        super(Equivalence, self).__init__(left, lambda x,y: x == y, right)


class NotEquivalence(BinaryExpression):

    def __init__(self, left, right):
        super(NotEquivalence, self).__init__(left, lambda x,y: x != y, right)


class GreaterOrEqual(BinaryExpression):

    def __init__(self, left, right):
        super(GreaterOrEqual, self).__init__(left, lambda x,y: x >= y, right)


class LessOrEqual(BinaryExpression):

    def __init__(self, left, right):
        super(LessOrEqual, self).__init__(left, lambda x,y: x <= y, right)


class Greater(BinaryExpression):

    def __init__(self, left, right):
        super(Greater, self).__init__(left, lambda x,y: x > y, right)


class Less(BinaryExpression):

    def __init__(self, left, right):
        super(Less, self).__init__(left, lambda x,y: x < y, right)


class And(BinaryExpression):

    def __init__(self, left, right):
        super(And, self).__init__(left, lambda x,y: x and y, right)


class Or(BinaryExpression):

    def __init__(self, left, right):
        super(Or, self).__init__(left, lambda x,y: x or y, right)


class UnaryExpression(Expression):

    def __init__(self, op, operand):
        super(UnaryExpression, self).__init__()
        self._function = op
        self._operand = operand


class UnaryMinus(UnaryExpression):
    
    def __init__(self, operand):
        super(UnaryMinus, self).__init__(lambda x: - x, operand)


class Transpose(UnaryExpression):
    
    def __init__(self, operand):
        super(Transpose, self).__init__(None, operand)


class Not(UnaryExpression):
    
    def __init__(self, operand):
        super(Not, self).__init__(lambda x: not x, operand)
