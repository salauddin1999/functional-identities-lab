# References and theorem map

This file records the mathematical sources behind the implemented tests. The code intentionally distinguishes **published certificates** from **bounded computations from the definition**.

## Core definition

1. M. Brešar, M. A. Chebotar, W. S. Martindale III, *Functional Identities*, Frontiers in Mathematics, Birkhäuser, 2007. DOI: `10.1007/978-3-7643-7796-0`.
   - Rigorous definition and general theory of d-free sets: Chapter 3.
   - Functional identities on d-free sets: Chapter 4.
   - d-freeness in prime/semiprime rings: Chapter 5.
   - Matrix-ring result used by the code: Corollary 2.22 as cited in later literature.

2. K. I. Beidar and M. A. Chebotar, “On functional identities and d-free subsets of rings. I,” *Communications in Algebra* 28 (2000), 3925–3951. DOI: `10.1080/00927870008827066`.

3. K. I. Beidar and M. A. Chebotar, “On functional identities and d-free subsets of rings. II,” *Communications in Algebra* 28 (2000), 3953–3972. DOI: `10.1080/00927870008827067`.

## Prime-ring degree criterion

4. M. Brešar, “Functional Identities and Rings of Quotients,” *Algebras and Representation Theory* 19 (2016), 1437–1450. DOI: `10.1007/s10468-016-9625-4`.
   - The introduction recalls the fundamental theorem: if `A` is prime, then `A` is d-free in `Q_ml(A)` iff `deg(A) >= d`.
   - Here `deg(A)` is the supremum of the algebraic degrees of elements over the extended centroid.

The code exposes this as `prime_degree_criterion(...)`. It is an **exact yes/no theorem test** only in the stated prime-ring/maximal-left-quotient setting.

## Matrix rings and tensor products

5. M. Brešar, “Functional identities on tensor products of algebras,” *Journal of Algebra* 455 (2016), 108–136. DOI: `10.1016/j.jalgebra.2016.02.012`.
   - Section 2 restates the d-free definition and standard solutions.
   - The introduction records that `M_n(S)` is d-free in itself when `n >= d`.
   - Theorem 3.2 / Corollary 3.3 give finite-dimensional tensor-product inheritance.

The code exposes these as `matrix_ring_criterion(...)` and `tensor_inheritance_criterion(...)`.

## Upper triangular matrix rings

6. D. Eremita, “Functional identities in upper triangular matrix rings,” *Linear Algebra and its Applications* 493 (2016), 580–605. DOI: `10.1016/j.laa.2015.12.022`.
   - If `R` is d-free in `Q`, then `T_n(R)` is d-free in `T_n(Q)`.

The code exposes this as `upper_triangular_inheritance_criterion(...)`.

## Computational interpretation used here

For one fixed finite case `(X,m,I,J)`, the definition tester does not sample functions. It represents every arbitrary set-map value independently, so it solves the entire finite functional identity exactly over `GF(p)`. The comparison with standard solutions is a finite-dimensional linear-algebra reformulation of the definition above.
