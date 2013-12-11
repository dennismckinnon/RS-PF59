import unittest
import itertools

import rs
from polynomial import Polynomial
from rs import b58conv
from rs import r58conv

class TestRSverify(unittest.TestCase):
    def setUp(self):
        self.coder = rs.RSCoder(58,46)

    def test_one(self):
        """Tests a codeword without errors validates"""
        code = self.coder.encode("1Ah56Cfe4SXA")

        self.assertTrue(self.coder.verify(code))

    def test_two(self):
        """Verifies that changing any single character will invalidate the
        codeword"""
        code = self.coder.encode("123456789abcdefghijkmnpqrstuvwxyzA")

        for i, c in enumerate(code):
            # Change the value at position i and verify that the code is not
            # valid
            # Change it to a 0, unless it's already a 0
            if b58conv(c) == 0:
                c = r58conv(1)
            else:
                c = r58conv(0)
            bad_code = code[:i] + c + code[i+1:]

            self.assertFalse(self.coder.verify(bad_code))

class TestRSdecoding(unittest.TestCase):
    def setUp(self):
        self.coder = rs.RSCoder(58,46)
        self.string = "818878"

        codestr = self.coder.encode(self.string)

        self.code = codestr

    def test_strip(self):
        """Tests that the nostrip feature works"""
        otherstr = self.string.rjust(46, "0")

        codestr = self.coder.encode(otherstr)

        self.assertEqual(58, len(codestr))
        
        # Decode with default behavior: stripping of leading null bytes
        decode = self.coder.decode(codestr)
        decode2 = (self.coder.decode(codestr[:5] + "1" + codestr[6:]))

        self.assertEqual(self.string, decode)
        self.assertEqual(self.string, decode2)

        # Decode with nostrip
        decode = self.coder.decode(codestr, nostrip=True)
        decode2 = self.coder.decode(codestr[:5] + "1" + codestr[6:], nostrip=True)

        self.assertEqual(otherstr, decode)
        self.assertEqual(otherstr, decode2)

    def test_noerr(self):
        """Make sure a codeword with no errors decodes"""
        decode = self.coder.decode(self.code)
        self.assertEqual(self.string, decode)

    def test_oneerr(self):
        """Change just one byte and make sure it decodes"""
        for i, c in enumerate(self.code):
            newch = r58conv( (b58conv(c)+1) % 59)
            r = self.code[:i] + newch + self.code[i+1:]

            decode = self.coder.decode(r)

            self.assertEqual(self.string, decode)


    def test_6err(self):
        """Tests if 16 byte errors still decodes"""
        errors = [5, 6, 12, 13, 38, 40]
        r = list(b58conv(x) for x in self.code)

        for e in errors:
            r[e] = (r[e] + 1)

        r = "".join(r58conv(x) for x in r)
        decode = self.coder.decode(r)
        self.assertEqual(self.string, decode)

    def test_17err(self):
        """Kinda pointless, checks that 17 errors doesn't decode.
        Actually, this could still decode by coincidence on some inputs,
        so this test shouldn't be here at all."""
        errors = [5, 6, 12, 13, 22, 38, 40, 42]
        r = list(b58conv(x) for x in self.code)

        for e in errors:
            r[e] = (r[e] + 50) % 256

        r = "".join(r58conv(x) for x in r)
        decode = self.coder.decode(r)
        self.assertNotEqual(self.string, decode)


if __name__ == "__main__":
    unittest.main()
