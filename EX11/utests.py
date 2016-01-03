#!/usr/bin/env python3

import unittest
import ex11
import math

class TestEx11(unittest.TestCase):

    def test_const(self):
        f = ex11.const_function(17)
        self.assertEqual(f(4),17)
        self.assertEqual(f(10),17)

    def identity(self):
        f = ex11.identity()
        self.assertEqual(f(7),7)
        self.assertEqual(f(-5),-5)

    def test_sin(self):
        f = ex11.sin_function()
        self.assertAlmostEqual(f(0),0)
        self.assertAlmostEqual(f(math.pi/2),1)
        self.assertAlmostEqual(f(math.pi),0)
        self.assertAlmostEqual(f(3*math.pi/2),-1)
        self.assertAlmostEqual(f(math.pi/4),(1/2)**(1/2))

    def test_sum(self):
        f = ex11.sum_functions(abs,math.sqrt)
        self.assertEqual(f(9),12)
        self.assertEqual(f(1/4),3/4)

    def test_sub(self):
        f = ex11.sub_functions(abs,math.sqrt)
        self.assertEqual(f(9),6)
        self.assertEqual(f(1/4),-1/4)

    def test_mul(self):
        f = ex11.mul_functions(abs,math.sqrt)
        self.assertEqual(f(9),27)
        self.assertEqual(f(1/4),1/8)

    def test_div(self):
        f = ex11.div_functions(abs,math.sqrt)
        self.assertEqual(f(9),3)
        self.assertEqual(f(1/4),1/2)
        self.assertRaises(ZeroDivisionError,f,0)

    def test_compose(self):
        f = ex11.compose(math.sqrt,math.exp)
        self.assertAlmostEqual(f(9),math.exp(4.5))
        self.assertAlmostEqual(f(-1/4),math.exp(-1/8))

    def test_inverse1(self):
        f = ex11.inverse(lambda x:2*x)
        self.assertAlmostEqual(f(9),4.5,delta=5*1e-5)
        self.assertAlmostEqual(f(-2),-1,delta=5*1e-5)

    def test_inverse2(self):
        f = ex11.inverse(lambda x:2*x,1e-6)
        self.assertAlmostEqual(f(9),4.5,delta=5*1e-6)
        self.assertAlmostEqual(f(-2),-1,delta=5*1e-6)

    def test_derivative1(self):
        f = ex11.derivative(lambda x:x*x)
        self.assertAlmostEqual(f(0),1e-3)
        self.assertAlmostEqual(f(9),18.001)

    def test_derivative2(self):
        f = ex11.derivative(lambda x:x*x,1)
        self.assertAlmostEqual(f(0),1)
        self.assertAlmostEqual(f(9),19)

    def test_integral1(self):
        f = ex11.integral_function(lambda x:x*x)
        self.assertAlmostEqual(f(0),0)
        self.assertAlmostEqual(f(6),72,delta=0.1)
        self.assertAlmostEqual(f(-6),-72,delta=0.1)
        
    def test_integral2(self):
        f = ex11.integral_function(lambda x:x*x,1)
        self.assertAlmostEqual(f(0),0)
        self.assertAlmostEqual(f(1),1/4)
        self.assertAlmostEqual(f(-1),-1/4)
        
    def test_errors(self):
        def fake(x): raise Exception
        self.assertRaises(Exception,ex11.sum_functions(fake,abs),5)
        self.assertRaises(Exception,ex11.sub_functions(fake,abs),5)
        self.assertRaises(Exception,ex11.mul_functions(fake,abs),5)
        self.assertRaises(Exception,ex11.div_functions(fake,abs),5)
        self.assertRaises(Exception,ex11.compose(fake,abs),5)
        self.assertRaises(Exception,ex11.compose(abs,fake),5)
        self.assertRaises(Exception,ex11.inverse(fake),5)
        self.assertRaises(Exception,ex11.derivative(fake),5)
        self.assertRaises(Exception,ex11.integral_function(fake),5)

if __name__=="__main__":
    unittest.main()
