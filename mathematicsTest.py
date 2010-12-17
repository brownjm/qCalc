"""Unit test for mathematics.py"""

import unittest
import io
from mathematics import *

iostream = io.IOstream(inputDict, outputDict)
classifier = io.Classifier(inputDict, outputDict)

class KnownStrings(unittest.TestCase):
    """Contains test strings and a list of correctly separated string tokens."""
    knownStrings = (('2+3', ['2', '+', '3']),
                    ('1-7', ['1', '-', '7']),
                    ('2*4', ['2', '*', '4']),
                    ('11/10', ['11', '/', '10']),
                    ('6^4', ['6', '^', '4']),
                    ('2*2', ['2', '*', '2']),
                    ('2.34*-19.3842', ['2.34', '*', '-', '19.3842']),
                    ('2.3e-10', ['2.3e-10']),
                    ('-2', ['-', '2']),
                    ('(2+3)', ['(2+3)']),
                    ('3+4*(2.3-7e-12)', ['3', '+', '4', '*', '(2.3-7e-12)']))

    def testSplit(self):
        """Split should separate known strings into known tokens"""
        for string, tokens in self.knownStrings:
            result = iostream.split(string)
            self.assertEqual(result, tokens)

    def testAssemble(self):
        """Assemble should combine known tokens into known strings"""
        for string, tokens in self.knownStrings:
            result = iostream.assemble(tokens)
            self.assertEqual(result, string)

class BadStrings(unittest.TestCase):
    """Contains invalid string input"""
    badStrings = ('&', '$', '@', '<<a|', '<>', '1..')

    def testSplit(self):
        """Bad strings should raise InputError"""
        for string in self.badStrings:
            self.assertRaises(io.InputError, iostream.split, string)

class KnownTokens(unittest.TestCase):
    """Contains test string tokens, correctly identified classes and their
values"""
    knownTokens = (('1', Number, '1'),
                   ('-3', Number, '-3'),
                   ('-3.453234', Number, '-3.453234'),
                   ('.1', Number, '.1'),
                   ('-.7', Number, '-.7'),
                   ('3.1453e-10', Number, '3.1453e-10'),
                   ('-14E200', Number, '-14E200'),

                   ('+', Operation, '+'),
                   ('-', Operation, '-'),
                   ('*', Operation, '*'),
                   ('/', Operation, '/'),
                   ('^', Operation, '^'))

    def testToObject(self):
        """ToObject should correctly instantiate string tokens into classes
with correct values."""
        for token, Type, value in self.knownTokens:
            result = classifier.toObject(token)
            print token
            self.assertEqual(Type, result.__class__)

    def testToToken(self):
        """ToToken should correctly produce a string token containing the
class' value"""
        for token, Type, value in self.knownTokens:
            result = classifier.toToken(Type(value))
            self.assertEqual(token, result)

class BadTokens(unittest.TestCase):
    """Contains invalid Tokens"""
    badTokens = ('-1-', '-.a', '3a', '20x320x93E-10', '&', '$', '@', '<<a|',
                 '|a|', '<>', '1..')

    def testBadTokens(self):
        """bad tokens should raise ClassificationError"""
        for token in self.badTokens:
            self.assertRaises(io.ClassificationError, classifier.toObject,
                              token)


if __name__ == '__main__':
    unittest.main()
