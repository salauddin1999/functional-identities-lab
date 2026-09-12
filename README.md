# Functional Identities Lab

**Exact computational experiments in noncommutative algebra**

A research companion for studying additive maps, inverse functional identities,
and the role of characteristic in matrix rings. Developed for the research
interests of **Sk Md Salauddin**, PhD Research Scholar in Mathematics,
Aligarh Muslim University.

## The first experiment

Find all additive maps satisfying

$$f(X)X^{-1}+X^n g(X^{-1})=0\qquad(X\in GL_2(\mathbb F_p)).$$

The toolkit constructs a homogeneous linear system over the prime field and
returns a basis of its entire solution space. You can impose $f=g$ as well.
Arithmetic is exact; no floating-point computations or third-party packages
are required.

## Quick start

Use Python 3.10 or newer. From the repository root:

```bash
python -m fi_lab --prime 3 --exponent 3
python -m fi_lab --prime 2 --exponent 2 --same-map
python -m unittest discover -s tests -v
```

The JSON output includes the ring, exponent, number of units checked, solution
space dimension, and basis vectors. Dimension zero means that only the zero
map (or zero pair) satisfies the identity in this particular finite ring.

### Reading a basis vector

Represent $X$ by $(x_{11},x_{12},x_{21},x_{22})$.
The first 16 entries describe a $4\times4$ coefficient matrix for $f$, in
row-major order. For a pair of maps, the next 16 describe $g$. For `--same-map`,
only 16 entries are returned. All coefficients are reduced modulo $p$.

## Computed examples

Dimensions over $\mathbb F_p$; all invertible matrices are checked.

| Prime | Exponent | Pairs $(f,g)$ | Maps with $f=g$ |
|---:|---:|---:|---:|
| 2 | 2 | 10 | 6 |
| 2 | 3 | 10 | 7 |
| 2 | 4 | 10 | 6 |
| 2 | 5 | 12 | 7 |
| 3 | 2, 3, 4, or 5 | 0 | 0 |
| 5 | 2, 3, 4, or 5 | 0 | 0 |

See [the mathematical method](notes/method.md) for the reduction and
[a characteristic-two example](notes/characteristic-two.md) for a direct proof.

## Scope

These are exhaustive computations for $M_2(\mathbb F_p)$, **not proofs about
arbitrary division rings**. The implementation supports prime $p\leq13$ and
integer $n\geq2$. Matrix rings contain singular elements; the identity is
imposed only on units. Over a prime field, additivity is equivalent to
$\mathbb F_p$-linearity. An extension-field implementation would require
working over its prime field to capture all additive maps.

## Contents

| Path | Purpose |
|---|---|
| `fi_lab/inverse.py` | Matrix arithmetic, identity constraints, kernel solver |
| `fi_lab/__main__.py` | Command-line interface with JSON output |
| `tests/test_inverse.py` | Exact arithmetic and original-identity checks |
| `notes/method.md` | Why the finite linear system captures all additive maps |
| `notes/characteristic-two.md` | An explicit nonzero example with proof |
| `notes/research-directions.md` | Concrete directions for extending the toolkit |

## Contributing

Include the ambient ring, characteristic, exponent, and exact command with
every computational observation. State whether a claim is an experiment,
conjecture, or proved statement. Include a proof or a precise source for new
theorems. Run the test suite before submitting changes.

This repository is an experimental research resource and makes no claim that
its questions are new or unsolved in the literature.
