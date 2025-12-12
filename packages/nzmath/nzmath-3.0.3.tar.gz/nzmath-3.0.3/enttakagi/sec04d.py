"""
Prime Numbers (continued)
"""
from random import randint
from math import log
from nzmath.arith1 import floorsqrt
from nzmath.arith1 import product as prod
from nzmath.combinatorial import factorial
from nzmath.factor.methods import rhomethod
from nzmath.prime import \
    generator_eratosthenes, primonial, primeq, generator, nextPrime
from utils import HitRet, again, strInt

size = 100 # maximum data size, positive integer
length = 5 # maximum data length, positive integer

print()
print("=========================================")
print("Variables here are all positive integers.")
print("=========================================")


HitRet()

def Thm1_10():
    """
    Print
        p: prime number
        a: (product of primes 2*3*5*7*11* ... *p) + 1 = primonial(p) + 1
        existence of prime q > p
    """
    for p in generator_eratosthenes(size):
        if p < 40:
            continue
        a = primonial(p) + 1
        print("(p, a) ==", (p, a))
        q = rhomethod(a)[0][0]
        if q <= p or not primeq(q):
            raise RuntimeError("Bigger prime was not found!")
        print("Given prime p ==", p, "<", q, "== q is found prime.\n")

print("Theorem 1.10")
print("============")
print("For prime p, prime factor q of a = 2*3*5*7*11* ... *p + 1 shows q > p.")
HitRet()
Thm1_10()

print("Prime Table")
print("===========")
print("By Eratosthenes sieve, if you sieve table by prime up to p, you get")
print("primes less than p**2.  You can see it by list [1, 2, ..., 100].")
HitRet()

print("size = 100; T = list(range(size + 1)) # initialize table")
size = 100; T = list(range(size + 1)); print(T[1:]); HitRet()
print("p = 1; T[p] = 0 # 1 is non-prime")
p = 1; T[p] = 0; print(T[1:]); HitRet()
print("for p in range(2, floorsqrt(size) + 1): # sieve 2 to p*p <= size")
print("    if T[p] != 0: # p is decided as prime")
print("        for q in range(p*p, size + 1, p): # sieve multiple q of p")
print("            T[q] = 0 # q is decided as composite\n")
for p in range(2, floorsqrt(size) + 1):
    if T[p] != 0:
        for q in range(p*p, size + 1, p):
            T[q] = 0
        print("p ==", p); print(T[1:]); HitRet()
P = [p for p in T if p]; print("Complete Prime Table up to", size, "is", P)
print()

def Thm1_10_rem():
    """
    Print
        p: prime number p%4 == 3
        a: (product 4*3*7*11*19* ... *p) - 1
        existence of prime q > p
        p: prime number p%6 == 5
        a: (product 6*5*11*17*23* ... *p) - 1
        existence of prime q > p
    """
    L = [p for p in generator_eratosthenes(size) if p%4 == 3]
    print("Case of 4*n - 1:\n")
    for p in L:
        a = 4*prod(r for r in L if r <= p) - 1
        print("(p, a) ==", (p, a))
        f = rhomethod(a)
        for q, e in f:
            if q%4 == 3:
                break
        if q <= p or not primeq(q) or q%4 != 3:
            raise RuntimeError("Bigger prime was not found!")
        print("Given prime p ==", p, "<", q, "== q is found prime.")
    HitRet()
    L = [p for p in generator_eratosthenes(size) if p%6 == 5]
    print("Case of 6*n - 1:\n")
    for p in L:
        a = 6*prod(r for r in L if r <= p) - 1
        print("(p, a) ==", (p, a))
        f = rhomethod(a)
        for q, e in f:
            if q%6 == 5:
                break
        if q <= p or not primeq(q) or q%6 != 5:
            raise RuntimeError("Bigger prime was not found!")
        print("Given prime p ==", p, "<", q, "== q is found prime.")

print("Remark of Theorem 1.10")
print("======================")
print("For given prime p, prime q > p is found by 4*3*7*11*19* ... *p - 1.")
print("Primes are all of the form 4*n - 1.  Same is possible for 6*n - 1.")
HitRet()
Thm1_10_rem()
print()

def PrimeNumberTheorem():
    """
    Print
        p: the pi-th prime number counting from below
        pi: the number of primes <= p
        pi/(p/log(p)): converges to 1 as p goes to infinity
    """
    pi = 0
    for p in generator():
        pi += 1
        if pi%10**4 == 0:
            print("pi-th prime p, (pi, p) ==", (pi, p), \
                    "and pi/(p/log(p)) ==", round(pi/(p/log(p)), 5))
            if pi == 1000000:
                break

print("Prime Number Theorem")
print("====================")
print("The limit of pi(x)/(x/log(x)) is 1 as x goes to infinity, where pi(x)")
print("is the number of primes not exceeding x.  We do numerical experiment.")
HitRet()
PrimeNumberTheorem()

print()

def Tschebyschef(n):
    """
    Input
        n: integer, n > 1
    Output
        p: prime, the smallest under p > n, also checked p < 2*n
    """
    p = nextPrime(n)
    if p > n + n:
        raise RuntimeError("no prime between n and 2*n, n ==", n)
    return p

length = 10 # maximum data length, positive integer

def doTschebyschef():
    x = randint(2, size**length); p = Tschebyschef(x)
    print("x ==", x, "<", p, "== p", "< 2*x and p - x ==", p - x)

print("Tschebyschef Theorem")
print("====================")
print("For given integer x, the smallest prime p > x will be obtained.")
print("Also p < 2*x is verified and p - x is computed.")
HitRet()
again(doTschebyschef, 40)

print()

def twinPrime(n):
    """
    Input
        n: integer, n > 0
    Output
        p: prime, the smallest under p >= n and p + 2 is also prime
    """
    if n < 4:
        return 3
    p = 6*(n//6) + 5
    while not primeq(p) or not primeq(p + 2):
        p += 6
    return p

def dotwinPrime():
    x = randint(2, size**length); p = twinPrime(x)
    print("x ==", x, "<=", p, "== p and p - x ==", p - x)

print("Twin Prime")
print("==========")
print("For given x, the smallest prime p >= x with prime p + 2 is obtained.")
print("Such twin primes are conjectured to be infinite, so p - x is computed.")
HitRet()
x = 10001441; p = twinPrime(x)
print("x ==", x, "<=", p, "== p and p - x ==", p - x)
again(dotwinPrime, 40)

print()

def gapPrime():
    """
    Print
        n consecutive composite integers
    """
    n = randint(1, size)
    N = factorial(n + 1)
    T = True
    for d in range(2, n + 2):
        T = T and not (N + d)%d
    print("n ==", n, "then d divides (n + 1)! + d (2 <= d <= n + 1):", T)
    print("(n + 1)! ==", strInt(N))
    print()

print("Prime Gap")
print("=========")
print("We can explicitly give n consecutive composites, n is prime gap.")
HitRet()
again(gapPrime, 10)

def Goldbach(n):
    """
    Input
        n: integer, n > 1
    Output
        G: list of primes p <= n such that 2*n - p is prime
    """
    if n < 2:
        raise ValueError("integer n == " + str(n) + " > 1?")
    if n == 2:
        return [2]
    G = []
    for p in range(3, n, 2):
        if primeq(p) and primeq(n + n - p):
            G.append(p)
    if primeq(n):
        G.append(n)
    return G

print("Goldbach Conjecture")
print("===================")
print("Any even integer 2*n (> 2) is written as 2*n == p + q with primes p, q.")
HitRet()
for n in range(2, 42):
    G = Goldbach(n)
    n2 = n + n
    print(n2, end = "")
    for p in G:
        print(" ==", p, "+", n2 - p, end = "")
    print()

print()


