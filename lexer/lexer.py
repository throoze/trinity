#!/usr/bin/env python
# ------------------------------------------------------------
# lexer.py
#
# Lexer
#
# Authors:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# Francisco Martinez, 09-10502, <frammnm@gmail.com>
#
# Usage:
#
# ------------------------------------------------------------

class Lexer():

	def __init__(self, module=None, filename=None):
		if filename is not None and filename != '':
			self.file = open(filename, 'r')
		if module is not None:
			from module import *

