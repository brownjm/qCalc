"""Quantum mechanics calculator

Run using:

python shell.py


"""

from environment import Environment
from mathematics import Variable
from io import Expression

class CommandLinePrompt(object):
    """Current interface to the quantum mechanics calculator."""
    def __init__(self):
        self.env = Environment()

    def doWelcome(self):
        print """
#    Quantum Mechanics Calculator 
#
#    Copyright (C) 2010  Jeffrey M. Brown, Kyle T. Taylor, Greg A. Cohoon
#
#    Type 'exit' to quit.
     
"""

    def run(self):
        """Begin the command line program"""
        self.doWelcome()
        
        while 1:
            try:
                line = raw_input('> ') # get a line from the prompt

                command = self.execute(line)
                if command == 'exit':
                    break
                        
            except Exception as ex:
                print ex
                
    def execute(self, line):
        self.env.addToHistory(line) #add to history
        command = line.split(' ')[0]
        aftercommand = line.split(' ')[1:]
        args = filter(lambda s: s[0] != '-', aftercommand)
        flags = filter(lambda s: s[0] == '-', aftercommand)
        if command in commands:
            exec 'self.' + command + '(args, flags)'    
        else:
            print self.env.Eval(line)

        return command

    def historyLength(self):
        return len(self.env.history)

    def getFromHistory(self, index=-1):
        return self.env.getFromHistory(index)
    #
    #Command Methods
    #
    def exit(self, args, flags):
        print 'Goodbye!!'

    def let(self, args, flags):
        #Currently assuming args like this: ['name', '=', 'val']
        #account for possibilities of lack of spaces between name, =, and val
        var = Variable(args[0], args[2])
        self.env.addVariable(var)

    def get(self, args, flags):
        if len(args) == 0:
            raise Exception("A variable name is required.")

        var = self.env.getVariable(args[0])
        
        print args[0] + ':', var.Value()

    def variables(self, args, flags):
        #print self.env.variables.keys()
        for var in self.env.variables.keys():
            print var + ':', self.env.getVariable(var).Value()

    def dummy(self, args, flags):
        print 'args: ', args
        print 'flags: ', flags

commands = ["exit", "let", "get", "variables", "dummy"]

if __name__ == '__main__':
    CLP = CommandLinePrompt()
    CLP.run()
