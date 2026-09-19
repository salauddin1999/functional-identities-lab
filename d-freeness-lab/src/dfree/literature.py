from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Status = Literal["certified-yes", "certified-no", "not-applicable", "inconclusive"]


@dataclass(frozen=True)
class CriterionResult:
    status: Status
    criterion: str
    statement: str
    reference: str
    scope: str


BOOK = (
    "M. Brešar, M. A. Chebotar, W. S. Martindale III, Functional Identities, "
    "Birkhäuser, 2007, especially Definition 3.8, Corollary 2.22, Theorem 5.11/Corollary 5.12."
)
QUOTIENTS_2016 = (
    "M. Brešar, Functional Identities and Rings of Quotients, Algebras and "
    "Representation Theory 19 (2016), 1437–1450, DOI:10.1007/s10468-016-9625-4."
)
TENSOR_2016 = (
    "M. Brešar, Functional identities on tensor products of algebras, Journal of "
    "Algebra 455 (2016), 108–136, DOI:10.1016/j.jalgebra.2016.02.012."
)
TRIANGULAR = (
    "D. Eremita, Functional identities in upper triangular matrix rings, Linear "
    "Algebra and its Applications 493 (2016), 580–605, DOI:10.1016/j.laa.2015.12.022."
)


def matrix_ring_criterion(matrix_size: int, d: int) -> CriterionResult:
    """Published sufficient test: M_n(S) is d-free in itself when n >= d."""
    if matrix_size >= d:
        return CriterionResult(
            "certified-yes",
            "matrix-ring",
            f"n={matrix_size} >= d={d}; M_n(S) is d-free in itself for every unital ring S.",
            f"{BOOK} See also {TENSOR_2016}",
            "d-freeness inside the matrix ring itself",
        )
    return CriterionResult(
        "inconclusive",
        "matrix-ring",
        f"n={matrix_size} < d={d}; this sufficient matrix criterion does not decide the case.",
        f"{BOOK} See also {TENSOR_2016}",
        "d-freeness inside the matrix ring itself",
    )


def prime_degree_criterion(*, is_prime: bool, degree: int | None, d: int) -> CriterionResult:
    """Exact prime-ring criterion for the maximal left quotient ambient ring.

    For a prime ring A, A is d-free in Q_ml(A) iff deg(A) >= d.
    """
    if not is_prime:
        return CriterionResult(
            "not-applicable",
            "prime-degree",
            "The criterion requires a prime ring.",
            QUOTIENTS_2016,
            "A as a subset of Q_ml(A)",
        )
    if degree is None:
        return CriterionResult(
            "inconclusive",
            "prime-degree",
            "Prime ring supplied, but deg(A) is unknown.",
            QUOTIENTS_2016,
            "A as a subset of Q_ml(A)",
        )
    status: Status = "certified-yes" if degree >= d else "certified-no"
    comparison = ">=" if degree >= d else "<"
    return CriterionResult(
        status,
        "prime-degree",
        f"deg(A)={degree} {comparison} d={d}; by the fundamental theorem this exactly decides d-freeness in Q_ml(A).",
        f"{QUOTIENTS_2016} Also summarized in {BOOK}",
        "A as a subset of its maximal left ring of quotients Q_ml(A)",
    )


def tensor_inheritance_criterion(*, base_is_d_free: bool, second_factor_finite_dimensional: bool) -> CriterionResult:
    if base_is_d_free and second_factor_finite_dimensional:
        return CriterionResult(
            "certified-yes",
            "finite-dimensional-tensor",
            "A d-free subset remains d-free after tensoring with a finite-dimensional unital algebra, in the theorem's stated ambient tensor algebra.",
            TENSOR_2016,
            "tensor-product setting of Brešar (2016), Theorem 3.2/Corollary 3.3",
        )
    return CriterionResult(
        "inconclusive",
        "finite-dimensional-tensor",
        "The inheritance theorem needs a d-free base and a finite-dimensional second factor.",
        TENSOR_2016,
        "tensor-product setting of Brešar (2016)",
    )


def upper_triangular_inheritance_criterion(*, base_is_d_free: bool) -> CriterionResult:
    if base_is_d_free:
        return CriterionResult(
            "certified-yes",
            "upper-triangular-inheritance",
            "If R is d-free in Q, then T_n(R) is d-free in T_n(Q).",
            TRIANGULAR,
            "upper triangular matrix rings",
        )
    return CriterionResult(
        "inconclusive",
        "upper-triangular-inheritance",
        "A d-free base certificate is required before applying the inheritance theorem.",
        TRIANGULAR,
        "upper triangular matrix rings",
    )
