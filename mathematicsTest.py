"""Unit test for mathematics.py"""

import unittest
import io
import mathematics as m

iostream = io.IOstream(m.inputDict, m.outputDict)

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

    def testBadStrings(self):
        """Bad strings should raise InputError"""
        for string in self.badStrings:
            self.assertRaises(io.InputError, iostream.split, string)

if __name__ == '__main__':
    unittest.main()
