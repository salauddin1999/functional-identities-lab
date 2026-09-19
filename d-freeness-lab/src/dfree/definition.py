from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable, Literal, Sequence

from .algebras import FiniteDimensionalAlgebra, Vector, rank_mod

Mode = Literal["zero", "central"]


@dataclass(frozen=True)
class DefinitionCaseResult:
    passes: bool
    mode: Mode
    m: int
    I: tuple[int, ...]
    J: tuple[int, ...]
    x_size: int
    unknown_dimension: int
    solution_dimension: int
    standard_dimension: int
    note: str


def _tuples(n: int, length: int):
    if length == 0:
        return [()]
    return list(product(range(n), repeat=length))


def _delete_positions(values: Sequence[int], *positions: int) -> tuple[int, ...]:
    blocked = set(positions)
    return tuple(v for k, v in enumerate(values) if k not in blocked)


class DefinitionTester:
    """Exact bounded tests of Beidar--Chebotar d-freeness over GF(p).

    The full definition quantifies over all m and all arbitrary maps. For one chosen
    (m, I, J), this class handles *all* maps at once by linear algebra: the FI is a
    homogeneous linear system and the standard solutions form the image of another
    linear map. The case passes iff these two subspaces have the same dimension.

    This is exact for the chosen finite set X and chosen case. A bounded collection
    of passing cases is evidence/audit, not by itself a proof of full d-freeness.
    A failed case is a genuine certificate that X is not d-free at the relevant d.
    """

    def __init__(self, algebra: FiniteDimensionalAlgebra, X: Iterable[Vector] | None = None):
        self.A = algebra
        self.X = list(X) if X is not None else algebra.elements()
        if not self.X:
            raise ValueError("X must be nonempty")
        if any(len(x) != self.A.dim for x in self.X):
            raise ValueError("every x in X must have algebra dimension coordinates")

    def check_case(self, *, m: int, I: Iterable[int], J: Iterable[int], mode: Mode = "zero") -> DefinitionCaseResult:
        if m < 1:
            raise ValueError("m must be positive")
        I = tuple(sorted(set(I)))
        J = tuple(sorted(set(J)))
        if any(i < 0 or i >= m for i in I + J):
            raise ValueError("I and J use 0-based positions in range(m)")
        if mode not in ("zero", "central"):
            raise ValueError("mode must be 'zero' or 'central'")

        p, r, q = self.A.p, self.A.dim, len(self.X)
        domains = _tuples(q, m - 1)

        offset = 0
        slots: dict[tuple[str, int, tuple[int, ...], int], int] = {}
        for kind, indices in (("E", I), ("F", J)):
            for idx in indices:
                for args in domains:
                    for c in range(r):
                        slots[(kind, idx, args, c)] = offset
                        offset += 1
        n_unknown = offset

        if mode == "zero":
            functionals = [tuple(1 if i == j else 0 for i in range(r)) for j in range(r)]
        else:
            functionals = self.A.center_annihilator_basis()

        fi_rows: list[list[int]] = []
        for x_idx in _tuples(q, m):
            contributions = [[0] * n_unknown for _ in functionals]
            for i in I:
                args = _delete_positions(x_idx, i)
                xi = self.X[x_idx[i]]
                for c, ec in enumerate(self.A.basis):
                    out = self.A.mul(ec, xi)
                    col = slots[("E", i, args, c)]
                    for h, ell in enumerate(functionals):
                        contributions[h][col] = sum(a*b for a, b in zip(ell, out)) % p
            for j in J:
                args = _delete_positions(x_idx, j)
                xj = self.X[x_idx[j]]
                for c, ec in enumerate(self.A.basis):
                    out = self.A.mul(xj, ec)
                    col = slots[("F", j, args, c)]
                    for h, ell in enumerate(functionals):
                        contributions[h][col] = (contributions[h][col] + sum(a*b for a, b in zip(ell, out))) % p
            fi_rows.extend(contributions)

        fi_rank = rank_mod(fi_rows, p)
        solution_dim = n_unknown - fi_rank

        std_columns: list[list[int]] = []

        if m >= 2:
            pij_domains = _tuples(q, m - 2)
            for i in I:
                for j in J:
                    if i == j:
                        continue
                    for pij_args in pij_domains:
                        for c, ec in enumerate(self.A.basis):
                            colvec = [0] * n_unknown
                            for e_args in domains:
                                original = [k for k in range(m) if k != i]
                                mapping = dict(zip(original, e_args))
                                reduced = tuple(mapping[k] for k in range(m) if k not in (i, j))
                                if reduced == pij_args:
                                    xj = self.X[mapping[j]]
                                    out = self.A.mul(xj, ec)
                                    for out_c, coeff in enumerate(out):
                                        colvec[slots[("E", i, e_args, out_c)]] = (colvec[slots[("E", i, e_args, out_c)]] + coeff) % p
                            for f_args in domains:
                                original = [k for k in range(m) if k != j]
                                mapping = dict(zip(original, f_args))
                                reduced = tuple(mapping[k] for k in range(m) if k not in (i, j))
                                if reduced == pij_args:
                                    xi = self.X[mapping[i]]
                                    out = self.A.neg(self.A.mul(ec, xi))
                                    for out_c, coeff in enumerate(out):
                                        colvec[slots[("F", j, f_args, out_c)]] = (colvec[slots[("F", j, f_args, out_c)]] + coeff) % p
                            std_columns.append(colvec)

        center_basis = self.A.center_basis()
        for k in sorted(set(I).intersection(J)):
            for args in domains:
                for z in center_basis:
                    colvec = [0] * n_unknown
                    for out_c, coeff in enumerate(z):
                        colvec[slots[("E", k, args, out_c)]] = (colvec[slots[("E", k, args, out_c)]] + coeff) % p
                        colvec[slots[("F", k, args, out_c)]] = (colvec[slots[("F", k, args, out_c)]] - coeff) % p
                    std_columns.append(colvec)

        if std_columns:
            std_matrix_rows = [[col[row] for col in std_columns] for row in range(n_unknown)]
            standard_dim = rank_mod(std_matrix_rows, p)
        else:
            standard_dim = 0

        passes = standard_dim == solution_dim
        note = (
            "Every solution of this finite basic FI is standard."
            if passes
            else "A nonstandard solution exists for this case; this is a genuine obstruction to the corresponding d-freeness claim."
        )
        return DefinitionCaseResult(
            passes=passes,
            mode=mode,
            m=m,
            I=I,
            J=J,
            x_size=q,
            unknown_dimension=n_unknown,
            solution_dimension=solution_dim,
            standard_dimension=standard_dim,
            note=note,
        )


def bounded_d_freeness_audit(
    algebra: FiniteDimensionalAlgebra,
    *,
    d: int,
    max_m: int = 2,
    X: Iterable[Vector] | None = None,
) -> list[DefinitionCaseResult]:
    """Run all definition cases up to max_m allowed by the d-free bounds.

    Zero-valued basic FIs are checked when max(|I|,|J|) <= d.
    Center-valued basic FIs are checked when max(|I|,|J|) <= d-1.

    Passing the bounded audit is not a proof of full d-freeness, because the
    definition quantifies over every m. Any failed case is a valid obstruction.
    """
    if d < 1:
        raise ValueError("d must be positive")
    if max_m < 1:
        raise ValueError("max_m must be positive")
    tester = DefinitionTester(algebra, X=X)
    results: list[DefinitionCaseResult] = []
    for m in range(1, max_m + 1):
        all_subsets = [
            tuple(i for i in range(m) if mask & (1 << i))
            for mask in range(1 << m)
        ]
        for I in all_subsets:
            for J in all_subsets:
                if max(len(I), len(J)) <= d:
                    results.append(tester.check_case(m=m, I=I, J=J, mode="zero"))
                if max(len(I), len(J)) <= d - 1:
                    results.append(tester.check_case(m=m, I=I, J=J, mode="central"))
    return results
