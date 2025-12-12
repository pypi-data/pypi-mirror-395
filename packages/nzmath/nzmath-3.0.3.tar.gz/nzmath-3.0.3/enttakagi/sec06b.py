"""
Congruences of Degree One (cotinued)
"""

from random import randint
from nzmath.arith1 import product as prod
from nzmath.gcd import gcd, lcm, extgcd, lcm_
from utils import HitRet, again

size = 100 # maximum data size, positive integer
length = 5 # maximum data length, positive integer

print()
print("===============================================================")
print("Generalizing the CRT, we are going to consider the congruences")
print("with non-coprime moduli.  In such cases, we should take care of")
print("solvability conditions.")
print("===============================================================")
print()

def Prob1(m, n, a, b):
    """
    Input
        m, n: moduli, integers, > 0
        a, b: integers
    d = GCD(m, n), l = LCM(m, n)
    (*) x == a (mod m), x == b (mod n)
    Print
        a != b (mod d) ==> (*) has no solution
        a == b (mod d) ==> solution of (*) unique mod l
    """
    d = gcd(m, n); l = lcm(m, n)
    print("(m, n, a, b) =", (m, n, a, b), "==> (d, l) ==", (d, l))
    q, r = divmod(b - a, d); print("a ", end = "")
    if r:
        print("!= b (mod d) so x != a (mod m) or x != b (mod n)")
    else:
        x = (a + m*q*extgcd(m//d, n//d)[0])%l
        print("== b (mod d), x = {}, x == a (mod m) {}, x == b (mod n) {}"\
                .format(x, not((x - a)%m), not((x - b)%n)))
    print()

def doProb1():
    m, n = randint(1, size), randint(1, size)
    a, b = \
        randint(-size*length, size*length), randint(-size*length, size*length)
    Prob1(m, n, a, b)

print("Problem 1 and its Example")
print("=========================")
print("For moduli m, n, let d = GCD(m, n), l = LCM(m, n).  For integers a, b,")
print("simultaneous congruences x == a (mod m), x == b (mod n) is solvable if")
print("and only if a == b (mod d), and then the solution is unique modulo l.")
HitRet()
Prob1(15, 21, 4, 10)
again(doProb1, 9)

def Prob2(m, a):
    """
    Input
        m: list of integers > 0 as moduli
        a: list of integers
    n = len(m) == len(a) > 1
    (*) x == a[h] (mod m[h]) (h in range(n))
    Output x
        x == None if (*) has no solution
        x: solution of (*) unique mod LCM(m[h] for h in range(n))
    """
    n = len(m); M, A = m[0], a[0]
    for h in range(1, n):
        N, B = m[h], a[h]; d = gcd(M, N)
        q, r = divmod(B - A, d)
        if r:
            return None
        l = lcm(M, N); M, A = l, (A + M*q*extgcd(M//d, N//d)[0])%l
    return A

def doProb2():
    n = randint(2, length); m = [randint(1, size) for _ in range(n)]
    a = [randint(-size*length, size*length) for _ in range(n)]
    print("x == {} ({})".format(a[0], m[0]), end = "")
    for h in range(1, n):
        print(", == {} ({})".format(a[h], m[h]), end = "")
    A = Prob2(m, a)
    print("\nmoduli product == {}, LCM == {}".format(prod(m), lcm_(*m)))
    if A == None:
        for h in range(n):
            for k in range(h + 1, n):
                mhk = gcd(m[h], m[k]); ah, ak = a[h], a[k]
                if (ah - ak)%mhk:
                    print("  h, k = {}, {} then a[h] == {} != {} == a[k] ({}),"\
                            .format(h, k, ah%mhk, ak%mhk, mhk),\
                            "where {} == GCD({}, {})".format(mhk, m[h], m[k]))
    else:
        print("  x == {} ({})".format(A, lcm_(*m)), end = "    ")
        print("Really x == a[h] (m[h]) (0 <= h < n)?  ", \
                    all(not((A - a[h])%m[h]) for h in range(n)))
    print()

print("Problem 2")
print("=========")
print("We write here the congruence C == D (mod M) shortly as C == D (M).")
print("For list m of moduli, let n = len(m), l = LCM(m[h] for h in range(n)).")
print("For list a of n integers, simultaneous congruences x == a[h] (m[h])")
print("(0 <= h < n) is solvable if and only if a[h] == a[k] (GCD(m[h], m[k]))")
print("(0 <= h < k < n), and then the solution is unique modulo l.")
HitRet()
again(doProb2, 9)

print("Remark on Total Ring of Fraction")
print("================================")
print("For an integer m > 1, let ZmZ be the residue class ring of integers")
print("modulo m, and S be the set of residues represented by an integer a with")
print("GCD(a, m) == 1.  Then S is the set of non-zero divisors of ZmZ and the")
print("ring of fraction ZmZ_S is the total ring of fraction.  So ordinary way")
print("of expressing formula by fraction is possible:")
print("(a/b) + (c/d) == (a*d + b*c)/(b*d)", end =", ")
print("(a/b)*(c/d) == (a*d + b*c)/(b*d) (mod m)\n")

