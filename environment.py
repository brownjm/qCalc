"""Module containing classes and functions to support a computational
environment."""

import copy, pickle
from plugin import PluginEngine
from io import IOEngine
from calc import CalcEngine

class Environment(object):
    """Class to represent an environment for performing calculations. Stores
items such as variables, current objects in environment, command history, etc.
"""
    def __init__(self):
        self.PluginEngine = PluginEngine()
        self.loadedPlugins = self.PluginEngine.loadedPlugins.keys()
        self.IOEngine = IOEngine(self.PluginEngine.inputDict,
                                 self.PluginEngine.outputDict,
                                 self.PluginEngine.parseOrder,
                                 self.PluginEngine.orderOfOperations,
                                 self.PluginEngine.containers) #Reference to IO Engine
        self.CalcEngine  = CalcEngine()  #Reference to Calc Engine
        self.history = []   #History of the user's actions
        self.variables = {} #Variables the user can create

    def addToHistory(self, histtoadd):
        """Method to add to the history"""
        self.history.append(histtoadd)

    def getFromHistory(self, index=-1):
        """Method to get from the history"""
        if(index == -1):
            return self.history[len(self.history) - 1]

        return self.history[index]

    def addVariable(self, variable):
        """Method to store a variable"""
        self.variables[repr(variable)] = variable

    def getVariable(self, variableStr):
        """Method to retrieve a variable"""
        return self.variables[variableStr]

    def Eval(self, inputStr):
        """Method to provide evaluation control to shell"""
        exprTree = self.IOEngine.parse(inputStr)
        redTree = self.CalcEngine.Evaluate(exprTree)
        finalStr = self.IOEngine.output(redTree)
        return finalStr
    
    """
    def save(self, filename):
        Save environment to disk to resume later.
        with open(filename + '.env', 'wb') as f: # ensures file gets closed
            saveList = [self.var, self.objects, self.history]
            pickle.dump(saveList, f, 2)

    def load(self, filename):
        Load previously saved environment
        with open(filename + '.env', 'rb') as f:
            loadList = pickle.load(f)
            self.var = loadList[0]
            self.objects = loadList[1]
            self.history = loadList[2]
    """
    
defaultCommands = {'quit': quit,
                   'exit': exit,
                   'save': 'self.save',
                   'load': 'self.load'}

if __name__ == '__main__':
    env = Environment()
    ans = env.Eval("4+3*2+8*3")
    print ans
