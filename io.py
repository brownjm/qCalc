"""Classes and functions to handle input and output streams"""

import re

class IOEngine(object):
    """Main class to handle input and output"""
    def __init__(self, inputDict, outputDict, parseOrder,
                 orderOfOperations):
        self.io = IOstream(inputDict, parseOrder)
        self.classify = Classifier(inputDict, outputDict)
        self.order = orderOfOperations

    def parse(self, string):
        """Parse string and build an Expression tree"""
        tokenList = self.io.split(string)
        objectList = []
        for token in tokenList:
            objectList.append(self.classify.toObject(token))
        tree = self.buildTree(objectList)
        return tree

    def output(self, tree):
        """Outputs string based on Expression tree"""
        objectList = self.builder.collapseTree(tree)
        tokenList = []
        for Object in objectList:
            tokenList.append(self.classify.toToken(Object))
        string = self.io.assemble(tokenList)
        return string

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
            objectList.insert(loc, exp.right)
            objectList.insert(loc, exp.op)
            objectList.insert(loc, exp.left)
            typeList = [type(item) for item in objectList] # update typeList
        return objectList


class Classifier(object):
    """Class that handles matching string tokens and their appropriate
objects."""
    def __init__(self, inputDict, outputDict):
        """inputDict is a dictionary containing regular expression strings
and their associated classes to instantiate.

inputDict = {class0: regex0,
             class1: regex1,
             class2: regex2}

outputDict = {class0: string0,
              class1: string1,
              class2: string2}

outputDict is a dictionary containing classes and their associated
string tokens representation, where the keyword 'val' is replaced by
the objects value or name.

Example:
If an objects has a string representation of <<(some value)>> and it's
name is A, the string in the output dictionary should be written as
<<val>>, so that the object is printed as <<A>>.
"""
        # inputDict for classifier must have regex keys that begin with ^ and
        # end with $ to guarantee that that a valid token surrounded by extra
        # characters raises a classification error
        self.inputDict = {}
        for Class, regex in inputDict.iteritems():
            newRegex = '^' + regex + '$'
            self.inputDict[Class] = newRegex
        self.outputDict = outputDict

    def toObject(self, stringToClassify):
        """Attempt to match string token to an object in the dictionary."""
        for Type, regex in self.inputDict.iteritems():
            match =  re.search(regex, stringToClassify)
            if match is not None:
                return Type(match.groups()[0]) # first element in tuple
            else:
                pass
        raise ClassificationError(stringToClassify) # no match in dictionary

    def toToken(self, classToTokenize):
        """Attempt to create string token from classes in dictionary. Also
replaces 'val' with actual class.val value."""
        try:
            token = self.outputDict[classToTokenize.__class__] # lookup class
            return token.replace('val', classToTokenize.val)
        except KeyError:
            raise ClassificationError(classToTokenize)


class IOstream(object):
    """Class to split a string into smaller string tokens"""
    def __init__(self, inputDict, parseOrder):
        """inputDict is a dictionary containing regular expression strings
and their associated classes to instantiate.

        inputDict = {regex0: class0,
                     regex1: class1,
                     regex2: class3}

        parseOrder is a list of classes in the order they should be removed
        from the input string
        """
        self.inputDict = inputDict
        self.order = parseOrder

    def split(self, string):
        """Split string into valid string tokens"""
        # Pipe Cleaner - fix problems arising from pipes in inner products
        # This is only a problem with qm.py, need to move this to a preprocess
        # method
        innerProdMatches = re.finditer(r'<[a-zA-Z][a-zA-Z0-9]*[|][a-zA-Z][a-zA-Z0-9]*>', string)
        for InnerProd in innerProdMatches:
            subStr = InnerProd.group(0)
            # double the pipe within the inner product
            string = string.replace(subStr, subStr.replace('|', '||'))
            
        tokenList = []
        for Class in self.order:
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
        outputString = outputString.replace('||', '|') # remove double pipes
        return outputString


class Expression(object):
    """Class to be used as a node when creating trees of Expressions"""
    def __init__(self, left, operation=None, right=None):
        self.left = left
        self.op = operation
        self.right = right


def printTree(tree, level=0):
    """Function to print expression tree"""
    if not isinstance(tree, Expression):
        print ' ' * level + str(tree)
        return
    printTree(tree.right, level+1)
    print ' ' * level + str(tree.op)
    printTree(tree.left, level+1)

def depth(tree, level=0):
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

if __name__ == '__main__':
    from mathematics import *

    test = r'1+2*(3+4)/1'
    print test
    io = IOEngine(inputDict, outputDict, parseOrder, orderOfOperations)
    tree = io.parse(test)
    printTree(tree)
