"""
Cyclotomic Polynomials and Related.
"""
from nzmath.factor.methods import factor
from nzmath.factor.misc import allDivisors
from nzmath.multiplicative import moebius as mu
from nzmath.poly.uniutil import IntegerPolynomial as IP
from nzmath.rational import theIntegerRing as IR

def cycloPoly(n):
    """
    Input
        n > 0, integer
    Output
        Fn: the n-th cyclotomic polynomial
    """
    f = dict(factor(n)); e = 0; r = 1; c = {0:-1, 1:1}; F = IP(c, IR)#Fn(x)
    if 2 in f:
        e = f.pop(2)
    for p in f:
        G = IP({p*j:c[j] for j in c}, IR)#Fn(x**p)
        F = G.monic_floordiv(F).normalize()#Fpn(x)=Fn(x**p)/Fn(x) if gcd(p,n)=1
        c = dict(F); r *= p#the squarefree part (radical) of n
    if e:
        for j in c:
            if j&1: c[j] = -c[j]#F2n(x)=Fn(-x) for odd n
        r *= 2#the squarefree part (radical) of n
    return IP({n//r*j:c[j] for j in c}, IR).normalize()#Fn(x)=Fr(x**(n/r))

def cycloMoebius(n):
    """
    Input
        n > 0, integer
    Output
        Fn: the n-th cyclotomic polynomial by Moebius
    """
    D = allDivisors(n); Fn = IP({0:1}, IR); Fd = IP({0:1}, IR)
    for d in D:
        if mu(d) == 1:
            Fn *= IP({0:-1, n//d:1}, IR)
        elif mu(d) == -1:
            Fd *= IP({0:-1, n//d:1}, IR)
    return Fn.monic_floordiv(Fd).normalize()

