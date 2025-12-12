"""
Fermat's Theorem
"""
from random import randint, choice
#from timeout_decorator import timeout, TimeoutError
from nzmath.algorithm import powering_func
from nzmath.arith1 import product as prod
from nzmath.cyclotomic import cycloPoly
from nzmath.factor.methods import factor
from nzmath.factor.misc import allDivisors
from nzmath.factor.misc import FactoredInteger as FI
from nzmath.gcd import gcd
from nzmath.multiplicative import euler, moebius
from nzmath.poly.uniutil import IntegerPolynomial as IP
from nzmath.poly.uniutil import PseudoDivisionProvider as PDP
from nzmath.prime import full_euler, randPrime, primeq, generator_eratosthenes
from nzmath.rational import IntegerRing as IR
from utils import HitRet, again, strInt

size = 100 # maximum data size, positive integer
length = 10 # maximum data length, positive integer

phi = euler

print("\n===============================================================")
print("Variables are (non-negative) integers if not specified.")
print("(Bellow '(least) exponent' and 'multiplicative order' are same.)\n")

print("Euler's theorem states that\n\t\ta**phi(m) == 1 (mod m)")
print("for any  a  with  GCD(a, m) == 1.  For example")
HitRet()
for _ in range(5):
    m = randint(1, size**length); a = randint(1, m)
    pow = powering_func(lambda x, y : x*y%m)
    while gcd(a, m) - 1:
        a = randint(1, m)
    phim = phi(m); aphim = pow(a, phim)
    print("m, a = {}, {}, then\n\ta**phi(m) == a**{} == {} (mod m) {}.\n"\
        .format(m, a, phim, aphim, aphim == 1))

print("Theorem 1.25 (Fermat's Theorem)")
print("===============================")
print("If  p  is prime and  a != 0 (mod p), then\n\ta**(p - 1) == 1 (mod p).")
print("If  p  is prime, then\n\ta**p == a (mod p).")
HitRet()
for m, a in [(7, 10), (13, 2), (16, 5)]:
    phim = phi(m); aphim = a**phim
    print("m, a = {}, {}, then\n\ta**phi(m) == a**{} == {} (mod m) {}."\
        .format(m, a, phim, aphim%m, aphim%m == 1))
    if m != 16:
        print("\t{}**{} - 1 == {} == {}*{}.\n"\
            .format(a, phim, aphim - 1, m, (aphim - 1)//m))
    else:
        print("\t{}**{} - 1 == ({}**{} - 1)*({}**{} + 1) == {}"\
        .format(a,phim,a,phim//2,a,phim//2,a**(phim//2)-1),end="")
        print("*{}== {}*{}*{}.\n"\
        .format(a**(phim//2)+1,m,(a**(phim//2)-1)//m,a**(phim//2)+1))

def Thm1_25(n):
    """
    Input
        n: integer > 1
    Output
        True or False iff.  n  is prime or composite
        (n  is prime iff.  phi(n) == n - 1  iff.  exist order  n - 1  residue)
    """
    return full_euler(n, allDivisors(n - 1))

def doThm1_25():
    n = choice([randPrime(length//2)\
                , randint(2, size**(length//3)), randint(2, size**(length//3))])
    j = Thm1_25(n); assert j == primeq(n), "n = {}, primality {}?".format(n, j)
    print("n = {}, primality is  {}(, phi(n) == {}).\n".format(n, j, phi(n)))

print("Application of Theorem 1.25")
print("===========================")
print("For a positive integer  n, by searching a reduced residue modulo  n  of")
print("order  (n - 1)//p  (prime factor  p  of  n - 1), we can judge whether")
print("phi(n) == n - 1  or not, and primality estimate of  n  is obtained.")
HitRet()
again(doThm1_25, 10)

def Thm1_26(m, a):
    """
    Input
        m: integer > 0
        a: integer, GCD(a, m) == 1
    Print
        m, a
        e: exponent for  a (mod m), e = min(k: integer > 0, a**k == 1 (mod m))
        a**k == 1 (mod m)  iff.  k == 0 (mod e)
    """
    pow = powering_func(lambda a, b : a*b%m)
    print("\nm = {}, a = {}  with".format(m, a)); P = phi(m) + 1
    K = [k for k in range(1, P) if pow(a, k) == 1]; e = min(K)
    E = list(range(e, P, e))
    print("exponent  e == {}, a**e == {} (mod m)".format(e, pow(a, e)))
    print("a**k == 1 (mod m)  iff.  k == 0 (mod e)  is  {}".format(K == E))
    ph = phi(m); print("esp.  phi(m) == {} == {} (mod e)".format(ph, ph%e))

print("Theorem 1.26")
print("============")
Thm1_26(63, 5)
for _ in range(5):
    m = randint(2, size**(length//5)); a = m
    while gcd(a, m) > 1:
        a = randint(2, m)
    Thm1_26(m, a)

HitRet()

print("Remark on Negative Powering")
print("===========================")
print("For an integer  m > 1, let  a  be  GCD(a, m) == 1  exponent e.  Then")
print("ordinary way of expressing formula by negative powering is possible:")
print("    h == k (mod e)  iff.  a**h == a**k (mod m).")
print("    a**h*a**k == a**(h + k) (mod m)", end =", ")
print("(a**h)**k == a**(h*k) (mod m).")
print("Here  h  and  k  are any integers maybe negative.")

HitRet()

def Prob1(m, a, k):
    """
    Input
        m: integer > 0
        a: integer, GCD(a, m) == 1
        k: integer
    Print
        m, a, k
        e: exponent for  a (mod m)
        f: exponent for  a**k (mod m), f == e//GCD(k, e)
    """
    pow = powering_func(lambda a, b : a*b%m)
    print("m = {}, a = {}, k = {}".format(m, a, k)); P = phi(m) + 1; x = 1
    for e in range(1, P):
        x = x*a%m
        if x == 1:
            break
    b = pow(a, k); x = 1
    for f in range(1, P):
        x = x*b%m
        if x == 1:
            break
    print("exponents e == {}, f == {} for a, a**k, and f == e//gcd(k, e) {}\n"\
            .format(e, f, f == e//gcd(k, e)))

print("Problem 1")
print("=========")
Prob1(63, 5, 7)
for _ in range(5):
    m = randint(2, size**(length//5)); a = m
    while gcd(a, m) - 1:
        a = randint(2, m)
    k = randint(1, phi(m))
    Prob1(m, a, k)

P = list(generator_eratosthenes(size))
P4 = [p for p in P if p%4 == 1]
P6 = [p for p in P if p%6 == 1]

def Thm1_25_rem(m, Pm):
    """
    Input
        m == 4  or  6
        Pm: the list of primes  p <= size, p%m == 1
    Print
        p: prime, p%m == 1
        x = 2*prod(q for q in Pm if q <= p)  or  6*prod(q for q in Pm if q <= p)
        Fm(x): m-th cyclotomic polymomial  a = x**2 + 1  or  x**2 - x + 1
        existence of prime q > p, q%m == 1
    """
    print("Case of {}*n + 1:\n".format(m))
    for p in Pm:
        x = 2*prod(q for q in Pm if q <= p)
        if m == 4:
            a = x**2 + 1
        else:
            x *= 3; a = x**2 - x + 1
        print("(p, a) ==", (p, a))
        f = factor(a)
        for q, e in f:
            if q%m == 1:
                break
        if q <= p or not primeq(q) or q%m != 1:
            raise RuntimeError("Bigger prime was not found!")
        print("Given prime p ==", p, "<", q, "== q found prime.")
    HitRet()

print("Remark of Theorem 1.25")
print("======================")
print("For given prime p, prime q > p is found by (4*5*13*17*...*p)**2 + 1.")
print("Primes are all of the form 4*n + 1.  Same is possible for 6*n + 1.")
HitRet()
Thm1_25_rem(4, P4)
Thm1_25_rem(6, P6)

mu = moebius

#@timeout(10)
def tryfactor(n):
    return factor(n)

def primeArith(m):
    """
    Input
        m: integer > 1
    Output
        p: prime  p == 1 (mod m)
    """
    Fm = cycloPoly(m); fm = factor(m)
    A = [0]
    for a in range(1, length):
        A += [a, -a]
    for a in A:
        Fma = abs(Fm(a))
        if Fma <= 1 or Fma > length**size:
            continue
        try:
            if m != 11*683 and m != 11*23:
                pFma = [p for p,e in tryfactor(Fma) if m%p]
            else:
                raise RuntimeError
        except RuntimeError:
            print("Timeout factor  Fm({}) == \n{}".format(a, strInt(Fma, 77)))
            continue
        if pFma == []:
            continue
        p = min(pFma)
        assert p%m == 1
        return p
    return 1

print("Theorem (There are infinitely many primes of the form  m*t + 1.)")
print("================================================================")
print("For m > 1, Fm(x) = prod((x**(m//d) - 1)**mu(d) for d in allDivisors(m))")
print("(the m-th cyclotomic polynomial).  Find prime  p == 1 (mod m).  Given")
print("prime  p == 1 (mod m), find prime  q == 1 (mod m), q > p.\n")
for m in [5, 8, 9, 12, 7, 10, 11, 2, 3, 4, 6]:
    print("modulus  m ==", m)
    p = primeArith(m)
    if p == 1:
        print("Failed to find  p == 1 (mod {}).\n".format(m))
        continue
    print("prime  p == {} == {} (mod m)".format(p, p%m))
    q = primeArith(m*p)
    if q == 1:
        print("Failed to find  q == 1 (mod {}), q > p.\n".format(m))
        continue
    assert q > p
    print("primes  q == {} > p, q == {} (mod m)\n".format(q, q%m))

