import unittest
import random

from pypearl import *

class NDArrayTests(unittest.TestCase):
    # A (len1, len2) B (len2, len3) C (len1, len3)
    def big_dot_test(self, afloat: ndarray, bfloat: ndarray, len1, len2, len3, msg = ""):
        cfloat = afloat.dot(bfloat)

        for i in range(len1):
            for j in range(len3):
                self.assertAlmostEqual(cfloat[i, j], 0.0)

        for i in range(len1):
            for j in range(len2):
                afloat[i, j] = random.random()
        
        for i in range(len2):
            for j in range(len3):
                bfloat[i, j] = random.random()

        cfloat = afloat.dot(bfloat)

        for i in range(len1):
            for j in range(len3):
                count = 0
                for k in range(len2):
                    count += afloat[i,k]*bfloat[k, j]
                self.assertAlmostEqual(cfloat[i, j], count, delta = 1e-4, msg=(msg + f" at {i},{j}"))


    def test_array_getset(self):   
        xfloat = ndarray((3, 4), zeros=True, dtype= "float32")
        self.assertAlmostEqual(xfloat[0,0], 0.0)
        for i in range(3):
            for j in range(4):
                rval = random.random()*10
                xfloat[i, j] = rval
                self.assertAlmostEqual(xfloat[i,j], rval, delta = 1e-6)

        xdouble = ndarray((7, 3), zeros=True, dtype= "float64")
        self.assertAlmostEqual(xdouble[0,0], 0.0)
        for i in range(7):
            for j in range(3):
                rval = random.random()
                xdouble[i, j] = rval
                self.assertAlmostEqual(xdouble[i,j], rval)


        xint = ndarray((2, 5), zeros=True, dtype= "int32")
        self.assertAlmostEqual(xint[0,0], 0.0)
        for i in range(2):
            for j in range(5):
                rval = random.randint(-50, 150)
                xint[i, j] = rval
                self.assertAlmostEqual(xint[i,j], rval)

        xlong = ndarray((6, 5), zeros=True, dtype= "int64")
        self.assertAlmostEqual(xlong[0,0], 0.0)
        for i in range(6):
            for j in range(5):
                rval = random.randint(-50, 150)
                xlong[i, j] = rval
                self.assertAlmostEqual(xlong[i,j], rval)

    def test_dot_identity(self):
        afloat = ndarray((2,2), zeros=True, dtype = "float32")
        bfloat = ndarray((2,2), zeros=True, dtype = "float32")
        for i in range(2):
            for j in range(2):
                bfloat[i,j] = random.random()
        
        afloat[0,0] = 1.0
        afloat[1,1] = 1.0

        cfloat = afloat.dot(bfloat)

        for i in range(2):
            for j in range(2):
                self.assertEqual(cfloat[i, j], bfloat[i, j], msg="Dot product by identity fail 32 bit")

        afloat = ndarray((2,2), zeros=True, dtype = "float64")
        bfloat = ndarray((2,2), zeros=True, dtype = "float64")
        for i in range(2):
            for j in range(2):
                bfloat[i,j] = random.random()
        
        afloat[0,0] = 1.0
        afloat[1,1] = 1.0

        cfloat = afloat.dot(bfloat)

        for i in range(2):
            for j in range(2):
                self.assertEqual(cfloat[i, j], bfloat[i, j], msg="Dot product by identity fail")


    def test_dot_complex(self):
        afloat = ndarray((2,3), zeros=True, dtype = "float32")
        bfloat = ndarray((3,4), zeros=True, dtype = "float32")

        cfloat = afloat.dot(bfloat)

        for i in range(2):
            for j in range(4):
                self.assertAlmostEqual(cfloat[i, j], 0.0)

        for i in range(2):
            for j in range(3):
                afloat[i, j] = random.random()
        
        for i in range(3):
            for j in range(4):
                bfloat[i, j] = random.random()

        cfloat = afloat.dot(bfloat)

        for i in range(2):
            for j in range(4):
                count = 0
                for k in range(3):
                    count += afloat[i,k]*bfloat[k, j]
                self.assertAlmostEqual(cfloat[i, j], count, delta = 1e-4, msg="error in complex dot products 32 bits")

        afloat = ndarray((2,3), zeros=True, dtype = "float64")
        bfloat = ndarray((3,4), zeros=True, dtype = "float64")

        cfloat = afloat.dot(bfloat)

        for i in range(2):
            for j in range(4):
                self.assertAlmostEqual(cfloat[i, j], 0.0)

        for i in range(2):
            for j in range(3):
                afloat[i, j] = random.random()
        
        for i in range(3):
            for j in range(4):
                bfloat[i, j] = random.random()

        cfloat = afloat.dot(bfloat)

        for i in range(2):
            for j in range(4):
                count = 0
                for k in range(3):
                    count += afloat[i,k]*bfloat[k, j]
                self.assertAlmostEqual(cfloat[i, j], count, msg = "Error in complex dot products 64 bits")

    def test_large_array(self):
        x = ndarray((2000,), zeros=True, dtype = "float32")
        x[1587] = 0.3
        self.assertAlmostEqual(x[1587], 0.3, msg = "Able to access large places")
        l1 = 200
        l2 = 300
        l3 = 400
        afloat = ndarray((l1, l2), zeros = True, dtype = "float64")
        bfloat = ndarray((l2, l3), zeros=True, dtype = "float64")

        self.big_dot_test(afloat, bfloat, l1, l2, l3, "dot test on very large values")

if __name__ == '__main__':
    unittest.main()    