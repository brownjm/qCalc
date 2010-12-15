"""Classes and functions to handle input and output streams"""

class IOEngine(object):
    """Main class to handle input and output"""
    def __init__(self, inputDict, outputDict):
        self.io = iostream(inputDict, outputDict)
        self.classify = Classifier(inputDict, outputDict)

    def parse(self, string):
        """Parse string and build a tree of expressions"""
        tokenList = self.io.split(string)
        tree = buildTree(tokenList)
        return tree

    def print(self, tree):
        """Construct a string based on the expression tree"""
        pass

    def buildTree(self, tokenList):
        """Construct a tree based on the string token list"""
        pass
