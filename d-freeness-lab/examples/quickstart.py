from dfree import DefinitionTester, bounded_d_freeness_audit, field, matrix_algebra
from dfree.literature import matrix_ring_criterion, prime_degree_criterion


print("=== Literature certificates ===")
print(matrix_ring_criterion(matrix_size=3, d=2))
print(prime_degree_criterion(is_prime=True, degree=2, d=3))

print("\n=== Direct definition test: M_2(F_2) ===")
A = matrix_algebra(2, 2)
case = DefinitionTester(A).check_case(m=2, I={0, 1}, J=set(), mode="zero")
print(case)

print("\n=== Bounded d=2 audit for M_2(F_2), m <= 2 ===")
audit = bounded_d_freeness_audit(A, d=2, max_m=2)
print("cases:", len(audit), "passed:", sum(r.passes for r in audit))

print("\n=== A 2-free obstruction in F_2 ===")
F2 = field(2)
bad = DefinitionTester(F2).check_case(m=2, I={0, 1}, J=set(), mode="zero")
print(bad)
