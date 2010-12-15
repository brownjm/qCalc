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


class Classifier(object):
    """Class that handles matching string tokens and their appropriate
objects."""
    def __init__(self, inputDict, outputDict):
        """inputDict is a dictionary containing regular expression strings
and their associated classes to instantiate.

inputDict = {regex0: class0,
             regex1: class1,
             regex2: class3}

outputDict is a dictionary containing classes and their associated string tokens

outputDict = {class0: string0,
              class1: string1,
              class2: string2}
"""
        self.inputDict = inputDict
        self.outputDict = outputDict

    def toClass(self, stringToClassify):
        """Attempt to match string token to an object in the dictionary."""
        for regex, Type in self.inputDict.iteritems():
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


# Define exceptions
class ClassificationError(Exception):
    def __init__(self, string):
        self.msg = "Cannot classify {0} from provided dictionary".format(string)
    def __str__(self):
        return repr(self.msg)
