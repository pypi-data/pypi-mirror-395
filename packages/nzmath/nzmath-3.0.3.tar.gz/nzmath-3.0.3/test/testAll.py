import unittest
import logging

from nzmath import *

import testAlgfield
import testAlgorithm
import testArith1
import testArygcd
import testBigrandom
import testBigrange
import testCombinatorial
import testCompatibility
import testCubic_root
import testCyclotomic # 22/11/2024 added
import testEcpp
import testElliptic
import testEquation
import testFiniteField
import testGcd
import testGroup
import testImaginary
import testIntresidue
import testLattice
import testMatrix
import testMatrixFiniteField # 24/11/2021 added
import testModule
import testMultiplicative
import testPermute
import testPlugins
import testPrime
import testPrime_decomp
import testQuad
import testRational
import testReal
import testResidue # 2025/02/19 added
import testRing
import testRound2
import testSequence
import testSquarefree
import testVector
# nzmath.factor
import testFactorEcm
import testFactorMethods
import testFactorMisc
import testFactorMpqs
import testFactorUtil
# nzmath.poly
import testPolyArray # 24/11/2021 added
import testPolyFactor
import testFormalsum
import testGroebner
import testPolyHensel
import testMultiutil
import testMultivar
import testRatfunc
import testPolyRing
import testTermOrder
import testUniutil
import testUnivar


def suite():
    suite = unittest.TestSuite()
    all_names = globals()
    for name in list(all_names):
        if name.startswith("test"):
            suite.addTest(all_names[name].suite())
    return suite

if __name__ == '__main__':
    logging.basicConfig()
    runner = unittest.TextTestRunner()
    runner.run(suite())
