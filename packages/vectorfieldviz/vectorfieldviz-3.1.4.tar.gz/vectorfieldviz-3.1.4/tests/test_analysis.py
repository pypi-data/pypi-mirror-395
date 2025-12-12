import numpy as np
import pytest

from vectorfieldviz.analysis import (
    validate_matrix,
    compute_eigendecomposition,
    format_eigendecomposition,
)


def test_validate_matrix_square_and_dim():
    A = [[1, 2], [3, 4]]
    arr = validate_matrix(A, dim=2)
    assert arr.shape == (2, 2)

    with pytest.raises(ValueError):
        validate_matrix([[1, 2, 3], [4, 5, 6]], dim=2)


def test_compute_eigendecomposition():
    A = np.eye(2)
    evals, evecs = compute_eigendecomposition(A)
    assert evals.shape == (2,)
    assert evecs.shape == (2, 2)
    assert np.allclose(np.sort(evals), np.array([1.0, 1.0]))


def test_format_eigendecomposition():
    evals = np.array([1 + 0j, 2 + 0j])
    evecs = np.eye(2)
    formatted = format_eigendecomposition(evals, evecs, precision=2)
    assert "λ1" in formatted
    assert "λ2" in formatted
    assert "[" in formatted
