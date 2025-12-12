"""
Prime Numbers (continued)
"""
from nzmath.arith1 import product as prod
from nzmath.combinatorial import combination_index_generator as comb
from nzmath.gcd import gcd_, lcm_
from nzmath.prime import generator_eratosthenes
from nzmath.factor.misc import FactoredInteger
from utils import HitRet, randFactLists, again, strInt

size = 100 # maximum data size, positive integer
length = 5 # maximum data length, positive integer

print()
print("=========================================")
print("Variables here are all positive integers.")
print("For factorlist f and integer n, we shall")
print("identify by n == prod(p**e for p, e in f)")
print("often in the following explanation.  Also")
print("we may identify n and FactoredInteger(n).")
print("=========================================")

HitRet()

def Prob6(a, b):
    """
    Input
        a, b: lists of factorlists with GCD(f, g) == 1 for f in a for g in b
    Print
        GCD(prod(a), prod(b)) == 1
    """
    print("lists a, b such that GCD(f, g) == 1 for f in a for g in b")
    print("  a:", end = "")
    for f in a:
        print("\t", f)
    print("  b:", end = "")
    for f in b:
        print("\t", f)
    a = prod(prod(p**e for p, e in f) for f in a)
    b = prod(prod(p**e for p, e in f) for f in b)
    print("GCD(prod(a), prod(b)) == 1:", gcd_(a, b) == 1)
    print()

Primes = list(generator_eratosthenes(size))

def doProb6():
    a = randFactLists(Primes, length)
    P = set(Primes)
    P.difference_update(set(p for f in a for p, e in f))
    b = randFactLists(list(P), length)
    Prob6(a, b)

print("Problem 6")
print("=========")
print("Elements of lists a, b are pairwise coprime factorlists.")
print("Then the product of elements of a and that of b are coprime.")
HitRet()
again(doProb6, 3)

def Prob7(a, b):
    """
    Input
        a, b: lists of factorlists
    Print
        GCD(a)*GCD(b) == GCD(ab), ab = [f*g for f in a for g in b]
    """
    print("lists a, b consists of general factorlists")
    print("  a:", end = "")
    for f in a:
        print("\t", f)
    print("  b:", end = "")
    for g in b:
        print("\t", g)
    a = [prod(p**e for p, e in f) for f in a]
    b = [prod(p**e for p, e in f) for f in b]
    ab = [f*g for f in a for g in b]
    print("  ab:\t [f*g for f in a for g in b]")
    a, b, ab = gcd_(*a), gcd_(*b), gcd_(*ab)
    print("(GCD(a), GCD(b), GCD(ab)) ==", (a, b, ab))
    print("    GCD(a)*GCD(b) == GCD(ab):", a*b == ab)
    print()

Primes = [2, 3, 5, 7, 11, 13]

def doProb7():
    Prob7(randFactLists(Primes, length), randFactLists(Primes, length))

print("Problem 7")
print("=========")
print("Elements of lists a, b are factorlists giving integers.")
print("GCD(a), GCD(b): the GCD of integers by factorlists in a, b")
print("GCD(a)*GCD(b) == GCD(ab), ab is elementwise product of a, b")
HitRet()
again(doProb7, 3)

def gcdlcmFI(*a):
    """
    Input
        a: FactoredIntegers f identified with positive integers
    Output
        (m, l): GCD m and LCM l (as FactoredInteger) of members f of a
        GCD and LCM of FactoredIntegers are obtained by their prime exponents
    """
    a = [f.factors for f in a]
    m = a.pop(); l = m.copy() # initialize GCD, LCM
    Pm, Pl = {p for p in m}, {p for p in l} # prime factors of m, l
    while a != []:
        f = a.pop() # next target
        Pf = {p for p in f} # prime factors of f
        mm, ll = {}, {} # initialize next GCD, LCM
        for p in Pm&Pf: # prime factor p common to m and f
            mm[p] = min(m[p], f[p])
        for p in Pl&Pf: # prime factor p common to l and f
            ll[p] = max(l[p], f[p])
        for p in Pl - Pf: # prime factor p of l alone
            ll[p] = l[p]
        for p in Pf - Pl: # prime factor p of f alone
            ll[p] = f[p]
        m, Pm, l, Pl = mm.copy(), Pm&Pf, ll.copy(), Pl|Pf
    return FactoredInteger(prod(p**e for p, e in m.items()), m), \
            FactoredInteger(prod(p**e for p, e in l.items()), l)

def Prob8(a):
    """
    Input
        a: list of FactoredIntegers f identified with positive integers
    Print
        GCD m and LCM l of FactoredIntegers f coincide with usual ones
    """
    print("members are FactoredIntegers f")
    print("  a:", end = "")
    for f in a:
        print("\t", f.integer, f.factors)
    m, l = gcdlcmFI(*a)
    a = [f.integer for f in a]
    print("FactoredIntegers f give (m, l) ==", (m.integer, l.integer))
    print("  and (GCD(a), LCM(a)) == (m, l):", \
                (gcd_(*a), lcm_(*a)) == (m.integer, l.integer))
    print()

def doProb8():
    Prob8([FactoredInteger(prod(p**e for p, e in f), dict(f)) \
            for f in randFactLists(Primes, length)])

print("Problem 8")
print("=========")
print("Elements of a are FactoredIntegers.")
print("Then (GCD(a), LCM(a)) == (m, l), where m, l are repectively")
print("GCD, LCM of a obtained by exponents of factorization.")
HitRet()
again(doProb8)

def Prob9(a):
    """
    Input
        a: list of FactoredIntegers identified with positive integers
    Print
        n = len(a): the number of integers a[0], ..., a[n - 1]
        d = [GCD(the product of k + 1 elements of a) for k in range(n)]
        d[k]%d[k - 1] == 0 for k in range(1, n)
        e = [d[0]] + [d[k]//d[k - 1] for k in range(1, n)]
        prod(e) == prod(a) and e[n - 1] == LCM(a)
    """
    n = len(a)
    print("members are n ==", n, "FactoredIntegers\n  a:", end = "")
    for k in range(n):
        print("\t", a[k].integer, a[k].factors)
    d = []; print("GCD of products of 1 to n elements of a\n  d:", end = "")
    for k in range(n):
        d.append(gcdlcmFI( \
            *[prod(a[c[i]] for i in range(k + 1)) for c in comb(n, k + 1)])[0])
        print("\t", strInt(d[k].integer, 20), d[k].factors)
        if k:
            T = T and d[k]%d[k - 1] == 0; e.append(d[k]//d[k - 1])
        else:
            T, e = True, [d[0]]
    for k in range(1, n):
        print("d[" + str(k) + "]%d[" + str(k - 1) + "] == ", end = "")
    if n > 1:
        print("0:", T)
    print("  e:", end = "")
    for k in range(n):
        print("\t", strInt(e[k].integer, 20), e[k].factors)
    print("prod(e) == prod(a):", prod(e) == prod(a), end = "    ")
    print("e[" + str(n - 1) + "] == LCM(a):", e[n - 1] == gcdlcmFI(*a)[1])
    print()

def doProb9():
    Prob9([FactoredInteger(prod(p**e for p, e in f), dict(f)) \
            for f in randFactLists(Primes, length)])

print("Problem 9")
print("=========")
print("Elements of list a are FactoredInteger f.")
print("All computation goes on by f.factors of FactoredInteger f.")
HitRet()
again(doProb9, 2)

def Prob10(a, m):
    """
    Input
        a: list of FactoredIntegers identified with positive integers
        m: FactoredInteger identified with positive integer
    Print
        FactoredIntegers f in a, FactoredInteger m
        LCM(GCD(f, m) for f in a) == GCD(LCM(f for f in a), m)
    """
    print("members are FactoredIntegers\n  a:", end = "")
    for f in a:
        print("\t", f.integer, f.factors)
    print("  m:\t", m.integer, m.factors)
    print("LCM(GCD(f, m) for f in a) == GCD(LCM(f for f in a), m):", \
            gcdlcmFI(*[gcdlcmFI(f, m)[0] for f in a])[1] == \
            gcdlcmFI(gcdlcmFI(*[f for f in a])[1], m)[0])
    print()

def doProb10():
    m = randFactLists(Primes, length)[0]
    m = FactoredInteger(prod(p**e for p, e in m), dict(m))
    Prob10([FactoredInteger(prod(p**e for p, e in f), dict(f)) \
            for f in randFactLists(Primes, length)], m)

print("Problem 10")
print("==========")
print("Elements f of list a and integer m are FactoredIntegers.")
print("All computation goes on by f.factors of FactoredIntegers.")
print("Show LCM(GCD(f, m) for f in a) == GCD(LCM(f for f in a), m).")
HitRet()
again(doProb10)

def Prob11(a):
    """
    Input
        a: list of FactoredIntegers identified with n = len(a) positive integers
    Print
        l = LCM(a[i] for i in range(n)) == prod(a0[i] for i in range(n)), where
            a0[i] are pairwise coprime and a[i]%a0[i] == 0 for i in range(n)
    """
    l = gcdlcmFI(*a)[1] # LCM of a
    n = len(a); a0 = [{} for _ in range(n)] # prime power factors of l
    for p, e in l.factors.items():
        for i in range(n):
            if (p, e) in a[i].factors.items():
                a0[i][p] = e
                break
    for i in range(n):
        a0[i] = FactoredInteger(prod(p**e for p, e in a0[i].items()), a0[i])
    print("members are FactoredIntegers\n  a:", end = "")
    for f in a:
        print("\t", f.integer, f.factors)
    print("LCM l:\t", l.integer, l.factors)
    print("prime power factors of l are distributed\n  a0:", end = "")
    for f in a0:
        print("\t", f.integer, f.factors)
    S, T = True, True
    for i in range(n):
        T = T and a[i]%a0[i] == 0
        for j in range(i + 1, n): # 0 <= i < j < n
            S = S and gcdlcmFI(a0[i], a0[j])[0] == 1
    print("a0[i] (0 <= i < n) are pairwise coprime:", S)
    for i in range(n):
        print("a[" + str(i) + "]%a0[" + str(i) + "] == ", end = "")
    print("0:", T)
    print("prod(a0[i] for i in range(n)) ==", prod(a0[i] for i in range(n)), \
            "== l:", prod(a0[i] for i in range(n)) == l)
    print()

def doProb11():
    Prob11([FactoredInteger(prod(p**e for p, e in f), dict(f)) \
            for f in randFactLists(Primes, length)])

print("Problem 11")
print("==========")
print("Elements f of list a are FactoredIntegers.")
print("All computation goes on by f.factors of FactoredIntegers.")
print("Show LCM(f for f in a) are divided into parewise coprime factors.")
HitRet()
again(doProb11, 3)

