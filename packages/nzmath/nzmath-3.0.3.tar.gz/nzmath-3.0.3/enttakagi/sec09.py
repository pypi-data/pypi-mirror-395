"""
Roots of Unity
"""
from random import randint, sample, random, choice
from cmath import exp, pi
from nzmath.gcd import gcd, coprime
from nzmath.multiplicative import euler, moebius; phi, mu = euler, moebius
from nzmath.cyclotomic import cycloPoly, cycloMoebius
from utils import HitRet, again, printPoly, cycloDef
from nzmath.rational import theIntegerRing as IR
from nzmath.poly.uniutil import IntegerPolynomial as IP

size = 100 # maximum data size, positive integer
length = 10 # maximum data length, positive integer

print("==============================================================")
print("For a positive integer  n, there are  n  numbers of  n-th roots")
print("of unity, namely roots of equation  x**n - 1 = 0, which are")
print("\texp(2*k*pi*1j/n) (= cos(2*k*pi/n) + 1j*sin(2*k*pi/n) )")
print("for  k in range(n).  Let  rho  be their list:")
print("\trho = [exp(2*k*pi*1j/n) for k in range(n)].")
print("Among them, the one that is  1  only if raised to the  n-th")
print("power is called a primitive  n-th root of unity.  Let")
print("\ts = set(k for k in range(n) if  rho[k]  is primitive).")
print("Further let  t  be the set of reduced residues modulo  n:")
print("\tt = set(k for k in range(n) if coprime(k, n)).")
print("===============================================================")

HitRet()

print("Theorem 1.23")
print("============")
print("There are  phi(n)  primitive  n-th roots of unity, which are")
print("rho[k]  for reduced residues  k  in range(n), or equivalently")
print("for  coprime(k, n).  Namely  s == t.")

print("Example")
print("=======")
print("Let  w = 3**(1/2).  Then the sixth roots of unity are")
print("\t1, -1, (-1 ± w*1j)/2, (1 ± w*1j)/2,")
print("of which  1**1 == 1, (-1)**2 == 1, ((-1 ± w*1j)/2)**3 == 1  and only")
print("the last two are primitive sixth roots of unity.")

HitRet()

for _ in range(5):
    n = randint(length//2, size*length//4)
    s = set(range(1, n)) - \
            set(k for k in range(1, n) for i in range(1, n) if not i*k%n)
    t = set(k for k in range(1, n) if coprime(k, n))
    print(f"\nn = {n}, then the  {phi(n)}  primitive roots of unity  s = {s}")
    if s != t:
        raise RuntimeError("s  or  t  is wrong!")

HitRet()

print("Cyclotomic Polynomials and Coefficients")
print("=======================================")
print("The Polynomial  Fn(x) = (x - z[1])* ... *(x - z[m]), where  z[1], ...,")
print("z[m]  are the  m = phi(n)  numbers of primitive  n-th roots of unity,")
print("is the  n-th cyclotomic polynomial.  As we know explicit  z[i]  above")
print("and  Fn  is monic integer coefficients by Theorem 1.24 below, we can")
print("numerically compute the  n-th cyclotomic polynomia  Fn_ = cycloDef(n)")
print("as an integer polynomial of degree  m.  If  n  becomes large, however,")
print("approximation error accumulate, hence correct answer is not obtained.")
print("But, we have the following simple recurrence relations:")
print("\tFpn(x) = Fn(x**p)/Fn(x)  if  gcd(p, n) = 1  for prime  p.")
print("\tF2n(x) = Fn(-x)  for odd  n.")
print("\tFn(x) = Fr(x**(n/r))  for the squarefree part (radical)  r  of  n.")
print("From these, we can derive an NZMATH function 'cycloPoly' of computing")
print("assured result  Fn = cycloPoly(n), and compare it with the above  Fn_.")
print("On the other hand, we aware that the coefficients of  Fn  are usually")
print("all very small.  Are they always contained in the set {-2, -1, 0, 1}?")

HitRet()

for n in [randint(1, 70) for _ in range(5)] + [105, 150, 975]:
    Fn_, Fn = cycloDef(n), cycloPoly(n)
    C = set(Fn[_] for _ in range(Fn.degree() + 1))
    print(f"n = {n}, then  Fn_ == Fn  is  {Fn_ == Fn}")
    printPoly(Fn, n = "Fn"); print(f"\nIts coefficients {C}\n")

HitRet()

print("Theorem 1.24")
print("============")
print("There is another formula to write  Fn  only by using multiplications")
print("and divisions of binomials  x**(n/d) - 1  for all divisors  d  of  n.")
print("Write the formula as another NZMATH function 'cycloMoebius', put  Mn =")
print("cycloMoebius(n) and compare to  Fn = cycloPoly(n)  above.")

HitRet()

for _ in range(5):
    n = randint(length//2, size*length//4)
    Fn = cycloPoly(n); Mn = cycloMoebius(n)
    print(f"n = {n}, then Mn == Fn is {Mn == Fn}")
    printPoly(Mn, n = "Mn"); print(); print()

HitRet()

print("Problems 1 and 2")
print("================")
print("Let  Fn  be the n-th cyclotomic polynomial.  Then the constant term")
print("Fn[0] == 1  except  F1[0] == -1  for  n = 1.  Furthermore the 2nd term")
print("coefficient  Fn[m - 1] == -mu(n) == -moebius(n), where  m = phi(n) ==")
print("euler(n).  Note that  Fn  is palindromic, so  F[0] == F[m]  and  F[1]")
print("== F[m - 1].  Indeed:"); HitRet()
for _ in range(5):
    n = randint(length//2, size*length//4)
    F = cycloPoly(n)
    print("n={}".format(n), end = "\t")
    printPoly(F, n = "Fn"); print()
    print("constant of Fn:{}".format(F[0]))
    print("coefficient of x of Fn:{},".format(F[1]), end = " ")
    print("-mu(n)={}\n".format(-moebius(n)))
HitRet(); UB = size*(length//5)
for n in range(2, UB):
    Fn = cycloPoly(n); m = euler(n); mn = moebius(n)
    assert Fn[0] == 1, f"Fn[0] != 1  for  n == {n}"
    assert Fn[m - 1] == -mn, f"Fn[m - 1] != -moebius(n) for  n == {n}"
print("Numerically verified upto  n <", UB)
HitRet()

print("Problem 3")
print("=========")
print("Take a fixed primitive n-th root  z**r  of unity with  r  in range(n),")
print("GCD(r, n) == 1, where  z = exp(2j*pi/n) (Theorem 1.23).  Then the set")
print("{z**(r*k) for k in range(n)}  coincides with  {z**k for k in range(n)},")
print("and the set  {z**(r*k) for k in range(n) if GCD(k, n) == 1}  coincides")
print("with  {z**k for k in range(n) if GCD(k, n) == 1}.  Namely any primitive")
print("n-th root  rho  of unity represents n-th roots of unity by rho**k (0 <=")
print("k < n) and those of primitive ones with  GCD(k, n) == 1.  To see this,")
print("it is enough to show  {r*k%n for k in range(n)} == set(range(n))  and")
print("{r*k%n for k in range(n) if gcd(k, n) == 1} == {k for k in range(n) if")
print("gcd(k, n) == 1}.  We shall see it numerically.  Indeed:")
HitRet(); UB = size*(length//2)
for n in range(1, UB):
    PR = {k for k in range(n) if gcd(k, n) == 1}
    r = choice(list(PR)); R = {r*k%n for k in range(n)}
    Z = set(range(n)); P = {r*k%n for k in range(n) if gcd(k, n) == 1}
    assert R == Z, f"R != Z  for  n == {n}"
    assert P == PR, f"P != PR for  n == {n}"
print("Numerically verified upto  n <", UB)
HitRet()

print("Problem 4")
print("=========")
print("Let  GCD(a, b) == 1, A = set(range(a)), B = set(range(b)) and  AB =")
print("set(range(a*b)).  Put  C = {(y*a + x*b)%(a*b) for x in A for y in B}.")
print("Further let  A_, B_, AB_  be the set of reduced residues in  A, B, AB")
print("modulo  a, b, a*b  respectively and put  C_ = {(y*a + x*b)%(a*b) for x")
print("in A_ for y in B_}.  Then  C == AB  and  C_ == AB_  (Theorem 1.19).  By")
print("taking primitive a-th, b-th roots  za = exp(2j*pi/a), zb = exp(2j*pi/b)")
print("of unity, all a*b-th roots of unity is given by")
print("\tza**x*zb**y == exp(2j*pi*(x*b + y*a)/(a*b)) == zab**(x*b + y*a)")
print("(x in A, y in B)  and  (x in A_, y in B_)  for primitive ones.  We")
print("shall verify numerically  C == AB, C_ == AB_.  Indeed:")
HitRet(); UB = size
for a in range(2, UB):
    for b in range(a + 1, UB):
        if gcd(a, b) > 1:
            continue
        A, B, AB = set(range(a)), set(range(b)), set(range(a*b))
        C = {(y*a + x*b)%(a*b) for x in A for y in B}
        assert C == AB, f"C != AB  for  (a, b) == ({a}, {b})"
        A_, B_, AB_ = {x for x in A if gcd(x, a) == 1},\
           {y for y in B if gcd(y, b) == 1}, {x for x in AB if gcd(x, a*b) == 1}
        C_ = {(y*a + x*b)%(a*b) for x in A_ for y in B_}
        assert C_ == AB_, f"C_ != AB_  for  (a, b) == ({a}, {b})"
print("Numerically verified upto  1 < a < b <", UB)


