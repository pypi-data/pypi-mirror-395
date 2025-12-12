"""
functions related to the greatest common divisor of integers.
"""

import nzmath.arygcd as arygcd

def gcd(a, b):
    """
    Return the greatest common divisor of 2 integers a and b.
    Return 0 if a == b == 0, though 0 cannot be any divisor.
    """
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def binarygcd(a, b):
    """
    Return the greatest common divisor of 2 integers a and b
    by binary gcd algorithm.
    Return 0 if a == b == 0, though 0 cannot be any divisor.
    """
    # use arygcd version
    a, b = abs(a), abs(b)
    return arygcd.binarygcd(a, b)

def extgcd(x, y):
    """
    Return a tuple (u, v, d); they are the greatest common divisor d
    of two integers x and y and u, v such that d = x * u + y * v.
    Return (1, 0, 0) if x == y == 0, though 0 cannot be any divisor.
    """
    # Crandall & Pomerance "PRIME NUMBERS", Algorithm 2.1.4
    a, b, g, u, v, w = 1, 0, x, 0, 1, y
    while w:
        q, t = divmod(g, w)
        a, b, g, u, v, w = u, v, w, a-q*u, b-q*v, t
    if g >= 0:
        return (a, b, g)
    else:
        return (-a, -b, -g)

def lcm(a, b):
    """
    Return the least common multiple of given 2 integers a and b.
    Return 0 if only one of them is 0 though there is no multiple of 0.
    If both are zero, it raises an exception.
    """
    return abs(a // gcd(a, b) * b)

def gcd_of_list(integers):
    """
    Return list [d, [c1, ..., cn]] for list integers == [x1, ..., xn], so that
    d = c1 * x1 + ... + cn * xn, where d is the greatest common divisor of
    x1, ..., xn and c1, ,,, cn are integers.  Return [0, integers] if integers
    == [0, ..., 0] or [] though 0 cannot be any divisor.
    """
    the_gcd = 0
    total_length = len(integers)
    coeffs = []
    coeffs_length = 0
    for integer in integers:
        multiplier, new_coeff, the_gcd = extgcd(the_gcd, integer)
        if multiplier != 1:
            for i in range(coeffs_length):
                coeffs[i] *= multiplier
        coeffs.append(new_coeff)
        coeffs_length += 1
        if the_gcd == 1:
            coeffs.extend([0] * (total_length - coeffs_length))
            break
    return [the_gcd, coeffs]

def extgcd_(*a):
    """
    Input
        a: integers, at least one non-zero
    Output
        [d, x]: list of d and x, where d is the greatest common divisor
                of a, also list x is such that
                sum(a[i]*x[i] for i in range(len(a))) == d
    """
    a = list(a)
    n = len(a)
    X = [[a[i], [1 if j == i else 0 for j in range(n)]]
            for i in range(n) if a[i]]
    if X == []:
        raise ValueError("At least one non-zero integer is required.")
    d = X[0]
    for x in X:
        if abs(x[0]) < abs(d[0]):
            d = x
    while len(X) > 1:
        for x in X:
            if x != d:
                q, x[0] = divmodl(x[0], d[0])
                for j in range(n):
                    x[1][j] = x[1][j] - q*d[1][j]
        X = [x for x in X if x[0]]
        d = X[0]
        for x in X:
            if abs(x[0]) < abs(d[0]):
                d = x
    if d[0] > 0:
        return d
    else:
        return [-d[0], [-d[1][j] for j in range(n)]]

def divmodl(a, b):
    """
    Input
        a: integer
        b: non-zero integer
    Output
        (q, r): pair of integers such that a == q*b + r, abs(r) <= abs(b)/2
    """
    q, r = divmod(a, b)
    if 2*abs(r) <= abs(b):
        return q, r
    return q + 1, r - b

def extgcd_gen(*a):
    """
    Input
        a: integers, at least one non-zero
            n = len(a)
    Output
        [d, s, A]
            d: the greatest common divisor of a
            k: integer divisible by d
            Diophantus equation
                sum(a[i]*x[i] for i in range(n)) == k
            general solution
                x = [sum(A[i][j]*y[j] for j in range(n)) for i in range(n)]
            integer parameter y, y[s] == k//d 
    """
    a = list(a)
    n, m = len(a), 0
    for i in range(n):
        if a[i]:
            m = m + 1
            if m == 1 or abs(a[i]) < abs(a[s]):
                s = i
    if m == 0:
        raise ValueError("At least one non-zero integer is required.")
    q, A = [1]*n, [[1 if j == i else 0 for j in range(n)] for i in range(n)]
    while m > 1:
        s_ = s
        for i in range(n):
            if i != s:
                q[i], a[i] = divmodl(a[i], a[s])
                if a[i] == 0:
                    m = m - 1
                elif abs(a[i]) < abs(a[s_]):
                    s_ = i
        for i in range(n):
            for j in range(n):
                if j != s:
                    A[i][j] = A[i][j] - q[j]*A[i][s]
        s = s_
    if a[s] > 0:
        return [a[s], s, A]
    return [-a[s], s, [[-A[i][j] for j in range(n)] for i in range(n)]]

def gcd_(*a):
    """
    Input
        a: integers, at least one non-zero
    Output
        the greatest common divisor of a
    """
    a = {abs(i) for i in a if i}
    if a == set():
        raise ValueError("At least one non-zero integer is required.")
    d = min(a)
    while len(a) > 1:
        a = {i if i == d else abs(modl(i, d)) for i in a}
        a.discard(0)
        d = min(a)
    return d

def modl(a, b):
    """
    Input
        a: integer
        b: non-zero integer
    Output
        r: residue of a modulo b such that abs(r) <= abs(b)/2
    """
    r = a%b
    if 2*abs(r) <= abs(b):
        return r
    return r - b

def lcm_(*a):
    """
    Input
        a: non-zero integers
    Output
        the least common multiple of a
    """
    a = {abs(i) for i in a}
    if a == set() or min(a) == 0:
        raise ValueError("Non-zero integers are required.")
    l = a.pop()
    for i in a:
        l = l//gcd_(l, i)*i
    return l

def coprime(a, b):
    """
    Return True if a and b are coprime, False otherwise.

    For Example:
    >>> coprime(8, 5)
    True
    >>> coprime(-15, -27)
    False
    >>>
    """
    return gcd(a, b) == 1

def pairwise_coprime(int_list):
    """
    Return True if all integers in int_list are pairwise coprime,
    False otherwise.

    For example:
    >>> pairwise_coprime([1, 2, 3])
    True
    >>> pairwise_coprime([1, 2, 3, 4])
    False
    >>>
    """
    int_iter = iter(int_list)
    product = next(int_iter)
    for n in int_iter:
        if not coprime(product, n):
            return False
        product *= n
    return True

# gcd.part_frac OK>man
# OK>?+ function for partial fraction decomposition
def part_frac(m, x):
    """
    Input
        m: list of pairwise coprime integers, min(m) > 1, k = len(m) > 0
        x: integer, x > 0
    GCD(M,x)=1, M = prod(m) (without arith1.product to avoid circular import)
    Output (X, s)
        X: list of numerators of partial fraction decomposition of x/M
        s: integer part of partial fraction decomposition of x/M
    x/M == sum(X[i]/m[i] for i in range(k)) + s
    0 < X[i] < m[i] for i in range(k)
    """
    k = len(m)
    if not(k and min(m) > 1 and pairwise_coprime(m)):
        raise ValueError("denominator list m is incorrect")
    M = m[0]
    for i in range(1, k):
        M *= m[i]
    if gcd_(M, x) > 1:
        raise ValueError("x/M should be irreducible")
    M_ = [M//m[i] for i in range(k)]
    d, t = extgcd_(*M_)
    if sum(M_[i]*t[i] for i in range(k)) != 1:
        raise RuntimeError("function extgcd_")
    X, s = [0]*k, 0
    for i in range(k):
        q, X[i] = divmod(x*t[i], m[i]); s += q
    if 0 in X or x != sum(M_[i]*X[i] for i in range(k)) + s*M:
        raise RuntimeError("wrong transformation")
    return X, s

