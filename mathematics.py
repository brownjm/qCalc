"""Basic mathematical classes and functions."""

class MathType(object):
    """Base type for all mathematical classes"""
    def __init__(self, val):
        """Saves a string representation of the mathematical value"""
        self.val = val
    def __eq__(self, other):
        """Equivalence includes comparison of type and value"""
        return (type(self)==type(other)) and (self.val == other.val)

class Number(MathType):
    """Wrapper class for numerical values"""
    def __init__(self, value):
        MathType.__init__(self, value)
    def __eq__(self, other):
        """Equivalence includes type and floating point version of value"""
        return (type(self) == type(other)) and (float(self.val) == float(other.val))
    def Value(self):
        return float(self.val)

class Operation(MathType):
    """Class for basic mathematical operations, e.g. +, -, *, /"""
    def __init__(self, operation):
        MathType.__init__(self, operation)

class Quantity(MathType):
    """Class to represent mathematical quantities, such as (A+3*B)"""
    def __init__(self, quantity):
        MathType.__init__(self, quantity)

class Variable(MathType):
    """Class to represent a symbolic variable"""
    pass

class Expression(object):
    """Class to be used as a node when creating trees of Expressions"""
    def __init__(self, left, operation=None, right=None):
        self.left = left
        self.op = operation
        self.right = right

    def __eq__(self, other):
        """Equivalence includes comparison of children and operation"""
        return (self.left == other.left) and \
               (self.op == other.op) and \
               (self.right == other.right)

# Dictionary containing regular expressions of quantum mechanical string tokens
# and their associated classes
inputDict = {r'[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?': Number,
             '[+*/\-]|\^': Operation,
             '\((.+)\)': Quantity}

# Dictionary containing QM classes and their associated strings tokens
outputDict = {Number: 'val',
              Operation: 'val',
              Quantity: '(val)'}

