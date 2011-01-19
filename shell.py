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

    def run(self):
        """Begin the command line program"""
        print """
#    Quantum Mechanics Calculator 
#
#    Copyright (C) 2010  Jeffrey M. Brown, Kyle T. Taylor, Greg A. Cohoon
#
#    Type 'exit' to quit.
     
"""
        while 1:
            try:
                line = raw_input('> ') # get a line from the prompt
                self.env.addToHistory(line) #add to history
                command = line.split(' ')[0]
                aftercommand = line.split(' ')[1:]
                args = filter(lambda s: s[0] != '-', aftercommand)
                flags = filter(lambda s: s[0] == '-', aftercommand)
                
                if command in commands:
                    exec 'self.' + command + '(args, flags)'    
                    if command == 'exit':
                        break
                        
                else:
                    print self.env.Eval(line)
            except Exception as ex:
                print ex
                
            """
            except iostream.InputError as i:
                print ' '*(i.loc+2) + '^' # displays caret under error
                print i.msg
            except classify.ClassificationError as c:
                print c.msg
            """
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

    def dummy(self, args, flags):
        print 'args: ', args
        print 'flags: ', flags

"""
def main(line):
    c = classify.Classifier(QMTypes.inputDict, QMTypes.outputDict)
    
    inputTokenList = iostream.parse(line) # parse input
    classList = []

    expr=c.toExpr(inputTokenList)
    res=Evaluator.Evaluate(expr)

    print iostream.assemble(c.toTokenList(res))
     # display all classes that were identified
""" 

commands = ["exit", "let", "get", "dummy"]

if __name__ == '__main__':
    CLP = CommandLinePrompt()
    CLP.run()
