#!/usr/bin/env python
# ------------------------------------------------------------
# token.py
#
# BaseToken specification
#
# Authors:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# Francisco Martinez, 09-10502, <frammnm@gmail.com>
#
# Usage:
#
# ------------------------------------------------------------
from abc import ABCMeta, abstractmethod, abstractproperty
import re

class Token:
    __metaclass__ = ABCMeta

    def __init__(self, pattern=None):
    	if pattern is not None:
    		self.pattern = pattern
    	if self.pattern is not None:
    		self.regex = re.compile(self.pattern)
    	self.column = -1
    	self.line = -1
    	self.value = None