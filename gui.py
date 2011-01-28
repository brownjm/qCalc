from executable import Executable
from Tkinter import *

class Launcher(object):
    def run(self):
        self.Root = Tk()
        self.App = CalcGui(self.Root)
        self.App.pack(expand='yes', fill='both')

        self.Root.title('qCalc')
        self.Root.protocol("WM_DELETE_WINDOW", closeCallback)
        self.Root.mainloop()

class CalcGui(Frame, Executable):
    def __init__(self,Master=None,**kw):
        #
        #Setting up the graphical components
        #        
        Frame.__init__(self)
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

        Executable.__init__(self)
         
        self.prompt = "\n> "

        self.histindex = -1

        self.writePrompt()
    #
    #Start of event handler methods
    #
    def upkey(self, Event=None):
        self.I.delete(0, END)
        if self.histindex < len(self.env.history) - 1:
            self.histindex += 1

        self.I.insert(INSERT, self.env.history(self.histindex))

    def downkey(self, Event=None):
        self.I.delete(0, END)
        if self.histindex > -1:
            self.histindex -= 1
        self.I.insert(INSERT, self.env.history(self.histindex))

    def enterkey(self, Event=None):
        line = self.I.get()
        self.I.delete(0, END)
        
        print line

        try:
            command = self.execute(line)
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


if __name__ == '__main__':
    def closeCallback():
        sys.stdout = origstdobj
        launcher.Root.destroy()

    origstdobj = sys.stdout
        
    launcher = Launcher()
    launcher.run()
