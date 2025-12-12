"""
Congruences
"""
from random import randint
from nzmath.arith1 import expand
from nzmath.gcd import gcd_
from nzmath.intresidue import IntegerResidueClass as IntResC
from utils import HitRet, again, strInt

size = 100 # maximum data size, positive integer
length = 10 # maximum data length, positive integer

print("============================================================")
print("Congruence implies equality in the residue class ring modulo")
print("some positive integer m.  In nzmath.intresidue, there exists")
print("IntegerResidueClass --- IntResC in short --- realizing it.")
print("============================================================")
HitRet()

def CongEquiv(m, a, b, c):
    """
    Input
        m, a, b, c: integers, m > 0, a == b == c (mod m)
    Print
        IntResC(a, m) == IntResC(a, m)
        IntResC(a, m) == IntResC(b, m) ==> IntResC(b, m) = IntResC(a, m)
        IntResC(a, m) == IntResC(b, m), IntResC(b, m) == IntResC(c, m)
                                    ==> IntResC(a, m) == IntResC(c, m)
    """
    print("modulus m =", m, end = ",")
    if m <= 0:
        raise ValueError("Positive modulus m is required.")
    print("    (a, b, c) = ({}, {}, {})".format(a, b, c))
    A, B, C = IntResC(a, m), IntResC(b, m), IntResC(c, m)
    print("A, B, C = IntResC(a, m), IntResC(b, m), IntResC(c, m)")
    print("A == A ?", A == A)
    print("A == B ?", A == B, "==> B == A ?", B == A)
    print("A == B, B == C ?", A == B and B == C, "==> A == C ?", A == C)
    print()

def doCongEquiv():
    m = randint(1, size)
    a, b, c = (randint(-size*length, size*length) for _ in range(3))
    while (a - b)%m:
        b = randint(-size*length, size*length)
    while (b - c)%m:
        c = randint(-size*length, size*length)
    CongEquiv(m, a, b, c)

print("congruence is equivalence.")
print("==========================")
print("We can check reflexive, symmetric, transitive laws.\n")
again(doCongEquiv)

def SysRes_eg():
    """
    Print
        several examples of systems of residues modulo 7
    """
    print("systems of residues modulo 7")
    print("============================")
    print("There are many kinds of systems of residues as below.")
    m = 7; print("modulus m =", m)
    S = set(range(m)); R = set(range(-m, 0))
    print("S = set(range(m)); R = set(range(-m, 0))")
    T = {3**i for i in range(m - 1)}; T.add(0)
    print("T = {3**i for i in range(m - 1)}; T.add(0)")
    U = {(-1)**i*2**j for i in range(2) for j in range(3)}; U.add(m)
    print("U = {(-1)**i*2**j for i in range(2) for j in range(3)}; U.add(m)")
    print("S ==", S, "the least non-negative residues modulo m")
    print("T ==", T); print("U ==", U); print("R ==", R)
    print("S == {n%m for n in T} == {n%m for n in U} == {n%m for n in R} is", \
            S == {n%m for n in T} == {n%m for n in U} == {n%m for n in R})

SysRes_eg()
HitRet()

def Thm1_11(m, a, b, c, d):
    """
    Input
        m, a, b, c, d: integers, m > 0, a == b, c == d (mod m)
    Print
        IntResC(a + c, m) == IntResC(b + d, m)
        IntResC(a - c, m) == IntResC(b - d, m)
        IntResC(a*c, m) == IntResC(b*d, m)
    """
    if m <= 0:
        raise ValueError("Positive modulus m is required.")
    print("modulus m =", m, end = ", ")
    print("(a, b, c, d) =", (a, b, c, d), "a == b, c == d (mod m)")
    A1, S1, P1 = IntResC(a + c, m), IntResC(a - c, m), IntResC(a*c, m)
    A2, S2, P2 = IntResC(b + d, m), IntResC(b - d, m), IntResC(b*d, m)
    print("IntResC(a + c, m) == IntResC({}, m) == {}".format(a + c, A1))
    print("IntResC(b + d, m) == IntResC({}, m) == {}".format(b + d, A2))
    print("    IntResC(a + c, m) == IntResC(b + d, m) is", A1 == A2)
    print("IntResC(a - c, m) == IntResC({}, m) == {}".format(a - c, S1))
    print("IntResC(b - d, m) == IntResC({}, m) == {}".format(b - d, S2))
    print("    IntResC(a - c, m) == IntResC(b - d, m) is", S1 == S2)
    print("IntResC(a*c, m) == IntResC({}, m) == {}".format(a*c, P1))
    print("IntResC(b*d, m) == IntResC({}, m) == {}".format(b*d, P2))
    print("    IntResC(a*c, m) == IntResC(b*d, m) is", P1 == P2)
    print()

def doThm1_11():
    m = randint(1, size*length)
    a, b, c, d = (randint(-size*length, size*length) for _ in range(4))
    while (a - b)%m:
        b = randint(-size*length, size*length)
    while (c - d)%m:
        d = randint(-size*length, size*length)
    Thm1_11(m, a, b, c, d)

print("Theorem 1.11")
print("============")
print("Addition, subtraction and multiplication are determined modulo m.")
print("Hence addition IntResC(a, m) + IntResC(c, m) = IntResC(a + c, m)")
print("is well defined, and subtraction or multiplication also.  Further")
print("multiplication is commutative, so it is a commutative ring Z/mZ.")
print("Any polynomial of integer coefficients is evaluated modulo m.")
HitRet()
again(doThm1_11, 4)

def Thm1_12(m, a, b, c):
    """
    Input
        m, a, b, c: integers, m > 0, a*c = b*c (mod m)
    Print
        a = b (mod (m//GCD(c, m)))
    """
    if m <= 0:
        raise ValueError("Positive modulus m is required.")
    d = gcd_(c, m); M = m//d
    print(
        "m = {}, (a, b, c) = ({}, {}, {}), d = GCD(c, m) == {}, M = m//d == {}"\
            .format(m, a, b, c, d, M))
    print("a*c == {} == {} == {} == {} == b*c (mod {})"\
            .format(a*c, a*c%m, b*c%m, b*c, m))
    print("==> a == {} == {} == {} == {} == b (mod {}) is {}"\
            .format(a, a%M, b%M, b, M, a%M == b%M))
    if d > 1 and a%m != b%m:
        print("    Actually a == {} == {} != {} == {} == b (mod {})"\
            .format(a, a%m, b%m, b, m))
    print()

def doThm1_12():
    m = randint(1, size)
    a, b, c = (randint(-size*length, size*length) for _ in range(3))
    while (a*c - b*c)%m:
        b = randint(-size*length, size*length)
    Thm1_12(m, a, b, c)

print("Theorem 1.12")
print("============")
print("Division is possible by integers relatively prime to the modulo m.")
print("For integers not coprime to m, reduction of modulus is required.\n")
again(doThm1_12, 10)

size = 200 # maximum data size, positive integer
length = 20 # maximum data length, positive integer

def Prob1(a):
    """
    Input
        a: integer, a > 0
    Print
        congruence residue computation by addition/subtraction of digits
        applied moduli are 9, 11, 7 and 13
    """
    print("a =", a)

    A = a; print("   %9:", end = "")
    while A > 9:
        A_ = expand(A, 10); A = sum(A_)
        print("\ta == sum({}) == {} (mod 9)".format(strInt(A_, 45), A))
    print("\ta%9 == {} or {} by decimal or direct method.  Same? {}"\
                .format(A%9, a%9, A%9 == a%9))

    s, A = 1, a; print("  %11:", end = "")
    while A > 9:
        A_ = expand(A, 10); A = s*(sum(A_[::2]) - sum(A_[1::2]))
        s = (A >= 0) - (A < 0); A = abs(A)
        print("\ta == {} (mod 11)".format(s*A))
    print("\ta%11 == {} or {} by decimal or direct method.  Same? {}"\
                .format((s*A)%11, a%11, (s*A)%11 == a%11))

    s, A = 1, a; print("7or13:", end = "")
    while A > 999:
        A_ = expand(A, 1000); A = s*(sum(A_[::2]) - sum(A_[1::2]))
        s = (A >= 0) - (A < 0); A = abs(A)
        print("\ta == {} (mod 7) and (mod 13)".format(s*A))
    print("\ta%7 == {} or {} by decimal or direct method.  Same? {}"\
                .format((s*A)%7, a%7, (s*A)%7 == a%7))
    print("\ta%13 == {} or {} by decimal or direct method.  Same? {}"\
                .format((s*A)%13, a%13, (s*A)%13 == a%13))
    print()

def doProb1():
    Prob1(randint(1, size**length))

print("Problem 1")
print("=========")
print("Divisibility criterion mod 9, 11, 7 and 13 compare with direct method.")
print("Congruence residue computation by addition/subtraction of digits.\n")
Prob1(26384)
Prob1(25683941)
again(doProb1, 2)

