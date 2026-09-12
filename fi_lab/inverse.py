"""Solve f(X) X^-1 + X^n g(X^-1) = 0 for all units of M_2(F_p).

Matrices are row-major tuples. A map has coefficients T[output][input],
flattened row-major; pair solutions concatenate the coefficients of f and g.
Only standard-library integer arithmetic is used.
"""
from itertools import product
from math import isqrt

I = (1, 0, 0, 1)


def check_prime(p):
    if p < 2 or any(p % d == 0 for d in range(2, isqrt(p) + 1)):
        raise ValueError("p must be prime")


def mul(a, b, p):
    return tuple(sum(a[2*i+k] * b[2*k+j] for k in range(2)) % p
                 for i in range(2) for j in range(2))


def power(a, n, p):
    if n < 0:
        raise ValueError("n must be nonnegative")
    result = I
    while n:
        if n & 1:
            result = mul(result, a, p)
        a = mul(a, a, p)
        n //= 2
    return result


def inverse(a, p):
    det = (a[0]*a[3] - a[1]*a[2]) % p
    if det == 0:
        raise ValueError("singular matrix")
    d = pow(det, -1, p)
    return tuple(d*x % p for x in (a[3], -a[1], -a[2], a[0]))


def apply(coefficients, a, p):
    return tuple(sum(coefficients[4*i+j]*a[j] for j in range(4)) % p
                 for i in range(4))


def units(p):
    for a in product(range(p), repeat=4):
        if (a[0]*a[3] - a[1]*a[2]) % p:
            yield a


def nullspace(rows, width, p):
    """Streaming row reduction followed by a basis of the homogeneous kernel."""
    pivots = {}
    for row in rows:
        row = [x % p for x in row]
        for j in sorted(pivots):
            factor = row[j]
            if factor:
                row = [(x-factor*y) % p for x, y in zip(row, pivots[j])]
        lead = next((j for j, x in enumerate(row) if x), None)
        if lead is not None:
            scale = pow(row[lead], -1, p)
            pivots[lead] = [scale*x % p for x in row]
    basis = []
    for free in range(width):
        if free in pivots:
            continue
        vector = [0]*width
        vector[free] = 1
        for j in sorted(pivots, reverse=True):
            vector[j] = -sum(pivots[j][k]*vector[k]
                             for k in range(j+1, width)) % p
        basis.append(vector)
    return basis


def equations(p, n, same_map=False):
    width = 16 if same_map else 32
    for a in units(p):
        inv = inverse(a, p)
        an = power(a, n, p)
        rows = [[0]*width for _ in range(4)]
        for output in range(4):
            e = tuple(int(k == output) for k in range(4))
            left, right = mul(e, inv, p), mul(an, e, p)
            for input_ in range(4):
                col = 4*output+input_
                for k in range(4):
                    rows[k][col] += a[input_]*left[k]
                    rows[k][col if same_map else col+16] += inv[input_]*right[k]
        yield from rows


def solve(p=3, n=3, same_map=False):
    check_prime(p)
    if n < 2:
        raise ValueError("exponent must be at least 2")
    if p > 13:
        raise ValueError("This exhaustive experiment is limited to primes <= 13")
    width = 16 if same_map else 32
    basis = nullspace(equations(p, n, same_map), width, p)
    return {"ring": f"M_2(F_{p})", "prime": p, "exponent": n,
            "same_map": same_map, "units_checked": (p*p-1)*(p*p-p),
            "unknowns": width, "dimension": len(basis), "basis": basis}
