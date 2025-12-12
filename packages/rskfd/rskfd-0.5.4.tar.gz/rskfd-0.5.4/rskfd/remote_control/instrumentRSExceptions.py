# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 13:32:35 2019

@author: RAMIAN
"""

class InstrumentError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class FileLoadError(Exception):
    """Exception raised for file load fails.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message