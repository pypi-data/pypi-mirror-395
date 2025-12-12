"""
Congruences of Degree One
"""

from random import randint, choice
from nzmath.equation import e1_ZnZ
from nzmath.gcd import gcd
from utils import HitRet, again

size = 100 # maximum data size, positive integer
length = 10 # maximum data length, positive integer

print()
print("===============================================================")
print("For f(x), polynomial with integer coefficients, finding unknown")
print("integers x that satisfy congruent expression f(x) == 0 (mod m),")
print("implies solving congruences.  By Theorem 1.11, we may check the")
print("the values f(x) for x == 0, 1, 2, ..., m - 1.  In this section,")
print("we shall give some systematic computation in case deg(f) == 1.")
print("===============================================================")
HitRet()

Thm1_13 = e1_ZnZ

def doThm1_13():
    m = randint(1, size)
    a, b = (randint(-size*length, size*length) for _ in range(2))
    d = choice([1]*16 + list(range(2, 10))); a *= d; m *= d; b *= d
    print("Congruence {}*x == {} (mod {})".format(a, b, m), end =", ")
    d, T = Thm1_13([-b, a], m); print("GCD({}, {}) == {}".format(a, m, d))
    if T == []:
        print("No solution\n")
    elif d == 1:
        print("unique solution  x = {}\n".format(T[0]))
    else:
        print("{} solutions  x in {} with gap {}\n".format(d, T, m//d))
        for x in T:
            if (a*x - b)%m:
                raise RuntimeError("Not a solution!")

print("Theorem 1.13")
print("============")
print("There is a typical systematic method to solve congruence of degree one.")
print("It is a method studied in Sections 2 and 3, Euclidean Algorithms.")
print("For integers a, b, m, m > 0, congruence a*x == b (mod m) is solvable if")
print("and only if d = GCD(a, m) divides b, and then there are d solutions.")
HitRet()
again(doThm1_13, 10)

def Thm1_13_rem():
    a, b, m = 26, 1, 57; print("a, b, m = {}, {}, {}".format(a, b, m))
    print("Solve equation {}*x - {}*y == {}".format(a, m, b))
    A, B, C, U, V, W = 1, 0, a, 0, 1, -m
    print("Initialize A, B, C, U, V, W = 1, 0, a, 0, b, -m ==", \
            "{}, {}, {}, {}, {}, {}".format(1, 0, a, 0, 1, -m))
    print("While W != 0, do the following:")
    while W:
        q, r = divmod(C, W); A, B, C, U, V, W = U, V, W, A - q*U, B - q*V, r
        print("W is non-zero, so q, r = C//W, C%W, namely C == q*W + r")
        print("  and A, B, C, U, V, W = U, V, W, A - q*U, B - q*V, r ==", \
                "{}, {}, {}, {}, {}, {}".format(A, B, C, U, V, W))
    print("W == 0, C == {} < 0, so {}*x - {}*y == {} for x, y = {}, {}"\
            .format(-1, a, m, -C, -A, -B))

print("Remark of Theorem 1.13")
print("======================")
print("Since a*x == b (mod m) is equivalent to a*x - m*y == b, Theorem")
print("1.13 is the same as Theorem 1.7.  But, there usually is an easier")
print("way to solve congruences than to solve indeterminate equations.")
print("We shall see such a case in the next two examples.  We consider")
print("the case (a, b, m) == (26, 1, 57).  First, we solve it by Extended")
print("Euclidean Algorithm as we did in Theorem 1.13.")
HitRet()
Thm1_13_rem()
HitRet()

def Thm1_13_eg():
    a, b, m = 26, 1, 57; print("a, b, m = {}, {}, {}".format(a, b, m))
    print("Solve congruence {}*x == {} (mod {})".format(a, b, m))
    d = gcd(a, m); print("d = gcd(a, m) == {}, so unique solution".format(d))
    print("  *2 to the both sides ==> {}*x == {} (mod {})".format(a*2, b*2, m))
    print("  -57*x from the left side ==> {}*x == {} (mod {})"\
            .format(a*2 - m, b*2, m))
    print("  *5 to the both sides ==> {}*x == {} (mod {})"\
            .format((a*2 - m)*5, b*2*5, m))
    print("add the both sides to the given congruence ==> {}*x == {} (mod {})"\
            .format(a + (a*2 - m)*5, b + b*2*5, m))
    print("verification {}*{} == {} == {}*{} + {}"\
            .format(a, b + b*2*5, a*(b + b*2*5), m, \
            (a*(b + b*2*5))//m, (a*(b + b*2*5))%m))
    print()

print("Example of Theorem 1.13")
print("=======================")
print("Next, we solve it by an easier way applicable only to this case.")
print("The next example shows a way to solve congruence easily from a simple")
print("identity 57 == 26*2 + 5.  We can find out similar hints by experience.")
HitRet()
Thm1_13_eg()

