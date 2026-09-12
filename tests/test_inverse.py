import unittest
from fi_lab.inverse import I, apply, inverse, mul, nullspace, power, solve, units


class ExactAlgebraTests(unittest.TestCase):
    def test_inverses(self):
        for p in (2, 3, 5):
            for a in units(p):
                self.assertEqual(mul(a, inverse(a, p), p), I)
                self.assertEqual(mul(inverse(a, p), a, p), I)

    def test_kernel(self):
        self.assertEqual(nullspace([[1, 2, 0], [0, 0, 1]], 3, 3), [[1, 1, 0]])

    def test_basis_satisfies_original_identity(self):
        for p in (2, 3):
            for n in (2, 3, 4):
                for same in (False, True):
                    result = solve(p, n, same)
                    for vector in result['basis']:
                        f = vector[:16]
                        g = f if same else vector[16:]
                        for a in units(p):
                            ai = inverse(a, p)
                            lhs = mul(apply(f, a, p), ai, p)
                            rhs = mul(power(a, n, p), apply(g, ai, p), p)
                            self.assertTrue(all((x+y) % p == 0 for x, y in zip(lhs, rhs)))

    def test_char_two_known_solution(self):
        self.assertGreater(solve(2, 2, True)['dimension'], 0)
        # An elementary solution is f=g=(trace X) I for n=2.
        for a in units(2):
            ai = inverse(a, 2)
            f = tuple((a[0]+a[3])*x % 2 for x in I)
            g = tuple((ai[0]+ai[3])*x % 2 for x in I)
            self.assertEqual(mul(f, ai, 2), mul(power(a, 2, 2), g, 2))

    def test_bad_parameters(self):
        for p in (0, 1, 4, 9):
            with self.assertRaises(ValueError):
                solve(p)
        with self.assertRaises(ValueError):
            solve(3, 1)


if __name__ == '__main__':
    unittest.main()
