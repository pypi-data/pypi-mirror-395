"""
Numerical Tables
"""
import csv
from nzmath.config import DATADIR
from nzmath.prime import \
    eratosthenes, generator_eratosthenes, generator_eratosthenes_
from nzmath.residue import primitiveRootGet
from utils import HitRet

print("\n|=================================================================|")
print("|                                                                 |")
print("|                       Numerical Tables                          |")
print("|                                                                 |")
print("|There are two types of tables here.  One is lists of input/output|")
print("|data values of computations.  Another is functions which can make|")
print("|tables of the first type and may not contain any data values.  We|")
print("|think such software will increase importance much more than data.|")
print("|                                                                 |")
print("|=================================================================|\n")

print("type 1: list of computed data // type 2: function creating type 1 table")

print("\nCONTENTS -------------------------------")
print("1.  Table of Prime Numbers")
print("2.  Table of Indices for Primitive Roots")
print("----------------------------------------\n")
HitRet()

print("1.  Table of Prime Numbers")
print("--------------------------")
print("Here we always denote  N  to be a positive integer!")
HitRet()

print("(1) The function  nzmath.prime.eratosthenes(N)  is the top of tables.")
print("Refined Eratosthenes Sieve (sec04d.py) is a function  eratosthenes(N)")
print("which gives the list  P  of primes up to  N.  Say  N = 100, then  P")
P = eratosthenes(100); print(f"    == {P[:15]}\n        + {P[15:]}.")
print("Hence  eratosthenes(N)  made up tables of prime numbers, so itself is")
print("a second type table.  Two more functions  generator_eratosthenes_(N)")
print("and  generator_eratosthenes(N)  do similarly in  nzmath.prime.  Namely")
print("list(generator_eratosthenes_(N)) == list(generator_eratosthenes(N)) ==")
print("eratosthenes(N)  for  N > 1.  No limit on  N  theoretically.")
HitRet()

print("(2) In our textbook, for every prime  p, 100 < p < 1000, one primitive")
print("root  r  modulo  p  is given, and a table of pairs  (p, r)  is printed.")
print('Later in "2. Table of Indices for Primitive Roots" (sect2.py), we will')
print("see data of indices modulo  p  for the case  2 < p < 100, which means") 
print("r  appears together, too, as  r == N  with  Ind(N) = 1.")
HitRet()

print("(3) For general  N > 2, we make a list of  (p, r)  with odd prime  p")
print("not exceeding  N  and its least positive primitive root  r  modulo  p.")
print("(i) Function type table  nzmath.residue.primitiveRoots(N = 1000)  makes")
print("the list of  (p, r)  for any  N > 2  theoretically with no restriction.")
print("Another function  nzmath.residue.primitiveRoots2(N=1000)  do the same.")
print("(ii) As table database, file  R = DATADIR + '/primitiveRoots.csv'")
R = DATADIR + '/primitiveRoots.csv'; print(" "*16, "==", R)
print("keeps numerical results by  primitiveRoots(1000000).")
print("We show the last 10 data in the file.")
with open(R) as f:L=[(int(l[0]), int(l[1])) for l in csv.reader(f)]
print(L[-10:-5]);print("+", L[-5:])
HitRet()

print("<*> nzmath.residue.primitiveRootGet(l, u = 0)  helps you to read the")
print("data", end = ""); D = primitiveRootGet(123, 193)
print(f"like this:  primitiveRootGet(123, 193)==\n{D[:7]}\n+{D[7:]}.")
HitRet()
print("<**> For these examples, time performance is verified that using (ii)")
print("is better than computing by  nzmath.residue.primitive_root(p)  etc.")
HitRet()


