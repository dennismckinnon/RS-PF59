# Adapted from code Copyright (c) 2010 Andrew Brown <brownan@cs.duke.edu, brownan@gmail.com>ddition in PF(59) is normal addition modulo 59"
# Copyright (c) 2013 Ryan Castellucci <code@ryanc.org>
# See LICENSE.txt for license terms

class PF59int(int):
    """Instances of this object are elements of the field GF(2^8)
    Instances are integers in the range 0 to 255
    This field is defined using the irreducable polynomial
    x^8 + x^4 + x^3 + x + 1
    and using 3 as the generator for the exponent table and log table.
    """
    # Maps integers to PF59int instances
    cache = {}
    # multiplicitive inverse table, modulo 59
    invtable = (None, 1, 30, 20, 15, 12, 10, 17, 37, 46, 6, 43, 5, 50, 38, 4, 48,
            7, 23, 28, 3, 45, 51, 18, 32, 26, 25, 35, 19, 57, 2, 40, 24, 34,
	    33, 27, 41, 8, 14, 56, 31, 36, 52, 11, 55, 21, 9, 54, 16, 53, 13,
	    22, 42, 49, 47, 44, 39, 29, 58)

    def __new__(cls, value):
        # Check cache
        # Caching sacrifices a bit of speed for less memory usage. This way,
        # there are only a max of 59 instances of this class at any time.
	try:
            return PF59int.cache[value]
        except KeyError:
            if value > 58 or value < 0:
                raise ValueError("Field elements of PF(59) are between 0 and 58. Cannot be %s" % value)

            newval = int.__new__(cls, value)
            PF59int.cache[int(value)] = newval
            return newval

    def __add__(a, b):
        "Addition in PF(59) is normal addition modulo 59"
        return PF59int((int(a) + int(b)) % 59)
    __radd__ = __add__

    def __sub__(a, b):
	"Subtraction in PF(59) is normal subtraction modulo 59"
	# Python's modulo operator handles negitive numbers. If we didn't, we
	# could just add 59 to a before subtracting b
	return PF59int((int(a) - int(b)) % 59)

    def __rsub__(a, b):
        # We have to reverse the argument order for rsub
	return PF59int((int(b) - int(a)) % 59)

    def __neg__(self):
        return PF59int((59 - int(self)) % 59)
    
    def __mul__(a, b):
        "Multiplication in PF(59)"
        return PF59int((int(a) * int(b)) % 59)
    __rmul__ = __mul__

    def __pow__(self, power):
        if isinstance(power, PF59int):
            raise TypeError("Raising a Field element to another Field element is not defined. power must be a regular integer")
        if (power < 0):
            return PF59int(pow(int(self), -power, 59)).inverse()
        return PF59int(pow(int(self), power, 59))

    def inverse(self):
        return PF59int(PF59int.invtable[self])

    def __div__(self, other):
        return self * PF59int(other).inverse()
    def __rdiv__(self, other):
        return self.inverse() * other

    def __repr__(self):
        n = self.__class__.__name__
        return "%s(%r)" % (n, int(self))

    multiply = __mul__
#    def multiply(self, other):
#        """A slow multiply method. This method gives the same results as the
#        other multiply method, but is implemented to illustrate how it works
#        and how the above tables were generated.
#
#        This procedure is called Peasant's Algorithm (I believe)
#        """
#        a = int(self)
#        b = int(other)
#
#        p = a
#        r = 0
#        while b:
#            if b & 1: r = r ^ p
#            b = b >> 1
#            p = p << 1
#            if p & 0x100: p = p ^ 0x11b
#
#        return PF59int(r)
