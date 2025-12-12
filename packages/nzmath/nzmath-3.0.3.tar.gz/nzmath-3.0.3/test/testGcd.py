import unittest
import doctest
import nzmath.gcd as gcd

class GcdTest (unittest.TestCase):
    def testDivmodl(self):
        self.assertEqual((2, -1), gcd.divmodl(5, 3))
        self.assertEqual((-2, -1), gcd.divmodl(5, -3))
        self.assertEqual((-2, 1), gcd.divmodl(-5, 3))
        self.assertEqual((2, 1), gcd.divmodl(-5, -3))
        self.assertRaises(ZeroDivisionError, gcd.divmodl, 5, 0)

    def testModl(self):
        self.assertEqual(-1, gcd.modl(5, 3))
        self.assertEqual(-1, gcd.modl(5, -3))
        self.assertEqual(1, gcd.modl(-5, 3))
        self.assertEqual(1, gcd.modl(-5, -3))
        self.assertRaises(ZeroDivisionError, gcd.modl, 5, 0)

    def testGcd(self):
        self.assertEqual(1, gcd.gcd(1, 2))
        self.assertEqual(2, gcd.gcd(2, 4))
        self.assertEqual(10, gcd.gcd(0, 10))
        self.assertEqual(10, gcd.gcd(10, 0))
        self.assertEqual(1, gcd.gcd(13, 21))

    def testGcd_(self):
        self.assertEqual(1, gcd.gcd_(1, 2))
        self.assertEqual(2, gcd.gcd_(2, 4))
        self.assertEqual(10, gcd.gcd_(0, 10))
        self.assertEqual(10, gcd.gcd_(10, 0))
        self.assertEqual(1, gcd.gcd_(13, 21))

    def testBinaryGcd(self):
        self.assertEqual(1, gcd.binarygcd(1, 2))
        self.assertEqual(2, gcd.binarygcd(2, 4))
        self.assertEqual(10, gcd.binarygcd(0, 10))
        self.assertEqual(10, gcd.binarygcd(10, 0))
        self.assertEqual(1, gcd.binarygcd(13, 21))

    def testLcm(self):
        self.assertEqual(2, gcd.lcm(1, 2))
        self.assertEqual(4, gcd.lcm(2, 4))
        self.assertEqual(0, gcd.lcm(0, 10))
        self.assertEqual(0, gcd.lcm(10, 0))
        self.assertEqual(273, gcd.lcm(13, 21))

    def testLcm_(self):
        self.assertEqual(2, gcd.lcm_(1, 2))
        self.assertEqual(4, gcd.lcm_(2, 4))
        self.assertRaises(ValueError, gcd.lcm_, 0, 10)
        self.assertRaises(ValueError, gcd.lcm_, 10, 0)
        self.assertEqual(273, gcd.lcm_(13, 21))

    def testExtgcd(self):
        u, v, d = gcd.extgcd(8, 11)
        self.assertEqual(1, abs(d))
        self.assertEqual(d, 8 * u + 11 * v)
        #sf.bug 1924839
        u, v, d = gcd.extgcd(-8, 11)
        self.assertEqual(1, abs(d))
        self.assertEqual(d, -8 * u + 11 * v)
        u, v, d = gcd.extgcd(8, -11)
        self.assertEqual(1, abs(d))
        self.assertEqual(d, 8 * u - 11 * v)
        u, v, d = gcd.extgcd(-8, -11)
        self.assertEqual(1, abs(d))
        self.assertEqual(d, -8 * u - 11 * v)
        import nzmath.rational as rational
        u, v, d = gcd.extgcd(rational.Integer(8), 11)
        self.assertEqual(1, abs(d))
        self.assertEqual(d, 8 * u + 11 * v)

    def testGcdOfList(self):
        self.assertEqual([8, [1]], gcd.gcd_of_list([8]))
        self.assertEqual([1, [-4, 3]], gcd.gcd_of_list([8, 11]))
        self.assertEqual([1, [-4, 3, 0, 0, 0, 0, 0]],
                            gcd.gcd_of_list([8, 11, 10, 9 ,6, 5, 4]))

    def testExtgcd_(self):
        a = [-30, -53, -13, -95, 10, 35, -15, -53, 57]; d_ = gcd.gcd_(*a)
        [d, x] = gcd.extgcd_(*a); ax = sum([a[j]*x[j] for j in range(len(a))])
        self.assertEqual(d_, d); self.assertEqual(d, ax); self.assertEqual(d, 1)
        self.assertEqual(x, [0, -2, 0, -1, -20, 0, 0, 0, 0])
        a = [-456, 450, 414, -390, -552, -174, 228]; d_ = gcd.gcd_(*a)
        [d, x] = gcd.extgcd_(*a); ax = sum([a[j]*x[j] for j in range(len(a))])
        self.assertEqual(d_, d); self.assertEqual(d, ax); self.assertEqual(d, 6)
        self.assertEqual(x, [1, 0, 0, 0, 2, -9, 0])
        a = [-35, 83, 14, -85, -1, -54, -10]; d_ = gcd.gcd_(*a)
        [d, x] = gcd.extgcd_(*a); ax = sum([a[j]*x[j] for j in range(len(a))])
        self.assertEqual(d_, d); self.assertEqual(d, ax); self.assertEqual(d, 1)
        self.assertEqual(x, [0, 0, 0, 0, -1, 0, 0])
        a = [-243, -279]; d_ = gcd.gcd_(*a)
        [d, x] = gcd.extgcd_(*a); ax = sum([a[j]*x[j] for j in range(len(a))])
        self.assertEqual(d_, d); self.assertEqual(d, ax); self.assertEqual(d, 9)
        self.assertEqual(x, [8, -7])
        a = [-340, -304, -328, -196, 292, -148, -52, -4]; d_ = gcd.gcd_(*a)
        [d, x] = gcd.extgcd_(*a); ax = sum([a[j]*x[j] for j in range(len(a))])
        self.assertEqual(d_, d); self.assertEqual(d, ax); self.assertEqual(d, 4)
        self.assertEqual(x, [0, 0, 0, 0, 0, 0, 0, -1])

    def testExtgcd_gen(self):
        a = [364, 144, -128, -252, 16]; [d, s, A] = gcd.extgcd_gen(*a)
        self.assertEqual(4, d); self.assertEqual(0, s)
        self.assertEqual([[-1, 0, 0, -1, -4],
                          [0, -1, 0, 0, 0],
                          [0, 0, -1, 0, 0],
                          [0, 0, 0, -1, 0],
                          [23, 9, -8, 7, 91]], A)
        a = [-89, 95, -25, -37, 25, -26, 47, 48]; [d, s, A] = gcd.extgcd_gen(*a)
        self.assertEqual(1, d); self.assertEqual(5, s)
        self.assertEqual([[-1, 0, 0, 0, 0, 0, 0, 0],
                          [0, -1, 0, 0, 0, 0, 0, 0],
                          [15, -9, -26, -11, -1, 1, -5, -4],
                          [0, 0, 0, -1, 0, 0, 0, 0],
                          [0, 0, 0, 0, -1, 0, 0, 0],
                          [-11, 5, 25, 12, 0, -1, 3, 2],
                          [0, 0, 0, 0, 0, 0, -1, 0],
                          [0, 0, 0, 0, 0, 0, 0, -1]], A)
        a = [-40, -194]; [d, s, A] = gcd.extgcd_gen(*a)
        self.assertEqual(2, d); self.assertEqual(0, s)
        self.assertEqual([[-34, 97], [7, -20]], A)
        a = [-400, -480]; [d, s, A] = gcd.extgcd_gen(*a)
        self.assertEqual(80, d); self.assertEqual(1, s)
        self.assertEqual([[-6, 1], [5, -1]], A)
        a = [-75, -38, -22, 61]; [d, s, A] = gcd.extgcd_gen(*a)
        self.assertEqual(1, d); self.assertEqual(0, s)
        self.assertEqual(A,
            [[1, -1, 2, 5], [0, 1, 0, 0], [-9, 10, -29, -42], [-2, 3, -8, -9]])

    def testCoprime(self):
        self.assertEqual(True, gcd.coprime(5, 3))
        self.assertEqual(True, gcd.coprime(8, 5))
        self.assertEqual(False, gcd.coprime(-15, -27))
        self.assertEqual(False, gcd.coprime(2301, -39))
        self.assertEqual(False, gcd.coprime(-35, 14))

    def testPairwiseCoprime(self):
        self.assertEqual(True, gcd.pairwise_coprime([1, 2, 3]))
        self.assertEqual(False, gcd.pairwise_coprime([1, 2, 3, 4]))
        self.assertEqual(False, gcd.pairwise_coprime([-15, 2, 7, 11, 13, -27]))
        self.assertEqual(False, gcd.pairwise_coprime([0, 3, 5, 7]))
        self.assertEqual(True, gcd.pairwise_coprime([1001, -81, 625, -32768]))

    def testPartFrac(self):
        m, x = [4, 9, 5, 17, 19], 1001; X, s = [3, 8, 2, 5, 13], -3
        self.assertEqual((X, s), gcd.part_frac(m, x))
        m, x = [19**2, 2**2, 23**3, 17**4], 33479066261025
        X, s = [346, 3, 5318, 55943], 20
        self.assertEqual((X, s), gcd.part_frac(m, x))
        m, x = [29**3, 11**2, 3**1, 17**5], 475
        X, s = [11197, 18, 1, 83496], -1
        self.assertEqual((X, s), gcd.part_frac(m, x))
        m, x = [11, 13, 17], 50; X, s = [6, 10, 12], -2
        self.assertEqual((X, s), gcd.part_frac(m, x))
        self.assertRaises(ValueError, gcd.part_frac, [11, 13], 33)

def suite():
    suite = unittest.makeSuite(GcdTest, "test")
    suite.addTest(doctest.DocTestSuite(gcd))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
