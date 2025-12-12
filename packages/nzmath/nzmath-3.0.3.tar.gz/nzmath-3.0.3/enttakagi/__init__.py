"""

====================================
Lectures on Elementary Number Theory
      (2nd Edition) by TAKAGI, Teiji
           notebook in Python-NZMATH
             enttakagi version 0.0.5(*1)
====================================

The purpose of this notebook is an easy introduction to Algorithmic
Number Theory --- ANT.  You can study three topics
    "Elementary Number Theory",
    "Python Programming",
    "English for Mathematics",(*2)
which are necessary for ANT, at a time, only by running and reading the
programs sec01.py, ..., sec60.py, sect1,py ..., sect4.py in this folder.
For that, you need three preparations:
    Get the book by Takagi in the title above.(*3)
    Let Python and package NZMATH usable on your machine.(*4)
    Download all files in this directory to your machine.(*5)
Then, on the command prompt or interactive shell, do
    $ python sec01.py
etc. and read the printed messages.(*6)  The programs themselves in the
files sec01.py, ... are easy English text to read.     That is all!(*7)
                        Tanaka, Satoru (TMCIT); NAKAMULA, Ken (TMU)(*8)
                                              2022/06/23 --- 2025/12/04
    (*1) Based on Python 3.9.16 and NZMATH 3.0.3.
    (*2) Maybe "Japanese for Mathematics" to English readers.
    (*3) https://www.kyoritsu-pub.co.jp/book/b10011316.html
    (*4) https://www.python.org/ and https://nzmath.sourceforge.io/
    (*5) https://sourceforge.net/projects/nzmath/files/nzmath-enttakagi/
    (*6) When running programs, you are requested to "Hit Return!"
         so that you can continue after reading the printed messages.
    (*7) Finding and fixing bugs of Python calculator NZMATH on ANT is
         another important purpose for us developers.
    (*8) Special thanks to MATSUI, Tetsushi; OGURA, Naoki; MIYAMOTO,
         Yasunori and others on ACKNOWLEDGEMENTS.txt in the directory
         https://sourceforge.net/p/nzmath/code/ci/default/tree/dist/
         Home Page (NAKAMULA) https://tnt-nakamu-lab.fpark.tmu.ac.jp/

<<<< CONTENTS (functions) >>>>

Chapter 1   Elementary Number Theory
====================================

Section 1   Divisibility of Integers
------------------------------------
    sec01.py    Thm1_01, Thm1_02 (divmod), Thm1_02_rem

Section 2   Greatest Common Divisors, Least Common Multiples
------------------------------------------------------------
    sec02.py    Thm1_03, Thm1_04, Thm1_05 (lcm), Thm1_06
                Prob1 (gcd, Eucledean Algorithm == GCD)
                Prob1_rem (gcd_, general GCD by modl)
                Prob1_rem_eg, Prob2 (lcm_, by gcd_)

Section 3   Linear Indeterminate Equations
------------------------------------------
    sec03.py    Thm1_07 (gcd_of_list, general extended GCD)
                Thm1_07_eg (general extended GCD by extgcd_gen), Prob1
                <<skip Prob2>>

Section 4   Prime Numbers
-------------------------
    sec04.py    Thm1_08, Thm1_09 (prime factorization)
    sec04a.py   Prob1 (tau function), Prob2 (sigma function)
                Prob3 (multiplicative function), Prob4
                PerfNumb (perfect number)
                Prob5 (Mersenne number, Lucas-Lehmer test)
    sec04b.py   Prob6, Prob7, gcdlcmFI, Prob8, Prob9, Prob10, Prob11
                    (FactoredInteger plays important role)
    sec04c.py   Prob12, Prob12_rem, Prob13, Prob14, Prob14_rem
                    (binomial coefficients, partial fraction decomposition)
    sec04d.py   Thm1_10, (Table of Primes by Eratosthenes Sieve)
                Thm1_10_rem (primes of arithmetic progression  4*n - 1)
                PrimeNumberTheorem (prime.generator)
                Tschebyschef (Tschebyschef, nextPrime)
                twinPrime (twin prime), gapPrime, Goldbach (Goldbach conjecture)

Section 5   Congruences
-----------------------
    sec05.py    CongEquiv, SysRes_eg, Thm1_11, Thm1_12
                    (fundamental arithmetic of congruence)
                Prob1 (congruence arithmetic by digital criterion)

Section 6   Congruences of Degree One
-------------------------------------
    sec06.py    Thm1_13 (e1_ZnZ, extended GCD), Thm1_13_rem, Thm1_13_eg
    sec06a.py   Thm1_14 (CRT_, Chinese Remainder Theorem)
                Thm1_14_eg (CRT_Gauss by moduli symmetric)
                Thm1_14_rem (partial fraction decomposition)
    sec06b.py   Prob1 (CRT of moduli m, n, GCD(m, n) > 1)
                Prob2 (CRT of general non-coprime moduli)
                <<skip Remark on Ring of Fraction>>

Section 7   Introduction to Solving Congruences
-----------------------------------------------
    sec07.py    Thm1_15 (allroots_Fp, cyclicity of  Fp*)
                Thm1_15_rem (digital method, Karatsuba)
                Thm1_16 (lift up prime power modulus, Hensel lift), Thm1_16_eg
    sec07a.py   Prob1, Thm1_17 (allroots_ZnZ, complete solutions modulo n)
                    (allroots_Fp, liftup_ZpnZ, CRT_, allroots_ZnZ)

Section 8   Euler's Function  phi(n)
------------------------------------
    sec08.py    phi, Thm1_18 (phi(n) == euler(n) in terms of factored  n)
                Thm1_19 (phi(n) is multiplicative, reduced system of residues)
                Phi, Phi_def, Prob1 (generalize phi to Phi over floating real)
                Thm1_20 (sum(phi(d)for d|n)==n), mu, Thm1_21 (Moebius function)
                Thm1_22 (Moebius inversion formula, mu(n) == moebius(n))

Section 9   Roots of Unity
--------------------------
    sec09.py    (Z/nZ: k (mod n) <--> exp(2j*pi*k/n): n-th roots of 1)
                Theorem 1.23 (n n-th roots of 1 and phi(n) primitive ones)
                Example, (Cyclotomic Polynomials and Coefficients), cycloPoly
                Theorem 1.24 (simple formula by Moebius function), cycloMoebius
                Problems 1 and 2 (norm and trace of primitive root of 1)
                Problem 3 (isomorphic Z/nZ residue classes <--> n-th roots of 1)
                Problem 4 (direct sum  Z/aZ + Z/bZ == Z/abZ  if  GCD(a, b) == 1)

Section 10  Fermat's Theorem
----------------------------
    sec10.py    Thm1_25 (primarity test full_euler by Fermat's Theorem)
                Thm1_26 (exponent of reduced residue), Prob1
                Thm1_25_rem (primes of arithmetic progression  4*n + 1)
                Theorem (There are infinitely many primes of the form  m*t + 1.)
    sec10a.py   Theorem (irreducible proper fraction = purely repeating decimal)
                Remark, repeatDecimal, Example 1, Example 2, Example 3

Section 11  Primitive Roots, Indices (Discrete Log)
---------------------------------------------------
    sec11.py    (Table of Primitive Roots), (Existence of Primitive Roots)
                Example, Theorem 1.27 ((Z/p)* == {1. r, ..., r**(p-2)})
                Remark (the exponent of  r**k), (Compare Several Methods)
                (generalize the computation of the textbook as a program)
                (Table of Index for Primitive Roots), Example
                Theorem 1.28 (Isomorphism via Index), Examples 1, 2, 3
                Problems 1, 2 (key point for small size table)
                Problem 3 (base change of Ind), Problem 4, Problem 5 (Wilson)
                power residue and non residue

Numerical Tables
================
    (type 1: list of computed data // type 2: function creating type 1 table)

Table 1  Table of Prime Numbers
----------------------------------
                always  p: odd prime,  r: primitive root of  p
                theoretically no restriction on parameter  N  of functions here
    sect1.py    (1) detailed explanation of type 1:  p < 100, sec04d.py
                    type 2:  p < N, nzmath.prime.eratosthenes(N)
                    type 2:  p < N, nzmath.prime.generator_eratosthenes_(N)
                    type 2:  p < N, nzmath.prime.generator_eratosthenes(N)
                (2) type 1:  r  of  p < 1000 (our textbook)
                (3) r:  the least positive
                    (i) type 2:  nzmath.residue.primitiveRoots(N=1000)
                        type 2:  nzmath.residue.primitiveRoots2(N=1000)
                   (ii) type 1:  r of p < 1000000,  DATADIR/primitiveRoots.csv

Table 2  Table of primitiveRoot Indicies
-------------------------------------------
                always  p: odd prime,  r: primitive root of  p
    sect2.py    (1) (previous) type 1:  Jacobi-Cunningham  p < 1000, sec11.py
                (2) index  Ind(N)  by  r**Ind(N) == N (mod p) (N in range(1,p))
                    index table  IX = [Ind(N) for N in range(1,p)]
                (3) IX type 1:  full  p < 50, part  50 < p < 100 (our textbook)
                (4) power  Pow(I) == r**I (mod p) (I in range(p-1))
                    essential part  PW = [Pow(I) for I in range(p-1)]
                    (i) PW type 2:  nzmath.primitiveRoot0PW(p, r)
                   (ii) PW type 1:  [p,r] + PW_  of  p < 2000, where
                            PW_ = [PW[I] for I in range((p-1)>>1)] (half size)
                        collect them to  DATADIR/primitiveRootPW_.csv

Bugs of imported NZMATH functions & classes / newly defined ones
================================================================
    See patch/fix_nzmath.py about everything on this matter!

List of utility functions of utils.py
=====================================
    HitRet, again, strInt, randFactLists, randmodPolyList, printPoly
    lcm_def, allDivisors_def, gcd_def, countDivisors_def, sumDivisors_def
    allroots_ZnZ_def, cycloDef

Copyright
=========
The package is a part of NZMATH, and is distributed under the BSD
license.  See https://nzmath.sourceforge.io/LICENSE.txt for detail.
Part 1 (sec01-04) enttakagi-0.0.1 release 2024/03/28
Part 2 (sec05-07) enttakagi-0.0.2 release 2024/08/08
Part 3 (sec08-10) enttakagi-0.0.3 release 2024/12/01
Part 4 (sec11)    enttakagi-0.0.4 release 2025/02/28 2025/12/04
Part t (sect1-t2) enttakagi-0.0.5 release 2025/12/04
The latest version of this file and the files in this directory are in
    https://sourceforge.net/p/nzmath/code/ci/default/tree/enttakagi/
however they are under construction so there are usually many bugs.
"""
