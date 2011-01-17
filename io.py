"""Classes and functions to handle input and output streams"""

import re
import mathematics

class IOEngine(object):
    """Main class to handle input and output"""
    def __init__(self, inputDict, outputDict, parseOrder,
                 orderOfOperations, containers):
        """inputDict is a dictionary containing regular expression strings
and their associated classes to instantiate.

inputDict = {class0: regex0,
             class1: regex1,
             class2: regex2}

outputDict is a dictionary containing classes and their associated
string tokens representation, where the keyword 'val' is replaced by
the objects value or name.

Example of outputDict:
If an objects has a string representation of <<(some value)>> and it's
name is A, the string in the output dictionary should be written as
<<val>>, so that the object is printed as <<A>>.

outputDict = {class0: string0,
              class1: string1,
              class2: string2}

parseOrder is a list of classes in the order they should be removed from the
input string

orderOfOperations is a list of the correct mathematical order of operations
"""
        self.inputDict = inputDict
        self.outputDict = outputDict
        self.parseOrder = parseOrder
        self.order = orderOfOperations
        self.containers = containers

    def input(self, string):
        """IOEngine main input method. Contructs a tree from a string"""
        objectList = []
        # find containers and parse into trees
        for container in containers:
            self.findContainer(string, container)
        
        tree = self.buildTree(objectList)
        
    def parse(self, string):
        """Parse string and build an Expression tree"""
        tokenList = self.split(string)
        objectList = []
        for token in tokenList:
            objectList.append(self.toObject(token))
        tree = self.buildTree(objectList)
        return tree

    def output(self, tree):
        """IOEngine main output method. Outputs string based on Expression tree
"""
        objectList = self.collapseTree(tree)
        tokenList = []
        for Object in objectList:
            tokenList.append(self.toToken(Object))
        string = self.assemble(tokenList)
        return string

    def toObject(self, tokenToClassify):
        """Attempt to match string token to an object in the dictionary."""
        for Type, regex in self.inputDict.iteritems():
            # ^regex$ guarantees no surrounding characters in tokenToClassify
            match =  re.search('^'+regex+'$', tokenToClassify)
            if match is not None:
                return Type(match.groups()[0]) # first element in tuple
            else:
                pass
        raise ClassificationError(tokenToClassify) # no match in dictionary

    def toToken(self, classToTokenize):
        """Attempt to create string token from classes in dictionary. Also
replaces 'val' with actual class.val value."""
        try:
            token = self.outputDict[classToTokenize.__class__] # lookup class
            return token.replace('val', str(classToTokenize.val))
        except KeyError:
            raise ClassificationError(classToTokenize)

    def buildTree(self, objectList):
        """Construct a tree based on the object list"""
        for operation in self.order:
            while operation in objectList:
                loc = objectList.index(operation) - 1
                left = objectList.pop(loc)
                op = objectList.pop(loc)
                right = objectList.pop(loc)
                objectList.insert(loc, Expression(left, op, right))
        tree = objectList[0]
        return tree

    def collapseTree(self, tree):
        """Construct an object list on the expression tree"""
        objectList = [tree]
        typeList = [type(tree)]
        while Expression in typeList:
            loc = typeList.index(Expression)
            exp = objectList.pop(loc)
            if not exp.right == None:
                objectList.insert(loc, exp.right)
            if not exp.op == None:
                objectList.insert(loc, exp.op)
                
            objectList.insert(loc, exp.left)
            typeList = [type(item) for item in objectList] # update typeList
        return objectList

    def findContainer(self, string, container):
        """Search given string for specified container and return a list of
occurances and their associated nested depth."""
        stack = []
        containerMatches = []
        for loc, char in enumerate(string):
            if char == container.openingChar:
                stack.append(loc) # save location of character
            elif char == container.closingChar:
                if stack: # check if not empty, opening character was found
                    openingCharLoc = stack.pop()
                    closingCharLoc = loc
                    depth = len(stack)
                    span = (openingCharLoc, closingCharLoc+1)
                    containedString = string[openingCharLoc+1:closingCharLoc]
                    containerMatches.append(ContainerMatch(depth, span,
                                                           containedString))
                else: # no opening character to match closing character
                    raise ContainerError(string, loc)
        if len(stack) != 0:
            raise ContainerError(string, stack.pop())
        return containerMatches

    def split(self, string):
        """Split string into valid string tokens"""
        #######################################################################
        # Pipe Cleaner - fix problems arising from pipes in inner products
        # This is only a problem with qm.py, need to move this to a preprocess
        # function
        #######################################################################
        innerProdMatches = re.finditer(r'<[a-zA-Z][a-zA-Z0-9]*[|][a-zA-Z][a-zA-Z0-9]*>', string)
        for InnerProd in innerProdMatches:
            subStr = InnerProd.group(0)
            # double the pipe within the inner product
            string = string.replace(subStr, subStr.replace('|', '||'))
        #######################################################################
        
        tokenList = []
        for Class in self.parseOrder:
            regex = self.inputDict[Class]
            tokenMatches = re.finditer(regex, string) # find all matches in string
            for eachMatch in tokenMatches:
                loc = eachMatch.span() # location of match: (begin, end)
                token = string[loc[0]:loc[1]] # string token
                tokenList.append([loc, token])
                string = string.replace(token, ' '*len(token), 1) # replace token with spaces

        # check to make sure all characters have been removed from s
        leftover = string.strip()
        if len(leftover) > 0:
            loc = string.find(leftover[0])
            raise InputError(leftover[0], loc)

        tokenList.sort() # sort in place by location returned from span()
        tokens = [item[1] for item in tokenList] # add only string tokens, not loc
        return tokens

    def assemble(self, tokenList):
        """Assembles valid tokens into an output string."""
        outputString = ''.join(tokenList) # combine tokens into string
        #######################################################################
        # Removes double pipes - problem with inner products in qm.py
        # Need to move this to a post process function
        #######################################################################
        outputString = outputString.replace('||', '|')
        #######################################################################
        return outputString

# Helper classes
class Expression(object):
    """Class to be used as a node when creating trees of Expressions"""
    def __init__(self, left, operation=None, right=None):
        self.left = left
        self.op = operation
        self.right = right

class ContainerMatch(object):
    """Class that will represent matched results from findContainer method."""
    def __init__(self, depth, span, string):
        self.depth = depth
        self.span = span
        self.string = string


# Helper functions
def printTree(tree, level=0):
    """Function to print expression tree"""
    if not isinstance(tree, Expression):
        print ' ' * level + str(tree)
        return
    printTree(tree.right, level+1)
    print ' ' * level + str(tree.op)
    printTree(tree.left, level+1)

def depth(tree, level=0):
    """Calculate the depth of a tree"""
    if not isinstance(tree, Expression):
        return level
    else:
        return max(depth(tree.right, level+1), depth(tree.left, level+1))


# Define exceptions
class ClassificationError(Exception):
    def __init__(self, string):
        self.msg = "Cannot classify {0} from provided dictionary".format(string)
    def __str__(self):
        return repr(self.msg)

class InputError(Exception):
    def __init__(self, string, loc=0):
        self.msg = "Invalid input: {0}".format(string)
        self.loc = loc
    def __str__(self):
        return repr(self.msg)

class ContainerError(Exception):
    def __init__(self, string, loc=0):
        self.msg = "Missing matching container symbol: {0}".format(string)
        self.loc = loc
    def __str__(self):
        return self.msg

if __name__ == '__main__':
    from mathematics import *
    p = ContainerType('(', ')')
    test = '1+(2+(3+4))'
    print test
    io = IOEngine(inputDict, outputDict, parseOrder, orderOfOperations,
                  containers)
    con = io.findContainer(test, p)
