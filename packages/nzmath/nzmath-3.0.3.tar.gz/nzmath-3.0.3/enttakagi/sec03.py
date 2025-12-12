"""
Linear Indeterminate Equations
"""

from random import randint, choice
from nzmath.gcd import gcd_of_list, extgcd_, gcd_, extgcd_gen
from utils import HitRet, again

size = 100 # maximum data size, positive integer
length = 10 # maximum data length, positive integer

print()

Thm1_07 = gcd_of_list

def doThm1_07():
    a = [0]
    while max(a) == min(a) == 0:
        d = choice([1]*9 + list(range(2, 10)))
        a = [randint(-size, size)*d for j in range(randint(1, length))]
    n, [d, x], [d_, x_], d__ = len(a), Thm1_07(a), extgcd_(*a), gcd_(*a)
    ax = sum([a[j]*x[j] for j in range(n)])
    ax_ = sum([a[j]*x_[j] for j in range(n)])
    print("a ==", a, ", n == len(a) ==", n)
    print("  gcd by 3 methods:  (d, d_, d__) ==", (d, d_, d__),
            "; d == d_ == d__ is", d == d_ == d__)
    print("  linear form by 2 methods: (x, x_) ==\n   ", (x, x_),
            ";\n  ax = sum([a[i]*x[i] for i in range(n)]) ==", ax,
            ";\n  ax_ = sum([a[i]*x_[i] for i in range(n)]) ==", ax_,
            ";\n  x == x_ is", x == x_, "; ax == ax_ == d is", ax == ax_ == d)
    print()

print("Theorem 1.7")
print("===========")
print("The GCD d of list a divides any linear form of a (Theorem 1.1).")
print("Conversely, we see d is expressed as some linear form of a.\n")
again(doThm1_07, 3)

def Thm1_07_eg(a, b, c):
    [d, s, A] = extgcd_gen(a, b, c)
    print("gcd", (a, b, c), "==", d)
    print("  solution of equation", a, "* x +", b, "* y +", c, "* z ==", d)
    u = ["x'", "y'", "z'"]
    u[s] = 1
    print("    x =", 
        A[0][0], "*", u[0], "+", A[0][1], "*", u[1], "+", A[0][2], "*", u[2])
    print("    y =", 
        A[1][0], "*", u[0], "+", A[1][1], "*", u[1], "+", A[1][2], "*", u[2])
    print("    z =", 
        A[2][0], "*", u[0], "+", A[2][1], "*", u[1], "+", A[2][2], "*", u[2])
    k = 0
    while k == 0:
        k = randint(-size, size)*d
    print("  solution of equation", a, "* x +", b, "* y +", c, "* z ==", k)
    u = ["x'", "y'", "z'"]
    u[s] = k//d
    print("    x =", 
        A[0][0], "*", u[0], "+", A[0][1], "*", u[1], "+", A[0][2], "*", u[2])
    print("    y =", 
        A[1][0], "*", u[0], "+", A[1][1], "*", u[1], "+", A[1][2], "*", u[2])
    print("    z =", 
        A[2][0], "*", u[0], "+", A[2][1], "*", u[1], "+", A[2][2], "*", u[2])
    print()

def doextgcd_gen():
    a = [0]
    while max(a) == min(a) == 0:
        d = choice([1]*9 + list(range(2, 10)))
        a = [randint(-size, size)*d for j in range(randint(1, length))]
    print("equation a ==", a)
    [d, s, A] = extgcd_gen(*a)
    print("  gcd d ==", d, "with constant parameter y[", s, "], solution A")
    for i in range(len(A)):
        print("    ", A[i])
    print()

print("Example")
print("=======")
print("General integer solution of linear equation a*x + b*y + c*z == k.\n")
Thm1_07_eg(32, 57, -68)
for _ in range(2):
    a = [0]
    while max(a) == min(a) == 0:
        d = choice([1]*9 + list(range(2, 10)))
        a = [randint(-size, size)*d for j in range(3)]
    Thm1_07_eg(*a)
print("General integer solution of linear equation, n = len(a),")
print("    sum(a[i]*x[i] for i in range(n)) == k")
print("for k divisible by the gcd d of a[i].  Solution is")
print("    x = [sum(A[i][j]*y[j] for j in range(n)) for i in range(n)]")
print("for integer parameter y with one constant y[s] = k//d.")
HitRet()
again(doextgcd_gen, 3)

def Prob1(a, b):
    """
    Input
        a, b: integers, either one non-zero
    Print
        a*y - b*x == k: linear equation
            (integer k divisible by the greatest common divisor d of a, b)
        x = x0 + a_*t, y = y0 + b_*t: general solution
    """
    [d, [y0, x0]] = extgcd_(a, -b)
    m = 0
    while m == 0:
        m = choice([1]*9 + list(range(2, 10)))
    k, x0, y0, a_, b_ = d*m, x0*m, y0*m, a//d, b//d
    print("lnear equation", a, "*y -", b, "*x ==", k)
    print("  general integer solution")
    print("    x =", x0, "+", a_, "*t")
    print("    y =", y0, "+", b_, "*t")

def doProb1():
    a = b = 0
    while a == b == 0:
        d = choice([1]*9 + list(range(2, 10)))
        a, b = randint(-size, size)*d, randint(-size, size)*d
    Prob1(a, b)
    print()

print("Problem 1")
print("=========")
again(doProb1)

print("Problem 2")
print("=========")
print("Gives the principle of the proofs of Theorems 1.3 and 1.7.")
print("Essentially proved 'eucledian ring is principal ideal domain.'")
print()
