"""
Introduction to Solving Congruences
"""

from random import randint, choice
from nzmath.algorithm import digital_method_func
from nzmath.arith1 import inverse
from nzmath.equation import allroots_Fp
from nzmath.gcd import modl
from nzmath.prime import randPrime
from nzmath.poly.hensel import HenselLiftPair
from nzmath.poly.uniutil import IntegerPolynomial
from nzmath.rational import IntegerRing
from utils import HitRet, again, randmodPolyList, printPoly

size = 100 # maximum data size, positive integer
length = 10 # maximum data length, positive integer

print()
print("===============================================================")
print("Let  f(x) = cn*x**n + ... + c1*x + c0  be a polynomial in")
print("variable  x  with integer  n >= 0 , integers  c0, c1, ..., cn .")
print("Solve the congruence  f(x) == 0 (mod m)  with modulus  m > 0 .")
print("If  cn != 0 (mod m) , we say the congruence is of degree  n .")
print("===============================================================")

HitRet()

print("===============================================================")
print("There are many types of polynomial ring defined in our NZMATH.")
print("In any case, the degree  n  (namely  cn != 0) polynomial")
print("\tf(x) = c0 + c1*x + ... + cn*x**n")
print("is represented by the coefficients dict")
print("\t{0:c0, 1:c1, ..., n:cn}")
print("or else by the coefficients tuple list")
print("\t[(0, c0), (1, c1), ..., (n, cn)]")
print("or sometimes by the ascending coefficients list (poly_list)")
print("\t[c0, c1, ..., cn]")
print("any of which is appropriate to the situation.  We shall use some")
print("of them to understand that we are applying general method.  Our")
print("purpose is not to show efficiency but to display techniques.")
print("===============================================================")

HitRet()

Thm1_15 = allroots_Fp

def doThm1_15():
    p = randPrime(randint(1, 2)); f = randmodPolyList(p, length)
    printPoly(f); print(" == 0 (mod {})".format(p))
    X = Thm1_15(f, p); X = [modl(x, p) for x in X]
    print("\tIn total {}  solutions in {}\n".format(len(X), set(X)))

print("Theorem 1.15")
print("============")
print("If modulus  m = p  is prime, then the congruence  f(x) == 0 (mod p)")
print("of degree  n  has at most  n  solutions.  To evaluate  f(x) , we")
print("applied FinitePrimeFieldPolynomial.")
HitRet()
for (p, f) in [(7, [0, -1, 0, 0, 0, 0, 0, 1]), (19, [-7, 7, 5, 3])]:
    printPoly(f); print(" == 0 (mod {})".format(p))
    X = Thm1_15(f, p); X = [modl(x, p) for x in X]
    print("\tIn total {} solutions in {}\n".format(len(X), set(X)))
again(doThm1_15, 8)

def Thm1_15_rem():
    for (m, g) in \
            [(12, [(2, 1), (1, 0), (0, -1)]), (3, [(2, 1), (1, 0), (0, -2)]), \
             (36, [(4, 1), (3, 2), (2, -1), (1, 1), (0, -2)]), \
             (60, [(4, 1), (0, -1)])]:
        evalDM = digital_method_func(lambda a, b : modl(a + b, m), \
                lambda a, b : modl(a*b, m), lambda i, a : modl(i*a, m), \
                lambda a, i : modl(a**i, m), 0, 1)
        f = IntegerPolynomial(g, IntegerRing())
        printPoly(f); print(" == 0 (mod {})".format(m))
        X = [modl(x, m) for x in range(m) if evalDM(g, x) == 0]
        print("In total  {}  solutions in  {} .\n".format(len(X), set(X)))

print("Theorem 1.15 Remark")
print("===================")
print("There can happen to have much number of solutions than the degree")
print("n  in case modulus  m  is composite.  On the other hand, it can")
print("happen, for prime modulus  p  also, there is no solution at all.")
print("To evaluate  f(x) , we applied digital_method_func (Karatsuba).\n")
Thm1_15_rem()

print("===============================================================")
print("For composite moduli, we consider power  m = p**n  of prime  p")
print("with  n > 1 .  Treating such a subject often leads us to more")
print("general perspective.  This case leads to p-adic number theory.")
print("===============================================================")

HitRet()

def Thm1_16(p, N, f, x0):
    """
    Input
        p: prime
        N: integer  > 0
        f: IntegerPolynomial
        x0: integer, f(x0) == 0 (mod p)
    Output
        x: integer list, x[0] == x0, f(x[n]) == 0 (mod p**(n + 1)) (0 <= n <= N)
            or  N  s.t.  f(x[N]) != 0 (mod p**(N + 1))  if f'(x0) == 0 (mod p)
    Print
        f(x[n]) (mod p**(n + 1)) (0 <= n <= N)
        a1(x), a2(x), f(x) == a1(x)*a2(x) (mod p**n)  if f'(x[0]) != 0 (mod p)
    """
    x = [x0]; df = modl((f.differentiate())(x0), p)
    print("solve  f(x) == 0 (mod p**{})  with  p = {}".format(N + 1, p))
    printPoly(f); print("\nx0 = {}, f(x0) == {}, f'(x0) == {} (mod p)" \
            .format(x0, modl(f(x0), p), df))
    if df:
        idf = inverse(df, p)
        print("(i) Standard\nf({}) == {} (mod p)".format(x0, modl(f(x0), p)))
        for n in range(N):
            x.append(modl(x[n] - f(x[n])*idf, p**(n + 2)))
            print("f({}) == {} (mod p**{})" \
                .format(x[n + 1], modl(f(x[n + 1]), p**(n + 2)), n + 2))
        a1 = IntegerPolynomial({0:-x0, 1:1}, IntegerRing())
        a2 = (f.monic_floordiv(a1)).reduce(p)
        HLP = HenselLiftPair.from_factors(f, a1, a2, p)
        print("Hensel lift  f(x) == a1(x)*a2(x) (mod p**n):")
        printPoly(HLP.a1, "a1"); print(", ", end = "")
        printPoly(HLP.a2, "a2"); print(" (mod p)")
        for n in range(N):
            HLP.lift_factors()
            printPoly((HLP.a1).reduce(p**(n + 2)), "a1"); print(", ", end = "")
            printPoly((HLP.a2).reduce(p**(n + 2)), "a2")
            print(" (mod p**{})".format(n + 2))
    else:
        print("(ii) Singular\nf({}) == {} (mod p)".format(x0, modl(f(x0), p)))
        for n in range(N):
            if modl(f(x[n]), p**(n + 2)):
                x.append(x[n]); N = n + 1; break
            else:
                x.append(x[n] + randint((2 - p)//2, p//2)*p**(n + 1))
        for n in range(N):
            print("f({}) == {} (mod p**{})" \
                .format(x[n + 1], modl(f(x[n + 1]), p**(n + 2)), n + 2))
    return x

def doThm1_16():
    p, N = randPrime(randint(1, 2)), randint(3, length)
    f = randmodPolyList(p, length); x0 = randint((2 - p)//2, p//2)
    f = IntegerPolynomial({i:f[i] for i in range(len(f))}, IntegerRing())
    Thm1_16(p, N, (f - f(x0)).reduce(p), x0); print()

print("Theorem 1.16")
print("============")
print("Congruences modulo a power  p**n  of prime  p  can be solved by lifting")
print("exponent  n  higher.  Case (i):  If polynomial congruence  f(x) == 0")
print("(mod p)  has a solution  x0  with  f'(x0) != 0 (mod p), then  x0  will")
print("be lift up uniquely to the solution  xn == x0 (mod p)  of  f(xn) == 0")
print("(mod p**n).  This fact is a special case of general Hensel lift, which")
print("is a method of p-adic squarefree polynomial factorization.  We further")
print("will apply Hensel lift to our special case.  Case (ii):  On the other")
print("hand, when  f'(x0) == 0 (mod p), lifting up  x0  to solutions  xn == x0")
print("(mod p)  of  f(xn) == 0 (mod p**n)  is more complicated.  We shall see")
print("it later as Problem 1 in a very special case for  p == 2 .")
for p, N, f, x0 in \
    [(5, 9, [1, 0, 0, -2, -1, -2], -2), (2, 9, [0, 1, 1, 0, 0, 1, 1], 1)]:
    f = IntegerPolynomial({i:f[i] for i in range(len(f))}, IntegerRing())
    HitRet(); Thm1_16(p, N, f, x0)
for _ in range(7):
    HitRet(); doThm1_16()
HitRet(); again(doThm1_16, 1)

def Thm1_16_eg(p, a, x0):
    """
    Input
        p: prime, p > 2
        a: integer, a%p != 0
        x0: integer, x0**2 == a (mod p)
    Output
        x1: integer, x1 == x0 (mod p), x1**2 == a (mod p**2)
    """
    print("From  p = {}, a = {}, x0**2 == a (mod p),".format(p, a), \
                "solve  x1**2 == a (mod p**2) .")
    if a%p == 0:
        raise ValueError("prime  p  should not divide  a")
    f = IntegerPolynomial({0:-a, 2:1}, IntegerRing()); df = f.differentiate()
    if modl(f(x0), p):
        raise ValueError("{}**2 != {} (mod {})".format(x0, a, p))
    printPoly(f); print(", ", end = ""); printPoly(df, "f'")
    print(", x1 = x0 - (1/f'(x0))*f(x0)")
    for x0 in [x0, -x0]:
        print("\n[direct computation]")
        print("x0 = {} ==> ".format(x0), end = "")
        df0 = df(x0); idf0 = inverse(df0, p); x1 = modl(x0 - idf0*f(x0), p**2)
        print("x1 == {} - {}*{} == {} (mod p**2)"\
                .format(x0, idf0, f(x0), x1))
        print("Verify  x1**2 == a (mod p**2)  is", f(x1)%p**2 == 0)
        print("\n[apply the function]")
        Thm1_16(p, 1, IntegerPolynomial({0:-a, 2:1}, IntegerRing()), x0)

def doThm1_16_eg():
    p = 2
    while p == 2:
        p = randPrime(randint(1, 2))
    x0 = choice([-1, 1])*randint(1, p//2); a = modl(x0**2, p)
    Thm1_16_eg(p, a, x0); print()

print("Example of Theorem 1.16")
print("=======================")
print("As an example of solving congruences, let us consider getting square")
print("root of a given number modulo square of a prime.  First, we compute")
print("directly following the proof of the theorem.  Next, we apply function")
print("Thm1_16(p, N, f, x0) to this case and verify the results.")
HitRet(); Thm1_16_eg(7, 2, 3)
HitRet(); doThm1_16_eg()
HitRet(); again(doThm1_16_eg, 1)

