"""
Primitive Roots and Power Residues.
"""
import csv
from bisect import bisect_left, bisect_right
from nzmath.config import DATADIR
from nzmath.arith1 import product as prod
from nzmath.factor.methods import factor
from nzmath.factor.misc import FactoredInteger

# Only definition is used to get all primitive roots.
def primitiveRootDef(p):
    """
    Input
        p: odd prime
    Output
        R: the increasing list of primitive roots  r  modulo  p, 1 < r < p
    """
    R = []
    for r in range(2, p):
        x = r
        for _ in range(3, p):
            x = x*r%p
            if x == 1: break
        else: R.append(r)
    return R

# Equal to  nzmath.prime.primitive_root(p), which will be removed in future.
def primitive_root(p):
    """
    Input
        p: odd prime with prime factorization of  p - 1  is known
    Output
        i: the least positive primitive root modulo  p
    """
    pd = FactoredInteger(p - 1).proper_divisors()
    for i in range(2, p):
        for d in pd:
            if pow(i, (p - 1)//d, p) == 1: break
        else: return i

# From Takagi's book "Lectures on Elementary Number Theory, pp.61--63."
def primitiveRootTakagi(p, a = 2):
    """
    Input
        p: odd prime
        a: initial integer, 1 < a < p
    Output
        a: primitive root modulo  p.
    """
    x = a; X = {a}
    while x > 1:
        x = x*a%p; X.add(x)
    m = len(X) # X = <a> order m
    while m < p - 1:
        b = min(set(range(1, p)) - X); x = b; n = 1
        while x > 1:
            x = x*b%p; n += 1 # <b> order n
        md, nd = dict(factor(m)), dict(factor(n))
        m0d = {p:md[p] for p in md if p not in nd or md[p] >= nd[p]}
        n0d = {p:nd[p] for p in nd if p not in md or md[p] < nd[p]}
        m0, n0 = prod(p**m0d[p] for p in m0d), prod(p**n0d[p] for p in n0d)
        a = a**(m//m0)%p*b**(n//n0)%p; m = m0*n0; x = a; X = {a}
        while x > 1:
            x = x*a%p; X.add(x)
    return a

def primitiveRoots(N = 1000):
    """
    Input
        N: integer
    Output
        P: the list of  (p, r)  with any odd prime  p <= N  and
           its least positive primitive root  r mod p
    """
    if N < 3: return []
    l = (N + 1)>>1; m = int(.5*N**.5 + .5); P = []; T = [False] + [True]*(l - 1)
    for i in range(1, l):
        if T[i]:
            p = (i<<1) + 1
            if i <= m: T[i*p + i:l:p] = [False]*((l - 1 - i)//p + 1 - i)
            for r in range(2, p):
                x = r
                for _ in range(3, p):
                    x = x*r%p
                    if x == 1: break
                else:
                    P.append((p, r)); break
    return P

def primitiveRoots2(N = 1000):
    """
    Input
        N: integer
    Output
        P: the list of  (p, r)  with any odd prime  p <= N  and
           its least positive primitive root  r mod p
    """
    if N < 3: return []
    l = (N + 1)>>1; m = int(.5*N**.5 + .5); P = []; T = [False] + [True]*(l - 1)
    for i in range(1, l):
        if T[i]:
            p = (i<<1) + 1
            if i <= m: T[i*p + i:l:p] = [False]*((l - 1 - i)//p + 1 - i)
            pd = FactoredInteger(p - 1).proper_divisors()
            for r in range(2, p):
                for d in pd:
                    if pow(r, (p - 1)//d, p) == 1: break
                else:
                    P.append((p, r)); break
    return P

def primitiveRootPW_(p, r):
    """
    Input
        p: odd prime
        r: primitive root modulo  p
    Output
        PW_ = [r**I%p for I in range((p-1)>>1)]: half of numeric list of powers
    """
    if p < 5: return [1]
    q = p>>1; PW_ = [1, r] + [-1]*(q-2); x = r
    for i in range(2,q):
        x = x*r%p; PW_[i] = x
    return PW_

def primitiveRootPW(p, r, PW_):
    """
    Input
        p: odd prime
        r: primitive root modulo  p
        PW_ = [r**I%p for I in range((p-1)>>1)]: half of numeric list of powers
    Output
        PW = [r**I%p for I in range(p-1)]: numeric list of powers
    """
    if p < 5: return [1,2]
    PW = PW_ + [p-1, p-r]
    for i in range(2,p>>1): PW.append(p - PW_[i])
    return PW

def primitiveRoot0PW(p, r):
    """
    Input
        p: odd prime
        r: primitive root modulo  p
    Output
        PW = [r**I%p for I in range(p-1)]: numeric list of powers
    """
    if p < 5: return [1, 2]
    q = p>>1; PW = [1, r] + [-1]*(q-2); x = r
    for i in range(2,q):
        x = x*r%p; PW[i] = x
    PW = PW + [p-1, p-r]
    for i in range(2,p>>1): PW.append(p - PW[i])
    return PW

def primitiveRootIX(p, r, PW):
    """
    Input
        p: odd prime
        r: primitive root modulo  p
        PW = [r**I%p for I in range(p-1)]: numeric list of powers
    Output
        IX = [Ind(N) for N in range(1,p)]: numeric list of indices
        functions  Ind(N)  and  Pow(I)
    """
    IX = [-1]*(p-1)
    for I in range(p-1): IX[PW[I] - 1] = I
    def Ind(N): return IX[N%p - 1]
    def Pow(I): return PW[I%(p-1)]
    return IX, Ind, Pow

def primitiveRootGet(l, u = 0):
    """
    The least positive primitive root  r  of odd prime  p
    Refers database table in the file  primitiveRoots.csv
    Upper bound restrictions 1000000 and 999983 depend on the database size
    Input
        u: u == 0  or  0 < u <= 1000000
        l: 0 < l <= 999983  when  u == 0  or  0 < l <= u <= 1000000
    Output
        u == 0 ==> (p, r)  s.t.  p = min(prime >= l)
        u >= l ==> [(p, r)  s.t.  l <= p <= u]
    """
    R = DATADIR + '/primitiveRoots.csv'
    with open(R) as f: D = [(int(d[0]), int(d[1])) for d in csv.reader(f)]
    P = [D[i][0] for i in range(len(D))]; l = bisect_left(P, l)
    if u: return D[l:bisect_right(P, u)]
    else: return D[l]

def primitiveRootPWGet(l, u = 0):
    """
    Power table  PW  of the least positive primitive root  r  of odd prime  p
    Refers database table in the file  primitiveRootPW_.csv
    Upper bound restrictions 2000 and 1999 depend on the database size
    Input
        u: u == 0  or  0 < u <= 2000
        l: 0 < l <= 1999  when  u == 0  or  0 < l <= u <= 2000
    Output
        u == 0 ==> (p, r, PW)   s.t.  p = min(prime >= l)
        u >= l ==> [(p, r, PW)  s.t.  l <= p <= u]
    """
    S_ = DATADIR + '/primitiveRootPW_.csv'
    with open(S_) as f: D = [[int(i) for i in d] for d in csv.reader(f)]
    P = [D[i][0] for i in range(len(D))]; l = bisect_left(P, l)
    if u: return [(d[0],d[1],primitiveRootPW(d[0],d[1],d[2:]))
                    for d in D[l:bisect_right(P,u)]]
    else: return (D[l][0],D[l][1],primitiveRootPW(D[l][0],D[l][1],D[l][2:]))


