"""
Introduction to Solving Congruences (continued)
"""

from random import randint, choice
from nzmath.arith1 import CRT_
from nzmath.arith1 import product as prod
from nzmath.equation import allroots_ZnZ
from nzmath.gcd import modl
from nzmath.prime import generator_eratosthenes
from nzmath.poly.uniutil import IntegerPolynomial
from nzmath.rational import IntegerRing
from utils import HitRet, again, allroots_ZnZ_def, randmodPolyList, \
                    printPoly, randFactLists

size = 100 # maximum data size, positive integer
length = 10 # maximum data length, positive integer

print()
print("===============================================================")
print("It is not easy to study the case (ii) of Theorem 1.16.  We next")
print("give an example as a problem, which is important in elementary")
print("number theory.  The number  p = 2  is a special prime and is a")
print("singular point in rational number theory.  We must care that.")
print("===============================================================")
HitRet()

def Prob1(N, a, x0):
    """
    Input
        N: integer, N >= 0
        a: integer, a == 1 (mod 8)
        x0: odd integer
    Output
        x: integer list, x[0] == x0, len(x) == N + 1
        For n = 0, ..., N, congruence  x[n]**2 == a (mod 2**(n + 3)),
            -2**(n + 2) + x[n], -x[n], x[n], 2**(n + 2) - x[n]
        are all solutions of X**2 == a (mod 2**(n + 3)) (0 < x[n] < 2**(n + 1))
    Print
        x[n]**2 == a (mod 2**(n + 3)) (0 <= n <= N)
    """
    if (a - 1)%8 or (x0 - 1)&1:
        raise ValueError("a == {} == 1 (mod 8)?  x0 == {} odd?".format(a, x0))
    z = [x0, -x0, x0 + 4, -x0 + 4]
    z = [modl(z[i], 8) for i in range(4)]
    x = [min([z[i] for i in range(4) if z[i] > 0])]
    print("x[{}]**2 == {}**2 == {} == a == {} (mod 2**{} == {})"\
            .format(0, x[0], modl(x[0]**2, 8), modl(a, 8), 3, 8))
    for n in range(N + 1):
        if (x[n]**2 - a)%2**(n + 4):
            z = [2**(n + 2)]*4; z[2] += 2**(n + 3); z[3] += 2**(n + 3)
            z = [z[i] + (-1)**i*x[n] for i in range(4)]
        else:
            z = [(-1)**i*x[n] for i in range(4)]
            z[2] += 2**(n + 3); z[3] += 2**(n + 3)
        z = [modl(z[i], 2**(n + 4)) for i in range(4)]
        for X in z:
            if modl(X**2 - a, 2**(n + 4)):
                raise RunTimeError("{}**2 != a (mod 2**{})".format(X, n + 3))
        x.append(min([z[i] for i in range(4) if z[i] > 0]))
        print("x[{}]**2 == {}**2 == {} == a == {} (mod 2**{} == {})"\
                .format(n + 1, x[n + 1], modl(x[n + 1]**2, 2**(n + 4)), \
                modl(a, 2**(n + 4)), n + 4, 2**(n + 4)))
    print("solution list  x =", x)
    print()
    return x

def doProb1():
    N = randint(2, length-4); a = randint(-size, size)*8 + 1
    x0 = randint(-size, size)*2 - 1; print("(N, a, x0) = ", (N, a, x0))
    print("solve  X**2 == {} (mod 2**{})  with initial solution  X = {} ."\
            .format(a, N + 3, x0))
    Prob1(N, a, x0)

print("Problem 1")
print("=========")
print("We are going to solve quadratic residue problem modulo a power of  2.")
print("Starting from  X**2 == a (mod 2**3), we shall solve congruence  X**2")
print("== a (mod 2**(n + 3)) for a given integer  a == 1 (mod 2**3) .")
print("We give one solution  x[n]  but there are four solutions bellow:")
print("\t-2**(n + 2) + x[n], -x[n], x[n], 2**(n + 2) - x[n] .")
HitRet()
again(doProb1)

Thm1_17 = allroots_ZnZ

Primes = list(generator_eratosthenes(size))

def e1_17(f, m):
    f = IntegerPolynomial(f, IntegerRing()); M = prod(p**a for p, a in m)
    printPoly(f); print(", m = {}, solve  f(x) == 0 (mod m)".format(M))
    print("factorlist of  m  is  [(p, a)] ==", m); fm, res = Thm1_17(f, m)
    fm = set(fm); print("Solutions for each  p, a")
    for i in range(len(m)):
        print("\tp, a = {}, {}:  total  {}  solutions in  {}"\
                    .format(m[i][0], m[i][1], len(res[i]), set(res[i])))
    return f, M, fm

def doThm1_17():
    f = randmodPolyList(size, 2*length//5)
    f = {i:f[i] for i in range(len(f)) if f[i]}
    m = choice(randFactLists(Primes, 2*length//5)); f, M, fm = e1_17(f, m)
    for al in fm:
        if f(al)%M:
            raise RuntimeError("x = {} is not a solution.".format(al))
    print("The solution set  S = {} .".format(fm))
    allroots = allroots_ZnZ_def(f, M, 10)
    if allroots == None:
        print("Skip direct computation by timeout!")
    else:
        allroots = set(allroots)
        print("Directly computed solutions in  {}, the same as  S  is  {} ."\
                .format(allroots, allroots == fm))
    print()

print("Theorem 1.17")
print("============")
print("Congruences of composite modulo  m  are reduced to those of modulo")
print("prime power  p**a  by CRT (Theorem 1.14).  They are further reduced")
print("to those of modulo prime  p  by Hensel lift (Theorem 1.16).  Then")
print("the case of modulo  p  is studied as equations of field coefficients")
print("polynomials.  We can apply several tools of such ring including the")
print("theory of Euclidean domain.  We have given the process as a function.")
HitRet()
again(doThm1_17, 7)

print("Theorem 1.17 Example")
print("====================")
print("In Theorem 1.15 Remark, we solved  x**2 == 1 (mod 12)  by digital")
print("method (Karatsuba).  We now solve it by applying Theorem 1.17.")
print("We also give three more examples with interesting results.\n")
for f, m in [({0:-1, 2:1}, [(2, 2), (3, 1)]),\
        ({0:20, 1:7, 2:-13}, [(3, 1), (7, 3)]),\
        ({0:-6, 1:8, 2:18, 3:38, 4:28, 5:-25}, [(41, 1), (29, 2)])]:
    f, M, fm = e1_17(f, m); print("Solutions by Theorem 1.17 ", fm)
    print("Directly computed in ", set(allroots_ZnZ_def(f, M)))
    print("They are the same set!"); HitRet()
f = {0:42, 1:-11, 2:-16}; m = [(53, 3), (83, 3)]; f, M, fm = e1_17(f, m)
for al in fm:
    if f(al)%M:
        raise RuntimeError("x = {} is not a solution.".format(al))
print("Total {} solutions in  S =\n{} .\n".format(len(fm), fm))

