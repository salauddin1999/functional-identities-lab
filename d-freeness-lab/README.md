# d-Freeness Lab

A small research-oriented Python toolkit for studying **d-free subsets of rings and algebras** in the sense of functional identity theory.

The project deliberately provides **two independent kinds of tests**:

1. **Literature/theorem tests** — apply published criteria that certify d-freeness (or, in one prime-ring setting, non-d-freeness).
2. **Definition tests** — for a finite algebra over `GF(p)`, translate the defining basic functional identities into linear systems and check whether **every arbitrary set-map solution** is standard.

The distinction matters: theorem tests can prove a general result when their hypotheses are met, while the finite definition engine is exact only for the finite set and the selected `(m, I, J)` cases it checks. A failed definition case is a genuine obstruction; passing finitely many cases is not a proof of the full all-`m` definition.

## Mathematical definition implemented

For a nonempty subset `X` of a unital ring `R`, and index sets `I,J ⊆ {1,...,m}`, the basic zero-valued functional identity is

\[
\sum_{i\in I} E_i(\bar x_m^i)x_i + \sum_{j\in J}x_jF_j(\bar x_m^j)=0,
\]

and the central-valued version requires the same expression to lie in `Z(R)`.

The standard solutions have the form

\[
E_i(\bar x_m^i)=\sum_{j\in J,\,j\ne i}x_jp_{ij}(\bar x_m^{ij})+\lambda_i(\bar x_m^i),
\]

\[
F_j(\bar x_m^j)=-\sum_{i\in I,\,i\ne j}p_{ij}(\bar x_m^{ij})x_i-\lambda_j(\bar x_m^j),
\]

where `p_ij` are arbitrary functions into the ambient ring and the `lambda_k` are arbitrary center-valued functions, with `lambda_k=0` when `k∉I∩J`.

`X` is d-free when the zero-valued identity has only standard solutions whenever `max(|I|,|J|) ≤ d`, and the central-valued identity has only standard solutions whenever `max(|I|,|J|) ≤ d-1`.

The implementation uses **0-based Python indices**, so `{0,1}` corresponds to mathematical indices `{1,2}`.

## Published criteria currently encoded

- **Matrix rings:** `M_n(S)` is d-free in itself whenever `n ≥ d` (for a unital ring `S`).
- **Prime-ring degree criterion:** for a prime ring `A`, `A` is d-free in its maximal left ring of quotients `Q_ml(A)` **iff** `deg(A) ≥ d`.
- **Finite-dimensional tensor inheritance:** the Brešar 2016 theorem is exposed as a certificate helper when a d-free base and a finite-dimensional second factor are known.
- **Upper triangular inheritance:** if `R` is d-free in `Q`, then `T_n(R)` is d-free in `T_n(Q)`.

The helpers state their **scope/ambient ring** so that a theorem about `A ⊂ Q_ml(A)` is not accidentally reported as a theorem about another ambient ring.

## Quick start

```python
from dfree import (
    DefinitionTester,
    bounded_d_freeness_audit,
    field,
    matrix_algebra,
)
from dfree.literature import matrix_ring_criterion, prime_degree_criterion

# 1. Published theorem test
print(matrix_ring_criterion(matrix_size=3, d=2))

# For a prime ring with known deg(A)
print(prime_degree_criterion(is_prime=True, degree=2, d=3))

# 2. Direct test from the definition on a finite algebra
A = matrix_algebra(2, 2)            # M_2(F_2), 16 elements
T = DefinitionTester(A)
result = T.check_case(m=2, I={0, 1}, J=set(), mode="zero")
print(result)

# A bounded audit of every allowed I,J for m <= 2
results = bounded_d_freeness_audit(A, d=2, max_m=2)
print("all checked cases pass:", all(r.passes for r in results))

# Contrast with the commutative field F_2: a 2-free obstruction appears
F2 = field(2)
bad = DefinitionTester(F2).check_case(m=2, I={0, 1}, J=set(), mode="zero")
print(bad)
```

## Why the definition tester is mathematically meaningful

For a finite `GF(p)`-algebra, an arbitrary function `E_i : X^(m-1) -> A` is represented by independent coordinate variables for **every input tuple**; no additivity or linearity of `E_i` is assumed. Thus the basic FI becomes a homogeneous linear system over `GF(p)`.

The standard solutions are also a linear subspace, obtained as the image of the parameters `p_ij` and center-valued `lambda_k`. For a fixed case, the tester compares

- `dim(kernel(FI constraints))`, and
- `dim(standard-solution subspace)`.

Because every standard solution satisfies the FI, equality of these dimensions means every solution is standard. Strict inequality gives a nonstandard solution and hence a valid counterexample to the corresponding d-free condition.

## Scope and limitations

- The direct engine currently handles finite-dimensional associative algebras over a **prime field** `GF(p)` and takes the ambient ring to be the same algebra.
- It can use all algebra elements or a user-supplied finite subset `X`.
- Full d-freeness quantifies over **every positive integer m**. Therefore `bounded_d_freeness_audit(..., max_m=2)` is an audit, not a general proof.
- The state space grows rapidly with `|X|^m`; start with small algebras/subsets and low `m`.
- Published theorem certificates should be preferred whenever their hypotheses are established.

## Run the tests

```bash
python -m pip install -e .
python -m pytest -q
```

The included regression tests check theorem boundaries, a direct obstruction for `GF(2)`, and selected cases for `M_2(GF(2))`.

## References

See [`REFERENCES.md`](REFERENCES.md) for the exact papers/books and the theorem/definition mapping used by the code.
