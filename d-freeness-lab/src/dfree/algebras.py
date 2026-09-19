from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable, Sequence

Vector = tuple[int, ...]


def _mod(v: Sequence[int], p: int) -> Vector:
    return tuple(int(x) % p for x in v)


def rank_mod(matrix: list[list[int]], p: int) -> int:
    if not matrix:
        return 0
    a = [[x % p for x in row] for row in matrix]
    rows, cols = len(a), len(a[0])
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if a[i][c] % p), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c], -1, p)
        a[r] = [(inv * x) % p for x in a[r]]
        for i in range(rows):
            if i != r and a[i][c] % p:
                f = a[i][c] % p
                a[i] = [(x - f * y) % p for x, y in zip(a[i], a[r])]
        r += 1
        if r == rows:
            break
    return r


def nullspace_mod(matrix: list[list[int]], p: int, ncols: int | None = None) -> list[Vector]:
    if not matrix:
        n = 0 if ncols is None else ncols
        return [tuple(1 if i == j else 0 for i in range(n)) for j in range(n)]
    a = [[x % p for x in row] for row in matrix]
    rows, cols = len(a), len(a[0])
    r = 0
    pivots: list[int] = []
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if a[i][c] % p), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c], -1, p)
        a[r] = [(inv * x) % p for x in a[r]]
        for i in range(rows):
            if i != r and a[i][c] % p:
                f = a[i][c] % p
                a[i] = [(x - f * y) % p for x, y in zip(a[i], a[r])]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    free = [c for c in range(cols) if c not in pivots]
    basis: list[Vector] = []
    for f in free:
        v = [0] * cols
        v[f] = 1
        for rr, pc in enumerate(pivots):
            v[pc] = (-a[rr][f]) % p
        basis.append(tuple(v))
    return basis


@dataclass(frozen=True)
class FiniteDimensionalAlgebra:
    """Finite-dimensional associative algebra over the prime field GF(p).

    `structure[i][j][k]` is the coefficient of basis vector k in e_i e_j.
    The class does not try to prove associativity; constructors below produce
    associative examples, while custom users should supply a valid table.
    """

    p: int
    structure: tuple[tuple[tuple[int, ...], ...], ...]
    name: str = "A"

    def __post_init__(self) -> None:
        if self.p < 2:
            raise ValueError("p must be prime (at least 2)")
        n = len(self.structure)
        if n == 0:
            raise ValueError("algebra dimension must be positive")
        if any(len(row) != n for row in self.structure):
            raise ValueError("multiplication table must be square")
        if any(len(v) != n for row in self.structure for v in row):
            raise ValueError("each product must have dimension-many coordinates")

    @property
    def dim(self) -> int:
        return len(self.structure)

    @property
    def basis(self) -> list[Vector]:
        return [tuple(1 if i == j else 0 for i in range(self.dim)) for j in range(self.dim)]

    def add(self, a: Sequence[int], b: Sequence[int]) -> Vector:
        return tuple((x + y) % self.p for x, y in zip(a, b))

    def neg(self, a: Sequence[int]) -> Vector:
        return tuple((-x) % self.p for x in a)

    def scale(self, c: int, a: Sequence[int]) -> Vector:
        return tuple((c * x) % self.p for x in a)

    def mul(self, a: Sequence[int], b: Sequence[int]) -> Vector:
        p, n = self.p, self.dim
        out = [0] * n
        for i, ai in enumerate(a):
            ai %= p
            if not ai:
                continue
            for j, bj in enumerate(b):
                bj %= p
                if not bj:
                    continue
                coeff = ai * bj
                prod_ij = self.structure[i][j]
                for k in range(n):
                    out[k] = (out[k] + coeff * prod_ij[k]) % p
        return tuple(out)

    def elements(self, max_elements: int = 4096) -> list[Vector]:
        total = self.p ** self.dim
        if total > max_elements:
            raise ValueError(
                f"{self.name} has {total} elements; increase max_elements or provide a smaller X"
            )
        return [tuple(v) for v in product(range(self.p), repeat=self.dim)]

    def center_basis(self) -> list[Vector]:
        # z = sum a_i e_i is central iff z e_j - e_j z = 0 for all j.
        equations: list[list[int]] = []
        for j in range(self.dim):
            ej = self.basis[j]
            for out_coord in range(self.dim):
                row = []
                for i in range(self.dim):
                    ei = self.basis[i]
                    diff = (self.mul(ei, ej)[out_coord] - self.mul(ej, ei)[out_coord]) % self.p
                    row.append(diff)
                equations.append(row)
        return nullspace_mod(equations, self.p, self.dim)

    def center_annihilator_basis(self) -> list[Vector]:
        # Linear forms ell with ell(z)=0 for every z in Z(A).
        z = self.center_basis()
        if not z:
            return self.basis
        return nullspace_mod([list(vec) for vec in z], self.p, self.dim)


def matrix_algebra(n: int, p: int) -> FiniteDimensionalAlgebra:
    if n < 1:
        raise ValueError("n must be positive")
    dim = n * n
    basis_pairs = [(r, c) for r in range(n) for c in range(n)]
    index = {pair: i for i, pair in enumerate(basis_pairs)}
    structure = []
    for (a, b) in basis_pairs:
        row = []
        for (c, d) in basis_pairs:
            v = [0] * dim
            if b == c:
                v[index[(a, d)]] = 1
            row.append(tuple(v))
        structure.append(tuple(row))
    return FiniteDimensionalAlgebra(p=p, structure=tuple(structure), name=f"M_{n}(GF({p}))")


def field(p: int) -> FiniteDimensionalAlgebra:
    return FiniteDimensionalAlgebra(p=p, structure=(((1,),),), name=f"GF({p})")
