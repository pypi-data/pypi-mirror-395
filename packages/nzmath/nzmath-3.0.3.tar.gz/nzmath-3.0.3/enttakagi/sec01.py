"""
Divisibility of Integers
"""

from random import randint
from nzmath.gcd import divmodl
from utils import HitRet, again

size = 100 # maximum data size, positive integer
length = 10 # maximum data length, positive integer

print()
print("=========================================")
print("When programs are running, they pause and")
print("request you to 'Hit Return!' like now you")
print("are just requested.  You can now continue")
print("after reading the printed messages.(^_^;)")
print("=========================================")

HitRet()

print("=======================================")
print("Do not consider integer multiples of 0.")
print("Hence 0 can be a divisor of no integer.")
print("=======================================")

HitRet()

print("=============================================")
print("After repeated computation several times, you")
print("will be asked 'again (y/N)? ' waiting for key")
print("input to repeat computation once more if your")
print("key input is 'y', otherwise next computation.")
print("=============================================")

HitRet()

def Thm1_01(b, a, x):
    """
    Input
        b: non-zero integer
        a: non-empty list of integer multiples of b
        x: list of integers such that len(x) == len(a)
    Print
        sum([a[i]*x[i] for i in range(len(a))])%b == 0
    """
    print("b ==", b)
    print("a ==", a, "multiple of b")
    print("x ==", x)
    ax = sum([a[i]*x[i] for i in range(len(a))])
    print("sum([a[i]*x[i] for i in range(len(a))])%b == " \
           + str(ax) + "%" + str(b), "==", ax%b, "multiple of b")

def doThm1_01():
    b = 0
    while b == 0:
        b = randint(-size, size)
    n = randint(1, length)
    a = [b*randint(-size, size) for j in range(n)]
    x = [randint(-size, size) for j in range(n)]
    Thm1_01(b, a, x)
    print()

print("Theorem 1.1")
print("===========")
print("Linear form of list a of multiples of integer b is multiple of b.\n")
again(doThm1_01)

Thm1_02 = divmod

def doThm1_02():
    a = randint(-size, size)
    b = randint(1, size)
    q, r = Thm1_02(a, b)
    print("(a, b) ==", (a, b), "then (q, r) ==", (q, r), \
           "a == q*b + r", a == q*b + r, "0 <= r < b", 0 <= r < b)
    print()

print("Theorem 1.2")
print("===========")
print("Any a divided by b > 0 takes quotient q and residue r, 0 <= r < b.\n")
again(doThm1_02)

print("Example of Theorem 1.2")
print("======================")
b = 12
print("b ==", b)
for a in [50, -50, -5]:
    print("a ==", a, "; (q, r) ==", Thm1_02(a, b))
print()

def Thm1_02_rem(a, b):
    """
    Input
        a: integer
        b: positive integer
    Output
        (q, r): pair of integers such that a == q*b + r, abs(r) <= b/2
    """
    q, r = Thm1_02(a, b)
    if r < b/2:
        return (q, r)
    if r > b/2:
        return (q + 1, r - b)
    return (q, r), (q + 1, r - b)

print("Example")
print("=======")
print("Any a divided by b > 0 can take residue r with |r| <= b/2.")
b = 12
print("b ==", b)
for a in [70, -67, 30]:
    print("a ==", a, "; (q, r) ==", Thm1_02_rem(a, b))
print()
print("Any a divided by b > 0 takes unique residue r with -b/2 < r <= b/2.")
b = 12
print("b ==", b)
for a in [-70, -66, 33]:
    print("a ==", a, "; (q, r) ==", divmodl(a, b))
print()

