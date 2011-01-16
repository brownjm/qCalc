"""Unit test for mathematics.py"""

import unittest
import io
from mathematics import *

iostream = io.IOEngine(inputDict, outputDict, parseOrder,
                       orderOfOperations, containers)

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
                    ('3+4*(2.3-7e-12)', ['3', '+', '4', '*', '(2.3-7e-12)']),
                    ('2*(2+3)', ['2', '*', '(2+3)']),
                    ('(1+1)*(1+1)', ['(1+1)', '*', '(1+1)']),
                    ('2*(1+(1+1))', ['2', '*', '(1+(1+1))']),
                    )

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
    badStrings = ('1.2&', '$+3', '3^@', '1.3e-3<<a|', '<>', '1..')

    def testSplit(self):
        """Bad strings should raise InputError"""
        for string in self.badStrings:
            self.assertRaises(io.InputError, iostream.split, string)

class KnownTokens(unittest.TestCase):
    """Contains test string tokens, correctly identified classes and their
values"""
    knownTokens = (('1', Number, '1'),
                   ('3.453234', Number, '3.453234'),
                   ('.1', Number, '.1'),
                   ('3.1453e-10', Number, '3.1453e-10'),
                   ('14E200', Number, '14E200'),

                   ('+', Operation, '+'),
                   ('-', Operation, '-'),
                   ('*', Operation, '*'),
                   ('/', Operation, '/'),
                   ('^', Operation, '^'),

                   ('(2+3)', Quantity, '2+3'),
                   ('(-2.3)', Quantity, '-2.3'),
                   ('(4+(7-10))', Quantity, '4+(7-10)'))

    def testToObject(self):
        """ToObject should correctly instantiate string tokens into classes
with correct values."""
        for token, Type, value in self.knownTokens:
            result = iostream.toObject(token)
            self.assertEqual(Type, result.__class__)

    def testToToken(self):
        """ToToken should correctly produce a string token containing the
class' value"""
        for token, Type, value in self.knownTokens:
            result = iostream.toToken(Type(value))
            self.assertEqual(token, result)

class BadTokens(unittest.TestCase):
    """Contains invalid Tokens"""
    badTokens = ('&', '$', '@')

    def testBadTokens(self):
        """Bad tokens should raise ClassificationError"""
        for token in self.badTokens:
            self.assertRaises(io.ClassificationError, iostream.toObject, 
                              token)


if __name__ == '__main__':
    unittest.main()
