"""
Numerical Tables (continued)
"""
import csv
from time import perf_counter as time
from nzmath.config import DATADIR
from nzmath.residue import primitiveRoot0PW, primitiveRootPWGet
from utils import HitRet

print("\n2.  Table of Indices for Primitive Roots")
print("----------------------------------------")
print("Here we always denote  'numeric variables'  to be rational integers!")
HitRet()

print("(1) Index calculus of primitive root modulo any odd prime  p  uses data")
print("of its index table.  previous: Jacobi-Cunningham p < 1000 (sec11.py).")
HitRet()

print("(2) Fix one primitive root  r (1 < r < p).  Then")
print("    Z/(p-1)==range(p-1)-->(Z/p)*==range(1,p); I-->r**I%p")
print("is an isomorphism of cyclic groups of order  p-1:")
print("    I == Ind(N) <==> N == r**I%p <==> N == Pow(I)")
print("On index calculus, it is useful to get the values of  Pow(I)  without")
print("computing every time.  It is like to have multiplication table of small")
print("numbers in elementary arithmetic (Japanese 'Kuku').  To get  Ind(N)  is")
print("much harder, therefore it is more useful like to have a division table")
print("in elementary arithmetic.  Index table of  (p, r)  is given numerically")
print("as in the following:")
print("    ------------------------------------")
print("    |    N   | 1 |   2  | ... |   p-1  |")
print("    |--------+---+------+-----+--------|")
print("    |Ind(N)=I| 0 |Ind(2)| ... |Ind(p-1)|")
print("    ------------------------------------")
print("If  p = 11, r = 8, then:"); p = 11; r = 8; IX = [0,7,6,4,8,3,9,1,2,5]
print("    "+"-"*(3*p+7)); print("    |"+"    N   |{:>2}".format(1),end="")
for i in range(2,p): print("|{:>2}".format(i),end="")
print("|"); print("    |"+"-"*8+"+--"*(p-1)+"|")
print("    |Ind(N)=I|{:>2}".format(IX[0]),end="")
for i in range(1,p-1): print("|{:>2}".format(IX[i]),end="")
print("|"); print("    "+"-"*(3*p+7))
HitRet()

print("(3) Our textbook gives two kinds of index tables.  For  2 < p < 50, it")
print("takes a primitive root  r, 1 < r < p, and give an index table as above,")
print("but primitive root  r  itself is given as the  N  with  Ind(N) = 1.")
print("For  50 < p < 100, it gives  r  explicitly, but it now gives  Ind(N)")
print("only when  N  is prime.")
HitRet()

print("(4) For any prime  p > 2  and any primitive root  r, 1 < r < p, modulo")
print("p, let us define functions  Pow(I)  and  Ind(N)  as above, and put")
print("  PW = [Pow(I) for I in range(p-1)], IX = [Ind(N) for N in range(1,p)].")
print("Among these data, we concentrate on  PW  with the highest complexity.")
print("(i) A table creating function for  PW  is  primitiveRoot0PW(p, r)")
print("in module  nzmath.residue.  It evaluates table  PW  with only  (p-5)>>1")
print("multiplications and reductions for  p > 5.  An example of index table:")
print("    p, r = 2003, 5; PW = primitiveRoot0PW(p, r)")
p, r = 2003, 5; PW = primitiveRoot0PW(p, r)
print(f"shows  PW == \
{PW[:5]} + ... +\n    {PW[((p-1)>>1)-5:((p-1)>>1)+5]}\n    + ... + {PW[-5:]}.")
print("(ii) We can easily make global big numeric data of  PW  gathering the")
print("results of  p  by (i).  But, we do not do so.  Since, table size of")
print("PW  for 'all' primes are huge, however we need usually a few (mostly")
print("one) of them which are quickly computable by (i).  On the other hand,")
print("we aware that data size to keep can be half.  Consequently, we create")
print("global numeric data as a csv file S_ for 2 < p < 2000.  It consists of")
print("[p, r] + PW_ with PW_ = [PW[I] for I in range((p-1)>>1)] (half size).")
print("The data file is", end=""); S_ = DATADIR + '/primitiveRootPW_.csv'
print(f"  S_ = DATADIR + '/primitiveRootPW_.csv =='\n          {S_}.")
print("We show the last data from the file!")
with open(S_) as f:F=[d for d in csv.reader(f)];I=[int(i)for i in F[-1]]
print(I[:14]);print('+'+"."*8+'+');print(I[-13:])
HitRet()

print("<*> primitiveRootPWGet(l, u = 0)  in nzmath.residue  helps to read")
print("the data", end = ""); I = primitiveRootPWGet(123)
print("  (p, r, PW)  is like this:  primitiveRootPWGet(123) ==")
print(f"({I[0]}, {I[1]}, {I[2][:6]} + ... + {I[2][-6:]}).")
print("For the last data,", end = ""); I = primitiveRootPWGet(1999)
print("  (p, r, PW)  is:  primitiveRootPWGet(1999) ==")
print(f"({I[0]}, {I[1]}, {I[2][:12]}\n + ....... + \n{I[2][986:999]} \
            + \n{I[2][999:1011]}\n + ........ + \n{I[2][-13:]}).")
HitRet()
print("<**> For these examples, time performance is verified that using (ii)")
print("is better than applying  nzmath.residue.primitiveRoot0PW(p, r).")
HitRet()


