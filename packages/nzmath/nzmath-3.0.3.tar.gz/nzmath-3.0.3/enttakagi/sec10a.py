"""
Addendum Repeating Decimals
"""

from random import randint
from nzmath.gcd import gcd
from nzmath.multiplicative import euler as phi
from utils import HitRet, again

size = 100 # maximum data size, positive integer
length = 10 # maximum data length, positive integer

print("=======================================================================")
print("Variables are positive integers if not specified.")
print("(Bellow '(least) exponent' and 'multiplicative order' are same.)\n")

def Thm(n, m):
    """
    Input
        n, m: fraction  m/n  with numerator  m, denominator  n  s.t.
                0 < m < n, GCD(m, n) == GCD(10, n) == 1
    Output
        e, a: the exponent  e  of  10  modulo  n  s.t. 10**e = 1 + a*n
        d: decimal string of  sum((a*m)/(10**e)**j for j = 1, 2 ...) (== m/n)
    """
    if not (0 < m < n and gcd(m, n) == gcd(10, n) == 1):
        raise ValueError("0 < m < n, GCD(m, n) == GCD(10, n) == 1")
    e, b = 1, 10; a, r = divmod(b, n)
    while n - 1 > r > 1:
        e += 1; b *= 10; a, r = divmod(b, n)
    if r == n - 1:
        a = (a + 1)*(b - 1); e += e
    d = "{0} {0} ...".format(str(a*m).zfill(e)); assert phi(n)%e == 0
    return e, a, d # 10**e == a*n + 1, c == a*m

def Inverse(e, c):
    """
    Input
        e, c: e > 0, 0 < c < 10**e
        give purely repeating decimal  m/n  with  e  digits period  c
                m/n = sum(c/(10**e)**j for j = 1, 2, 3, ...)
    Output
        n, m: fraction  m/n  with numerator  m, denominator  n  s.t.
                0 < m < n, GCD(m, n) == GCD(10, n) == 1
    """
    if not (e > 0 and 0 < c < 10**e):
        raise ValueError("e > 0, 0 < c < 10**e")
    n = 10**e - 1; a = gcd(c, n); m, n = c//a, n//a
    return n, m # m/n == c/(10**e - 1), c == a*m

print("Theorem")
print("=======")
print("For an irreducible proper fraction  m/n, when the denominator  n  is")
print("not divisible both by  2  and  5, namely when  GCD(10, n) == 1, let  e")
print("be the least exponent of  10  modulo  n.  Then  m/n  is expanded to a")
print("purely repeating decimal with period  e.  Conversely, if  m/n  is")
print("expanded to a purely repeating decimal with period  e, then  e  is the")
print("least exponent of  10  molulo  n  such that  10**e == 1 (mod n), and  e")
print("is a divisor of Euler's function  phi(n)  depending only on the")
print("denominator  n.  Let  fn  be the factorlist of  n  such that  n ==")
print("prod(p**a for p,a in fn)  and let  ep  be the least exponent of  10")
print("molulo  p**a.  Then the exponent  e  of  10  modulo  n  satisfies  e ==")
print("LCM(ep for p,a in fn).\n")

print("Let us check these by numerical computation.  Inverse also!")

HitRet()

for _ in range(10):
    m = randint(1, size//5); n = randint(m + 1, size//3)
    while gcd(10, n) > 1 or gcd(m, n) > 1:
        n = randint(m + 1, size//3)
    e, a, d = Thm(n, m); c = a*m; assert (n, m) == Inverse(e, c)
    print("m/n = {}/{}  is  e = {}  digits periodic fraction  m/n =="\
        .format(m, n, e))
    print("  0 . " + d); print()

print("We continue under the same situation  0 < m < n  and  GCD(m, n) == 1.")
print("Let us consider the case  GCD(10, n) > 1, i.e.  n == 2**u*5**v*n_  with")
print("GCD(10, n_) == 1, k = max(u, v) > 0.  Then  10**k*m/n == m_/n_, m_ =")
print("2**(k - u)*5**(k - v)*m, GCD(m_, n_) == GCD(m, n) == 1.  Hence, if  e")
print("is the exponent of  10  modulo  n_, then  m_/n_ == m_//n_ + m_%n_/n_")
print("and  m_%n_/n_  is purely repeating decimal with period  e  digits.  So")
print("is  m/n  also, but the period starts from the (k + 1)-th decimal place.")
print("In case  n_ == 1, the fraction  m/n  is finite.")

HitRet()

def doThm():
    m = randint(1, size//5); n = randint(m + 1, size//3)
    while gcd(10, n) == 1 or gcd(m, n) > 1:
        m = randint(1, size//5); n = randint(m + 1, size//3)
    u, v, n_ = 0, 0, n
    while n_&1 == 0:
        u += 1; n_ >>= 1
    while n_%5 == 0:
        v += 1; n_ //= 5
    k = max(u, v); assert (n == 2**u*5**v*n_ and gcd(10, n_) == 1 and k > 0)
    m_ = 2**(k - u)*5**(k - v)*m # m_/n_ = 10**k*(m/n)
    if n_ == 1:
        print("finite decimal  m/n = {}/{} = {}\n"\
            .format(m, n, "0." + str(m_).zfill(k)))
    else:
        e, a, d = Thm(n_, m_%n_); assert (n_, m_%n_) == Inverse(e, a*(m_%n_))
        print("m/n = {}/{}, k = {}, m_/n_ = {}/{}".format(m, n, k, m_, n_))
        print("e = {} digits period m_%n_/n_ = {}/{} = 0 . {}"\
                .format(e, m_%n_, n_, d))
        print("  m_/n_ = {} . {}".format(m_//n_, d))
        print("  m/n = 0 . {} {}\n".format(str(m_//n_).zfill(k), d))

again(doThm, 10)

print("Remark")
print("======")
print("For prime factorization  n == p0**a0 * ... * pj**aj, let exponents of")
print("10  modulo  p0**a0, ..., pj**aj  be  e0, ..., ej  respectively.  Then")
print("exponent  e  of  10  modulo  n  is equal to the least common multiple")
print("of  e0, ..., ej, i.e.  e == LCM(e0, ..., ej).")

HitRet()

def repeatDecimal(n, m = 0):
    """
    Input
        n: denominator  n > 2, GCD(10, n) == 1, of fractions  m/n
            (numerators  m  s.t.  0 < m < n, GCD(m, n) == 1)
    Print
        process of expansion for  m/n
    Output
        a, e: period  a  of  1/n  in e-digits including 0-fill
    """
    l = len(str(n)); M = [1]; e, b = 1, 10; a, r = divmod(b, n)
    while n - 1 > r > 1:
        M.append(r); e += 1; b *= 10; a, r = divmod(b, n)
    if r == n - 1:
        M = M + [n - r for r in M]; a = (a + 1)*(b - 1); e += e
    if m:
        print("m/n == {0}/{1} == 0. {2} {2} ..."\
            .format(str(m).rjust(l), n, str(a*m).zfill(e)))
        return a, e
    print("denominator  n = {}, period  {}  digits  e = {}"\
            .format(n, str(a).zfill(e), e))
    L = [M]; S = set(m for m in range(1, n) if gcd(m, n) == 1) - set(M)
    while S != set():
        N = [min(S)*m%n for m in M]; L.append(N); S -= set(N)
    for i in range(len(L)):
        M = L[i]
        if i > 1:
            if i == 2:
                print("  other numerators")
                for j in [0, 1]:
                    m = L[j][0]
                    print("  m/n == {0}/{1} == 0. {2} {2} ..., {3}"\
                        .format(str(m).rjust(l), n, str(a*m).zfill(e), L[j]))
            m = M[0]
            print("  m/n == {0}/{1} == 0. {2} {2} ..., {3}"\
                .format(str(m).rjust(l), n, str(a*m).zfill(e), M))
            continue
        print("  numerators  {}".format(M))
        for m in M:
            print("  m/n == {0}/{1} == 0. {2} {2} ..."\
                .format(str(m).rjust(l), n, str(a*m).zfill(e)))
        I, J = 10**e, 1
        for m in M:
            print("period  {} == {}*{} == {} + {} {}".format(str(a*m).zfill(e),\
                str(a).zfill(e), str(m).rjust(l), str(a*M[0]%I*J).zfill(e),\
                str(a*M[0]//I).zfill(len(str(J)) - 1).rjust(e - 1),\
                a*m == a*M[0]%I*J + a*M[0]//I))
            I //= 10; J *= 10
        if i > 0:
            continue
        f, r = divmod(e, 2); F = 10**f
        if r == 0:
            for m in M:
                q = a*m//F; Q = str(q).zfill(f); R = str(F - 1 - q).zfill(f)
                print("{0}{1} + {2} - {3} == {0}{1} + {4} == {5} {6}"\
                    .format(Q, ''.zfill(f), F - 1, Q, R, str(a*m).zfill(e),\
                    q*F + F - 1 - q == a*m))
    return a, e

print("Example 1")
print("=========")
repeatDecimal(7)
HitRet()

print("Example 2")
print("=========")
repeatDecimal(13)
HitRet()

print("Example 3")
print("=========")
repeatDecimal(91)
HitRet()

for _ in range(20):
    m = randint(1, size//5); n = randint(m + 1, size//3)
    while not (0 < m < n and gcd(m, n) == gcd(10, n) == 1):
        n = randint(m + 1, size//3)
    a, e = repeatDecimal(n, m); assert (n, m) == Inverse(e, a*m)

HitRet()


