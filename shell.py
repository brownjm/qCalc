"""Quantum mechanics calculator

Run using:

python QMcalc.py


"""

from environment import Environment

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
        
                
            """
            except iostream.InputError as i:
                print ' '*(i.loc+2) + '^' # displays caret under error
                print i.msg
            except classify.ClassificationError as c:
                print c.msg
            """
    def exit(self, args, flags):
        print 'Goodbye!!'

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

commands = ["exit", "dummy"]

if __name__ == '__main__':
    CLP = CommandLinePrompt()
    CLP.run()
