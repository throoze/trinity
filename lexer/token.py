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

class Token:
    __metaclass__ = ABCMeta

    @abstractmethod
    def say_something(self): pass