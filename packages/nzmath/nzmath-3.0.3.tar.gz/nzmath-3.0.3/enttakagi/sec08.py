"""
Euler's Function  phi(n)
"""
from random import randint, sample, random
from itertools import product
from math import floor
from nzmath.arith1 import floorsqrt
from nzmath.arith1 import product as prod
from nzmath.combinatorial import combinationIndexGenerator as C
from nzmath.factor.misc import allDivisors
from nzmath.gcd import gcd, extgcd
from nzmath.multiplicative import euler, moebius
from nzmath.prime import randPrime, generator_eratosthenes, nextPrime
from utils import HitRet

size = 100 # maximum data size, positive integer
length = 10 # maximum data length, positive integer

print()
print("===============================================================")
print("Among natural numbers  1, 2, ..., n, let  phi(n)  be the number")
print("of numbers  x  relatively prime to  n.  In Python, we can write")
print("    def phi(n):return len({x for x in range(1,n+1)if gcd(x,n)==1})")
print("as a function.  Then, by a program")
print('    for n in range(1,6):print("phi({})={}".format(n,phi(n)),end=", ")')
print('    print("phi(6)={}, ...".format(phi(6)));n=randint(1001,2345)')
print('    print("phi({})={}, ...".format(n, phi(n)))')
print("we get")

def phi(n):return len({x for x in range(1, n + 1) if gcd(x, n) == 1})

print("    ", end = "")
for n in range(1, 6): print("phi({})={}".format(n, phi(n)), end = ", ")
print("phi(6)={}, ...".format(phi(6))); n = randint(1001, 2345)
print("    phi({})={}, ...".format(n, phi(n)))
print("Moreover we can actually get")
print("Example")
print("=======")
for n in range(1, 7):
    X={x for x in range(1, n + 1) if gcd(x, n) == 1}
    print("\tphi({}) == {},\t(x in {})".format(n, phi(n), X))
print("\t  **************************")

HitRet()

print("We call it arithmetic (number theoretic) function such a function")
print("defined over (positive) integers.  Especially, above  phi(n)  is")
print("Euler's (totient) function.")
print("=================================================================")
print("If  p  is a prime, then  phi(p**e) == p**e - p**(e - 1)  as below.\n")
for _ in range(5):
    p, e = randPrime(randint(1, length//4)), randint(1, length//3)
    print("prime p = {}, e = {}, phi(p**e) == {} == p**e - p**(e - 1) {}"\
        .format(p, e, phi(p**e), phi(p**e) == p**e - p**(e - 1)))
HitRet()

Thm1_18 = euler

print("Theorem 1.18")
print("============")
print("If prime factorization of  n == prod(p**e for p, e in factorlist),")
print("then phi(n) == n*prod((1 - 1/p) for p, e in factorlist).\n")
for _ in range(5):
    n = randint(1, size**(length//4))
    print("n = {}, phi(n) by def. {} == {} by Thm1_18, same? {}"\
        .format(n, phi(n), Thm1_18(n), phi(n) == Thm1_18(n)))

HitRet()

def Thm1_19(a, b, x, y):
    """
    Input
        a, b: coprime integers  > 0
        x, y: integer residues
    Output
        z: integer residue  z == x (mod a), z == y (mod b), 0 <= z < a*b
    """
    return (x + a*((y - x)*extgcd(a, b)[0]%b))%(a*b)

print("Theorem 1.19")
print("============")
print("For coprime integers  a > 0, b > 0,  holds  phi(a*b) == phi(a)*phi(b).")
print("Namely Euler's totient is a multiplicative arithmetic function.\n")
print("Example of Theorem 1.19")
print("=======================")
print("By CRT (Thm1_14), residues  x, y  modulo  a, b  uniquely correspond")
print("to the residue  z  modulo  a*b  so that  z==x (mod a), z==y (mod b).")
print("The map from  x, y  to  z = f(a, b, x, y)  is given by"); f = Thm1_19
print("\n    def f(a,b,x,y):return(x+a*((y-x)*extgcd(a,b)[0]%b))%(a*b)")
for a, b, X, Y in [(3, 5, [1, 2], [1, 2, 3, 4]),\
        (8, 15, [1, 3, 5, 7], [1, 2, 4, 7, 8, 11, 13, 14]),\
        (5, 9, [1, 2, 3, 4], [1, 2, 4, 5, 7, 8])]:
    HitRet()
    print("\ta="+str(a)+"\tb="+str(b)+"\tab="+str(a*b)+"\tphi(a)="+\
        str(phi(a))+", phi(b)="+str(phi(b))+", phi(ab)="+str(phi(a*b)))
    print("\tx", "\ty", "\tz")
    for x,y in product(X,Y):print("\t"+str(x)+"\t"+str(y)+"\t"+str(f(a,b,x,y)))

HitRet()

def Phi(x, A):
    """
    Input
        x: positive real (upper bound)
        A: list of pairwise coprime natural numbers
    Output
        the number of natural numbers  n <= x, n%a != 0 for a in A
    """
    l = len(A)
    return floor(x) + sum((-1)**k*sum(floor(x/prod(A[i[j]] \
            for j in range(k))) for i in C(l, k)) for k in range(1, l + 1))

def Phi_def(x, A):
    """
    Input
        x: positive real (upper bound)
        A: list of pairwise coprime natural numbers
    Output
        the number of natural numbers  n <= x, n%a != 0 for a in A
    """
    x1 = floor(x) + 1; P = set(range(1, x1))
    for a in A:
        P -= set(range(a, x1, a))
    return len(P)

Primes = list(generator_eratosthenes(size//2))

print("Problem 1")
print("=========")
print("Generalize phi(n) to functions Phi(x, A) and Phi_def(x, A) for")
print("floating real x and pairwise coprime integer list A.  Let us")
print("check Phi(x, A) == Phi_def(x, A) and, if A consists of prime")
print("divisors of n, then Phi(n, A) == phi(n).  For the definitions")
print("of Phi(n, A) and Phi_def(n, A), see the source code in this")
print("file sec08.py.")

HitRet()

for _ in range(5):
    x = size**length
    while x > floor(size**(length/2.7)):
        A = sample(Primes, randint(1, length//2))
        f = [(p, randint(1, length//3)) for p in A]
        n = prod(p**e for p, e in f); x = randint(n, n + n)
    print("x = {}, A = {}".format(x, A))
    print("Phi(x, A) == {} == Phi_def(x, A) {}"\
        .format(Phi(x, A), Phi(x, A) == Phi_def(x, A)))
    print("factorlist {}, n = {}".format(f, n))
    print("Phi(n, A) == {} == phi(n) {}".format(Phi(n, A), Phi(n, A) == phi(n)))
    print()

def Thm1_20(n):
    """
    Input
        n: positive integer
    Print
        sum(phi(d)  for all divisors  d  of n) == n
    """
    D = allDivisors(n)
    S = sum(phi(d) for d in D)
    print("n ==", n)
    print("phi(1)", end="")
    for d in D[1:]:
        print("+phi({})".format(d), end="")
    print("\n== 1", end="")
    for d in D[1:]:
        print("+{}".format(phi(d)), end="")
    print("\n== {} == n {}\n".format(S, S == n))

print("Theorem 1.20")
print("============")
print("The sum of  phi(d)  for all divisors  d  of  n  is equal to  n.")

HitRet()

print("Example of Theorem 1.20")
print("=======================")
n = 15; D = allDivisors(n)
S = sum(phi(d) for d in D); print("\nn ==", n)
print("\td\tphi(n/d)\tx  such that  GCD(x, n) == d")
for d in D:
    print("\t"+str(d)+"\t"+str(phi(n//d))+"\t\t", end="")
    for x in range(1, n + 1):
        if gcd(x, n) == d:
            print(str(x)+", ", end="")
    print()
print("\t\tsum", n)
print("phi(1)", end="")
for d in D[1:]:
    print("+phi({})".format(d), end="")
print(" == 1", end="")
for d in D[1:]:
    print("+{}".format(phi(d)), end="")
print(" == {} == n {}".format(S, S == n))
HitRet()
for _ in range(5):
    Thm1_20(randint(1, size**(length//3)))

print("Example of Theorem 1.22")
print("=======================")
print("For any arithmetic function  F(n), put")
print("\t\tG(n) = sum(F(d) for all divisors  d  of  n).  Then")
print("n = 15, d==1, 3, 5, 15.  Hence")
print("\tF(1)                ==G(1),")
print("\tF(1)+F(3)           ==G(3),")
print("\tF(1)     +F(5)      ==G(5),")
print("\tF(1)+F(3)+F(5)+F(15)==G(15),")
print("F(1)==G(1),F(3)==G(3)-G(1),F(5)==G(5)-G(1),F(15)==G(1)-G(3)-G(5)+G(15).")

HitRet()

mu = moebius

print("Moebius function")
print("================")
print("mu(1) = 1, mu(n) = (-1)**k  for squarefree  n  with just  k  distinct")
print("prime divisors and m(n) = 0  otherwise.\n")

print("Example of Moebius function")
print("===========================")
for n in range(1, 7):
    print("mu({})={},".format(n, mu(n)), end="")
n = randint(size, size*size); print("...mu({})={},...\n".format(n, mu(n)))

def Thm1_21(n):
    """
    Input
        n: integer > 1
    Print
        sum(mu(d)  for all divisors  d  of n) == 0
    """
    D = allDivisors(n)
    S = sum(mu(d) for d in D)
    print("\nn ==", n)
    print("mu(1)", end="")
    for d in D[1:]:
        print("+mu({})".format(d), end="")
    print("\n== 1", end="")
    for d in D[1:]:
        if mu(d) < 0:
            print("{}".format(mu(d)), end="")
        else:
            print("+{}".format(mu(d)), end="")
    print("\n== {} == 0 {}".format(S, S == 0))

print("Theorem 1.21")
print("============")
print("For  n > 1, the sum of  mu(d)  for all divisors  d  of  n  is  0.")
HitRet()
for _ in range(5):
    Thm1_21(randint(1, size**(length//3)))

HitRet()

print("Example of Theorem 1.22 (again)")
print("===============================")
print("For any arithmetic function  F(n), put")
print("\t\tG(n) = sum(F(d) for all divisors  d  of  n).  Then")
print("n = 15, d==1, 3, 5, 15.  Hence")
print("\tF(1)                ==G(1),")
print("\tF(1)+F(3)           ==G(3),")
print("\tF(1)     +F(5)      ==G(5),")
print("\tF(1)+F(3)+F(5)+F(15)==G(15),")
print("F(1)==G(1),F(3)==G(3)-G(1),F(5)==G(5)-G(1),F(15)==G(1)-G(3)-G(5)+G(15).")
print()
print("Theorem 1.22")
print("============")
print("If  G(n) = sum(F(d)  for all divisors  d  of  n), Moebius inversion")
print("formula  F(n) == sum(mu(n//d)*G(d)  for all divisors  d  of  n) holds.")
HitRet()
r=random()
def nx(n): return nextPrime(nextPrime(n))**(0.5*(1 + r))
def pol(n): return n**3 - 15*n + 1/3
for F, f in [(phi, "Euler"), (mu, "Moebius"), (nx, "next prime related"), \
                (floorsqrt, "floorsqrt"), (pol, "cubic polynomial")]:
    print(f, "function F(n) and G(n)=sum(F(d)d|n).")
    def G(n): return sum(F(d) for d in allDivisors(n))
    n = randint(size*length, size**(length//3))
    muGn, Fn = sum(mu(n//d)*G(d) for d in allDivisors(n)), F(n)
    print("n = {}, sum={}, F(n)={}, same {}.\n"\
            .format(n, muGn, Fn, muGn == Fn))

