#!/usr/bin/python

#import rpErrorHandler
from Tkinter import *
from environment import Environment
from shell import CommandLinePrompt
import sys

#------------------------------------------------------------------------------#
#                                                                              #
#                                   CalcGui                                    #
#                                                                              #
#------------------------------------------------------------------------------#
class CalcGui(Frame):
    def __init__(self,Master=None,**kw):
        #
        #Setting up the graphical components
        #        
        apply(Frame.__init__,(self,Master),kw)
        self.T = Text(self, state='disabled')
        self.s = Scrollbar(self)
        self.I = Entry(self)

        self.I.focus_set()
        self.I.pack(side=BOTTOM, fill=X)
        self.s.pack(side=RIGHT, fill=Y)
        self.T.pack(side=LEFT, fill=Y)
        self.s.config(command=self.T.yview)
        self.T.config(yscrollcommand=self.s.set)

        self.I.bind("<Up>", self.upkey)
        self.I.bind("<Down>", self.downkey)
        self.I.bind("<Return>", self.enterkey)

        #
        #Setting up control
        #
        self.opWrap = OutputWrapper(self)
        sys.stdout = self.opWrap
        
        self.shell = CommandLinePrompt()
        self.shell.doWelcome()
        self.prompt = "\n> "

        self.histindex = -1

        self.writePrompt()
        #
        #Your code here
        #
    #
    #Start of event handler methods
    #
    def upkey(self, Event=None):
        self.I.delete(0, END)
        if self.histindex < self.shell.historyLength() - 1:
            self.histindex += 1

        self.I.insert(INSERT, self.shell.getFromHistory(self.histindex))

    def downkey(self, Event=None):
        self.I.delete(0, END)
        if self.histindex > -1:
            self.histindex -= 1
        self.I.insert(INSERT, self.shell.getFromHistory(self.histindex))

    def enterkey(self, Event=None):
        line = self.I.get()
        self.I.delete(0, END)
        
        print line

        try:
            command = self.shell.execute(line)
            if command == 'exit':
                closeCallback()
        except Exception as ex:
            print ex
        finally:
            self.writePrompt()
            self.histindex = -1

    #
    #Other Methods
    #
    def writeCallback(self, string):
        self.T.config(state=NORMAL)
        self.T.mark_set(INSERT, END)
        self.T.insert(INSERT, string)
        self.T.config(state=DISABLED)
        self.T.see(END)

    def writePrompt(self):
        print self.prompt,

class OutputWrapper(object):
    def __init__(self, parent):
        self.parent = parent

    def write(self, string):
        self.parent.writeCallback(string)
    #
    #Start of non-Rapyd user code
    #


try:
    #--------------------------------------------------------------------------#
    # User code should go after this comment so it is inside the "try".        #
    #     This allows rpErrorHandler to gain control on an error so it         #
    #     can properly display a Rapyd-aware error message.                    #
    #--------------------------------------------------------------------------#

    #Adjust sys.path so we can find other modules of this project
    import sys
    if '.' not in sys.path:
        sys.path.append('.')
    #Put lines to import other modules of this project here
    
    if __name__ == '__main__':

        def closeCallback():
            sys.stdout = origstdobj
            Root.destroy()

        origstdobj = sys.stdout

        Root = Tk()
        import Tkinter
        #Tkinter.CallWrapper = rpErrorHandler.CallWrapper
        del Tkinter
        App = CalcGui(Root)
        App.pack(expand='yes',fill='both')

        #Root.geometry('640x480+10+10')
        Root.title('qCalc')
        Root.protocol("WM_DELETE_WINDOW", closeCallback)
        Root.mainloop()
    #--------------------------------------------------------------------------#
    # User code should go above this comment.                                  #
    #--------------------------------------------------------------------------#
except Exception as ex:
    print ex
    #rpErrorHandler.RunError()    
