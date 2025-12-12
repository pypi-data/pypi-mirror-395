"""
Utilities
"""

from time import perf_counter as time
from random import randint, sample
from math import cos, pi
from nzmath.algorithm import digital_method
from nzmath.arith1 import product as prod
from nzmath.gcd import modl, gcd
from nzmath.poly.uniutil import FieldPolynomial as FP
from nzmath.poly.uniutil import IntegerPolynomial as IP
from nzmath.rational import theIntegerRing as IR
from nzmath.real import theRealField as RF

def HitRet():
    """
    Input
        pause to wait for input a line
    Output
        a blank line
    """
    input('\n\x1b[1mHit Return!\x1b[m'); print()

def again(func, i = 5):
    """
    Input
        func: function to repeat, call in the form  'func()' (no argument)
        i: minimum repeat times, positive integer
    Output
        repeat  func  just  i  times
        ask "Again?"
        if reply is "y" or "Y", repeat func again and go back to ask "Again?"
        else end repeating  func
    """
    if type(i) != int or i <= 0:
        raise ValueError("repeat times  i  is a positive integer")
    while i:
        func(); i -= 1
        if not i:
            i += (input(
            '\n\x1b[1mAgain? ("y"+Return if so, else Return!) \x1b[m') == "y")
            print()

def strInt(n, d = 50):
    """
    Input
        n: integer etc. that str() accept
        d: upper bound of digits, d >= 5
    Output
        string of integer n at most in d digits (without \n)
            if n does not exceed d digits, then str(n) as ordinary
            else upper d - 3 digits of n and '...' are concatenated
    """
    if d < 5:
        raise ValueError("Digits upper bound d >= 5.")
    s = str(n); l = len(s)
    if l <= d:
        return s 
    else:
        return s[-l : d - 3 - l] + 3*'.'

def randFactLists(P, ub, cp = False):
    """
    Input
        P: sequence or set of possible primes p below
        ub: upper bound of len(a), len(f), e below
        cp: pairwise coprime condition for generated integers f
            if cp then len(P) >= ub*ub is required
            else len(P) >= ub is enough
    Output
        a: random list of factorlists f of pairs (p, e) = (prime, exponent)
            if cp then integers correspoding to f are pairwise coprime
    """
    a = []
    if cp:
        P = set(P)
    for _ in range(randint(1, ub)):
        f = sample(P, randint(1, ub))
        if cp:
            P.difference_update(f)
        for k in range(len(f)):
            f[k] = (f[k], randint(1, ub))
        a.append(f)
    return a

def randmodPolyList(m, ub):
    """
    Input
        m: integer, m > 1, moduli, bound of coefficients below
        ub: upper bound of degree  d  below
    Output
        f: random poly_list of degree  d (f[d] != 0)
            with  (2 - m)//2 <= f[i] < (m + 2)//2 (0 <= i <= d)
    """
    ml, mh = (2 - m)//2, m//2; d = randint(1, ub)
    f = [randint(ml, mh) for i in range(d + 1)]
    while f[d] == 0:
        f[d] = randint(ml, mh)
    return f

def printPoly(f, n = "f", v = "x"):
    """
    Input
        f: polynomial  f[0] + f[1]*x + ... + f[d]*x**d  with  f[d] != 0
            maybe an instance of 'polynomial class' or a 'poly_list'
        n: polynomial name
        v: variable name
    Print
        expanded form of f(x)
    """
    if type(f) == list:
        l = len(f)
    else:
        l = f.degree() + 1
    t = f[0] != 0
    if t:
        print("{}({})={}".format(n, v, f[0]), end = "")
    else:
        print("{}({})=".format(n, v), end = "")
    for i in range(1, l):
        if f[i]:
            if f[i] == 1:
                if t:
                    print("+", end = "")
                print(v, end = "")
            elif f[i] == -1:
                print("-" + v, end = "")
            else:
                if t and (f[i] > 0):
                    print("+", end = "")
                print("{}*{}".format(f[i], v), end = "")
            if i > 1:
                print("**{}".format(i), end = "")
            t = True

def lcm_def(*a):
    """
    Input
        a: non-zero integers
    Output
        cm: the set of positive common multiples of a at most abs(prod(a))
        min(cm): the least common multiple of a
    """
    a = {abs(i) for i in a}
    if a == set() or min(a) == 0:
        raise ValueError("Non-zero integers are required.")
    u = prod(a) + 1
    i = a.pop()
    cm = set(range(i, u, i))
    for i in a:
        cm = set.intersection(cm, set(range(i, u, i)))
    return cm, min(cm)

def allDivisors_def(a):
    """
    Input
        a: positive integer
    Output
        the set of positive divisors of a
    """
    if a <= 0:
        raise ValueError("Positive integer is required.")
    sqrta, s = int(a**.5), {1, a}
    for d in range(2, sqrta + 1):
        q, r = divmod(a, d)
        if r == 0:
            s = s | {d, q}
    return s

def gcd_def(*a):
    """
    Input
        a: integers, at least one non-zero
    Output
        cd: the set of positive common divisors of a
        max(cd): the greatest common divisor of a
    """
    a = {abs(i) for i in a if i}
    if a == set():
        raise ValueError("At least one non-zero integer is required.")
    cd = set.intersection(*[allDivisors_def(i) for i in a])
    return cd, max(cd)

def countDivisors_def(a):
    """
    Input
        a: positive integer
    Output
        the number of positive divisors of a
    """
    return len(allDivisors_def(a))

def sumDivisors_def(a):
    """
    Input
        a: positive integer
    Output
        the sum of divisors of a
    """
    return sum(allDivisors_def(a))

def allroots_ZnZ_def(f, n, chk = 0):
    """
    Input
        f: non-zero IntegerPolynomial
        n: integer, n > 1
        chk: number, chk >=0, default  chk == 0
    Timeout check by  chk  seconds when  chk > 0
    apply digital method (Karatsuba)
    Output
        x: list of all  al  in range((2 - n)//2, (2 + n)//2)  if  f(al)%n == 0
        None is returned in case of timeout
    """
    g = [(i, f[i]) for i in range(f.degree(), -1, -1)] # descending ordered
    def h(al):
        return modl(digital_method(g, al, lambda a, b: modl(a + b, n), \
                lambda a, b: modl(a*b, n), lambda i, a: modl(i*a, n), \
                lambda a, i: modl(a**i, n), 0, 1), n)
    if chk:
        x = []; chk += time()
        for al in range((2 - n)//2, (2 + n)//2):
            if h(al) == 0:
                x.append(al)
            if time() > chk:
                return None
        return x
    return [al for al in range((2 - n)//2, (2 + n)//2) if h(al) == 0]

def cycloDef(n):
    """
    Input
        n > 0, integer (valid up to  n < 71)
    Output
        Fn: the n-th cyclotomic polynomial by definition
    """
    if n == 1:
        return IP({0:-1, 1:1}, IR)
    if n == 2:
        return IP({0:1, 1:1}, IR)
    Fn = prod(FP({0:1, 1:-2*cos(2*k*pi/n), 2:1}, RF)\
                for k in range(1, n//2 + 1) if gcd(k, n) == 1)
    return IP({d:round(dict(Fn)[d]) for d in dict(Fn)}, IR).normalize()

