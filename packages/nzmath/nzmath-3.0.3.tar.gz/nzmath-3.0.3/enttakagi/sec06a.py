"""
Congruences of Degree One (cotinued)
"""

from time import perf_counter as time
from gc import collect, disable, enable
from random import randint
from nzmath.arith1 import CRT_, CRT_Gauss
from nzmath.arith1 import product as prod
from nzmath.gcd import extgcd, divmodl, pairwise_coprime, gcd, part_frac
from nzmath.prime import generator_eratosthenes
from utils import HitRet, again, randFactLists, strInt

size = 100 # maximum data size, positive integer
length = 5 # maximum data length, positive integer

print()
print("===============================================================")
print("As systematic computation of solving congruences of polynomials")
print("of degree 1, the Chinese Remainder Theorem (CRT) is popular and")
print("will be quoted later.  There are only a finite number of cases")
print("to check for given congruences.  So the problem is efficiency.")
print("===============================================================")
print()

Primes = set(generator_eratosthenes(size))

Thm1_14 = CRT_

def doThm1_14():
    c = []
    while len(c) < 2:
        c = [prod(p**e for p, e in m) \
                for m in randFactLists(Primes, length, True)]
    c = [(randint(0, m - 1), m) for m in c]
    for a, m in c:
        print("x == {} (mod {})".format(a, m))
    n, M = Thm1_14(c)
    print("==> x == {}\n  (mod {})\n".format(strInt(n, 70), strInt(M[0], 70)))
    for a, m in c:
        if n%m != a:
            raise RuntimeError("Something wrong!")

print("Theorem 1.14")
print("============")
print("For pairwise coprime moduli m[i] (0 <= i < k) and residues a[i]")
print("(0 <= i < k), solve    x == a[i] (mod m[i])  (0 <= i < k).")
print("First we show a classical example, and another simple one.")
HitRet()
print("Consider the case of 3 congruences:")
print("\tx == a0 (mod m0), x == a1 (mod m1), x == a2 (mod m2)")
print("The first two is equivalent to obtain t below:")
print("\tx == a0 + m0*t == a1 (mod m1)")
print("Since GCD(m0, m1) == 1, such t == t0 + m1*s is given by Theorem 1.13:")
print("\tt0 = (a1 - a0)*extgcd(m0, m1)[0]%m1")
print("Then x == a0 + m0*(t0 + m1*s) == a0 + m0*t0 (mod m0*m1).")
print("Now we may solve the third congruence together with this one.")
print("\tx == a0 + m0*t0 + m0*m1*t == a2 (mod m2)")
print("By Theorem 1.13 again, such t == t1 + m2*s is given by")
print("\tt1 = (a2 - a0 - m0*t0)*extgcd(m0*m1, m2)[0]%m2")
print("Then x == a0 + m0*t0 + m0*m1*t1 (mod m0*m1*m2) is obtained.")
HitRet()
for c in [[(1, 2), (2, 3), (3, 5)], [(2, 3), (2, 5), (6, 7)]]:
    a0, m0, a1, m1, a2, m2 = \
        c[0][0], c[0][1], c[1][0], c[1][1], c[2][0], c[2][1]
    for a, m in c:
        print("x == {} (mod {})".format(a, m), end = "  ")
    print()
    t0 = (a1 - a0)*extgcd(m0, m1)[0]%m1
    print("Compute t0 = (a1 - a0)*extgcd(m0, m1)[0]%m1 ==", t0)
    t1 = (a2 - a0 - m0*t0)*extgcd(m0*m1, m2)[0]%m2
    print("Compute t1 = (a2 - a0 - m0*t0)*extgcd(m0*m1, m2)[0]%m2 ==", t1)
    M = m0*m1*m2; n = (a0 + m0*t0 + m0*m1*t1)%M
    print("Then x == a0 + m0*t0 + m0*m1*t1 (mod m0*m1*m2) is obtained.")
    nn, MM = Thm1_14(c)
    if (nn, MM[0]) != (n, M):
        raise RuntimeError((nn, MM[0]), "!=", (n, M))
    print("  ==> x == {} +{}*{} + {}*{}*{} == {} (mod {})\n"\
            .format(a0, m0, t0, m0, m1, t1, n, M))
print("A few more examples.")
HitRet()
again(doThm1_14, 3)

def doCRT_Gauss():
    k = len(m); a = [randint(0, m[i] - 1) for i in range(k)]
    for i in range(k):
        print("x == {} (mod {})".format(a[i], m[i]))
    n, M = CRT_Gauss(a, m, P)
    print("==> x == {}\n  (mod {})\n".format(strInt(n, 70), strInt(M[0], 70)))
    for i in range(k):
        if n%m[i] != a[i]:
            raise RuntimeError("Something wrong!")

print("CRT by Gauss")
print("============")
print("Another method is to treat all moduli symmetrically.")
print("For a while, fix moduli m == [m[i] for i in range(k)] with k > 1.")
HitRet()
m = []
while len(m) < 2:
    m = [prod(p**e for p, e in c) for c in randFactLists(Primes, length, True)]
P = CRT_Gauss([0]*len(m), m)[1]
again(doCRT_Gauss)

def Thm1_14_eg():
    m1, m2, m3 = 3, 5, 7
    print("Moduli m1 = {}, m2 = {}, m3 = {}".format(m1, m2, m3), end = "")
    M = m1*m2*m3; M1, M2, M3 = M//m1, M//m2, M//m3
    print(" ==> M = m1*m2*m3 == {},".format(M))
    print("M1 = M//m1 == {}, M2 = M//m2 == {}, M3 = M//m3 == {},"
            .format(M1, M2, M3))
    t1, t2, t3 = [divmodl(extgcd(a, b)[0], b)[1] \
                    for a, b in [(M1, m1), (M2, m2), (M3, m3)]]
    print("Inverses of M1, M2, M3: t1 = {}, t2 = {}, t3 = {},"\
                                                .format(t1, t2, t3))
    M1t1, M2t2, M3t3 = M1*t1, M2*t2, M3*t3
    Mt1, Mt2, Mt3 = [divmodl(Mt, m)[1] \
                    for Mt, m in [(M1t1, m1), (M2t2, m2), (M3t3, m3)]]
    print("M1*t1 == {} == {} (mod {}), ".format(M1t1, Mt1, m1) + \
        "M2*t2 == {} == {} (mod {}), ".format(M2t2, Mt2, m2) + \
        "M3*t3 == {} == {} (mod {}).".format(M3t3, Mt3, m3))
    print("Solution of x == a1 (mod {}), == a2 (mod {}), == a3 (mod {}) is"\
        .format(m1, m2, m3))
    print("x == {}*a1 + {}*a2 + {}*a3 (mod {}).".format(M1t1, M2t2, M3t3, M))
    print("Here, the residues a1, a2, a3 appeared for the first time!")
    a1, a2, a3 = 1, 2, 3; s = M1t1*a1 + M2t2*a2 + M3t3*a3
    print("Constants a1 = {}, a2 = {}, a3 = {}".format(a1, a2, a3))
    print("==> x == {}*{} + {}*{} + {}*{} == {} == {} (mod {})"\
            .format(M1t1, a1, M2t2, a2, M3t3, a3, s, s%M, M))

print("Example of Theorem 1.14")
print("=======================")
print("Let us see symmetric method in detail by a simpler example.\n")
Thm1_14_eg()
HitRet()

def CRT_pre():
    mS = [prod(p**e for p, e in m) for m in randFactLists(Primes, length, True)]
    P = CRT_Gauss([0]*len(mS), mS)[1]
    gord, gpre = 0, 0
    collect(); disable()
    for _ in range(size*length):
        c = [(randint(0, m - 1), m) for m in mS]; aS = [a for a, m in c]
        s = time(); CRT_Gauss(aS, mS, P); t = time(); gpre += t - s
        s = time(); CRT_Gauss(aS, mS); t = time(); gord += t - s
    enable()
    return gord/gpre

    print("Time Symmetric Ordinary/Improved  {}.".format(round(gord/gpre, 3)))
    print()

print("Performance Check")
print("=================")
print("As we see, if the moduli m is fixed, only the final step differs.")
print("Then we see that precomputation works to improve the algorithm.")
print("\nNow after hitting return key, wait for a while to finish experiment!")
HitRet()
OP = 0
for _ in range(size*length):
    OP += CRT_pre()
print("Time Ordinary/Improved {}.".format(round(OP/(size*length), 3)))
HitRet()

def Thm1_14_rem(m, x):
    """
    Input
        m: list of pairwise coprime integers, min(m) > 1, k = len(m) > 0
        x: integer > 0
    M = prod(m), GCD(M, x) == 1
    Output (X, s)
        X: list of numerators of partial fraction decomposition of x/M
        s: integer part of partial fraction decomposition of x/M
    x/M == sum(X[i]/m[i] for i in range(k)) + s
    0 < X[i] < m[i] for i in range(k)
    """
    k = len(m); M = prod(m)
    if not(k and min(m) > 1 and pairwise_coprime(m)):
        raise ValueError("denominator list m is incorrect")
    if gcd(M, x) > 1:
        raise ValueError("x/M should be irreducible")
    M_ = [M//m[i] for i in range(k)]
    t = [extgcd(M_[i], m[i])[0]%m[i] for i in range(k)]
    a = [x%m[i] for i in range(k)]
    if (x - sum(a[i]*M_[i]*t[i] for i in range(k)))%M:
        raise RuntimeError("wrong transformation")
    s = (x - sum(a[i]*M_[i]*t[i] for i in range(k)))//M
    X = [a[i]*t[i]%m[i] for i in range(k)]
    s += sum(a[i]*t[i]//m[i] for i in range(k))
    return X, s

print("Remark of Theorem 1.14")
print("======================")
print("For a list m of pairwise coprime integers, min(m) > 1, k = len(m) > 0,")
print("let M = prod(m), the product of the elements of m, and take an integer")
print("x > 0 with GCD(M, x) == 1.  Consider the partial fraction decomposition")
print("of x/M.  Let a = [x%m[i] for i in range(k)].  Then x == a[i] (mod m[i])")
print("for i in range(k).  Therefore CRT by Gauss enables us to compute x ==")
print("sum(a[i]*M_[i]*t[i] for i in range(k)), where M_[i] == M//m[i] and")
print("M_[i]*t[i] == 1 (mod m[i]).  So x/M == sum(a[i]*t[i]/m[i]) + integer.")
print("We define it as a function and compare with Problem 14 in Section 4.")
HitRet()
for m, x in [([3, 5, 7], 52),\
            ([2**2, 3**2, 5**1, 17**1, 19**1], 1001),\
            ([17**4, 23**4], 343),\
            ([13**2, 17**1, 23**2, 29**5, 19**3], 99225)]:
    M = prod(m); print("(m, x) =", (m, x))
    print("\twith M = prod(m) ==", M)
    print("\tx/M == sum(X[i]/m[i] for i in range(k)) + s")
    X, s = Thm1_14_rem(m, x)
    print("\tBy CRT_Gauss (X, s) ==", (X, s))
    print("\tBy Sec4.Prob14 (X, s) is same ?", (X, s) == part_frac(m, x))
    print("\t{}/{} ==\n\t{}/{}".format(x, M, X[0], m[0]), end = " ")
    for i in range(1, len(m)):
        print("+ {}/{} ".format(X[i], m[i]), end = "")
    print("+", s)
    print()

