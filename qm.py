"""Quantum mechanical plugin"""

class QMType(MathType):
    """Base type for all quantum mechanical types"""
    def __init__(self, val):
        self.val = val

class Operator(QMType):
    """Class for representing operators"""
    def __init__(self, name):
        QMType.__init__(self, name)

class State(QMType):
    """Class for representing bras and kets in Dirac notation: <a| or |a>"""
    def __init__(self, stateType, name):
        QMType.__init__(self, name)
        self.stateType = stateType  #Bra or Ket

class Bra(State):
    """Class for representing a bra in Dirac notation: <a|"""
    def __init__(self, name):
        State.__init__(self, "bra", name)

class Ket(State):
    """Class for representing a ket in Dirac notation: |a>"""
    def __init__(self, name):
        State.__init__(self, "ket", name)

# Dictionary containing regular expressions of quantum mechanical string tokens
# and their associated classes
inputDict = {'^([a-zA-Z][a-zA-Z0-9]*)$': Operator,
             '^<([a-zA-Z][a-zA-Z0-9]*)[|]$': Bra,
             '^[|]([a-zA-Z][a-zA-Z0-9]*)>$': Ket}

# Dictionary containing quantum mechanical classes and their associated strings
# tokens
outputDict = {Operator: 'val',
              Bra: '<val|',
              Ket: '|val>'}
