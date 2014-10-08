#!/usr/bin/env python
# ------------------------------------------------------------
# exceptions.py
#
# Exceptions for the lexer
#
# Authors:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# Francisco Martinez, 09-10502, <frammnm@gmail.com>
# ------------------------------------------------------------

class TokensNotDefinedException(Exception):
    pass

class InputNotProvidedException(Exception):
    pass

class PatternNotDefinedException(Exception):
    pass

class LexicographicalError(Exception):

    def __init__(self, errors, *args, **kwargs):
        super(LexicographicalError, self).__init__(args,kwargs)
        self._error_list = errors

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        string = "LexicographicalError: The following lexicographical errors were found:\n"
        for error in self._error_list:
            string += "\n\t%s" % error
        return string
        