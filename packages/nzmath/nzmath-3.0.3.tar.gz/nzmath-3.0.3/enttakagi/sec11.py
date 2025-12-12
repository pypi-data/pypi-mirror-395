"""
Primitive Roots, Indices (Discrete Log)
"""
from random import randint, choice
from itertools import combinations as comb
from nzmath.arith1 import inverse
from nzmath.equation import e1_ZnZ
from nzmath.factor.methods import factor
from nzmath.gcd import lcm_, gcd_
from nzmath.prime import generator_eratosthenes, randPrime
from nzmath.residue import primitive_root, primitiveRootDef, primitiveRootTakagi
from nzmath.residue import primitiveRoot0PW as full
from nzmath.residue import primitiveRootIX as etc
from utils import HitRet

primeUB = 100 # upper bound of primes

print("\n==== 1.  Primitive Roots ======================================")
print("By Fermat's theorem, for prime  p > 0  and  a != 0 (mod p), we")
print("have  a**(p-1) == 1 (mod p).  If  a**e != 1 (mod p)  for any")
print("e, 0 < e < p-1, we say  a  is a primitive root modulo  p.")
print("===============================================================")

HitRet()

print("Table of Primitive Roots")
print("========================")
print("We give all primitive roots  mod p  for small  p's.\n")
P = list(generator_eratosthenes(primeUB)); P[:1] = []
S = {p:primitiveRootDef(p) for p in P}
for p in P:
    l = len(S[p]); m = 5; n = 25
    print(f"p = {p} ==> the list of all  {l}  primitive roots", end="")
    if l < m:
        print('    [' + ','.join(str(S[p][i]) for i in range(l)) + ']')
    else:
        if l < n:
            print('    [' + ','.join(str(S[p][i]) for i in range(m)) + ',')
            print('     ' + ','.join(str(S[p][i]) for i in range(m, l)) + ']')
        else:
            print('    [' + ','.join(str(S[p][i]) for i in range(m)) + ',')
            print('     ' + ','.join(str(S[p][i]) for i in range(m, n)) + ',')
            print('     ' + ','.join(str(S[p][i]) for i in range(n, l)) + ']')

HitRet()

print("Existence of Primitive Roots")
print("============================")
print("Takagi gives a constructive proof of the existence of primitive roots.")
print("It is summarized as a Python function 'cyclotomic.primitiveRootTakagi'")
print("implemented in NZMATH.  You understand its algorithm by reading the")
print("next example together:")

HitRet()

print("Example")
print("=======")
print("For  p = 41, we are going to find a primitive root  a  modulo  p.  Put")
print("I = {1, ..., p-1}  and let  o(x) = min({i for i in I if x**i%p == 1})")
print("for any integer  x  with  GCD(p, x) == 1.")
print("    p = 41; I = set(range(1, p))")
print("    def o(x): return min({i for i in I if x**i%p == 1})")
p = 41; I = set(range(1, p))
def o(x): return min({i for i in I if x**i%p == 1})
print("We search  a  with  o(a) == p-1 == 40.  Let  a = min(I - {1}) == 2")
print("be the first candidate.  Compute  X = {a**i%p for i in I}.  Then  X ==")
print("{1, 2, 4, 5, 8, 9, 10, 16, 18, 20,",
            "21, 23, 25, 31, 32, 33, 36, 37, 39, 40}")
print("and  m = o(a) == len(X) == 20.  Since  m < p-1, we cannot take  a  to")
print("be a primitive root modulo  p.  Hence let  b = min(I - {1} - X) == 3")
print("and compute  n = o(b) == 8.")
print("    a = min(I - {1}); X = {a**i%p for i in I}; m = o(a)")
a = min(I - {1}); X = {a**i%p for i in I}; m = o(a)
print("    b = min(I - {1} - X); n = o(b)")
b = min(I - {1} - X); n = o(b)
print("Take divisors  m0  of  m  and  n0  of  n  so that  l = LCM(m, n) == 40")
print("== m0*n0  with  GCD(m0, n0) = 1 (Sec.4_Prob.11), then  m0 = 5, n0 = 8.")
print("Let now  a**(m//m0)*b**(n//n0)%p  be new  a  again.  Then  o(a) ==")
print("m0*n0 == 40  for  a == 2**(20//5)*3**(8//8)%41 == 16*3%41 == 7.  Hence")
print("a == 7  is a primitive root modulo  p == 41.")
print("    m0 = 5; n0 = 8; a = a**(m//m0)*b**(n//n0)%p")
m0 = 5; n0 = 8; a = a**(m//m0)*b**(n//n0)%p; print(f"a, o(a) == {a}, {o(a)}")

HitRet()

print("Theorem 1.27")
print("============")
print("For prime  p, there exists a primitive root  r  modulo  p, and")
print("        [r**k%p for k in range(p-1)]")
print("is a list of reduced representatives modulo  p.\n")
for _ in range(5):
    p = choice(P); r = primitiveRootTakagi(p, p-1)
    print(f"p = {p}, then  r = {r}  and representatives are"); x, X = 1, [1]
    for _ in range(p - 2):
        x = x*r%p; X.append(x)
    print(X); print()

print("Remark")
print("======")
print("For prime  p, the exponent (multiplicative order) of  r**k  modulo  p")
print("is  (p-1)/GCD(k, p-1), where  r  is a primitive root modulo  p.\n")
def o(x): return min({i for i in range(1, p) if pow(x, i, p) == 1})
for _ in range(5):
    p = choice(P); r = primitiveRootTakagi(p); k = randint(0, p - 2)
    print(f"p,r,k = {p,r,k}, the exponent of  r**k == {r}**{k}  is  {o(r**k)}")
    print(f"        while  (p-1)//GCD(k, p-1) == {(p-1)//gcd_(k, p-1)}")

HitRet()

print("Compare Several Methods")
print("=======================")
print("respectively by definition, by Takagi and by factoring  p - 1.\n")
for p in [randPrime(3) for _ in range(20)]:
    x, y, z = primitiveRootDef(p)[randint(0, 2)], \
        primitiveRootTakagi(p, randint(2, 5)), primitive_root(p)
    print(f"p = {p}, then  {x}, {y}, {z}  are primitive roots mod  p")

HitRet()

print("\n==== 2.  Index Table ==== Bijection via Index =================")
print("For prime  p  and primitive root  r  modulo  p, the index map")
print("    Ind: Z - pZ --> Z; r**al == a --> al == Ind(a)")
print("induces a bijection  (Z/p)* --> Z/(p-1)  between two residues.")
print("===============================================================")

HitRet()

print("We generalize the computation of the textbook as a program.")
print("Take and fix a prime number  p  and a primitive root  r  modulo  p.")
p=choice([7,11,13,17,19,23]); r=primitiveRootTakagi(p,randint(2,p-1))
print(
'    p=choice([7,11,13,17,19,23]);r=primitiveRootTakagi(p,randint(2,p-1))')
print(f"prime  p == {p}, primitive root  r == {r}  modulo  p.\n")

print("Do the following preparation in advance:")

IX = [-1]*(p-1); x = r; PW = [1, r]
for _ in range(2,p-1):
    x = x*r%p; PW.append(x) # PW == [r**I%p for I in range(p-1)]
for I in range(p-1): IX[PW[I] - 1] = I # IX[r**I%p-1]=I
def Ind(N): return IX[N%p - 1]
def Pow(I): return PW[I%(p-1)]

print('    IX = [-1]*(p-1); x = r; PW = [1, r]')
print('    for _ in range(2,p-1):')
print('        x = x*r%p; PW.append(x)')
print('    for I in range(p-1): IX[PW[I] - 1] = I')
print('    def Ind(N): return IX[N%p - 1]')
print('    def Pow(I): return PW[I%(p-1)]')

print("Then we can utilize the facts bellow in our computation:")
print("    r**I==N (mod p) <==> Ind(N)==I (mod p-1) <==> Pow(I)==N (mod p)")
print("    PW==[r**I%p for I in range(p-1)],",
                    "IX==[Ind(N) for N in range(1,p)]")
print("    Pow(I) == PW[I%(p-1)], Ind(N) == IX[N%p -1]")
print("We may also use the next tables  N-->I=Ind(N)  and  I-->N=Pow(I):")
print("-"*(3*p+6)); print(" "*7+"N|{:>2}".format(1),end="")
for i in range(2,p): print("|{:>2}".format(i),end="")
print("|"); print("Ind(N)=I|{:>2}".format(IX[0]),end="")
for i in range(1,p-1): print("|{:>2}".format(IX[i]),end="")
print("|"); print("-"*6+"--+"*p); print(" "*7+"I|{:>2}".format(0),end="")
for i in range(1,p-1): print("|{:>2}".format(i),end="")
print("|"); print("Pow(I)=N|{:>2}".format(PW[0]),end="")
for i in range(1,p-1): print("|{:>2}".format(PW[i]),end="")
print("|"); print("-"*(3*p+6))
print("===============================================================")
print("By this preparation, every computation of index  Ind(N)  or its")
print("inverse  Pow(I)  will be obtained only by looking tables above.")
print("Or, you may be able to quote data in the lists  IX  and  PW.")
print("===============================================================")
HitRet()

print("Example")
print("=======")
print(f"prime  p == {p}, primitive root  r == {r}  modulo  p.")
i = randint(10, 50); n = 0
while not n%p: n = randint(100, 200)
#n = 100; i = 9
print(f"constants  n == {n}, i == {i}.")

HitRet()

print(f"1)  Compute  Ind(n)==Ind(n%p)==Ind({n%p})"+
                f"(==IX[{n%p-1}])=={IX[n%p-1]}  use  IX  or by table.")
print(f"2)  Compute  Ind(-1)==Ind(p-1)==Ind({p-1})"+
                f"=={IX[p-2]}  use  IX  or by table.")
print(f"3)  Solve Ind(N)==i, N==Pow(i%(p-1))"+
                f"==Pow({i%(p-1)})=={PW[i%(p-1)]}  use  PW  or by table.")
print(f"4)  Solve Ind(N)==-1, N==Pow(-1%(p-1))"+
                f"==Pow({-1%(p-1)})=={PW[-1%(p-1)]}  use  PW  or by table.")

HitRet()

print("Theorem 1.28")
print("============")
print("Let  p  be a prime and  r  be a primitive root modulo  p.  Then the")
print("above bijection  Ind: (Z/p)* --> Z/(p-1)  is a homomorphism, so is an")
print("isomorphism from multiplicative to additive order p-1 cyclic groups.\n")

a, b, n = 0, 0, randint(2,9)
while not a*b%p: a, b = randint(-primeUB,primeUB), randint(-primeUB,primeUB)
print(f"p,r = {p},{r}; a,b,n = {a},{b},{n} ==>"); iab=Ind(a)+Ind(b)
print(f"    Ind(a*b)==Ind({a*b})==Ind({a*b%p})=={Ind(a*b)} (mod {p-1})")
print(f"    Ind(a)+Ind(b)==Ind({a})+Ind({b})=={iab%(p-1)} (mod {p-1})")
print(f"    Ind(a*b)==Ind(a)+Ind(b) (mod p-1) is {Ind(a*b)==iab%(p-1)}")
print(f"    Ind(a**n)==Ind({a**n})=={Ind(a**n)} (mod {p-1})")
print(f"    n*Ind(a)=={n}*Ind({a})=={n*Ind(a)%(p-1)} (mod {p-1})")
print(f"    Ind(a**n)==n*Ind(a) (mod p-1) is {Ind(a**n)==n*Ind(a)%(p-1)}")

print("\nFor every  p, a table of  Ind(N) (0 <= N <= p - 1) is an index table.")
print("There is an index table for odd primes  p < 1000  by Jacobi-Cunningham.")
HitRet()

print("Examples 1, 2, 3")
print("================")
print("Notatons and assumptions being as above, we continue computation.")
a,b,c,d,e,f,g=randint(2,p-1),randint(1,p-1),randint(3,p-1),randint(2,p-1),\
        randint(1,p-1),randint(1,p-1),randint(1,p-1); D=(f*f+4*e*g)%p
while Ind(d)%c or (p-1)%c: c,d=randint(3,p-1),randint(2,p-1)
while D==0 or Ind(D)&1:
    e,f,g=randint(1,p-1),randint(1,p-1),randint(1,p-1); D=(f*f+4*e*g)%p
#a>1,b>0,c>2,d>1,e>0,f>0,g>0;Ind(d)%c==(p-1)%c==0;D=(f*f+4*e*g)%p>0,Ind(D)&1==0
#a, b, c, d, e, f, g = 11, 5, 3, 5, 5, 3, 10

HitRet()
print(f"prime  p == {p}, primitive root  r == {r}  modulo  p.")
print(f"a == {a}, b == {b}, a*b%p > 0.\n")

print(f"E1) Solve  a*x == b (mod p)  <==>  {a}*x == {b} (mod {p}).")
print("  Usually we solve the diophantine equation  a*u + p*v == 1, get")
print("the inverse  u  of  a  modulo  p, a*u == 1 (mod p), and obtain the")
print("answer  x = b*u (mod p).  For example, NZMATH can realize it by the")
print("function 'equation.e1_ZnZ([b,-a],p)' but call 'gcd.extgcd(a,p)' still.")
print(f"Then  x == e1_ZnZ([b,-a],p)[1][0] == {e1_ZnZ([b,-a],p)[1][0]}.")
print("  If we may apply the 'index table' (or the computed lists  PW, IX),")
print("we can solve this problem as follows without extended GCD algorithm:")
print("    Ind(a)+Ind(x)==Ind(b), Ind(x)==Ind(b)-Ind(a) (mod p-1).")
print("    x==Pow(Ind(b)-Ind(a))==PW[(IX[b%p-1]-IX[a%p-1])%(p-1)]")
print(f"     ==PW[(IX[{b%p-1}]-IX[{a%p-1}])%{(p-1)}]"+
            f"==PW[({IX[b%p-1]}-{IX[a%p-1]})%{(p-1)}]"+
            f"==PW[{(IX[b%p-1]-IX[a%p-1])}%{(p-1)}]"+
            f"==PW[{(IX[b%p-1]-IX[a%p-1])%(p-1)}]"+
            f"=={PW[(IX[b%p-1]-IX[a%p-1])%(p-1)]} (mod p).")
x = PW[(IX[b%p - 1] - IX[a%p -1])%(p-1)]
print(f"Really  a*x=={a}*{x}%{p}=={a*x%p}=={b%p}==b (mod {p}).")

HitRet()
print(f"prime  p == {p}, primitive root  r == {r}  modulo  p.")
print(f"c == {c}, d == {d}, c*d%p > 0, Ind(d)%c == (p-1)%c == 0.\n")

print(f"E2) Solve  x**c == d (mod p)  <==>  x**{c} == {d} (mod {p}).")
print("  Solve the equivalent index equation  c*Ind(x) == Ind(d) (mod p-1).")
print("We may apply the above quoted NZMATH function  e1_ZnZ, but we shall")
print(f"directly treat this.  Since  c=={c}  divides  Ind(d)=={Ind(d)}  and")
print(f"p-1=={p-1}, holds  Ind(x) == Ind(d)//c (mod (p-1)//c).  By mod p-1,")
print(f"holds  Ind(x) == Ind(d)//c + i*(p-1)//c for i in range(c) (mod p-1).")
X = [Pow((Ind(d)//c)%((p-1)//c) + i*((p-1)//c)) for i in range(c)]
print(f"So  X = [Pow((Ind(d)//c)%((p-1)//c) + i*((p-1)//c)) for i in range(c)]")
print(f"is the list of solutions")
print(f"    X == {X} (mod {p}).\nReally for x in X:")
for x in X:
    print(f"    x**c-d == {x**c-d} == {(x**c-d)//p}*{p} == (x**c-d)//p*p")
    if (x**c - d)%p:
        raise RuntimeError(f"x**c==d (mod p), (x,c,d,p)={(x,c,d,p)}")

HitRet()
print(f"prime  p == {p}, primitive root  r == {r}  modulo  p.")
print(f"e,f,g=={e,f,g}, e*f*g%p>0, D=(f**2+4*e*g)%p=={D}>0, Ind(D)&1==0.\n")

print(f"E3) Solve e*x**2+f*x-g == 0 (mod p)"+
        f"<==>{e}*x**2+{f}*x-{g} == 0 (mod {p}).")
print(f"  All job will be done by the 'index table' or the lists  IX, PW.")
s = Pow(p-1 - Ind(e)); t = f*s%p; u = g*s%p; T = Pow(p-1 - Ind(-2)); v = T*t
print(f"Since  p > 2  and  D  is non-zero square, this has 2 distinct roots.")
print(f"Multiply the both sides of equation by  s = Pow(p-1 - Ind(e)) == {s},")
print(f"i.e. the inverse of e mod p.  The equation is x**2 + t*x - u == 0")
print(f"(mod p) now, and is monic, where  t = f*s%p == {t}, u = g*s%p == {u}.")
print(f"Let  T  be the inverse of  -2  mod p, namely  -2*T == 1 (mod p), and")
print(f"put v=T*t=={v}.  Then (x - v)**2 == v**2 + u (mod p), so 2*Ind(x - v)")
print(f"== Ind(v**2 + u) (mod p-1).  Further  Ind(x - v) == Ind(v**2 + u)//2")
print(f"or Ind(v**2 + u)//2 + (p-1)//2 (mod p-1).  Consequently, we obtained")
print(f"x - v == Pow(Ind(v**2 + u)//2)  or  Pow(Ind(v**2 + u)//2 + (p-1)//2)")
print(f"(mod p).  So, x == {Pow(Ind(v**2 + u)//2) + v}  or  "+
                f"{Pow(Ind(v**2 + u)//2 + (p-1)//2) + v} (mod p).",end="  ")
X = [(Pow(Ind(v**2 + u)//2) + v)%p, (Pow(Ind(v**2 + u)//2 + (p-1)//2) + v)%p]
print(f"Finally, x == {X[0]} or {X[1]} (mod {p}).")
print(f"Actually  {e}*{X[0]}**2 + {f}*{X[0]} - {g} "+
        f"== {(e*X[0]**2 + f*X[0] - g)%p}, {e}*{X[1]}**2 + {f}*{X[1]} - {g} "+
        f"== {(e*X[1]**2 + f*X[1] - g)%p} (mod {p}).\n")

HitRet()

print("=================================================================")
print("Let us numerically verify Problems 1, 2, 3, 4, 5 by functions in")
print("module nzmath.residue.  They are written by reading this section.")
print("=================================================================")

HitRet()

print("Problem 1")
print("=========")
print("p: odd prime, r: primitive root mod p  ==>  Ind(-1) == (p-1)>>1.")
print("(Solution) We may show that  r**((p-1)>>1)%p==p-1.")

print("F=[]\nfor p in P:\n    for r in S[p]:\n        Ind = etc(p, r, full(p, r))[1]\n        if Ind(-1)!=(p-1)>>1: F.append((p,r))")
F=[]
for p in P:
    for r in S[p]:
        Ind = etc(p, r, full(p, r))[1]
        if Ind(-1)!=(p-1)>>1: F.append((p,r))
print(f"There are  {len(F)}  errors for  p < {primeUB}.")

HitRet()

print("Problem 2")
print("=========")
print("p: odd prime, a + b == p  ==>  Ind(a) - Ind(b) == (p-1)>>1 (mod p-1).")
print("(Solution) We may say that  Ind(a) - Ind(p-a) == (p-1)>>1 (mod p-1).")
print("Of course, we can suppose  a, b  are indivisible by  p.")

print("F=[]\nfor p in P:\n    for r in S[p]:\n        Ind = etc(p, r, full(p, r))[1]\n        for a in range(1, p):\n            if (Ind(a)-Ind(p-a)-((p-1)>>1))%(p-1): F.append((p,r,a))")
F=[]
for p in P:
    for r in S[p]:
        Ind = etc(p, r, full(p, r))[1]
        for a in range(1, p):
            if (Ind(a)-Ind(p-a)-((p-1)>>1))%(p-1): F.append((p,r,a))
print(f"There are  {len(F)}  errors for  p < {primeUB}.")

HitRet()

print("Problem 3")
print("=========")
print("p: odd prime, r, s: primitive roots mod p, t = Ind_s(r)  ==>")
print("base change.  Ind_s(a) == t*Ind_r(a) (mod p-1).")
print("(Solution) We may say that  (Ind_s(a) - t*Ind_r(a))%(p-1) == 0.")

print("F=[]\nfor p in P:\n    for r, s in comb(S[p], 2):\n        Ind_r=etc(p,r,full(p,r))[1]; Ind_s=etc(p,s,full(p,s))[1]; t=Ind_s(r)\n        for a in range(1, p):\n            if (Ind_s(a)-t*Ind_r(a))%(p-1): F.append((p,r,a))")
F=[]
for p in P:
    for r, s in comb(S[p], 2):
        Ind_r=etc(p,r,full(p,r))[1]; Ind_s=etc(p,s,full(p,s))[1]; t=Ind_s(r)
        for a in range(1, p):
            if (Ind_s(a)-t*Ind_r(a))%(p-1): F.append((p,r,a))
print(f"There are  {len(F)}  errors for  p < {primeUB}.")

HitRet()

print("Problem 4")
print("=========")
print("p: odd prime, k: integer, k%(p-1)!=0 ==> (1**k+2**k+...+(p-1)**k)%p==0")
print("(Solution) We may say that  sum(i**k for i in range(p))%p == 0.")

print("F=[]\nfor p in P:\n    for k in range(1, p-1):\n            if (sum(i**k for i in range(p)))%p: F.append((p,r,a))")
F=[]
for p in P:
    for k in range(1, p-1):
            if (sum(i**k for i in range(p)))%p: F.append((p,r,a))
print(f"There are  {len(F)}  errors for  p < {primeUB}, k in range(1, p-1).")

HitRet()

print("Problem 5")
print("=========")
print("(Wilson's Theorem) p: prime ==> factorial (p-1)! == -1 (mod p).")
print("(Solution) By taking  Ind  of the both sides, we may say that")
print("(sum(Ind(i)for i in range(1,p))-((p-1)>>1))%(p-1)==0 (Problem 1).")

print("F=[]\nfor p in P:\n    for r in S[p]:\n        Ind=etc(p,r,full(p,r))[1]\n        if (sum(Ind(i)for i in range(1,p))-((p-1)>>1))%(p-1): F.append((p,r,a))")
F=[]
for p in P:
    for r in S[p]:
        Ind=etc(p,r,full(p,r))[1]
        if (sum(Ind(i)for i in range(1,p))-((p-1)>>1))%(p-1): F.append((p,r,a))
print(f"There are  {len(F)}  errors for  p < {primeUB}.")

HitRet()

print("\n==== 3.  Power Residues ======================================")
print("For prime  p  and primitive root  r  modulo  p, the index map")
print("    Ind: Z - pZ --> Z; r**al == a --> al == Ind(a)")
print("induces a bijection  (Z/p)* --> Z/(p-1)  between two residues.")
print("This leads us to the theory of power residues of  p.")
print("===============================================================")

HitRet()

print("Theorem 1.29")
print("============")
print("p:prime, a in range(1,p), n in range(p-1), e=GCD(n,p-1), f=(p-1)//e.")
print("    x**n == a (mod p)  solvable <==> a**f == 1 (mod p).")
print("(Proof) Taking index, we may verify")
print("    n*Ind(x) == Ind(a) (mod p-1) solvable <==> f*Ind(a)%(p-1)==0.")
print("By Theorem 1.13, we may show")
print("    Ind(a)%e==0 <==> f*Ind(a)%(p-1)==0.")
print("F=[]\nfor p in P:\n    r = choice(S[p])\n    for n in range(p-1):\n        for a in range(1,p):\n            Ind=etc(p,r,full(p,r))[1];e=gcd_(n,p-1);f=(p-1)//e\n            if (Ind(a)%e==0)!=(f*Ind(a)%(p-1)==0): F.append((p,r,n,a))")
F=[]
for p in P:
    r = choice(S[p])
    for n in range(p-1):
        for a in range(1,p):
            Ind=etc(p,r,full(p,r))[1];e=gcd_(n,p-1);f=(p-1)//e
            if (Ind(a)%e==0)!=(f*Ind(a)%(p-1)==0): F.append((p,r,n,a))
print(f"{len(F)}  errors for  p < {primeUB}, n in range(p-1), a in range(1,p).")

print("\nRemark")
print("======")
print("If solvable, the number of solutions is  e = GCD(n,p-1) (Theorem 1.13).")

HitRet()

print("Definition")
print("==========")
print('For a prime  p, n >= 0, an integer  a  is an "n-th power residue"')
print('(or a "non-residue") of  p  when the conguence  x**n == a  (mod p) is')
print("solvable (or not solvable), respectively.")

HitRet()

print("Comments")
print("========")
print("[[0]] The integer  a == 0  is always an n-th power residue for any  n.")
print("[[1]] The 0-th power residue can occur only for  a == 1, n == 0.")
print("[[2]] Except [[0]], we can restrict  n in range(p-1), a in range(1,p).")
print("[[3]] Then the set of n-th power residue of  p  is given as follows:")

while True:
    print("\n((Example))  Ctrl+C to stop repeating the loop."); HitRet()
    p = choice(P); r = choice(S[p]); Ind=etc(p,r,full(p,r))[1]
    n = choice(range(p-1)); e = gcd_(n, p-1)
    nPR = set(a for a in range(1,p) if Ind(a) in range(0,p-1,e))
       # a = 1,2,...< p  with  Ind(a) = 0,e,2*e,...< p-1 (Theorem 1.29)
    nPR_ = set(x**n%p for x in range(1,p)) # n-th power residues (definition)
    print(f"p = {p}, n = {n}, e = GCD(n,p-1) == {e}")
    print("nPR = set(a for a in range(1,p) if Ind(a) in range(0,p-1,e)) ==")
    print(nPR); print("nPR_ = set(x**n%p for x in range(1,p))")
    print(f"Total {(p-1)//e} power residues  nPR == nPR_ is {nPR == nPR_}")

