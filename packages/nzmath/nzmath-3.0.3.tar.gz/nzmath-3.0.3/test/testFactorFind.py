import unittest
import logging
import nzmath.factor.find as find

try:
    _log = logging.getLogger('test.testFactorFind')
except:
    try:
        _log = logging.getLogger('nzmath.test.testFactorFind')
    except:
        _log = logging.getLogger('testFactorFind')
_log.setLevel(logging.INFO)

class FactorFindTest (unittest.TestCase):
    def testRho(self):
        self.assertIn(find.rhomethod(60), [2, 3, 4, 5, 6, 10, 12, 15, 20, 30])
        self.assertIn(find.rhomethod(128), [2, 4, 8, 16, 32, 64])
        self.assertIn(find.rhomethod(200819), [409, 491])
        self.assertIn(find.rhomethod(1042387), [701, 1487])
        self.assertIn(find.rhomethod(17**2*19), [17, 19, 289, 323])

    def testPMinusOneMethod(self):
        self.assertIn(find.pmom(1919), [19, 101])
        # 6133 = prime.prime(800) > sqrt(B) & 800 == 0 mod 20
        p = 4 * 6133 + 1
        self.assertIn(find.pmom(p*154858631), [p, 154858631])

    def testTrialDivision(self):
        self.assertEqual(2, find.trialDivision(60))
        self.assertEqual(2, find.trialDivision(128))
        self.assertEqual(409, find.trialDivision(200819))
        self.assertEqual(701, find.trialDivision(1042387))
        self.assertEqual(17, find.trialDivision(17**2*19))

    def testVerbosity(self):
        # default method
        p = 4 * 6133 + 1
        _log.info("silent:")
        result = find.pmom(p*154858631, verbose=False)
        _log.info("verbose:")
        result = find.pmom(p*154858631, verbose=True)

def suite(suffix = "Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in list(all_names):
        if name.endswith(suffix):
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    return suite

if __name__ == '__main__':
    logging.basicConfig()
    runner = unittest.TextTestRunner()
    runner.run(suite())
