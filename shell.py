"""Quantum mechanics calculator

Run using:

python shell.py


"""

from executable import Executable

class CommandLinePrompt(Executable):
    """Current interface to the quantum mechanics calculator."""
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
"""
    def historyLength(self):
        return len(self.env.history)

    def getFromHistory(self, index=-1):
        return self.env.getFromHistory(index)
"""

if __name__ == '__main__':
    CLP = CommandLinePrompt()
    CLP.run()
