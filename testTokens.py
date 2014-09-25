from lexer.token import Token

class Tk_plus(Token):
	pattern = r'\+'

class Tk_minus(Token):
	pattern = r'-'

class Tk_equals(Token):
	pattern = r'='

class Tk_num(Token):
	patter = r'\d'