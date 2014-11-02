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

class Trinity(object):

    SPACE = "    "

    def __init__(self, functions, statements):
        self._functions  = functions
        self._statements = statements

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
        for fun in self._functions :
            symtab.addName(fun._name,fun._type,token) # Duda en cual es el token
        if self._functions is not None:
            for fun in self._functions :
                fun.check(symtab)
        if self._statements is not None:
            for state in self._statements : 
                state.check(symtab)

class FunctionDefinition(Trinity):

    def __init__(self, name, params, return_type, statements):
        self._name       = name
        self._params     = params
        self._type       = return_type
        self._statements = statements
    
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

    def check(self,symtab):
        
        symtab.push()
        for param in self._params:
            symtab.addName(param._name,param._type,token)
            
        for state in self._statements:
            rtype = state.check(symtab)
            if type(rtype) is not type(self._type):
                print "Return type error in function : " + self._name 
             
class FormalParameter(Trinity):

    def __init__(self, data_type, name):
        self._type = data_type
        self._name = name

    def printAST(self,level):
        
        string  = self.getIndent(level) + "Parameter:"
        string += "\n" + self.getIndent(level+1) + "Type: "+ self._type.printAST(level)
        string += "\n" + self.getIndent(level+1) + "Name: "+ self._name
        return string

class Type(Trinity):

    def __init__(self):
        pass


class BooleanType(Type):
    
    def printAST(self, level):
        string = "Boolean"
        return string


class NumberType(Type):

    def printAST(self, level):
        string = "Number"
        return string


class MatrixType(Type):

    def __init__(self, r, c):
        self._rows = int(r)
        self._cols = int(c)
    
    def printAST(self, level):
        string = "Matrix(%d,%d)" % (self._rows,self._cols)
        return string
    

class ColumnVectorType(MatrixType):

    def __init__(self, r):
        super(ColumnVectorType, self).__init__(r,1)

    def printAST(self, level):
        string = "Column(%d)" % (self._rows)
        return string


class RowVectorType(MatrixType):

    def __init__(self, c):
        super(RowVectorType, self).__init__(1,c)

    def printAST(self, level):
        string = "Row(%d)" % (self._cols)
        return string


class Statement(Trinity):
    def __init__(self):
        pass


class PrintStatement(Statement):

    def __init__(self, printables):
        self._printables = printables

    def printAST(self, level):
        string  = self.getIndent(level) + "Print Statement:"
        string += "\n" + self.getIndent(level+1) + "Expressions to be printed:"
        if self._printables is not None:
            string += "\n" + self._printables[0].printAST(level+2)
            for printable in self._printables[1:]:
                string += "\n" + printable.printAST(level+2)
        return string


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

    def __init__(self, value):
        self._value = value

    def printAST(self, level):
        return "%sString Literal: %s" % (self.getIndent(level), repr(self._value))


class ReadStatement(Statement):

    def __init__(self, variable):
        self._variable = variable

    def printAST(self, level):
        string = "%sRead Statement in variable '%s'" % (self.getIndent(level), self._variable)
        return string


class AssignmentStatement(Statement):

    def __init__(self, lvalue, rvalue):
        self._lvalue = lvalue
        self._rvalue = rvalue

    def printAST(self, level):
        string  = "%sAssignment Statement:" % self.getIndent(level)
        string += "\n%sLeft Side:" % self.getIndent(level+1)
        string += "\n%s" % self._lvalue.printAST(level+2)
        string += "\n%sRight Side:" % self.getIndent(level+1)
        string += "\n%s" % self._rvalue.printAST(level+2)
        return string
    

class Variable(Expression):
    
    def __init__(self, identifier):
        self._id = identifier

    def printAST(self, level):
        string = "%sVariable: %s" % (self.getIndent(level), self._id)
        return string


class ProjectedMatrix(Expression):

    def __init__(self, matrix, row, col):
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

class ProjectedVector(ProjectedMatrix):

    def __init__(self, matrix, component):
        super(ProjectedVector, self).__init__(matrix,None,None)
        self._component = component



class ProjectedVariable(Expression):

    def __init__(self, matrix, row, col=None):
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


class ReturnStatement(Statement):

    def __init__(self, expression):
        self._expression = expression

    def printAST(self, level):
        string  = "%sReturn Statement:" % self.getIndent(level)
        string += "\n%s" % self._expression.printAST(level+1)
        return string


class DiscardedExpression(Statement):

    def __init__(self, expression):
        self._expression = expression

    def printAST(self, level):
        string  = "%sDiscarded Expression Statement:" % self.getIndent(level)
        string += "\n%s" % self._expression.printAST(level+1)
        return string


class IfStatement(Statement):

    def __init__(self, condition, statements, alt_statements=None):
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




class ForStatement(Statement):

    def __init__(self, item, iterable, statements):
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


class WhileStatement(Statement):

    def __init__(self, condition, statements):
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


class BlockStatement(Statement):

    def __init__(self, declared_vars, statements):
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


class VariableDeclaration(Trinity):

    def __init__(self, data_type, identifier):
        self._type = data_type
        self._id = identifier

    def printAST(self, level):
        string  = "%sVariable Declaration:" % self.getIndent(level)
        string += "\n%sType: %s" % (self.getIndent(level+1), self._type.printAST(0))
        string += "\n%sIdentifier: %s" % (self.getIndent(level+1), self._id)
        return string


class VariableDeclarationAssign(VariableDeclaration):

    def __init__(self, data_type, identifier, rvalue):
        super(VariableDeclarationAssign, self).__init__(data_type, identifier)
        self._rvalue = rvalue

    def printAST(self, level):
        string  = "%sVariable Declaration with Assignment:" % self.getIndent(level)
        string += "\n%sType: %s" % (self.getIndent(level+1), self._type.printAST(0))
        string += "\n%sIdentifier: %s" % (self.getIndent(level+1), self._id)
        string += "\n%sAssigned Value:" % self.getIndent(level+1)
        string += "\n%s" % self._rvalue.printAST(level+2)
        return string


class BinaryExpression(Expression):

    def __init__(self, left, op, right):
        super(BinaryExpression, self).__init__()
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
    
            

class TrueLiteral(Literal, Expression):

    def printAST(self, level):
        string = "%sTrue Boolean Literal" % self.getIndent(level)
        return string

    def check(self):
        t = Boolean()
        return t 
    
class FalseLiteral(Literal, Expression):

    def printAST(self, level):
        string = "%sFalse Boolean Literal" % self.getIndent(level)
        return string

    def check(self):
        t = Boolean()
        return t
        

class NumberLiteral(Literal, Expression):

    def __init__(self, value):
        self._value = value

    def printAST(self, level):
        string = "%sNumber Literal: %s" % (self.getIndent(level), self._value)
        return string

    def check(self):
        t = Number()
        return t

class MatrixLiteral(Literal, Expression):

    def __init__(self, matrix):
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

    def check(self):
        if self._matrix is not None and self._matrix != []:
            for row in self._matrix:
                for elm in row : 
                    if type(elm.check) is not Number : 
                        print " Error en matriz literal, expresion no es numerica"
        t = Matrix()
        return t 

class FunctionCall(Expression):

    def __init__(self, identifier, args):
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

class Sum(BinaryExpression):

    def __init__(self, left, right):
        super(Sum, self).__init__(left, lambda x,y: x + y, right)
        self._operation = "Sum"

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) & (type(rtype) is Number) :
            
            return rtype
        else:
            print " Error: trying to (+)  %s expression with %s \n " % (ltype.__str__(),rtype.__str__())  
        

class Subtraction(BinaryExpression):

    def __init__(self, left, right):
        super(Subtraction, self).__init__(left, lambda x,y: x - y, right)
        self._operation = "Subtraction"

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) & ( type(rtype) is Number) :
            
            return rtype
        else:
            print " Error: trying to (-)  %s expression with %s \n " % (ltype.__str__(),rtype.__str__()) 

class Times(BinaryExpression):

    def __init__(self, left, right):
        super(Times, self).__init__(left, lambda x,y: x * y, right)
        self._operation = "Multiplication"
    
    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) & ( type(rtype) is Number) :
            
            return rtype
        else:
            print " Error: trying to (*)  %s expression with %s \n " % (ltype.__str__(),rtype.__str__()) 

class Division(BinaryExpression):

    def __init__(self, left, right):
        super(Division,self).__init__(left, lambda x,y: x//y, right)
        self._operation = "Division" 

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) & (type(rtype) is Number) :
            
            return rtype
        else:
            print " Error: trying to div  %s expression with %s \n " % (ltype.__str__(),rtype.__str__()) 

class Modulus(BinaryExpression):
    
    def __init__(self, left, right):
        super(Modulus, self).__init__(left, lambda x,y: x % y, right)
        self._operation = "Modulus"
    
    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) & (type(rtype) is Number) :
            
            return rtype
        else:
            print " Error: trying to mod  %s expression with %s \n " % (ltype.__str__(),rtype.__str__()) 


class RealDivision(BinaryExpression):

    def __init__(self, left, right):
        super(RealDivision, self).__init__(left, lambda x,y: x / y, right)
        self._operation = "Real Division"

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) & ( type(rtype) is Number) :
            
            return rtype
        else:
            print " Error: trying to /  %s expression with %s \n " % (ltype.__str__(),rtype.__str__()) 


class RealModulus(BinaryExpression):
    
    def __init__(self, left, right):
        super(RealModulus, self).__init__(left, lambda x,y: x % y, right)
        self._operation = "Real Modulus"

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) & (type(rtype) is Number) :
            return rtype
        else:
             print " Error: trying to (%)  %s expression with %s \n " % (ltype.__str__(),rtype.__str__()) 


class MatrixSum(BinaryExpression):

    def __init__(self, left, right):
        super(MatrixSum, self).__init__(left, None, right)
        self._operation = "Matrix Sum"

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) & (type(rtype) is Matrix):
            return rtype
        elif (type(ltype) is Number) & (type(rtype) is Matrix) : 
            return ltype
        else:
            print " Error: trying to (.+.)  %s expression with %s \n " % (ltype.__str__(),rtype.__str__())
    

class MatrixSubtraction(BinaryExpression):

    def __init__(self, left, right):
        super(MatrixSubtraction, self).__init__(left, None, right)
        self._operation = "Matrix Subtraction"

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) & (type(rtype) is Matrix):
            return rtype
        elif (type(ltype) is Number) & (type(rtype) is Matrix) : 
            return ltype
        else:
            print " Error: trying to (.-.)  %s expression with %s \n " % (ltype.__str__(),rtype.__str__())


class MatrixTimes(BinaryExpression):

    def __init__(self, left, right):
        super(MatrixTimes, self).__init__(left, None, right)
        self._operation = "Matrix Multiplication"

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) & (type(rtype) is Matrix):
            return rtype
        elif (type(ltype) is Number) & (type(rtype) is Matrix) : 
            return ltype
        else:
            print " Error, trying to (.*.)  %s expression with %s \n " % (ltype.__str__(),rtype.__str__())


class MatrixDivision(BinaryExpression):

    def __init__(self, left, right):
        super(MatrixDivision, self).__init__(left, None, right)
        self._operation = "Matrix Division"

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) & (type(rtype) is Matrix):
            return rtype
        elif (type(ltype) is Number) & (type(rtype) is Matrix) : 
            return ltype
        else:
            print " Error: trying to (.div)  %s expression with %s \n " % (ltype.__str__(),rtype.__str__())


class MatrixModulus(BinaryExpression):

    def __init__(self, left, right):
        super(MatrixModulus, self).__init__(left, None, right)
        self._operation = "Matrix Modulus"

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) & (type(rtype) is Matrix):
            return rtype
        elif (type(ltype) is Number) & (type(rtype) is Matrix) : 
            return ltype
        else:
            print " Error: trying to (.mod.)  %s expression with %s \n " % (ltype.__str__(),rtype.__str__())



class MatrixRealDivision(BinaryExpression):

    def __init__(self, left, right):
        super(MatrixRealDivision, self).__init__(left, None, right)
        self._operation = "Matrix Real Division"

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) & (type(rtype) is Matrix):
            return rtype
        elif (type(ltype) is Number) & (type(rtype) is Matrix) : 
            return ltype
        else:
            print " Error: trying to (./.)  %s expression with %s \n " % (ltype.__str__(),rtype.__str__())


class MatrixRealModulus(BinaryExpression):

    def __init__(self, left, right):
        super(MatrixRealModulus, self).__init__(left, None, right)
        self._operation = "Matrix Real Modulus"

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is Number) & (type(rtype) is Matrix):
            return rtype
        elif (type(ltype) is Number) & (type(rtype) is Matrix) : 
            return ltype
        else:
            print " Error: trying to (.%.)  %s expression with %s \n " % (ltype.__str__(),rtype.__str__())


class Equivalence(BinaryExpression):

    def __init__(self, left, right):
        super(Equivalence, self).__init__(left, lambda x,y: x == y, right)
        self._operation = "Equivalence"

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) == type(rtype)):
            t = Boolean()
            return t
        else:
            print " Error: comparing   %s expression with %s \n " % (ltype.__str__(),rtype.__str__())


class NotEquivalence(BinaryExpression):

    def __init__(self, left, right):
        super(NotEquivalence, self).__init__(left, lambda x,y: x != y, right)
        self._operation = "Not Equivalence"
   
    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) == type(rtype)):
            t = Boolean()
            return t
        else:
            print " Error: comparing   %s expression with %s \n " % (ltype.__str__(),rtype.__str__())


class GreaterOrEqual(BinaryExpression):

    def __init__(self, left, right):
        super(GreaterOrEqual, self).__init__(left, lambda x,y: x >= y, right)
        self._operation = "Greater Or Equal"

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if type(ltype) is not Number : 
            print " Error: comparing not numeric expression >=  " 
        if (type(ltype) == type(rtype)):
            t = Boolean()
            return t
        else:
            print " Error: comparing   %s expression with %s \n " % (ltype.__str__(),rtype.__str__())

class LessOrEqual(BinaryExpression):

    def __init__(self, left, right):
        super(LessOrEqual, self).__init__(left, lambda x,y: x <= y, right)
        self._operation = "Less Or Equal"

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if type(ltype) is not Number : 
            print " Error: comparing not numeric expression <=  " 
        if (type(ltype) == type(rtype)):
            t = Boolean()
            return t
        else:
            print " Error: comparing   %s expression with %s \n " % (ltype.__str__(),rtype.__str__())

class Greater(BinaryExpression):

    def __init__(self, left, right):
        super(Greater, self).__init__(left, lambda x,y: x > y, right)
        self._operation = "Greater"

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if type(ltype) is not Number : 
            print " Error: comparing not numeric expression for > " 
        if (type(ltype) == type(rtype)):
            t = Boolean()
            return t
        else:
            print " Error: comparing   %s expression with %s \n " % (ltype.__str__(),rtype.__str__())


class Less(BinaryExpression):

    def __init__(self, left, right):
        super(Less, self).__init__(left, lambda x,y: x < y, right)
        self._operation = "Less"

    def check(self, symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if type(ltype) is not Number : 
            print " Error: comparing not numeric expression for < \n" 
        if (type(ltype) == type(rtype)):
            t = Boolean()
            return t
        else:
            print " Error: comparing   %s expression with %s \n " % (ltype.__str__(),rtype.__str__())


class And(BinaryExpression):

    def __init__(self, left, right):
        super(And, self).__init__(left, lambda x,y: x and y, right)
        self._operation = "And"
           
    def check(self,symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is not  Boolean) : 
            print " Error : left operand is not of type boolean \n" 
        if (type(rtype) is not  Boolean) : 
            print " Error : right operand is not of type boolean \n" 
        else : 
            t=Boolean()
            return t
    

class Or(BinaryExpression):

    def __init__(self, left, right):
        super(Or, self).__init__(left, lambda x,y: x or y, right)
        self._operation = "Or"
          
    def check(self,symtab):
        ltype = self._left.check(symtab)
        rtype = self._right.check(symtab)
        if (type(ltype) is not  Boolean) : 
            print " Error : left operand is not of type boolean \n" 
        if (type(rtype) is not  Boolean) : 
            print " Error : right operand is not of type boolean \n" 
        else : 
            t=Boolean()
            return t

class UnaryExpression(Expression):

    def __init__(self, op, operand):
        super(UnaryExpression, self).__init__()
        self._function = op
        self._operand = operand
        self._operation = ""

    def printAST(self, level):
        string  = "%s%s:" % (self.getIndent(level), self._operation)
        string += "\n%sOperand:" % self.getIndent(level+1)
        string += "\n" + self._operand.printAST(level+2)
        return string


class UnaryMinus(UnaryExpression):
    
    def __init__(self, operand):
        super(UnaryMinus, self).__init__(lambda x: - x, operand)
        self._operation = "Unary Minus"
        
    def check(self,symtab):
        otype = self._operand.check(symtab)
        if type(otype) is Boolean:
           print " Can't apply Unary Minus to boolean expression " 
        else:
           return otype

class Transpose(UnaryExpression):
    
    def __init__(self, operand):
        super(Transpose, self).__init__(None, operand)
        self._operation = "Matrix Transpose"
   
        
class Not(UnaryExpression):
    
    def __init__(self, operand):
        super(Not, self).__init__(lambda x: not x, operand)
        self._operation = "Not"
