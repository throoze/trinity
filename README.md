Trinity
=======

Version: 0.0.1

Trinity is an imperative programming language with static scope and types
focused in linear algebra over real numbers basics, with direct support for
operations between scalars, vectors and matrixes. Its main influence is
[_Octave_](http://www.gnu.org/software/octave/) language.

This project is an implementation of an interpreter of the Trinity language,
written in Python, using a custom lexer, and [PLY](http://www.dabeaz.com/ply/)'s
parser - `yacc` -. Details on the implementation will be documented here. So
far, the lexer and the definition of tokens are finished. Lexer integration with
PLY's yacc, and the definition of the grammar are currently being implemented. 


Contents:
---------

1. [Example Trinity program](https://github.com/throoze/trinity#example-trinity-program)
2. [Trinity Lexical components](https://github.com/throoze/trinity#trinity-lexical-components)
3. [Trinity's grammar](https://github.com/throoze/trinity#trinity-grammar)


Example trinity program:
------------------------

    program
    use
      matrix(2,2) m;  # all elements initialized as '0'
      number x;       # initialized as '0'
      boolean b;      # initialized as 'false'
    in
      set m = { 1, 2
              : 3, 4 };

      read x;

      for i in m do
        if i % 2 == 0 then
          # if 'i' is even
          print i;
        else
          print x;
          read x;
          set b = not b;
        end;
      end;

      if b then
        print i;
      else
        print "b is a lie";
      end;
    end;

[Go to top](https://github.com/throoze/trinity#trinity)

Trinity Lexical components:
---------------------------
[Go to top](https://github.com/throoze/trinity#trinity)

There's a limited set of valid lexemes in Trinity. They must be written using
only [ASCII](http://tools.ietf.org/html/rfc20) characters. The following is a
complete list of the valid lexemes and their semantics.

|    Token    |   Lexeme  |                           Semantics                           |                                   Example                                   |
|:-----------:|:---------:|:-------------------------------------------------------------:|:---------------------------------------------------------------------------:|
| Tk_Comment  | # comment | Ignored text, for documentation purposes                      | # this is a comment                                                         |
| Tk_str      |  "String" | Text string literal, written between double quotes            | "This is a string with \n\"more text\""                                     |
| Tk_true     |    true   | Reserved word. Boolean literal true                           |                                                                             |
| Tk_false    |   false   | Reserved word. Boolean literal false                          |                                                                             |
| Tk_bool     |  boolean  | Reserved word. Boolean type specificator                      | boolean b;                                                                  |
| Tk_number   |   number  | Reserved word. Number type specificator                       | number n;                                                                   |
| Tk_mat      |   matrix  | Reserved word. Matrix type specificator                       | matrix(4,2) m;                                                              |
| Tk_row      |    row    | Reserved word. Row type (row vector) specificator             | row(42) r;                                                                  |
| Tk_col      |    col    | Reserved word. Column type (column vector) specificator       | col(42) c;                                                                  |
| Tk_not      |    not    | Reserved word. Not unary boolean operator                     | not true;                                                                   |
| Tk_div      |    div    | Reserved word. Integer division operator                      | 5 div 3; # equals 1                                                         |
| Tk_mod      |    mod    | Reserved word. Integer module operator                        | 5 mod 3; # equals 2                                                         |
| Tk_print    |   print   | Reserved word. Prints expressions in standard output.         | print "Hello world";                                                        |
| Tk_use      |    use    | Reserved word. Marks start of variable declaration block.     | use number n = 42; in print n; end;                                         |
| Tk_in       |     in    | Reserved word. Marks start of code block.                     | use number n = 42; in print n; end;                                         |
| Tk_end      |    end    | Reserved word. Marks end of code block.                       | use number n = 42; in print n; end;                                         |
| Tk_set      |    set    | Reserved word. Marks start of assignment.                     | set n = 42;                                                                 |
| Tk_read     |    read   | Reserved word. Reads expression from standard input.          | read e;                                                                     |
| Tk_if       |     if    | Reserved word. Starts selection statement.                    | if cake then print "The cake is true"; else print "The cake is a lie"; end; |
| Tk_then     |    then   | Reserved word. Starts selection statement's normal flow.      | if cake then print "The cake is true"; else print "The cake is a lie"; end; |
| Tk_else     |    else   | Reserved word. Starts selection statement's alternative flow. | if cake then print "The cake is true"; else print "The cake is a lie"; end; |
| Tk_for      |    for    | Reserved word. Starts matrix based iteration.                 | for i in matrix do print "element: ", i; end;                               |
| Tk_do       |    do     | Reserved word. Starts iteration's body.                       | for i in matrix do print "element: ", i; end;                               |
| Tk_while    |   while   | Reserved word. Starts conditional iteration.                  | while i < 10 do print i; set i = i + 1; end;                                |
| Tk_function |  function | Reserved word. Starts function definition.                    | function foo(number n) return boolean begin print n; return true; end;      |
| Tk_ret      |   return  | Reserved word. Used in function definition.                   | function foo(number n) return boolean begin print n; return true; end;      |
| Tk_beg      |   begin   | Reserved word. Starts function definition code block.         | function foo(number n) return boolean begin print n; return true; end;      |
| Tk_prog     |  program  | Reserved word. Starts a trinity program code block.           | program print "Hello world"; end;                                           |
| Tk_ID       |    foo    | Any variable or function identifier.                          | print foo;                                                                  |
| Tk_minus    |     -     | Unary minus or binary scalar or matrix subtraction.           | -42; 4 - 2;                                                                 |
| Tk_num      |     42    | Numeric literal, may include decimals.                        | 42;                                                                         |
| Tk_mplus    |    .+.    | Scalar or matrix addition.                                    | a + 42                                                                      |
| Tk_mminus   |    .-.    | Crossed subtraction between a scalar and a matrix.            | { 1, 2 : 3, 4 } .+. 42;                                                     |
| Tk_mtimes   |    .*.    | Crossed multiplication between a scalar and a matrix.         | { 1, 2 : 3, 4 } .*. 42;                                                     |
| Tk_mrdiv    |    ./.    | Crossed real divition between a scalar and a matrix.          | { 1, 2 : 3, 4 } ./. 42;                                                     |
| Tk_mrmod    |    .%.    | Crossed real module between a scalar and a matrix.            | { 1, 2 : 3, 4 } .%. 42;                                                     |
| Tk_mdiv     |   .div.   | Crossed integer divition between a scalar and a matrix.       | { 1, 2 : 3, 4 } .div. 42;                                                   |
| Tk_mmod     |   .mod.   | Crossed integer module between a scalar and a matrix.         | { 1, 2 : 3, 4 } .mod. 42;                                                   |
| Tk_eq       |     ==    | Equivalence                                                   | false == false == true;                                                     |
| Tk_neq      |     /=    | Not equivalence                                               | false == true /= true;                                                      |
| Tk_leq      |     <=    | Less or equal than                                            | 10 <= 42 == true;                                                           |
| Tk_geq      |     >=    | Greater or equal than                                         | 100 >= 42 == true;                                                          |
| Tk_comma    |     ,     | Arguments and row elements separator.                         | foo(arg0, { 1, 2 : 3, 4 });                                                 |
| Tk_colon    |     :     | Columns separator                                             | { 1, 2 : 3, 4 }                                                             |
| Tk_scolon   |     ;     | Discards the value of an expression.                          | 10;                                                                         |
| Tk_obrace   |     {     | Open brace. Used in literal matrix.                           | { 1, 2 : 3, 4 }                                                             |
| Tk_cbrace   |     }     | Close brace. Used in literal matrix.                          | { 1, 2 : 3, 4 }                                                             |
| Tk_oparen   |     (     | Open parenthesis. Used in function calls and definition.      | foo(bar);                                                                   |
| Tk_cparen   |     )     | Close parenthesis. Used in function calls and definition.     | foo(bar);                                                                   |
| Tk_obrack   |     [     | Open bracket. Used when accessing matrix elements.            | m[1,2];                                                                     |
| Tk_cbrack   |     ]     | Close bracket. Used when accessing matrix elements.           | m[1,2];                                                                     |
| Tk_and      |     &     | AND boolean operator                                          | true & false == false;                                                      |
| Tk_or       |     \|    | OR boolean operator                                           | true | false == true;                                                       |
| Tk_assign   |     =     | Asignment                                                     | set n = 42;                                                                 |
| Tk_great    |     >     | Greater than                                                  | 100 > 42 == true;                                                           |
| Tk_less     |     <     | Less than                                                     | 10 < 42 == true;                                                            |
| Tk_plus     |     +     | Scalar and matrix addition.                                   | { 1, 2 : 3, 4 } + { 5, 6 : 7, 8 } == { 6, 8 : 10, 12 } == true;             |
| Tk_times    |     *     | Scalar and matrix multiplication.                             | 6 * 7 == 42 == true;                                                        |
| Tk_rdiv     |     /     | Scalar real division.                                         | 84 / 2 == 42 == true;                                                       |
| Tk_rmod     |     %     | Scalar real module                                            | 4.2 % 2 == 0.2 == true;                                                     |
| Tk_trans    |     '     | Transpose matrix.                                             | m';                                                                         |

Tokens in this list are matched in the same order as they appear here, hence the
first token shown has more precedence when being matched than the following one.

[Go to top](https://github.com/throoze/trinity#trinity)

## Trinity Grammar:
[Go to top](https://github.com/throoze/trinity#trinity)

Next is the grammar that specifies Trinity's syntax. Capitalized words represent
production rules. The initial production rule is **Trinity**. Terminal nodes are
shown as their Token names, as listed in the table of
[lexemes](https://github.com/throoze/trinity#trinity-lexical-components), in the
column **Tokens**. The _empty rule_ is represented with the word _lambda_. Some
rules are unnecesary, but are written anyways for readability purposes.

```
Trinity : FuncDefinitions Tk_prog InstBlock Tk_end Tk_scolon
```

```
FuncDefinitions : FuncDefinitions FuncDefinition
                | lambda
```

```
FuncDefinition : Tk_function Tk_ID Tk_oparen FormalParams Tk_cparen Tk_ret Type FunctionBody
```

```
FunctionBody : Tk_beg FunInstBlock Tk_end Tk_scolon
```

```
FormalParams : FParamList
             | lambda
```

```
FParamList : FormalParam
           | FParamList Tk_comma FormalParam
```

```
FormalParam : Type Tk_ID
```

```
Type : Tk_bool
     | Tk_number
     | Tk_mat Tk_oparen Tk_num Tk_comma Tk_num Tk_cparen
     | Tk_row Tk_oparen Tk_num Tk_cparen
     | Tk_col Tk_oparen Tk_num Tk_cparen
```

```
InstBlock : InstList
          | lambda
```

```
InstList : Statement
         | InstList Statement
```

```
Statement : Matched
          | Unmatched
```

```
Matched : Tk_if Expression Tk_then Matched Tk_else Matched Tk_end Tk_scolon
        | Print
        | Read
        | Assignment
        | While
        | For
        | Block
```

```
Unmatched : Tk_if Expression Tk_then Statement Tk_end Tk_scolon
          | Tk_if Expression Tk_then Matched Tk_else Unmatched Tk_end Tk_scolon
```

```
FunInstBlock : FunInstList
             |  lambda
```

```
FunInstList : FunStatement
            | FunInstList FunStatement
```

```
FunStatement : FunMatched
             | FunUnmatched
```

```
FunMatched : Tk_if Expression Tk_then FunMatched Tk_else FunMatched Tk_end Tk_scolon
           | Print
           | Read
           | Assignment
           | FunWhile
           | FunFor
           | Return
           | FunBlock
```

```
FunUnmatched : Tk_if Expression Tk_then FunStatement Tk_end Tk_scolon
             | Tk_if Expression Tk_then FunMatched Tk_else FunUnmatched Tk_end Tk_scolon
```

```
Print : Tk_print PrintableList
```

```
PrintableList : Printable
              | PrintableList Tk_comma Printable
```

```
Printable : Expression
          | Tk_str
```

```
Read : Tk_read Tk_ID Tk_scolon
```

```
Assignment : Tk_set LeftSide Expression Tk_scolon
```

```
LeftSide : Tk_ID
         | Tk_ID Tk_obrack Tk_num Tk_cbrack
         | Tk_ID Tk_obrack Tk_num Tk_comma Tk_num Tk_cbrack
```

```
While : Tk_while Expression Tk_do InstBlock Tk_end Tk_scolon
```

```
For : Tk_for Tk_ID Tk_in Expression Tk_do InstBlock Tk_end Tk_scolon
```

```
Block : Tk_use VariableDeclarations Tk_in InstBlock Tk_end Tk_scolon
```

```
FunWhile : Tk_while Expression Tk_do FunInstBlock Tk_end Tk_scolon
```

```
FunFor : Tk_for Tk_ID Tk_in Expression Tk_do FunInstBlock Tk_end Tk_scolon
```

```
Return : Tk_ret Expression Tk_scolon
```

```
FunBlock : Tk_use VariableDeclarations Tk_in FunInstBlock Tk_end Tk_scolon
```

```
VariableDeclarations : VariableDeclaration
                     | VariableDeclarations VariableDeclaration
```

```
VariableDeclaration : Type Tk_ID Tk_scolon
                    | Type Tk_ID Tk_assign Expression Tk_scolon
```

```
Expression : Tk_oparen Expression Tk_cparen
           | UnaryOperatorExpression
           | Expression BinaryOperator Expression
           | LeftSide
           | FunctionCall
           | Literal
```

```
UnaryOperatorExpression : Tk_minus Expression %prec UMINUS
                        | Matrix Tk_trans
                        | Tk_ID Tk_trans
                        | Tk_not Expression
```

```
Literal : Matrix
        | Tk_true
        | Tk_false
        | Tk_num
```

```
Matrix : Tk_obrace RowList Tk_cbrace
```

```
RowList : Row
        | RowList Tk_colon Row
```

```
Row : Tk_num                # TODO: Check if it's a number or an expression
    | Row Tk_comma Tk_num 
```

```
FunctionCall : Tk_ID Tk_oparen Params Tk_cparen Tk_scolon
```

```
Params : ParamList
       | lambda
```

```
ParamList : Expression
          | ParamList Tk_comma Expression
```

```
BinaryOperator : ArithmeticBinaryOperator
               | BooleanBinaryOperator
```

```
ArithmeticBinaryOperator : OverloadedBinaryOperator
                         | ScalarBinaryOperator
                         | CrossedBinaryOperator
```

```
OverloadedBinaryOperator : Tk_plus
                         | Tk_minus
                         | Tk_times
```

```
ScalarBinaryOperator : Tk_div
                     | Tk_mod
                     | Tk_rdiv
                     | Tk_rmod
```

```
CrossedBinaryOperator : Tk_mplus
                      | Tk_mminus
                      | Tk_mtimes
                      | Tk_mdiv
                      | Tk_mmod
                      | Tk_mrdiv
                      | Tk_mrmod
```

```
BooleanBinaryOperator : Tk_eq
                      | Tk_neq
                      | Tk_leq
                      | Tk_geq
                      | Tk_great
                      | Tk_less
                      | Tk_and
                      | Tk_or
```

[Go to top](https://github.com/throoze/trinity#trinity)












    