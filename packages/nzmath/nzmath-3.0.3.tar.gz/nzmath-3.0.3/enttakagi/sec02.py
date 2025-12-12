"""
Greatest Common Divisors, Least Common Multiples
"""

from random import randint, choice
from nzmath.arith1 import product as prod
from nzmath.gcd import lcm, gcd, gcd_, modl, lcm_
from utils import HitRet, lcm_def, again, gcd_def

size = 40 # maximum data size, positive integer
length = 4 # maximum data length, positive integer

print()
print("=============================================")
print("Though 0 does not have its multiple, we allow")
print("exceptional return from NZMATH functions that")
print("seems to mean 0 is a divisor of some integer.")
print("On the other hand, NZMATH function whose name")
print("is ending with only one '_' follows the rule.")
print("For example, the result gcd(0, 0) == 0 can be")
print("accepted, but gcd_(0, 0) will raise an error.")
print("=============================================")

HitRet()

def Thm1_03(a, l, m):
    """
    Input
        a: non-empty list of non-zero integers
        l: the least common multiple of a
        m: common multiple of a, 0 < m <= abs(prod(a))
    Print
        m%l == 0
    """
    print("a ==", a)
    print("the least common multiple l ==", l, "of a")
    print("common multiple m ==", m, "of a, then m%l ==", m%l, \
                "(m is divisible by l)")

def doThm1_03():
    a = [0]
    while prod(a) == 0:
        d = choice(range(1, length))
        a = [randint(-size, size)*d for _ in range(randint(1, length))]
    cm, l = lcm_def(*a)
    m = choice(list(cm))
    Thm1_03(a, l, m)
    print()

print("Theorem 1.3")
print("===========")
print("Any common multiple m of list a of non-zero integers")
print("    is divisible by the least common multiple l of a.\n")
again(doThm1_03)

size = 100 # maximum data size, positive integer
length = 10 # maximum data length, positive integer

def Thm1_04(a, m, d):
    """
    Input
        a: non-empty list of integers, at least one non-zero
        m: the greatest common divisor of a
        d: common divisor of a
    Print
        m%d == 0
    """
    print("a ==", a)
    print("the greatest common divisor m ==", m, "of a")
    print("common divisor d ==", d, "of a, then m%d ==", m%d, \
                "(m is divisible by d)")

def doThm1_04():
    a = [0]
    while max(a) == min(a) == 0:
        d = choice(range(1, length))
        a = [randint(-size, size)*d for _ in range(randint(1, length))]
    cd, m = gcd_def(*a)
    d = choice(list(cd))
    Thm1_04(a, m, d)
    print()

print("Theorem 1.4")
print("===========")
print("Any common divisor d of list a of integers, not all zero,")
print("    divides the greatest common divisor m of a.\n")
again(doThm1_04)

Thm1_05 = lcm

def doThm1_05():
    a, b = randint(1, size), randint(1, size)
    m, l = lcm_def(a, b)[1], Thm1_05(a, b)
    print("(a, b) ==", (a, b), "then (m, l) ==", (m, l), "and m == l", m == l)
    print()

print("Theorem 1.5")
print("===========")
print("The least common multiple m of a, b is equal to l = a*b//gcd(a, b).\n")
again(doThm1_05)

def Thm1_06(a, b, c):
    """
    Input
        a, b, c: integers such that a != 0, a, b are coprime, b*c%a == 0
    Print
        c%a == 0
    """
    print("(a, b, c) ==", (a, b, c))
    print("a != 0, a, b are coprime, b*c%a == " \
                + str(b*c) + "%" + str(a), "==", b*c%a)
    print("then c%a == " + str(c) + "%" + str(a), "==", c%a, \
            "(c is divisible by a)")

def doThm1_06():
    a = 0
    while a == 0:
        a = randint(-size, size)
    b = randint(-size, size)
    while gcd_def(a, b)[1] > 1:
        b = randint(-size, size)
    c = randint(-size, size)
    while b*c%a:
        c = randint(-size, size)
    Thm1_06(a, b, c)
    print()

print("Theorem 1.6")
print("===========")
print("For coprime a, b, if b*c is divisible by a, then c is divisible by a.\n")
again(doThm1_06)

Prob1 = gcd

def doProb1():
    d = choice([1]*9 + list(range(2, 10)))
    a = b = 0
    while a == b == 0:
        a, b = randint(-size, size)*d, randint(-size, size)*d
    md, m = gcd_def(a, b)[1], Prob1(a, b)
    print("(a, b) ==", (a, b), "then md == m is", md == m, "as below")
    print(md, "== md == the greatest common divisor of a, b by definition")
    print("==", m, "== m == the greatest common divisor of a, b by Prob1")
    print()

print("Problem 1")
print("=========")
print("Eucledian Algorithm computes the greatest common divisor.\n")
again(doProb1)

Prob1_rem = gcd_

def doProb1_rem():
    a = [0]
    while max(a) == min(a) == 0:
        d = choice([1]*9 + list(range(2, 10)))
        a = [randint(-size, size)*d for j in range(randint(1, length))]
    md, m = gcd_def(*a)[1], Prob1_rem(*a)
    print("a ==", a, "then md == m is", md == m, "as below")
    print(md, "== md == the greatest common divisor of a by definition")
    print("==", m, "== m == the greatest common divisor of a by Prob1_rem")
    print()

print("Remark of Problem 1")
print("===================")
print("Eucledian Algorithm with least absolute remainder")
print("    also applies for any number of integers.\n")
again(doProb1_rem)

def Prob1_rem_eg(*a):
    """
    Input
        a: integers, at least one non-zero
    Print
        gcd(a) with computing process by least absolute remainder
    """
    print("gcd", a)
    a = {i for i in a if i}
    m = min({abs(i) for i in a})
    while len(a) > 1:
        a = {i if abs(i) == m else modl(i, m) for i in a}
        a.discard(0)
        print("== gcd", tuple(a))
        m = min({abs(i) for i in a})
    print("==", m)

print("Example")
print("=======")
print("gcd(a) with computing process by least absolute remainder")
Prob1_rem_eg(629, 391, 255)
HitRet()

Prob2 = lcm_

def doProb2():
    a = [randint(1, size) for j in range(randint(1, length))]
    ld, l = lcm_def(*a)[1], Prob2(*a)
    print("a ==", a, "then ld == l is", ld == l, "as below")
    print(ld, "== ld == the least common multiple of a by definition")
    print("==", l, "== l == the least common multiple of a by Prob2")
    print()

size = 50 # maximum data size, positive integer
length = 5 # maximum data length, positive integer

print("Problem 2")
print("=========")
print("Repeated use of Eucledian Algorithm and Theorem 1.5")
print("    also applies for any number of integers.\n")
again(doProb2)



