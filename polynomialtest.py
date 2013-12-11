import unittest

from polynomial import Polynomial
from ffp import PF59int

class TestPFPoly(unittest.TestCase):
    """Tests that the Polynomial class works when given GF256int objects
    instead of regular integers
    """
    def test_add(self):
        one = Polynomial(map(PF59int,     (1,3,5,1)))
        two = Polynomial(map(PF59int, (5,3,58,1,6,8)))

        r = one + two

        self.assertEqual(r.coefficients,(PF59int(5),PF59int(3),PF59int(0),PF59int(4),PF59int(11),PF59int(9)))

    def test_sub(self):
        one = Polynomial(map(PF59int,     (8,3,5,1)))
        two = Polynomial(map(PF59int, (5,3,1,1,6,8)))
        r = one - two
        self.assertEqual(r.coefficients, (PF59int(54),PF59int(56),PF59int(7),PF59int(2),PF59int(58),PF59int(52)))

    def da_test_mul(self):
        one = Polynomial(map(PF59int,     (8,3,5,1)))
        two = Polynomial(map(PF59int, (5,3,1,1,6,8)))
        r = one * two
        self.assertEqual(r.coefficients, (40,23,28,1,53,78,7,46,8))

    def test_div(self):
        one = Polynomial(map(PF59int,     (1,58)))
        two = Polynomial(map(PF59int, (1,0,58)))
        q, r = divmod(two,one)
        self.assertEqual(q.coefficients, (PF59int(1),PF59int(1)))
        self.assertEqual(r.coefficients, (0,))

        # Make sure they multiply back out okay
        self.assertEqual(q*one + r, two)

    def da_test_div_scalar(self):
        """Tests division by a scalar"""
        numbers = map(GF256int, (5,20,50,100,134,158,0,148,233,254,4,5,2))
        scalar = PF59int(17)

        poly = Polynomial(numbers)
        scalarpoly = Polynomial(x0=scalar)

        self.assertEqual(
                (poly // scalarpoly).coefficients,
                tuple(map(lambda x: x / scalar, numbers))
                )

    def da_test_div_scalar2(self):
        """Test that dividing by a scalar is the same as multiplying by the
        scalar's inverse"""
        a = Polynomial(map(PF59int, (5,3,1,1,6,8)))

        scalar = GF256int(50)

        self.assertEqual(
                a * Polynomial(x0=scalar),
                a // Polynomial(x0=scalar.inverse())
                )



class TestPolynomial(unittest.TestCase):
    def da_test_add_1(self):
        one = Polynomial((2,4,7,3))
        two = Polynomial((5,2,4,2))

        r = one + two

        self.assertEqual(r.coefficients, (7, 6, 11, 5))

    def da_test_add_2(self):
        one = Polynomial((2,4,7,3,5,2))
        two = Polynomial((5,2,4,2))

        r = one + two

        self.assertEqual(r.coefficients, (2,4,12,5,9,4))

    def da_test_add_3(self):
        one = Polynomial((7,3,5,2))
        two = Polynomial((6,8,5,2,4,2))

        r = one + two

        self.assertEqual(r.coefficients, (6,8,12,5,9,4))

    def da_test_mul_1(self):
        one = Polynomial((2,4,7,3))
        two = Polynomial((5,2,4,2))

        r = one * two

        self.assertEqual(r.coefficients,
                (10,24,51,49,42,26,6))

    def da_test_div_1(self):
        one = Polynomial((1,4,0,3))
        two = Polynomial((1,0,1))

        q, r = divmod(one, two)
        self.assertEqual(q, one // two)
        self.assertEqual(r, one % two)

        self.assertEqual(q.coefficients, (1,4))
        self.assertEqual(r.coefficients, (-1,-1))

    def da_test_div_2(self):
        one = Polynomial((1,0,0,2,2,0,1,2,1))
        two = Polynomial((1,0,-1))

        q, r = divmod(one, two)
        self.assertEqual(q, one // two)
        self.assertEqual(r, one % two)

        self.assertEqual(q.coefficients, (1,0,1,2,3,2,4))
        self.assertEqual(r.coefficients, (4,5))

    def da_test_div_3(self):
        # 0 quotient
        one = Polynomial((1,0,-1))
        two = Polynomial((1,1,0,0,-1))

        q, r = divmod(one, two)
        self.assertEqual(q, one // two)
        self.assertEqual(r, one % two)

        self.assertEqual(q.coefficients, (0,))
        self.assertEqual(r.coefficients, (1,0,-1))

    def da_test_div_4(self):
        # no remander
        one = Polynomial((1,0,0,2,2,0,1,-2,-4))
        two = Polynomial((1,0,-1))

        q, r = divmod(one, two)
        self.assertEqual(q, one // two)
        self.assertEqual(r, one % two)

        self.assertEqual(q.coefficients, (1,0,1,2,3,2,4))
        self.assertEqual(r.coefficients, (0,))

    def da_test_getcoeff(self):
        p = Polynomial((9,3,3,2,2,3,1,-2,-4))
        self.assertEqual(p.get_coefficient(0), -4)
        self.assertEqual(p.get_coefficient(2), 1)
        self.assertEqual(p.get_coefficient(8), 9)
        self.assertEqual(p.get_coefficient(9), 0)

if __name__ == "__main__":
    unittest.main()
