Trinity
=======

Trinity is an imperative programming language with static scope and types
focused in linear algebra over real numbers basics, with direct support for
operations between scalars, vectors and matrixes. Its main influence is
[_Octave_](http://www.gnu.org/software/octave/) language.

Example trinity program:
------------------------

    program
    use
      matrix(2,2) m;  # initialized all as '0'
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

#Trinity Lexical components:

There's a limited set of valid lexemes in Trinity. They must be written using
only [ASCII](http://tools.ietf.org/html/rfc20) characters. The following is a
complete list of the valid lexemes and their semantics.

|    Token    |   Lexeme  |                           Semantics                           |                                   Example                                   |
|:-----------:|:---------:|:-------------------------------------------------------------:|:---------------------------------------------------------------------------:|
| Tk_Comment  | # comment | Ignored text, for documentation purposes                      | # this is a comment                                                         |
| Tk_str      |  "String" | Text string literal, written between double quotes            | "This is a string with \n\"more text\""                                     |
| Tk_true     |    true   | Boolean literal true                                          |                                                                             |
| Tk_false    |   false   | Boolean literal false                                         |                                                                             |
| Tk_bool     |  boolean  | Boolean type specificator                                     | boolean b;                                                                  |
| Tk_number   |   number  | Number type specificator                                      | number n;                                                                   |
| Tk_mat      |   matrix  | Matrix type specificator                                      | matrix(4,2) m;                                                              |
| Tk_row      |    row    | Row type (row vector) specificator                            | row(42) r;                                                                  |
| Tk_col      |    col    | Column type (column vector) specificator                      | col(42) c;                                                                  |
| Tk_not      |    not    | Not unary boolean operator                                    | not true;                                                                   |
| Tk_div      |    div    | Integer division operator                                     | 5 div 3; # equals 1                                                         |
| Tk_mod      |    mod    | Integer module operator                                       | 5 mod 3; # equals 2                                                         |
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
| Tk_do       |   Tk_do   | Reserved word. Starts iteration's body.                       | for i in matrix do print "element: ", i; end;                               |
| Tk_while    |   while   | Reserved word. Starts conditional iteration.                  | while i < 10 do print i; set i = i + 1; end;                                |
| Tk_function |  function | Reserved word. Starts function definition.                    | function foo(number n) return boolean begin print n; return true; end;      |
| Tk_ret      |   return  | Reserved word. Used in function definition.                   | function foo(number n) return boolean begin print n; return true; end;      |
| Tk_beg      |   begin   | Reserved word. Starts function definition code block.         | function foo(number n) return boolean begin print n; return true; end;      |
| Tk_prog     |  program  | Reserved word. Starts a trinity program code block.           | program print "Hello world"; end;                                           |
| Tk_ID       |    foo    | Any variable or function identifier.                          | print foo;                                                                  |
| Tk_minus    |     -     | Unary minus or binary scalar or matrix subtraction.           | -42; 4 - 2;                                                                 |
| Tk_num      |     42    | Numeric literal, may include decimals.                        | 42;                                                                         |
| Tk_mplus    |     +     | Scalar or matrix addition.                                    | a + 42                                                                      |
| Tk_mminus   |    .-.    | Crossed subtraction between a scalar and a matrix.            | { 1, 2 : 3, 4 } .+. 42;                                                     |
| Tk_mtimes   |    .*.    | Crossed multiplication between a scalar and a matrix.         | { 1, 2 : 3, 4 } .*. 42;                                                     |
| Tk_mrdiv    |    ./.    | Crossed real divition between a scalar and a matrix.          | { 1, 2 : 3, 4 } ./. 42;                                                     |
| Tk_mrmod    |    .%.    | Crossed real module between a scalar and a matrix.            | { 1, 2 : 3, 4 } .%. 42;                                                     |
| Tk_mdiv     |   .div.   | Crossed integer divition between a scalar and a matrix.       | { 1, 2 : 3, 4 } .div. 42;                                                   |
| Tk_mmod     |   .mod.   | Crossed integer module between a scalar and a matrix.         | { 1, 2 : 3, 4 } .mod. 42;                                                   |
| Tk_eq       |     ==    | Equivalence                                                   |                                                                             |
| Tk_neq      |     /=    | Not equivalence                                               |                                                                             |
| Tk_leq      |     <=    | Less or equal than                                            |                                                                             |
| Tk_geq      |     >=    | Greater or equal than                                         |                                                                             |
| Tk_comma    |     ,     | Arguments and row elements separator.                         | foo(arg0, { 1, 2 : 3, 4 });                                                 |
| Tk_colon    |     :     | Columns separator                                             | { 1, 2 : 3, 4 }                                                             |
| Tk_scolon   |     ;     | Discards the value of an expression.                          | 10;                                                                         |
| Tk_obrace   |     {     | Open brace. Used in literal matrix.                           | { 1, 2 : 3, 4 }                                                             |
| Tk_cbrace   |     }     | Close brace. Used in literal matrix.                          | { 1, 2 : 3, 4 }                                                             |
| Tk_oparen   |     (     | Open parenthesis. Used in function calls and definition.      | foo(bar);                                                                   |
| Tk_cparen   |     )     | Close parenthesis. Used in function calls and definition.     | foo(bar);                                                                   |
| Tk_obrack   |     [     | Open bracket. Used when accessing matrix elements.            | m[1,2];                                                                     |
| Tk_cbrack   |     ]     | Close bracket. Used when accessing matrix elements.           | m[1,2];                                                                     |
| Tk_and      |     &     | AND boolean operator                                          |                                                                             |
| Tk_or       |     |     | OR boolean operator                                           |                                                                             |
| Tk_assign   |     =     | Asignment                                                     |                                                                             |
| Tk_great    |     >     | Greater than                                                  |                                                                             |
| Tk_less     |     <     | Less than                                                     |                                                                             |
| Tk_plus     |     +     | Scalar and matrix addition.                                   |                                                                             |
| Tk_times    |     *     | Scalar and matrix multiplication.                             |                                                                             |
| Tk_rdiv     |     /     | Scalar real division.                                         |                                                                             |
| Tk_rmod     |     %     | Scalar real module                                            |                                                                             |
| Tk_trans    |     '     | Transpose matrix.                                             |                                                                             |


#Trinity Grammar:



Trinity
