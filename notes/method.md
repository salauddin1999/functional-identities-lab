# From an inverse identity to a finite linear system

Let $V=M_2(\mathbb F_p)$, where $p$ is prime. Its ordered basis is
$E_{11},E_{12},E_{21},E_{22}$.

## Why additive maps have 16 coefficients

If $f$ is additive, repeated addition gives $f(kX)=kf(X)$ for each integer
$k$. Reducing modulo $p$ proves $\mathbb F_p$-linearity. Therefore the four
images of the basis matrices determine $f$, and each image has four
coordinates. A pair $(f,g)$ has 32 unknown coefficients.

## Constructing the constraints

Fix an invertible matrix $A$ and set $B=A^{-1}$. Write the coefficient of
output basis matrix $E_i$ in $f(E_j)$ as $t_{ij}$ and in $g(E_j)$ as $s_{ij}$.
If $a_j,b_j$ are the coordinates of $A,B$, then

$$f(A)B+A^n g(B)=\sum_{i,j}t_{ij}a_jE_iB+\sum_{i,j}s_{ij}b_jA^nE_i.$$

Equating the four coordinates to zero gives four linear equations.
Enumerating every invertible matrix imposes exactly the required identity.
There are $(p^2-1)(p^2-p)$ units: choose a nonzero first column, then a
second column outside its one-dimensional span.

For $f=g$, identify $s_{ij}$ with $t_{ij}$ before row reduction. The
nullspace basis parametrizes all solutions; every linear combination is
taken over $\mathbb F_p$.

## Verification and limits

The tests check two-sided inverses, a known kernel, and substitute each
computed basis vector back into the original identity for primes 2 and 3
and exponents 2 through 4. A separate explicit nonzero solution provides
an independent check that the solver does not always return a zero kernel.

The enumeration is exhaustive, not random. Nevertheless, a computed result
for one finite matrix ring does not establish a theorem for all rings.
In particular, $M_2(\mathbb F_p)$ is not a division ring.
