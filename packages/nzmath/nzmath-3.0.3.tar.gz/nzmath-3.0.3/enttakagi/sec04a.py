"""
Prime Numbers (continued)
"""
from time import perf_counter as time
from random import randint
from nzmath.arith1 import product as prod
from nzmath.factor.misc import \
    countDivisors, sumDivisors, squarePart, allDivisors
from nzmath.multiplicative import sigma
from nzmath.gcd import gcd_
from nzmath.prime import generator_eratosthenes, primeq, LucasLehmer
from utils import \
    HitRet, countDivisors_def, again, sumDivisors_def, allDivisors_def, strInt

size = 100 # maximum data size, positive integer
length = 5 # maximum data length, positive integer

print()
print("=========================================")
print("Variables here are all positive integers.")
print("=========================================")
print()
print("Prime factorization can easily solve several divisibility problems.")
print("For integer a = p1**e1*...*pn**en with prime factorization, tau")
print("function T(a) = (e1 + 1)*...*(en + 1) and sigma function S(a) =")
print("(p1**(e1 + 1) - 1)//(p1 - 1)*...*(pn**(en + 1) - 1)//(pn - 1).")
print("Furthermore, generalized sigma function sigma(z, a) =")
print("(p1z**e1 +...+ p1z**2 + p1z + 1)*...*(pnz**en +...+ pnz**2 + pnz + 1),")
print("where p1z = p1**z, ..., pnz = pn**z (z-th-divisor-power-sum of a).")

HitRet()

T = countDivisors # usually tau function

def Prob1(a):
    """
    Input
        a: positive integer
    Print
        the number of divisors of a coinsides by 3 different ways of computation
    """
    print("(a, T(a)) ==", (a, T(a)))
    print("  T(a) == sigma(0, a) == (that without factorization) is", \
            T(a) == sigma(0, a) == countDivisors_def(a))

def doProb1():
    Prob1(randint(2, size**length))
    print()

print("Problem 1")
print("=========")
print("The number T(a) of divisors of a coinsides by 3 different ways.")
again(doProb1)

S = sumDivisors # usually sigma function

def Prob2(a):
    """
    Input
        a: positive integer
    Print
        the sum of divisors of a coinsides by 3 different ways of computation
    """
    print("(a, S(a)) ==", (a, S(a)))
    print("  S(a) == sigma(1, a) == (that without factorization) is", \
            S(a) == sigma(1, a) == sumDivisors_def(a))

def doProb2():
    Prob2(randint(2, size**length))
    print()

print("Problem 2")
print("=========")
print("The sum S(a) of divisors of a coinsides by 3 different ways.\n")
again(doProb2)

def Prob3(m, *a):
    """
    Input
        m: arithmetic function
        a: pairwise coprime positive integers
    Print
        check m is multiplicative using a as example 
    """
    stra = str(a[0])
    for i in range(1, len(a)):
        stra = stra + "," + str(a[i])
    print(",a=(" + stra + "),m(prod(a))==prod(m(n)for n in a):"+ \
            str(m(prod(a)) == prod(m(n) for n in a)))

def doProb3():
    for k in range(3):
        a, b = (randint(2, size**length) for j in range(2))
        while gcd_(a, b) > 1:
            b = randint(2, size**length)
        if k < 2:
            ab, c = a*b, randint(2, size**length)
            while gcd_(ab, c) > 1:
                c = randint(2, size**length)
            if k == 0:
                print("m=T", end = "")
                Prob3(T, a, b, c)
            else:
                print("m=S", end = "")
                Prob3(S, a, b, c)
        else:
            print("m=squarePart", end = "")
            Prob3(squarePart, a, b)
    print()

print("Problem 3")
print("=========")
print("Complex valued functions on positive integers are arithmetic functions.")
print("Arithmetic function m such that m(a*b) == m(a)*m(b) for gcd(a, b) == 1")
print("is called multiplicative and is computable from prime factorization.")
print("For m = T or S, we may check m(a*b) == m(a)*m(b) if a, b are coprime.")
print("Let's see m(a*b*c) == m(a)*m(b)*m(c) if a, b, c are pairwise coprime.")
print("Also squarPart(a) = max(d such that a%d**2 == 0) is multiplicative.")
HitRet()
again(doProb3)

def Prob4(a):
    """
    Input
        a: positive integer
    Print
        the divisors of a coincide by 2 different ways of comutation
        and its product is given by a**(T(a)/2) with tau function T(a)
    """
    aD, aDd = allDivisors(a), allDivisors_def(a)
    pD, Ta = prod(aD), T(a)
    if Ta&1:
        apowT = int(a**.5)**Ta
    else:
        apowT = a**(Ta//2)
    print("a ==", a)
    print("  the divisors allDivisors(a) and allDivisors_def(a) are equal:",\
            set(aD) == aDd)
    print("  product of all divisors of a\n       == " + strInt(pD))
    print("       == a**(T(a)/2) is", pD == apowT)

def doProb4():
    Prob4(randint(2, size**length))
    print()

print("Problem 4")
print("=========")
print("Check the divisors of a coincide by 2 different ways of computation.")
print("Let us see the product of all divisors of a is given by a**(T(a)/2).")
print("\tT(a):odd<==>e:even(prime p,p**e||a)<==>a:square<==>a**.5:int")
HitRet()
again(doProb4)

def PerfNumb(a):
    """
    Input
        a: positive integer
    Print
        a, S(a) - a, 'a is perfect, abundant or deficient'
    """
    Sa_a = S(a) - a; which = Sa_a - a
    if which > 0:
        which = "abundant."
    elif which < 0:
        which = "deficient."
    else:
        which = "perfect."
    print("(a, S(a) - a) ==", (a, Sa_a), "so a ==", a, "is", which)

print("Perfect Number")
print("==============")
print("Let us directory check S(a) == 2*a by prime factorization of a.\n")
for a in range(2, 10):
    PerfNumb(a)
print("..........")
for a in range(20, 30):
    PerfNumb(a)

def Prob5(n):
    """
    Input
        n: prime number
    Output
        b = 2**n - 1: Mersenne number
        a = 2**(n - 1)*b: candidate of even perfect number
        d = primeq(b): dicision of b to be prime
        ta, tb: execution time to judge 'a to be perfect', 'b to be prime'
    No check that decisions of 'a to be perfect', 'b to be prime' are equal.
    """
    b = 2**n - 1
    a = 2**(n - 1)*b
    start = time()
    a == S(a) - a
    stop = time()
    ta = stop - start
    start = time()
    d = primeq(b)
    stop = time()
    tb = stop - start
    return b, a, d, ta, tb

HitRet()

print("Problem 5")
print("=========")
print("a == 2**(n - 1)*b with b == 2**n - 1 for prime n.")
print("\teven perfect <==> a is perfect <==> b is prime (Mersenne prime)")
print("Compare execution time to determine a is perfect or not.\n")

K, L, M, N = 5000, 607, 127, 61

time_def = time_euler = 0
print("(n, b, a) for n <=", M)
print()
for n in generator_eratosthenes(M):
    b, a, d, ta, tb = Prob5(n)
    time_def += ta
    time_euler += tb
    if n <= N:
        print((n, b, a), "perfect:", d)
    elif d:
        print("(n, b) ==", (n, b), "and perfect a ==")
        print(a)
print("\nTested (a == S(a) - a) or (b is prime) respectively in",
        "%#.3g"%time_def, "sec. or", "%#.3g"%time_euler, "sec.")

HitRet()

print("Wait for a while for (n, b, a) with prime b and", N, "<= n <=", L)
print("Triples (n, b, a) giving Mersenne primes and perfect numbers:\n")
for n in generator_eratosthenes(L):
    if n < N:
        continue
    b = 2**n - 1
    a = 2**(n - 1)*b
    if primeq(b):
        print((n, b, a))
print()

print("Lucas-Lehmer Test")
print("=================")
print("For Mersenne number b = 2**n - 1 with n odd prime,")
print("\tb is prime <==>  s[n - 2] is divisible by b,")
print("where s[0] = 4, s[i] = s[i - 1]**2 - 2.\n")
print("Mersenne prime b == 2**n - 1 with n <=", K)
HitRet()
for n in range(3, K):
    if primeq(n):
        b, j = LucasLehmer(n)
        if j:
            print("n == " + str(n) + ", b == " + strInt(b, 60))
print()

