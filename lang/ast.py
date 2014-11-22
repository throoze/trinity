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

from sym_table import * 
from exceptions import *

class Trinity(object):

    SPACE = "    "

    def __init__(self, position, functions, statements):
        self._position = position
        self._functions  = functions
        self._statements = statements

    def getPosition(self):
        return self._position

    def getIndent(self,num):
        return self.SPACE * num 
        
    def __str__(self):
        string = "Trinity:"
        if self._functions is not None:
            for fun in self._functions :
                string += "\n" + fun.printAST(1)
        
        string += self.SPACE + "\nProgram:"
        
        if self._statements is not None:
            for state in self._statements : 
                string += "\n" + state.printAST(1)
        string += "\nend of Program"
        return string
    
    def check(self):
        symtab=SymTable()
        for fun in self._functions:
            symtab.addName(fun.getName(), fun.functionType(), self._position)
        if self._functions is not None:
            for fun in self._functions:
                fun.check(symtab)
        if self._statements is not None:
            for state in self._statements: 
                state.check(symtab)
        return symtab
    
    def execute(self):
        sym_table=SymTable()
        for fun in self._functions:
            symtab.addName(fun.getName(), fun.functionType(), self._position)
        if self._statements is not None:
            for state in self._statements: 
                state.execute(sym_table)
        return sym_table


class FunctionDefinition(Trinity):

    def __init__(self, position, name, params, return_type, statements):
        self._position   = position
        self._name       = name
        self._params     = params
        self._type       = return_type.toType()
        self._statements = statements

    def getName(self):
        return self._name

    def getParams(self):
        return self._params
    
    def printAST(self,level):
        
        string  = self.getIndent(level) + "Function Declaration:"
        string += "\n" + self.getIndent(level+1) +"Name: " + self._name
        if self._params is not None and self._params != []:
            string += "\n" +self.getIndent(level+1) + "Parameter List:" 
            for param in self._params :
                string += "\n" + param.printAST(level+2)
        string += "\n" + self.getIndent(level+1) + "Return Type: " + self._type.printAST(0)
        string += "\n" + self.getIndent(level+1) + "Function Body:"
        for state in self._statements :
            string += "\n" + state.printAST(level+2)

        string += "\n" + self.getIndent(level+1) + "end of Function Body"
        string += "\n" + self.getIndent(level) + "end of Function Declaration\n"
        return string

    def functionType(self):
        types = []
        for param in self._params:
            types.append(param.getType())
        return Function(types, self._type)


    def check(self, symtab):
        sym_table = SymTable(symtab, in_function=True, function_type=self._type)
        for param in self._params:
            sym_table.addName(param._name, param._type, param._position)
            
        ok = True
        for state in self._statements:
            rtype = state.check(sym_table)
            if rtype is not True and rtype is not False:
                if type(rtype) is not type(self._type):
                    position = rtype.getPosition()
                    error = "In function '%s', line %d, column %d, " % (self._name, position[0], position[1])
                    error += "return type does not match function type."
                    raise TrinityTypeError(error)
            else:
                ok = ok and rtype
        return ok
             
class FormalParameter(Trinity):

    def __init__(self, position, data_type, name):
        self._position = position
        self._type = data_type.toType()
        self._name = name

    def getType(self):
        return self._type

    def printAST(self,level):
        
        string  = self.getIndent(level) + "Parameter:"
        string += "\n" + self.getIndent(level+1) + "Type: "+ self._type.printAST(level)
        string += "\n" + self.getIndent(level+1) + "Name: "+ self._name
        return string

class Type(Trinity):

    def __init__(self):
        pass

    def toType(self):
        pass

class BooleanType(Type):

    def __init__(self, position):
        self._position = position
    
    def printAST(self, level):
        string = "Boolean"
        return string
    
    def toType(self):
        return Boolean(self._position)


class NumberType(Type):

    def __init__(self, position):
        self._position = position

    def printAST(self, level):
        string = "Number"
        return string

    def toType(self):
        return Number(self._position)

class MatrixType(Type):

    def __init__(self, position, r, c):
        self._position = position
        self._rows = int(r)
        self._cols = int(c)
        if (self._rows < 1 ) or (self._cols < 1) :
            error = "Matrix row or column number is incorrect " 
            raise TrinityMatrixDimensionError(error)
    
    def printAST(self, level):
        string = "Matrix(%d,%d)" % (self._rows,self._cols)
        return string
    
    def toType(self):
        return Matrix(self._rows, self._cols, self._position)
    
    

class ColumnVectorType(MatrixType):

    def __init__(self, position, r):
        super(ColumnVectorType, self).__init__(position, r, 1)

    def printAST(self, level):
        string = "Column(%d)" % (self._rows)
        return string
    
    def toType(self):
        return Matrix(self._rows, 1, self._position)


class RowVectorType(MatrixType):

    def __init__(self, position, c):
        super(RowVectorType, self).__init__(position, 1, c)

    def printAST(self, level):
        string = "Row(%d)" % (self._cols)
        return string

    def toType(self):
        return Matrix(1, self._cols, self._position)

class Statement(Trinity):
    def __init__(self):
        pass


class PrintStatement(Statement):

    def __init__(self, position, printables):
        self._position = position
        self._printables = printables

    def printAST(self, level):
        string  = self.getIndent(level) + "Print Statement:"
        string += "\n" + self.getIndent(level+1) + "Expressions to be printed:"
        if self._printables is not None:
            string += "\n" + self._printables[0].printAST(level+2)
            for printable in self._printables[1:]:
                string += "\n" + printable.printAST(level+2)
        return string
    
    def check(self,symtab):
        if self._printables is not None :
            for printa in self._printables :
                printa.check(symtab)
        return True


        
class Printable(object):

    def printAST(self, level):
        return "%s%s: Not Implemented" % (self.getIndent(level), self.__class__.__name__)


class Expression(Trinity,Printable):
    
    def __init__(self):
        pass

    def printAST(self, level):
        return "%s%s: Not Implemented" % (self.getIndent(level), self.__class__.__name__)

class Literal(Expression):

    def printAST(self, level):
        return "%s%s: Not Implemented" % (self.getIndent(level), self.__class__.__name__)


class StringLiteral(Literal):

    def __init__(self, position, value):
        self._position = position
        self._value = value

    def printAST(self, level):
        return "%sString Literal: %s" % (self.getIndent(level), repr(self._value))

    def check(self, symtab):
        return String(self._position)


class ReadStatement(Statement):

    def __init__(self, position, variable):
        self._position = position
        self._variable = variable

    def printAST(self, level):
        string = "%sRead Statement in variable '%s'" % (self.getIndent(level), self._variable)
        return string

    def check(self,symtab):
        if (type(self._variable.check(symtab)) is Number) or (type(self._variable.check(symtab)) is Boolean):
            return True
        else :
            error = "Trying to read with non-numeric variable " 
            raise TrinityTypeError(error)


class AssignmentStatement(Statement):

    def __init__(self, position, lvalue, rvalue):
        self._position = position
        self._lvalue = lvalue
        self._rvalue = rvalue

    def printAST(self, level):
        string  = "%sAssignment Statement:" % self.getIndent(level)
        string += "\n%sLeft Side:" % self.getIndent(level+1)
        string += "\n%s" % self._lvalue.printAST(level+2)
        string += "\n%sRight Side:" % self.getIndent(level+1)
        string += "\n%s" % self._rvalue.printAST(level+2)
        return string
    
    def check(self, symtab):
        ltype = self._lvalue.check(symtab)
        rtype = self._rvalue.check(symtab)
        if type(ltype) is not type(rtype):
            error = "In line %d, column %d, " % self._position
            error += "assigment of %s to %s" % (ltype.__str__(),rtype.__str__())
            raise TrinityTypeError(error)
        else:
            if (type(ltype) is Matrix) & (type(rtype) is Matrix) :
                if (ltype.rows != rtype.rows) | (ltype.cols != rtype.cols) :
                    error = "In line %d, column %d, matrix sizes don't match. " % self._position
                    error += "Trying to assing (%d,%d) to (%d,%d)." % (rtype._rows, rtype._cols, ltype._rows, ltype._cols)
                    raise TrinityMatrixDimensionError(error)

    def execute(self, symtab):
        if type(self._lvalue) is Variable:
            symtab.setValue(self._lvalue._id, self._rvalue.execute(symtab), self._position)
        elif type(self._lvalue) is ProjectedVariable:
            if self._lvalue._component is None:
                matrix = symtab.getValue(self._lvalue._matrix._id, self._position)
                try:
                    matrix[int(self._lvalue._row)][int(self._lvalue._col)] = self._rvalue.execute(symtab)
                except ValueError:
                    error = "In line %d, column %d, " % self._position
                    error += "trying to access matrix with a non integer number: (%d, %d)" % (self._row, self._col)
                    raise TrinityMatrixDimensionAccessError(error)
            else:
                type_class, matrix = symtab.get(self._lvalue._matrix._id, self._position)
                if type(type_class) is Matrix:
                    if type_class.rows == 0:
                        try:
                            matrix[0][int(self._component)] = self._rvalue.execute(symtab)
                        except ValueError:
                            error = "In line %d, column %d, " % self._position
                            error += "trying to access matrix with a non integer number: (%d, %d)" % (self._row, self._col)
                            raise TrinityMatrixDimensionAccessError(error)
                    elif type_class.cols == 0:
                        try:
                            matrix[int(self._component)][0] = self._rvalue.execute(symtab)
                        except ValueError:
                            error = "In line %d, column %d, " % self._position
                            error += "trying to access matrix with a non integer number: (%d, %d)" % (self._row, self._col)
                            raise TrinityMatrixDimensionAccessError(error)
            symtab.setValue(self._lvalue._matrix._id, matrix, self._position)
        return True

        
    
class Variable(Expression):
    
    def __init__(self, position, identifier):
        self._position = position
        self._id = identifier

    def printAST(self, level):
        string = "%sVariable: %s" % (self.getIndent(level), self._id)
        return string

    def __str__(self, level):
        string = "%sVariable: %s" % (self.getIndent(level), self._id)
        return string

    
    def check(self, symtab):
        return symtab.lookup(self._id, self._position)

    def execute(self, symtab):
        return symtab.getValue(self._id, self._position)

class ProjectedMatrix(Expression):

    def __init__(self, position, matrix, row, col):
        self._position = position
        self._matrix = matrix
        self._component = None
        self._row = row
        self._col = col

    def printAST(self, level):
        if self._component is not None:
            string  = "%sProjected Literal Vector:" % self.getIndent(level)
        else:
            string  = "%sProjected Literal Matrix:" % self.getIndent(level)
        string += "\n%sMatrix: " % self.getIndent(level+1)
        string += "\n%s" % self._matrix.printAST(level+2)
        string += "\n%sProjection: " % self.getIndent(level+1)
        if self._component is not None:
            string += "\n%sUnique component: " % self.getIndent(level+2)
            string += "\n%s" % self._component.printAST(level+3)
        else:
            string += "\n%sFirst component:" % self.getIndent(level+2)
            string += "\n%s" % self._row.printAST(level+3)
            string += "\n%sSecond component:" % self.getIndent(level+2)
            string += "\n%s" % self._col.printAST(level+3)
        return string
        return string

    def check(self, symtab):
        matrix_type = self._matrix.check(symtab)
        if self._component is None:
            if type(self._row.check(symtab)) is not Number:
                error = "In line %d, column %d, " % self._position
                error += "expression for rows in matrix projection is not a Number."
                raise TrinityTypeError(error)
            if type(self._col.check(symtab))is not Number:
                error = "In line %d, column %d, " % self._position
                error += "expression for columns in matrix projection is not a Number."
                raise TrinityTypeError(error)
        else:
            if type(self._component.check(symtab)) is not Number:
                error = "In line %d, column %d, " % self._position
                error += "expression in vector projection is not a Number."
                raise TrinityTypeError(error)
            # if matrix_type is not None:

            #     if matrix_type.rows != 1 or matrix_type.cols != 1:
            #         error = "In line %d, column %d, " % self._position
            #         error += "matrix has not vectorial dimentions (either rows or columns equals to 1)."
            #         raise TrinityMatrixDimensionError(error)

        return Number(self._position);

    def execute(self, symtab):
        matrix = self._matrix.execute(symtab)
        result = None
        if self._component is None:
            try:
                result =  matrix[int(self._row)][int(self._col)]
            except ValueError:
                error = "In line %d, column %d, " % self._position
                error += "trying to access matrix with a non integer number: (%d, %d)" % (self._row, self._col)
                raise TrinityMatrixDimensionAccessError(error)
        else:
            if len(matrix) == 0:
                try:
                    result =  matrix[0][int(self._component)]
                except ValueError:
                    error = "In line %d, column %d, " % self._position
                    error += "trying to access matrix with a non integer number: (%d, %d)" % (self._row, self._col)
                    raise TrinityMatrixDimensionAccessError(error)
            elif len(matrix[0]) == 0:
                try:
                    result =  matrix[int(self._component)][0]
                except ValueError:
                    error = "In line %d, column %d, " % self._position
                    error += "trying to access matrix with a non integer number: (%d, %d)" % (self._row, self._col)
                    raise TrinityMatrixDimensionAccessError(error)
        return result


class ProjectedVector(ProjectedMatrix):

    def __init__(self, position, matrix, component):
        super(ProjectedVector, self).__init__(position, matrix, None, None)
        self._component = component



class ProjectedVariable(Expression):

    def __init__(self, position, matrix, row, col=None):
        self._position = position
        self._matrix = matrix
        if col is None :
            self._component = row
            self._row = None
            self._col = None
        else:
            self._component = None
            self._row = row
            self._col = col

    def printAST(self, level):
        string  = "%sProjected Variable Matrix or Vector:" % self.getIndent(level)
        string += "\n%sMatrix: " % self.getIndent(level+1)
        string += "\n%s" % self._matrix.printAST(level+2)
        string += "\n%sProjection: " % self.getIndent(level+1)
        if self._component is not None:
            string += "\n%sUnique component: " % self.getIndent(level+2)
            string += "\n%s" % self._component.printAST(level+3)
        else:
            string += "\n%sFirst component:" % self.getIndent(level+2)
            string += "\n%s" % self._row.printAST(level+3)
            string += "\n%sSecond component:" % self.getIndent(level+2)
            string += "\n%s" % self._col.printAST(level+3)
        return string
    
    def check(self,symtab):
        variable_type=symtab.lookup(self._matrix._id, self._position)
        if  type(variable_type) is not Matrix:
            error = "Trying to project non-matrix variable " 
            raise TrinityTypeError(error)
        matrix_type = self._matrix.check(symtab)
        if self._component is None:
            if type(self._row.check(symtab)) is not Number:
                error = "In line %d, column %d, " % self._position
                error += "expression for rows in matrix projection is not a Number."
                raise TrinityTypeError(error)
            if type(self._col.check(symtab))is not Number:
                error = "In line %d, column %d, " % self._position
                error += "expression for columns in matrix projection is not a Number."
                raise TrinityTypeError(error)
        else:
            if type(self._component.check(symtab)) is not Number:
                error = "In line %d, column %d, " % self._position
                error += "expression in vector projection is not a Number."
                raise TrinityTypeError(error)
            # if matrix_type.rows != 1 or matrix_type.cols != 1:
            #     error = "In line %d, column %d, " % self._position
            #     error += "matrix has not vectorial dimentions (either rows or columns equals to 1)."
            #    raise TrinityMatrixDimensionError(error)
        return Number(self._position);

    def execute(self, symtab):
        result = None
        if self._component is None:
            matrix = self._matrix.execute(symtab)
            try:
                result =  matrix[int(self._row)][int(self._col)]
            except ValueError:
                error = "In line %d, column %d, " % self._position
                error += "trying to access matrix with a non integer number: (%d, %d)" % (self._row, self._col)
                raise TrinityMatrixDimensionAccessError(error)
        else:
            type_class, matrix = symtab.get(self._matrix._id, self._position)
            if type(type_class) is Matrix:
                if type_class.rows == 0:
                    try:
                        result =  matrix[0][int(self._component)]
                    except ValueError:
                        error = "In line %d, column %d, " % self._position
                        error += "trying to access matrix with a non integer number: (%d, %d)" % (self._row, self._col)
                        raise TrinityMatrixDimensionAccessError(error)
                elif type_class.cols == 0:
                    try:
                        result =  matrix[int(self._component)][0]
                    except ValueError:
                        error = "In line %d, column %d, " % self._position
                        error += "trying to access matrix with a non integer number: (%d, %d)" % (self._row, self._col)
                        raise TrinityMatrixDimensionAccessError(error)
        return result



class ReturnStatement(Statement):

    def __init__(self, position, expression):
        self._position = position
        self._expression = expression

    def printAST(self, level):
        string  = "%sReturn Statement:" % self.getIndent(level)
        string += "\n%s" % self._expression.printAST(level+1)
        return string

    def check(self, symtab):
        if not symtab.isInFunction():
            error = "In line %d, column %d, " % self._position
            error += "return statement occurs out of a function definition."
            raise TrinityScopeError(error)
        else:
            ret_type = self._expression.check(symtab)
            if not ret_type.compare(symtab.getFunctionType()):
                error = "In line %d, column %d, " % self._position
                error += "return expression type (%s) is not the function return type (%s)." % ret_type, symtab.getFunctionType()
                raise TrinityTypeError(error)
        return ret_type

class DiscardedExpression(Statement):

    def __init__(self, position, expression):
        self._position = position
        self._expression = expression

    def printAST(self, level):
        string  = "%sDiscarded Expression Statement:" % self.getIndent(level)
        string += "\n%s" % self._expression.printAST(level+1)
        return string

    def check(self,symtab):
        if self._expression is not None:
            exp_type = self._expression.check(symtab)
        return True

    def check(self, symtab):
        return self._expression.execute(symtab)


class IfStatement(Statement):

    def __init__(self, position, condition, statements, alt_statements=None):
        self._position = position
        self._condition = condition
        self._statements = statements
        self._alt_statements = alt_statements

    def printAST(self, level):
        string  = "%sIf Statement:" % self.getIndent(level)
        string += "\n%sConditional Expression:" % self.getIndent(level+1)
        string += "\n%s" % self._condition.printAST(level+2)
        string += "\n%sGuarded Statements:" % self.getIndent(level+1)
        if self._statements is not None and self._statements != []:
            for statement in self._statements:
                 string += "\n" + statement.printAST(level+2)
        string += "\n%send of Guarded Statements" % self.getIndent(level+1)
        if self._alt_statements is not None and self._statements != []:
            string += "\n%sAlternative Statements:" % self.getIndent(level+1)
            for statement in self._alt_statements:
                 string += "\n" + statement.printAST(level+2)
            string += "\n%send of Alternative Statements" % self.getIndent(level+1)
        string += "\n%send of If Statement" % self.getIndent(level)
        return string

    def check(self,symtab):
        if type(self._condition.check(symtab))is not Boolean:
            error = "In line %d, column %d, " % self._position
            error += "'If' statement condition is not boolean."
            raise TrinityTypeError(message)
        if self._statements is not None and self._statements != []:
            for statement in self._statements:
                statement.check(symtab)
        if self._alt_statements is not None and self._alt_statements != []:
            for alt_statement in self._alt_statements:
                alt_statement.check(symtab)
        return True

    def execute(self,symtab):
        if self._condition.execute(symtab):
            if self._statements is not None and self._statements != []:
                for statement in self._statements:
                    statement.execute(symtab)
        else:
            if self._alt_statements is not None and self._alt_statements != []:
                for alt_statement in self._alt_statements:
                    alt_statement.execute(symtab)
        return True 
        
        

class ForStatement(Statement):

    def __init__(self, position, item, iterable, statements):
        self._position = position
        self._item = item
        self._iterable = iterable
        self._statements = statements

    def printAST(self, level):
        string  = "%sFor Statement:" % self.getIndent(level)
        string += "\n%sCounter Variable: " % self.getIndent(level+1)
        string += "\n%s%s" % (self.getIndent(level+2), self._item)
        string += "\n%sIterable Object:" % self.getIndent(level+1)
        string += "\n%s" % self._iterable.printAST(level+2)
        string += "\n%sIteration Statements:" % self.getIndent(level+1)
        if self._statements is not None and self._statements != []:
            for statement in self._statements:
                 string += "\n" + statement.printAST(level+2)
        string += "\n%send of Iteration Statements" % self.getIndent(level+1)
        string += "\n%send of For Statement" % self.getIndent(level)
        return string

    def check(self,symtab):
        if type(self._iterable.check(symtab)) is not Matrix :
            error = "In line %d, column %d, " % self._position
            error += "'for' statement iterable expression is not Matrix."
            raise TrinityTypeError(error)
        sym_table = SymTable(father=symtab)
        sym_table.addName(self._item, Number(self._position), self._position)
        for state in self._statements: 
            state.check(sym_table)
        return True
    
    def execute(self,symtab):
        if self._iterable is not None:
            m = self._iterable.execute(symtab)
        sym_table = SymTable(father=symtab)
        sym_table.addName(self._item, Number(self._position), self._position)
        if self._statements is not None and self._statements != []:
            for i in range(len(m)):
                for j in range(len(m[0])):
                    sym_table.setValue(self._item, m[i][j], self._position)
                    for state in self._statements:
                        state.execute(sym_table)
        return True
                              
           
         
class WhileStatement(Statement):

    def __init__(self, position, condition, statements):
        self._position = position
        self._condition = condition
        self._statements = statements

    def printAST(self, level):
        string  = "%sWhile Statement:" % self.getIndent(level)
        string += "\n%sConditional Expression:" % self.getIndent(level+1)
        string += "\n%s" % self._condition.printAST(level+2)
        string += "\n%sIteration Statements:" % self.getIndent(level+1)
        if self._statements is not None and self._statements != []:
            for statement in self._statements:
                 string += "\n" + statement.printAST(level+2)
        string += "\n%send of Iteration Statements" % self.getIndent(level+1)
        string += "\n%send of For Statement" % self.getIndent(level)
        return string
    
    def check(self,symtab):
        if type(self._condition.check(symtab)) is not Boolean:
            error = "In line %d, column %d, " % self._position
            error += "'while' statement condition is not boolean."
            raise TrinityTypeError(error)
        if self._statements is not None:
            for statement in self._statements : 
                statement.check(symtab)
        return True
        
    def execute(self,symtab):
        if self._statements is not None and self._statements != []:
            while self._condition.execute(symtab):
                for statement in self._statements:
                    statement.execute(symtab)
        return True


class BlockStatement(Statement):

    def __init__(self, position, declared_vars, statements):
        self._position = position
        self._declared_vars = declared_vars
        self._statements = statements

    def printAST(self, level):
        string  = "%sCode Block Statement:" % self.getIndent(level)
        string += "\n%sVariable Declaration Block:" % self.getIndent(level+1)
        if self._declared_vars is not None and self._declared_vars != []:
            for declaration in self._declared_vars:
                 string += "\n" + declaration.printAST(level+2)
        string += "\n%send of Variable Declaration Block:" % self.getIndent(level+1)
        string += "\n%sInstructions Block:" % self.getIndent(level+1)
        if self._statements is not None and self._statements != []:
            for statement in self._statements:
                 string += "\n" + statement.printAST(level+2)
        string += "\n%send of Instructions Block:" % self.getIndent(level+1)
        string += "\n%send of Code Block Statement:" % self.getIndent(level)
        return string

    def check(self,symtab):
        sym_table = SymTable(father=symtab)
        if self._declared_vars is not None and self._declared_vars != []: 
            for declared in self._declared_vars:
                declared.check(sym_table)
        if self._statements is not None :
            for state in self._statements:
                state.check(sym_table)
        return True
            
    def execute(self,symtab):
        sym_table=SymTable(father=symtab)
        if self._declared_vars is not None and self._declared_vars != []:
            for declared in self._declared_vars:
                declared.execute(sym_table)
        if self._statements is not None:
            for state in self._statements:
                state.execute(sym_table)
        return True
                    

class VariableDeclaration(Trinity):

    def __init__(self, position, data_type, identifier):
        self._position = position
        self._type = data_type.toType()
        self._id = identifier

    def printAST(self, level):
        string  = "%sVariable Declaration:" % self.getIndent(level)
        string += "\n%sType: %s" % (self.getIndent(level+1), self._type.printAST(0))
        string += "\n%sIdentifier: %s" % (self.getIndent(level+1), self._id)
        return string

    def check(self,symtab):
        symtab.addName(self._id, self._type, self._position)
        return self._type

    def execute(self, symtab):
        symtab.addName(self._id, self._type, self._position)
        return True

class VariableDeclarationAssign(VariableDeclaration):

    def __init__(self, position, data_type, identifier, rvalue):
        super(VariableDeclarationAssign, self).__init__(position, data_type, identifier)
        self._rvalue = rvalue

    def printAST(self, level):
        string  = "%sVariable Declaration with Assignment:" % self.getIndent(level)
        string += "\n%sType: %s" % (self.getIndent(level+1), self._type.printAST(0))
        string += "\n%sIdentifier: %s" % (self.getIndent(level+1), self._id)
        string += "\n%sAssigned Value:" % self.getIndent(level+1)
        string += "\n%s" % self._rvalue.printAST(level+2)
        return string
    
    def check(self,symtab):
        rtype=self._rvalue.check(symtab)
        if not rtype.compare(self._type):
            error = "In line %d, column %d, " % self._position
            error += "trying to assing %s to %s" % (rtype.__str__(), self._type.__str__())
            raise TrinityTypeError(error)
        symtab.addName(self._id, self._type, self._position)
        return self._type

    def execute(self, symtab):
        super(VariableDeclarationAssign, self).execute(symtab)
        symtab.setValue(self._id, self._rvalue.execute(symtab), self._position)
        return self._type

class TrueLiteral(Literal, Expression):

    def __init__(self, position):
        self._position = position

    def printAST(self, level):
        string = "%sTrue Boolean Literal" % self.getIndent(level)
        return string

    def check(self,symtab):
        t = Boolean(self._position)
        return t

    def execute(self, symtab):
        return True
    
class FalseLiteral(Literal, Expression):

    def __init__(self, position):
        self._position = position

    def printAST(self, level):
        string = "%sFalse Boolean Literal" % self.getIndent(level)
        return string

    def check(self, symtab):
        t = Boolean(self._position)
        return t

    def execute(self, symtab):
        return False
        

class NumberLiteral(Literal, Expression):

    def __init__(self, position, value):
        self._position = position
        self._value = value

    def printAST(self, level):
        string = "%sNumber Literal: %s" % (self.getIndent(level), self._value)
        return string

    def check(self, symtab):
        t = Number(self._position)
        return t

    def execute(self, symtab):
        return self._value

class MatrixLiteral(Literal, Expression):

    def __init__(self, position, matrix):
        self._position = position
        self._matrix = matrix

    def printAST(self, level):
        string = "%sMatrix Literal:" % self.getIndent(level)
        if self._matrix is not None and self._matrix != []:
            for i, row in enumerate(self._matrix):
                string += "\n%sRow number %d:" % (self.getIndent(level+1), i)
                for j, elem in enumerate(row):
                    string += "\n%sColumn number %d:" % (self.getIndent(level+2), j)
                    string += "\n%s" % elem.printAST(level+3)
            string += "\n%send of Matrix Literal" % self.getIndent(level)
        return string

    def check(self, symtab):
        if self._matrix is not None and self._matrix != []:
            rows = 0
            cols = None
            for row in self._matrix:
                rows += 1
                for elm in row : 
                    if type(elm.check(symtab)) is not Number : 
                        error = "In line %d, column %d, " % elm.getPosition()
                        error += "non-numeric value in matrix literal."
                        raise TrinityTypeError(message)
                if cols is None:
                    cols = len(row)
                else:
                    if len(row) != cols:
                        error = "In line %d, column %d, " % self._position
                        error += "column number doesn't match."
                        raise TrinityMatrixDimensionError(error)
        return Matrix(rows, cols, self._position)

    def execute(self, symtab):
        return self._matrix

class FunctionCall(Expression):

    def __init__(self, position, identifier, args):
        self._position = position
        self._id = identifier
        self._arguments = args

    def printAST(self, level):
        string  = "%sFunction Call:" % self.getIndent(level)
        string += "\n%sName: %s" % (self.getIndent(level+1), self._id)
        if self._arguments is not None and self._arguments != []:
            string += "\n%sArguments:" % self.getIndent(level+1)
            for arg in self._arguments:
                string += "\n%s" % arg.printAST(level+2)
        return string

    def check(self,symtab):
        fun_type = symtab.lookup(self._id,self._position)
        if self._arguments is not None:
            if len(self._arguments) != fun_type.n_args:
                error = "In line %d, column %d, " % self._position
                error += "number of arguments doesn't match. "
                error += " Passed %d arguments and %d were expected." % (len(self._arguments), fun_type.n_args)
                raise TrinityTypeError(error)
            for i in range(len(self._arguments)):
                if not self._arguments[i].check(symtab).compare(fun_type.args_types[i]):
                    error = "In line %d, column %d, " % self._position
                    error += "type of arguments doesn't match. "
                    error += "Passed %s and %s was expected." % (self._arguments[i], fun_type.args_types[i])
                    raise TrinityTypeError(error)
        return fun_type.return_type



class BinaryExpression(Expression):

    def __init__(self, position, left, op, right):
        super(BinaryExpression, self).__init__()
        self._position = position
        self._left = left
        self._function = op
        self._right = right
        self._operation = ""

    def printAST(self, level):
        string  = "%s%s:" % (self.getIndent(level), self._operation)
        string += "\n%sLeft Operand:" % self.getIndent(level+1)
        string += "\n%s" % self._left.printAST(level+2)
        string += "\n%sRight Operand:" % self.getIndent(level+1)
        string += "\n%s" % self._right.printAST(level+2)
        return string

    def execute(self, symtab):
        return self._function(self._left, self._right, symtab)

class Sum(BinaryExpression):

    def __init__(self, position, left, right):
        super(Sum, self).__init__(position, left, Sum.sum, right)
        self._operation = "Sum"

    @staticmethod
    def sum(left, right, symtab):
        e1 = left.execute(symtab)
        e2 = right.execute(symtab)
        if type(left._type) is Matrix and type(right._type) is Matrix:
            result = Matrix.ones(len(e1), len(e1[0]))
            for i in range(len(e1)):
                for j in range(len(e1[0])):
                    result[i][j] = e1[i][j] + e2[i][j]
            return result
        elif type(left._type) is Number and type(right._type) is Number:
            return e1 + e2

    def check(self, symtab):
        ltype = self._left.check(symtab)
        print ltype
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) and (type(rtype) is Number) :
            return rtype
        elif (type(ltype) is Matrix) and (type(rtype) is Matrix):
            if ltype.rows != rtype.rows or ltype.cols != rtype.cols:
                error = "In line %d, column %d, " % self._position
                error += "Matrix rows or cols don't match. "
                error += "Trying to sum (%d,%d) to (%d,%d)." % (
                    ltype.rows,
                    ltype.cols,
                    rtype.rows,
                    rtype.cols
                    )
                raise TrinityMathDimensionError(error)
            else :
                return ltype
        else:
            error = "In line %d, column %d, " % self._position
            error =  "Trying to sum (+) a '%s' expression to a '%s' expression." % (ltype.__str__(),rtype.__str__())  
            raise TrinityTypeError(error)


class Subtraction(BinaryExpression):

    def __init__(self, position, left, right):
        super(Subtraction, self).__init__(position, left, Subtraction.subtraction, right)
        self._operation = "Subtraction"

    @staticmethod
    def subtraction(left, right, symtab):
        e1 = left.execute(symtab)
        e2 = right.execute(symtab)
        if type(left._type) is Matrix and type(right._type) is Matrix:
            result = Matrix.ones(len(e1), len(e1[0]))
            for i in range(len(e1)):
                for j in range(len(e1[0])):
                    result[i][j] = e1[i][j] - e2[i][j]
            return result
        elif type(left._type) is Number and type(right._type) is Number:
            return e1 - e2

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) and ( type(rtype) is Number) :
            return rtype
        elif (type(ltype) is Matrix) and (type(rtype) is Matrix):
            if ltype.rows != rtype.rows or ltype.cols != rtype.cols :
                error = "In line %d, column %d, " % self._position
                error += "Matrix rows or cols don't match. "
                error += "Trying to subtract (%d,%d) to (%d,%d)." % (
                    ltype.rows,
                    ltype.cols,
                    rtype.rows,
                    rtype.cols
                    )
                raise TrinityMatrixDimensionError(error)
            else:
                return ltype
        else:
            error = "In line %d, column %d, " % self._position
            error =  "Trying to subtract (-) a '%s' expression to a '%s' expression." % (ltype.__str__(),rtype.__str__())  
            raise TrinityTypeError(error)


class Times(BinaryExpression):

    def __init__(self, position, left, right):
        super(Times, self).__init__(position, left, Times.times, right)
        self._operation = "Multiplication"

    @staticmethod
    def times(left, right, symtab):
        e1 = left.execute(symtab)
        e2 = right.execute(symtab)
        if type(left._type) is Matrix and type(right._type) is Matrix:
            return Times.matrix_multiply(e1, e2)
        elif type(left._type) is Number and type(right._type) is Number:
            return e1 * e2

    @staticmethod
    def matrix_multiply(left, right):
        """
        Computes dot product. An MxP matrix with an PxN matrix, resulting in an
        MxN matrix.
        """
        from itertools import product
        cols, rows = len(right[0]), len(right)
        result_rows = xrange(len(left))
        result_matrix = [[0] * cols for _ in result_rows]
        for i in result_rows:
            for j, k in product(xrange(cols), xrange(rows)):
                result_matrix[i][j] += left[i][k] * right[k][j]
        return result_matrix
    
    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) and ( type(rtype) is Number) :
            return rtype
        elif (type(ltype) is Matrix) and (type(rtype) is Matrix):
            if ltype.rows != rtype.cols or ltype.cols != rtype.rows:
                error = "In line %d, column %d, " % self._position
                error += "Matrix rows or cols don't match. "
                error += "Trying to multiply (%d,%d) by (%d,%d)." % (
                    ltype.rows,
                    ltype.cols,
                    rtype.rows,
                    rtype.cols
                    )
                raise TrinityMatrixDimensionError(error)
        else:
            error = "In line %d, column %d, " % self._position
            error =  "Trying to multiply (*) a '%s' expression by a '%s' expression." % (ltype.__str__(),rtype.__str__())  
            raise TrinityTypeError(error)

            
class Division(BinaryExpression):

    def __init__(self, position, left, right):
        super(Division,self).__init__(position, left, Division.division, right)
        self._operation = "Division"

    @staticmethod
    def division(left, right, symtab):
        e1 = left.execute(symtab)
        e2 = right.execute(symtab)
        try :
            result = e1 // e2
        except ZeroDivisionError as zde:
            error = "In line %d, column %d, " % right._position
            error += "trying to compute a zero division."
            raise TrinityZeroDivisionError(error)
        return result

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) & (type(rtype) is Number) :
            return rtype
        elif (type(ltype) is Matrix) or (type(rtype) is Matrix):
            error = "Can't apply (div) to matrices "  
            raise TrinityTypeError(error)
        else:
            error = "In line %d, column %d, " % self._position
            error =  "Trying to divide (div) a '%s' expression by a '%s' expression." % (ltype.__str__(),rtype.__str__())  
            raise TrinityTypeError(error)


class Modulus(BinaryExpression):
    
    def __init__(self, position, left, right):
        super(Modulus, self).__init__(position, left, Modulus.modulus, right)
        self._operation = "Modulus"

    @staticmethod
    def modulus(left, right, symtab):
        e1 = left.execute(symtab)
        e2 = right.execute(symtab)
        try :
            result = e1 % e2
        except ZeroDivisionError as zde:
            error = "In line %d, column %d, " % right._position
            error += "trying to compute a zero division."
            raise TrinityZeroDivisionError(error)
        return result
    
    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) and (type(rtype) is Number) :
            return rtype
        elif (type(ltype) is Matrix) or (type(rtype) is Matrix):
            error = "Can't apply (mod) to matrices "  
            raise TrinityTypeError(error)
        else:
            error = "In line %d, column %d, " % self._position
            error += "trying to compute modulus (mod) of a '%s' expression by a '%s' expression." % (ltype.__str__(),rtype.__str__())
            raise TrinityTypeError(error)


class RealDivision(BinaryExpression):

    def __init__(self, position, left, right):
        super(RealDivision, self).__init__(position, left, RealDivision.real_division, right)
        self._operation = "Real Division"

    @staticmethod
    def real_division(left, right, symtab):
        e1 = left.execute(symtab)
        e2 = right.execute(symtab)
        try :
            result = e1 / e2
        except ZeroDivisionError as zde:
            error = "In line %d, column %d, " % right._position
            error += "trying to compute a zero division."
            raise TrinityZeroDivisionError(error)
        return result

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) and ( type(rtype) is Number) :            
            return rtype
        elif (type(ltype) is Matrix) or (type(rtype) is Matrix):
            error = "Can't apply (/) to matrices "  
            raise TrinityTypeError(error)
        else:
            error = "In line %d, column %d, " % self._position
            error =  "Trying to divide (/) a '%s' expression by a '%s' expression." % (ltype.__str__(),rtype.__str__())  
            raise TrinityTypeError(error)


class RealModulus(BinaryExpression):
    
    def __init__(self, position, left, right):
        super(RealModulus, self).__init__(position, left, RealModulus.real_modulus, right)
        self._operation = "Real Modulus"

    @staticmethod
    def real_modulus(left, right, symtab):
        e1 = left.execute(symtab)
        e2 = right.execute(symtab)
        try :
            result = e1 % e2
        except ZeroDivisionError as zde:
            error = "In line %d, column %d, " % right._position
            error += "trying to compute a zero division."
            raise TrinityZeroDivisionError(error)
        return result

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) and (type(rtype) is Number):
            self._type = rtype
            return rtype

        elif (type(ltype) is Matrix) or (type(rtype) is Matrix):
            error = "Can't apply (%) to matrices "  
            raise TrinityTypeError(error)
        else:
            error = "In line %d, column %d, " % self._position
            error =  "Trying to compute modulus (%) of a '%s' expression by a '%s' expression." % (ltype.__str__(),rtype.__str__())  
            raise TrinityTypeError(error)


class MatrixSum(BinaryExpression):

    def __init__(self, position, left, right):
        super(MatrixSum, self).__init__(position, left, MatrixSum.matrix_sum, right)
        self._operation = "Matrix Sum"

    @staticmethod
    def matrix_sum(left, right, symtab):
        if type(left._type) is Matrix:
            matrix = left.execute(symtab)
            scalar = right.execute(symtab)
            return map(lambda x: map(lambda y: y + scalar, x), matrix)
        elif type(right._type) is Matrix:
            matrix = right.execute(symtab)
            scalar =left.execute(symtab)
            return map(lambda x: map(lambda y: scalar  +y, x), matrix)

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) and (type(rtype) is Matrix):
            self._type = rtype
            return rtype
        elif (type(rtype) is Number) and (type(ltype) is Matrix):
            self._type = ltype
            return ltype
        else:
            error = "In line %d, column %d, " % self._position
            error =  "Trying to compute (.+.) of a '%s' expression by a '%s' expression." % (ltype.__str__(),rtype.__str__())  
            raise TrinityTypeError(error)


class MatrixSubtraction(BinaryExpression):

    def __init__(self, position, left, right):
        super(MatrixSubtraction, self).__init__(position, left, MatrixSubtraction.matrix_subtraction, right)
        self._operation = "Matrix Subtraction"

    @staticmethod
    def matrix_subtraction(left, right, symtab):
        if type(left._type) is Matrix:
            matrix = left.execute(symtab)
            scalar = right.execute(symtab)
            return map(lambda x: map(lambda y: y - scalar, x), matrix)
        elif type(right._type) is Matrix:
            matrix = right.execute(symtab)
            scalar =left.execute(symtab)
            return map(lambda x: map(lambda y: scalar - y, x), matrix)

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) and (type(rtype) is Matrix):
            self._type = rtype
            return rtype
        elif (type(rtype) is Number) and (type(ltype) is Matrix):
            self._type = ltype
            return ltype
        else:
            error = "In line %d, column %d, " % self._position
            error =  "Trying to compute (.-.) of a '%s' expression by a '%s' expression." % (ltype.__str__(),rtype.__str__())  
            raise TrinityTypeError(error)


class MatrixTimes(BinaryExpression):

    def __init__(self, position, left, right):
        super(MatrixTimes, self).__init__(position, left, MatrixTimes.matrix_times, right)
        self._operation = "Matrix Multiplication"

    @staticmethod
    def matrix_times(left, right, symtab):
        if type(left._type) is Matrix:
            matrix = left.execute(symtab)
            scalar = right.execute(symtab)
            return map(lambda x: map(lambda y: y * scalar, x), matrix)
        elif type(right._type) is Matrix:
            matrix = right.execute(symtab)
            scalar =left.execute(symtab)
            return map(lambda x: map(lambda y: scalar * y, x), matrix)

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) and (type(rtype) is Matrix):
            self._type = rtype
            return rtype
        elif (type(rtype) is Number) and (type(ltype) is Matrix):
            self._type = ltype
            return ltype
        else:
            error = "In line %d, column %d, " % self._position
            error =  "Trying to compute (.*.) of a '%s' expression by a '%s' expression." % (ltype.__str__(),rtype.__str__())  
            raise TrinityTypeError(error)
        

class MatrixDivision(BinaryExpression):

    def __init__(self, position, left, right):
        super(MatrixDivision, self).__init__(position, left, MatrixDivision.matrix_division, right)
        self._operation = "Matrix Division"

    @staticmethod
    def matrix_division(left, right, symtab):
        if type(left._type) is Matrix:
            matrix = left.execute(symtab)
            scalar = right.execute(symtab)
            try :
                result = map(lambda x: map(lambda y: y // scalar, x), matrix)
            except ZeroDivisionError as zde:
                error = "In line %d, column %d, " % right._position
                error += "trying to compute a zero division."
                raise TrinityZeroDivisionError(error)
            return result
        elif type(right._type) is Matrix:
            matrix = right.execute(symtab)
            scalar =left.execute(symtab)
            try :
                result = map(lambda x: map(lambda y: scalar // y, x), matrix)
            except ZeroDivisionError as zde:
                error = "In line %d, column %d, " % right._position
                error += "trying to compute a zero division."
                raise TrinityZeroDivisionError(error)
            return result

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) and (type(rtype) is Matrix):
            self._type = rtype
            return rtype
        elif (type(rtype) is Number) and (type(ltype) is Matrix):
            self._type = ltype
            return ltype
        else:
            error = "In line %d, column %d, " % self._position
            error =  "Trying to compute (.div.) of a '%s' expression by a '%s' expression." % (ltype.__str__(),rtype.__str__())  
            raise TrinityTypeError(error)


class MatrixModulus(BinaryExpression):

    def __init__(self, position, left, right):
        super(MatrixModulus, self).__init__(position, left, MatrixModulus.matrix_modulus, right)
        self._operation = "Matrix Modulus"

    @staticmethod
    def matrix_modulus(left, right, symtab):
        if type(left._type) is Matrix:
            matrix = left.execute(symtab)
            scalar = right.execute(symtab)
            try :
                result = map(lambda x: map(lambda y: y % scalar, x), matrix)
            except ZeroDivisionError as zde:
                error = "In line %d, column %d, " % right._position
                error += "trying to compute a zero division."
                raise TrinityZeroDivisionError(error)
            return result
        elif type(right._type) is Matrix:
            matrix = right.execute(symtab)
            scalar =left.execute(symtab)
            try :
                result = map(lambda x: map(lambda y: scalar % y, x), matrix)
            except ZeroDivisionError as zde:
                error = "In line %d, column %d, " % right._position
                error += "trying to compute a zero division."
                raise TrinityZeroDivisionError(error)
            return result

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) and (type(rtype) is Matrix):
            self._type = rtype
            return rtype
        elif (type(rtype) is Number) and (type(ltype) is Matrix):
            self._type = ltype
            return ltype
        else:
            error = "In line %d, column %d, " % self._position
            error =  "Trying to compute (.mod.) of a '%s' expression by a '%s' expression." % (ltype.__str__(),rtype.__str__())  
            raise TrinityTypeError(error)


class MatrixRealDivision(BinaryExpression):

    def __init__(self, position, left, right):
        super(MatrixRealDivision, self).__init__(
            position, left, MatrixRealDivision.matrix_real_division, right)
        self._operation = "Matrix Real Division"

    @staticmethod
    def matrix_real_division(left, right, symtab):
        if type(left._type) is Matrix:
            matrix = left.execute(symtab)
            scalar = right.execute(symtab)
            try :
                result = map(lambda x: map(lambda y: y / scalar, x), matrix)
            except ZeroDivisionError as zde:
                error = "In line %d, column %d, " % right._position
                error += "trying to compute a zero division."
                raise TrinityZeroDivisionError(error)
            return result
        elif type(right._type) is Matrix:
            matrix = right.execute(symtab)
            scalar =left.execute(symtab)
            try :
                result = map(lambda x: map(lambda y: scalar / y, x), matrix)
            except ZeroDivisionError as zde:
                error = "In line %d, column %d, " % right._position
                error += "trying to compute a zero division."
                raise TrinityZeroDivisionError(error)
            return result

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) and (type(rtype) is Matrix):
            self._type = rtype
            return rtype
        elif (type(rtype) is Number) and (type(ltype) is Matrix):
            self._type = ltype
            return ltype
        else:
            error = "In line %d, column %d, " % self._position
            error =  "Trying to compute (./.) of a '%s' expression by a '%s' expression." % (ltype.__str__(),rtype.__str__())  
            raise TrinityTypeError(error)


class MatrixRealModulus(BinaryExpression):

    def __init__(self, position, left, right):
        super(MatrixRealModulus, self).__init__(
            position, left, MatrixRealModulus.matrix_real_modulus, right)
        self._operation = "Matrix Real Modulus"

    @staticmethod
    def matrix_real_modulus(left, right, symtab):
        if type(left._type) is Matrix:
            matrix = left.execute(symtab)
            scalar = right.execute(symtab)
            try :
                result = map(lambda x: map(lambda y: y % scalar, x), matrix)
            except ZeroDivisionError as zde:
                error = "In line %d, column %d, " % right._position
                error += "trying to compute a zero division."
                raise TrinityZeroDivisionError(error)
            return result
        elif type(right._type) is Matrix:
            matrix = right.execute(symtab)
            scalar =left.execute(symtab)
            try :
                result = map(lambda x: map(lambda y: scalar % y, x), matrix)
            except ZeroDivisionError as zde:
                error = "In line %d, column %d, " % right._position
                error += "trying to compute a zero division."
                raise TrinityZeroDivisionError(error)
            return result

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) and (type(rtype) is Matrix):
            self._type = rtype
            return rtype
        elif (type(rtype) is Number) and (type(ltype) is Matrix):
            self._type = ltype
            return ltype
        else:
            error = "In line %d, column %d, " % self._position
            error =  "Trying to compute (.%.) of a '%s' expression by a '%s' expression." % (ltype.__str__(),rtype.__str__())  
            raise TrinityTypeError(error)


class Equivalence(BinaryExpression):

    def __init__(self, position, left, right):
        super(Equivalence, self).__init__(position, left, Equivalence.equivalence, right)
        self._operation = "Equivalence"

    @staticmethod
    def equivalence(left, right, symtab):
        e1 = left.execute(symtab)
        e2 = right.execute(symtab)
        return e1 == e2

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if ltype.compare(rtype):
            self._type = Boolean(self._position)
            return self._type
        else:
            error = "In line %d, column %d, " % self._position
            error =  "Trying to compare (==) a '%s' expression with a '%s' expression." % (ltype.__str__(),rtype.__str__())
            raise TrinityTypeError(error)


class NotEquivalence(BinaryExpression):

    def __init__(self, position, left, right):
        super(NotEquivalence, self).__init__(position, left, NotEquivalence.not_equivalence, right)
        self._operation = "Not Equivalence"

    @staticmethod
    def not_equivalence(left, right, symtab):
        e1 = left.execute(symtab)
        e2 = right.execute(symtab)
        return e1 != e2
   
    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if type(ltype) is type(rtype):
            if type(ltype) is Matrix  :
                if (ltype.cols != rtype.cols) or (ltype.cols != rtype.cols):
                    error = "Trying to compare wrong sized matrices " 
                    raise TrinityMatrixDimensionError(error)
            t = Boolean()
            self._type = t
            return t
        else:
            error = "In line %d, column %d, " % self._position
            error =  "Trying to compare (/=) a '%s' expression with a '%s' expression." % (ltype.__str__(),rtype.__str__())
            raise TrinityTypeException(message)


class GreaterOrEqual(BinaryExpression):

    def __init__(self, position, left, right):
        super(GreaterOrEqual, self).__init__(position, left, GreaterOrEqual.greater_or_equal, right)
        self._operation = "Greater Or Equal"

    @staticmethod
    def greater_or_equal(left, right, symtab):
        e1 = left.execute(symtab)
        e2 = right.execute(symtab)
        return e1 >= e2

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is not Number) | (type(rtype) is not Number) : 
            message =  " Error: comparing   %s expression with %s \n " % (ltype.__str__(),rtype.__str__())
            raise TrinityTypeError(message)
        else:
            t = Boolean()
            self._type = t
            return t


class LessOrEqual(BinaryExpression):

    def __init__(self, position, left, right):
        super(LessOrEqual, self).__init__(position, left, LessOrEqual.less_or_equal, right)
        self._operation = "Less Or Equal"

    @staticmethod
    def less_or_equal(left, right, symtab):
        e1 = left.execute(symtab)
        e2 = right.execute(symtab)
        return e1 <= e2

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is not Number) | (type(rtype) is not Number) : 
            message =  " Error: comparing   %s expression with %s \n " % (ltype.__str__(),rtype.__str__())
            raise TrinityTypeError(message)
        else:
            t = Boolean()
            self._type = t
            return t


class Greater(BinaryExpression):

    def __init__(self, position, left, right):
        super(Greater, self).__init__(position, left, Greater.greater, right)
        self._operation = "Greater"

    @staticmethod
    def greater(left, right, symtab):
        e1 = left.execute(symtab)
        e2 = right.execute(symtab)
        return e1 > e2

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is not Number) | (type(rtype) is not Number ): 
            message =  " Error: comparing   %s expression with %s \n " % (ltype.__str__(),rtype.__str__())
            raise TrinityTypeError(message)
        else:
            t = Boolean()
            self._type = t
            return t


class Less(BinaryExpression):

    def __init__(self, position, left, right):
        super(Less, self).__init__(position, left, Less.less, right)
        self._operation = "Less"

    @staticmethod
    def less(left, right, symtab):
        e1 = left.execute(symtab)
        e2 = right.execute(symtab)
        return e1 < e2

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is not Number) | (type(rtype) is not Number) : 
            message =  " Error: comparing   %s expression with %s \n " % (ltype.__str__(),rtype.__str__())
            raise TrinityTypeError(message)
        else:
            t = Boolean()
            self._type = t
            return t


class And(BinaryExpression):

    def __init__(self, position, left, right):
        super(And, self).__init__(position, left, And.and_func, right)
        self._operation = "And"

    @staticmethod
    def and_func(left, right, symtab):
        e1 = left.execute(symtab)
        e2 = right.execute(symtab)
        return e1 and e2
           
    def check(self,symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is not  Boolean) | (type(rtype) is not  Boolean): 
            raise TrinityTypeError(" Error : right operand is not boolean \n") 
        else : 
            t=Boolean()
            self._type = t
            return t
    

class Or(BinaryExpression):

    def __init__(self, position, left, right):
        super(Or, self).__init__(position, left, Or.or_func, right)
        self._operation = "Or"

    @staticmethod
    def or_func(left, right, symtab):
        e1 = left.execute(symtab)
        e2 = right.execute(symtab)
        return e1 or e2
          
    def check(self,symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is not  Boolean)| (type(rtype) is not  Boolean) : 
             raise TrinityTypeError("Error:right operand is not boolean \n") 
        else:
            t=Boolean()
            self._type = t
            return t

class UnaryExpression(Expression):

    def __init__(self, position, op, operand):
        super(UnaryExpression, self).__init__()
        self._position = position
        self._function = op
        self._operand = operand
        self._operation = ""

    def printAST(self, level):
        string  = "%s%s:" % (self.getIndent(level), self._operation)
        string += "\n%sOperand:" % self.getIndent(level+1)
        string += "\n" + self._operand.printAST(level+2)
        return string

    def execute(self, symtab):
        return self._function(self._operand, symtab)


class UnaryMinus(UnaryExpression):
    
    def __init__(self, position, operand):
        super(UnaryMinus, self).__init__(position, UnaryMinus.unary_minus, operand)
        self._operation = "Unary Minus"

    @staticmethod
    def unary_minus(expression, symtab):
        operand = expression.execute(symtab)
        if type(expression._type) is Matrix:
            return map(lambda x: map(lambda y: - y, x), operand)
        else:
            return - operand
        
    def check(self,symtab):
        otype = self._operand.check(symtab)
        if type(otype) is Boolean:
            raise TrinityTypeError("Can't apply Unary Minus to boolean expression ") 
        else:
            self._type = otype
            return otype

class Transpose(UnaryExpression):
    
    def __init__(self, position, operand):
        super(Transpose, self).__init__(position, Transpose.transpose, operand)
        self._operation = "Matrix Transpose"

    @staticmethod
    def transpose(expression, symtab=None):
        matrix = expression.execute(symtab)
        transposed = ones(len(matrix[1]),len(matrix))
        for i in range(len(matrix)):
            for j in range(len(matrix[1])):
                transposed[j][i] = matrix[i][j]
        return transposed

    def check(self,symtab):
        otype = self._operand.check(symtab)
        if type(otype) is not Matrix:
            raise TrinityTypeError("Can't apply traspose to non-matrix expression ") 
        else:
            self._type = otype
            return otype

        
class Not(UnaryExpression):
    
    def __init__(self, position, operand):
        super(Not, self).__init__(position, lambda expression, symtab: not expression.execute(symtab), operand)
        self._operation = "Not"
    
    def check(self,symtab):
        otype = self._operand.check(symtab)
        if type(otype) is not Boolean:
           raise TrinityTypeError("Can't apply not to non-boolean expression ") 
        else:
            self._type = otype
            return otype
