"""
Utility functions and shared constants for vectorfieldviz.
"""

from __future__ import annotations

from typing import Iterable, Tuple

import numpy as np

__version__ = "0.1.0"


def to_ndarray(matrix: Iterable[Iterable[float]]) -> np.ndarray:
    """
    Convert the input to a 2D NumPy array of dtype float64.

    Parameters
    ----------
    matrix :
        Array-like object convertible to a 2D array.

    Returns
    -------
    np.ndarray
        2D float64 array.

    Raises
    ------
    ValueError
        If the input cannot be converted to a 2D array.
    """
    arr = np.array(matrix, dtype=float)
    if arr.ndim != 2:
        raise ValueError("Input matrix must be 2-dimensional.")
    return arr


def is_square(matrix: np.ndarray) -> bool:
    """
    Check whether a matrix is square.

    Parameters
    ----------
    matrix :
        2D NumPy array.

    Returns
    -------
    bool
        True if matrix is square, False otherwise.
    """
    return matrix.shape[0] == matrix.shape[1]


def default_2d_colors() -> dict:
    """
    Default color configuration for 2D visualizations.

    Returns
    -------
    dict
        Dictionary with keys: 'field', 'eigenvectors', 'background'.
    """
    return {
        "field": "rgba(50, 50, 150, 0.7)",
        "eigenvectors": ["red", "green", "orange", "purple"],
        "background": "white",
    }


def default_3d_colors() -> dict:
    """
    Default color configuration for 3D visualizations.

    Returns
    -------
    dict
        Dictionary with keys: 'field', 'eigenvectors', 'background'.
    """
    return {
        "field": "Viridis",
        "eigenvectors": ["red", "green", "orange"],
        "background": "white",
    }


def real_eigen_pairs(
    eigenvalues: np.ndarray,
    eigenvectors: np.ndarray,
    imag_tol: float = 1e-8,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Filter eigenvalues/eigenvectors to those that are real within a tolerance.

    Parameters
    ----------
    eigenvalues :
        Complex eigenvalues.
    eigenvectors :
        Complex eigenvectors, each column corresponds to an eigenvalue.
    imag_tol :
        Maximum absolute imaginary part tolerated to consider a value "real".

    Returns
    -------
    eigenvalues_real, eigenvectors_real :
        Arrays containing only (approximately) real eigenvalues/vectors.
    """
    mask = np.abs(eigenvalues.imag) < imag_tol
    vals = eigenvalues[mask].real
    vecs = eigenvectors[:, mask].real
    return vals, vecs
