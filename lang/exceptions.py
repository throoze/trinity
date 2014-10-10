#!/usr/bin/env python
# ------------------------------------------------------------
# exceptions.py
#
# Exceptions for the Trinity Language
#
# Authors:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# Francisco Martinez, 09-10502, <frammnm@gmail.com>
# ------------------------------------------------------------
class TrinitySyntaxError(Exception):

    def __init__(self, error, *args, **kwargs):
        super(TrinitySyntaxError, self).__init__(args,kwargs)
        self._error = error

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        string = "TrinitySyntaxError: %s" % self._error
        return string