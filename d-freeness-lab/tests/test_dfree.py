from dfree import DefinitionTester, field, matrix_algebra
from dfree.literature import matrix_ring_criterion, prime_degree_criterion


def test_matrix_ring_literature_certificate():
    result = matrix_ring_criterion(matrix_size=3, d=2)
    assert result.status == "certified-yes"


def test_prime_degree_exact_boundary():
    assert prime_degree_criterion(is_prime=True, degree=2, d=2).status == "certified-yes"
    assert prime_degree_criterion(is_prime=True, degree=2, d=3).status == "certified-no"


def test_field_f2_fails_a_2free_definition_case():
    A = field(2)
    result = DefinitionTester(A).check_case(m=2, I={0, 1}, J=set(), mode="zero")
    assert not result.passes
    assert result.solution_dimension > 0
    assert result.standard_dimension == 0


def test_m2_f2_passes_same_definition_case():
    A = matrix_algebra(2, 2)
    result = DefinitionTester(A).check_case(m=2, I={0, 1}, J=set(), mode="zero")
    assert result.passes


def test_m2_f2_central_one_variable_case():
    A = matrix_algebra(2, 2)
    result = DefinitionTester(A).check_case(m=1, I={0}, J={0}, mode="central")
    assert result.passes


def test_bounded_audit_detects_field_obstruction():
    from dfree import bounded_d_freeness_audit
    results = bounded_d_freeness_audit(field(2), d=2, max_m=2)
    assert any(not r.passes for r in results)
