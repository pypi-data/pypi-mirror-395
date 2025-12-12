"""
Prime Numbers
"""
from random import randint, choice
from nzmath.arith1 import product as prod
from nzmath.factor.misc import primeDivisors
from nzmath.factor.methods import \
    factor, trialDivision, rhomethod, pmom, mpqs, ecm
from nzmath.prime import primonial
from utils import HitRet, again

size = 100 # maximum data size, positive integer
length = 10 # maximum data length, positive integer

print()
print("=========================================")
print("Variables here are all positive integers.")
print("=========================================")

HitRet()

def Thm1_08(a, m, p):
    """
    Input
        a: non-empty list of positive integers
        m = prod(a): the product of a
        p: prime divisor of m
    Print
        d%p == 0 for some d in a
    """
    print("a ==", a)
    print("m == prod(a) ==", m)
    print("prime divisor p ==", p, "of m")
    for d in a:
        if d%p == 0:
            print("d%p ==", d%p, "for d ==", d, "in a")
            break
    else:
        print("ERROR: none of d in", a, "is divisible by", p)

def doThm1_08():
    m = 1
    while m == 1:
        a = [randint(1, size) for j in range(randint(2, length))]
        m = prod(a)
    p = choice(primeDivisors(m))
    Thm1_08(a, m, p)
    print()

print("Theorem 1.8")
print("===========")
print("For list a of positive integers, let m be the product of all integers")
print("in a.  Then prime divisor p of m surely divides some integer in a.\n")
again(doThm1_08)

print("Remark of Theorem 1.8")
print("=====================")
a = [3, 4]
m = prod(a)
p = 6
Thm1_08(a, m, p)
print("actually because p = 6 == 2*3 is not prime")

HitRet()

def Thm1_09(a):
    """
    Input
        a: integer > 1
    Print
        sorted prime factorlist [(p1, e1), ..., (pn, en)] satisfying
            a == p1**e1 * ... * pn**en,
        checking several other methods give the same list
    """
    print("integer a ==", a); f = factor(a); cf = prod(p**e for p, e in f)
    print("prime factorlist of a is\n  f ==", f)
    print("f gives composite cf ==", cf, "and cf == a is", cf == a)
    print("Trial Division, rho Method, p-1 Method, MPQS, ECM give")
    print("  other prime factorlists ft, fr, fp, fm, fe")
    print("  check f == ft == fr == fp == fm == fe")
    a2, f2 = prod(p**e for p, e in f if p > 2), [(p, e) for p, e in f if p <= 2]
    if a == primonial(67) + 1:
        ft = [(a, 1)]
    else:
        ft = trialDivision(a)
    fr = rhomethod(a); fp = f2 + pmom(a2); fm = mpqs(a); fe = ecm(a)
    for x, y in [(ft, "ft"), (fr, "fr"), (fp, "fp"), (fm, "fm"), (fe, "fe")]:
        if x != f:
            if y == "ft":
                print("  Trial Division skipped", end = "")
            if y == "fp":
                print("  p-1 Method failed", end = "")
            if y == "fm":
                print("  MPQS failed", end = "")
            if y == "fe":
                print("  ECM failed", end = "")
            print("  f !=", y, "==", x)
    HitRet()

length = 5 # maximum data length, positive integer

def doThm1_09():
    Thm1_09(randint(2, size**length))

print("Theorem 1.9")
print("===========")
print("Prime factorization of integer  a > 1  will be tried by several ways.")
print("---------------------------------------------------------------------")
print("They take different techniques of finding divisors of  a  which are")
print("Trial Division, rho method, p-1 method, MPQS and ECM.  Among them,")
print("Trial Division is deterministic but others are probabilistic.  MPQS can")
print("apply only to composite coprime to 2*3*5*7*11*13.  ECM can apply only")
print("to composite coprime to 2*3.  Each has the following weak point.")
print("  Trial Division:  slow if non-trivial divisors of  a  are large")
print("  rho method:  endless if  a  is prime > 3")
print("  p-1 method:  only trivial divisor is found if  a  is 2's power > 3")
print("We compute factorlist  f  of  a  by default method (Trial Division, p-1")
print("method and MPQS in order).  Then compute other factor lists  ft, fr,")
print("fp, fm, fe  of  a  respectively only by Trial Division, only by rho")
print("method, only by p-1 method, only by MPQS, only by ECM.  In that case,")
print("we make some correction to recover weak point of each algorithm.  For")
print("rho method, check the primarity of  a  to recover.  For p-1 method,")
print("split the 2 part of  a  to recover.  However, Trial Division is still")
print("sometimes slow.  We shall skip such slow computation.\n")
print("Further p-1 Method or MPQS fails for other integers by reason unknown.")
print("It is a nature of probabilistic algorithms.\n")
print("Please be patient!  Sometimes computation may take a long time.")
HitRet()
Thm1_09(17**2)
Thm1_09(primonial(67) + 1) # ft slow and seems to be endless, fp fails
Thm1_09(20145664162231) # fp fails
Thm1_09(57692064547540) # fm fails
again(doThm1_09, 10)

print("By Theorem 1.9 above, several expressions of integer n exist.")
print("\tAt first, integer n itself of course.")
print("\tNext, factorlist f = [(p1, e1), ..., (pk, ek)] with")
print("\t\tprime numbers p1, ..., pk and exponents e1, ..., pk")
print("\t\trepresents the prime factorization p1**e1*...*pk**ek.")
print("\tAlso, factordict d = {p1:e1, ..., pk:ek} represents")
print("\t\tthe same prime factorization p1**e1*...*pk**ek.")
print("Transformations among them are as follows:")
print("\tn-->f by f = nzmath.factor.methods.factor(n).")
print("\tn-->d by d = dict(nzmath.factor.methods.factor(n)).")
print("\tf-->n by n = nzmath.arith1.product(p**e for p, e in f).")
print("\td-->n by n = nzmath.arith1.product(p**e for p, e in d.items()).")
print("\tf-->d by d = dict(f).")
print("\td-->f by f = list(d.items()).")
print()

