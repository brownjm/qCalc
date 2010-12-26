"""Classes to evaluate an expression tree"""

from io import Expression
from mathematics import Operation

class CalcEngine(object):
    """Main class to perform evaluation"""
    def Evaluate(self, ExprTree):
        """Method to start evaluation"""
        return self.Eval(ExprTree)
    def Eval(self, Node):
        """Recursive method to evaluate the tree"""
        left = Node.left
        right = Node.right
        if not Node.left == None and isinstance(Node.left, Expression):
            left = self.Eval(Node.left)
        if not Node.right == None and isinstance(Node.right, Expression):
            right = self.Eval(Node.right)

        #Do some evals here
        res = None
        if not left == None and not right == None:
            exec "res = left " + Node.op.val + " right"
        else:
            res = left

        return res

if __name__ == '__main__':
    ce = CalcEngine()
    opl = Operation("+")
    opr = Operation("*")
    op = Operation("-")
    exprl = Expression(4, opl, 5)
    exprr = Expression(2, opr, 6)
    expr = Expression(exprl, op, exprr)
    print ce.Evaluate(expr)
