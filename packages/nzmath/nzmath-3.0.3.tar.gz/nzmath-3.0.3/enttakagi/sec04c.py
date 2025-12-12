"""
Prime Numbers (continued)
"""
from random import randint, choice
from nzmath.arith1 import expand
from nzmath.arith1 import product as prod
from nzmath.combinatorial import binomial, multinomial
from nzmath.gcd import gcd_, extgcd_, part_frac
from nzmath.prime import primeq, generator_eratosthenes
from utils import HitRet, again, randFactLists

size = 100 # maximum data size, positive integer
length = 5 # maximum data length, positive integer

print()
print("=========================================")
print("Variables here are all positive integers,")
print("except for integer s in Problem 14 below.")
print("For factorlist f and integer n, we shall")
print("identify by n == prod(p**e for p, e in f)")
print("often in the following explanation.")
print("=========================================")

HitRet()

def Prob12():
    """
    Print
        p: prime number
        n: positive integer for the exponent of p
        k: 0 < k < p**n
        e: p-adic valuation of k, namely 0 <= e < n, just p**e divides k
        binomial coefficient binomial(p**n, k) is divisible by p**(n - e)
    """
    pn = 100000
    while pn > 99999:
        p, n = randint(2, size), randint(1, length)
        while not primeq(p):
            p = randint(2, size)
        pn = p**n
    print("prime p == " + str(p) + ", p**n == " + str(pn) + \
            " with n == " + str(n))
    e = randint(0, n - 1); pe = p**e; pne = pn//pe; k = randint(1, pne - 1)
    while not k%p:
        k = randint(1, pne - 1)
    k *= pe; bpnk = binomial(pn, k)

    print("let 0 < k ==", k, "< p**n with p-adic valuation e ==", e, "of k")
    print("binomial(p**n, k) == ", end = "")
    if bpnk < 10**55:
        print(bpnk)
    else:
        print("(too large to print)")
    print("is divisible by p**(n - e) ==", pne, ":", bpnk%pne == 0)
    print()

print("Problem 12")
print("==========")
print("For k-th binomial coefficient of prime power p**n, its p**(n - e)")
print("divisibility is shown, where e is the p-adic valuation of k.")
HitRet()
again(Prob12)

def Prob12_rem():
    """
    Print
        p: prime number
        n: positive integer for the exponent of p
        a: partition list of positive integers such that sum(a) == p**n
        k: 0 <= k < n, p-adic valuation of one element b of a
        multinomial coefficient multinomial(p**n, a) is divisible by p**(n - k)
    """
    pn = 100000
    while pn > 99999:
        p, n = randint(2, size), randint(1, length)
        while not primeq(p):
            p = randint(2, size)
        pn = p**n
    print("prime p == " + str(p) + ", p**n == " + str(pn) + \
            " with n == " + str(n))
    k = randint(0, n - 1); pk = p**k; pnk = pn//pk
    b = randint(1, pnk - 1); l = randint(2, length)
    while not b%p or pn < b*pk + l - 1:
        k = randint(0, n - 1); pk = p**k; pnk = pn//pk
        b = randint(1, pnk - 1); l = randint(2, length)
    b *= pk; a = [b]; s = pn - b
    for i in range(l - 2):
        b = randint(1, s - (l - 2 - i))
        a.append(b); s -= b
    a.append(pn - sum(ai for ai in a)); b = a[0]
    print("partition a ==", a, "of p**n with element b ==", b)
    mpna = multinomial(pn, a)
    print("0 < b ==", b, "< p**n with p-adic valuation k ==", k, "of b")
    print("multinomial(p**n, a) == ", end = "")
    if mpna < 10**55:
        print(mpna)
    else:
        print("(too large to print)")
    print("and p**(n - k) ==", pnk, "divides it:", mpna%pnk == 0)
    print()

print("Remark of Problem 12")
print("====================")
print("For multinomial coefficient multinomial(p**n, a) of prime power p**n")
print("and partition a, sum(a) == p**n, its p**(n - k) divisibility is shown,")
print("where k is the p-adic valuation of one element of a .")
HitRet()
again(Prob12_rem)

def Prob13(n, p):
    """
    Input
        n: positive integer
        p: prime number
    Output
        e: p-adic valuation of n!, just p**e divides n!
    """
    e, q = 0, n//p
    while q:
        e += q; q //= p
    return e

def doProb13():
    p = randint(2, size)
    while not primeq(p):
        p = randint(2, size)
    n = randint(p, size**length)
    print("(n, p) ==", (n, p), \
            "then p-adic valuation of n! is e ==", Prob13(n, p))
    print()

print("Problem 13")
print("==========")
print("For prime p and positive integer n, the p-adic valuation e of")
print("factorial n!, just p**e divides n!, is obtained without computing")
print("factorial itself, but division of n by p repeatedly.")
HitRet()
again(doProb13, 10)

def doProb13_rem():
    p = randint(2, size)
    while not primeq(p):
        p = randint(2, size)
    n = randint(p, size**length)
    a = expand(n, p); e = (n - sum(a))//(p - 1)
    print("(n, p) ==", (n, p), "then p-adic valuation of n! is e ==", e)
    print("p-adic coefficients of n is ", end = "")
    if len(str(a)) < 50:
        print(a)
    elif len(str(a)) < 75:
        print("\n ", a)
    else:
        print("(too large to print)")
    print()

print("Remark of Problem 13")
print("====================")
print("For prime p and positive integer n, the p-adic valuation e of")
print("factorial n!, just p**e divides n!, is obtained without computing")
print("factorial itself, but computing p-adic expansion of only n.")
HitRet()
n, p = 120759, 7
a = expand(n, p); e = (n - sum(a))//(p - 1)
print("(n, p) ==", (n, p), "then p-adic valuation of n! is e ==", e)
print("p-adic coefficients of n is", a)
print()
again(doProb13_rem, 10)

def Prob14(f, m):
    pe = [p**e for p, e in f]; n = prod(pe)
    x, s = part_frac(pe, m); l = len(f)
    print("m / n ==", m, "/", n, "==\n  m / (",\
                str(f[0][0]) + "**" + str(f[0][1]), end = " ")
    for i in range(1, l):
        print("*", str(f[i][0]) + "**"+ str(f[i][1]), end = " ")
    print(") ==\n", end = "  ")
    for i in range(l):
        print("(" + str(x[i]) + "/" + \
                str(f[i][0]) + "**" + str(f[i][1]), end = ") + ")
    print(s); print()

Primes = list(generator_eratosthenes(30))

def doProb14():
    f = choice(randFactLists(Primes, length))
    P = set(Primes)
    P.difference_update(set(p for p, e in f))
    g = choice(randFactLists(list(P), length))
    m = prod(p**e for p, e in g)
    Prob14(f, m)

print("Problem 14")
print("==========")
print("For coprime integers m > 0, n > 1, partial fraction decomposition")
print("of m/n can be executed by prime factorization of n and Theorem 1.7.")
HitRet()
f = [(2, 2), (3, 2), (5, 1), (17, 1), (19, 1)]; m =1001
Prob14(f, m)
again(doProb14, 9)

def Prob14_rem():
    """
    Print
        p: prime number
        e: integer, e > 0
        x: integer, 0 < x < p**e, x%p != 0
        p-adic fraction expansion of x/p**e
    """
    p = choice(Primes); e = randint(1, length); pe = p**e
    x = randint(1, pe - 1)
    while not x%p:
        x = randint(1, pe - 1)
    a = expand(x, p); l = len(a)
    print("x / p**e ==", x, "/", str(p) + "**" + str(e), "==")
    print("  (" + str(a[0]) + "/" + str(p) + "**" + str(e), end = ")")
    for i in range(1, l):
        print(" + (" + str(a[i]) + "/" + str(p) + "**" + str(e - i), end = ")")
    print(); print()

print("Remark of Problem 14")
print("====================")
print("Fraction x/p**e with prime power denominator, appearing in partition")
print("fraction decomposition, can be expanded to polynomial in 1/p further")
print("by utilizing p-adic expansion of x in Remark of Problem 13.")
HitRet()
again(Prob14_rem, 10)

