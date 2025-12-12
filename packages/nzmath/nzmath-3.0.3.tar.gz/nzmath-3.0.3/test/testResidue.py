import unittest
import nzmath.residue as residue

class ResidueTest (unittest.TestCase):
    def testPrimitiveRootDef(self):
        self.assertEqual([2], residue.primitiveRootDef(3))
        self.assertEqual([3,11,12,13,17,21,22,24],residue.primitiveRootDef(31))
        self.assertEqual(\
            [6, 7, 11, 12, 13, 15, 17, 19, 22, 24, 26, 28, 29, 30, 34, 35]\
            , residue.primitiveRootDef(41))
        self.assertEqual(\
            [2, 5, 6, 8, 13, 14, 15, 18, 19, 20, 22, 24, 32, 34, 35, 39, 42\
            , 43, 45, 46, 47, 50, 52, 53, 54, 55, 56, 57, 58, 60, 62, 66, 67\
            , 71, 72, 73, 74, 76, 79, 80]\
            , residue.primitiveRootDef(83))
        self.assertEqual([5, 7, 10, 13, 14, 15, 17, 21, 23, 26, 29, 37,\
            38, 39, 40, 41, 56, 57, 58, 59, 60, 68, 71, 74, 76, 80, 82, 83,\
            84, 87, 90, 92], residue.primitiveRootDef(97))
    def testPrimitive_Root(self):
        self.assertTrue(residue.primitive_root(461) \
                            in residue.primitiveRootDef(461))
        self.assertTrue(residue.primitive_root(967) \
                            in residue.primitiveRootDef(967))
        self.assertTrue(residue.primitive_root(149) \
                            in residue.primitiveRootDef(149))
        self.assertTrue(residue.primitive_root(911) \
                            in residue.primitiveRootDef(911))
    def testPrimitiveRootTakagi(self):
        self.assertTrue(residue.primitiveRootTakagi(461) \
                            in residue.primitiveRootDef(461))
        self.assertTrue(residue.primitiveRootTakagi(967) \
                            in residue.primitiveRootDef(967))
        self.assertTrue(residue.primitiveRootTakagi(149, 147)\
                            in residue.primitiveRootDef(149))
        self.assertEqual(2, residue.primitiveRootTakagi(509))
    def testPrimitiveRoots(self):
        self.assertEqual([(3,2),(5,2),(7,3),(11,2),(13,2),(17,3),(19,2),(23,5),\
        (29,2),(31,3),(37,2),(41,6),(43,3),(47,5),(53,2),(59,2),(61,2),(67,2),\
        (71,7),(73,5),(79,3),(83,2),(89,3),(97,5)],residue.primitiveRoots(100))
        self.assertEqual(residue.primitiveRoots(),residue.primitiveRoots2())
    def testPrimitiveRootPW(self):
        p,r=(97,5);self.assertEqual(\
            residue.primitiveRootPW(p,r,residue.primitiveRootPW_(p,r)),\
            residue.primitiveRoot0PW(p,r))
        p=2003;r=residue.primitiveRootDef(p)[0];self.assertEqual(\
            residue.primitiveRootPW(p,r,residue.primitiveRootPW_(p,r)),\
            residue.primitiveRoot0PW(p,r))

def suite(suffix="Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.endswith(suffix):
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
