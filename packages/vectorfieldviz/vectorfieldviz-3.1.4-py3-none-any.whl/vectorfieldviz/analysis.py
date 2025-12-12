"""
Eigenanalysis utilities for vectorfieldviz.
"""

from __future__ import annotations

from typing import Iterable, Tuple

import numpy as np

from .utils import to_ndarray, is_square


def validate_matrix(matrix: Iterable[Iterable[float]], dim: int | None = None) -> np.ndarray:
    """
    Validate that the input is a square matrix (optionally of given dimension).

    Parameters
    ----------
    matrix :
        Array-like matrix input.
    dim :
        If provided, required dimension (e.g. 2 for 2×2, 3 for 3×3).

    Returns
    -------
    np.ndarray
        Validated 2D float64 array.

    Raises
    ------
    ValueError
        If the matrix is not square or does not match the required dimension.
    """
    arr = to_ndarray(matrix)
    if not is_square(arr):
        raise ValueError(f"Matrix must be square; got shape {arr.shape}.")

    if dim is not None and arr.shape != (dim, dim):
        raise ValueError(f"Matrix must be of shape ({dim}, {dim}); got {arr.shape}.")

    return arr


def compute_eigendecomposition(
    matrix: Iterable[Iterable[float]],
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute the eigenvalues and eigenvectors of a square matrix.

    Parameters
    ----------
    matrix :
        Square matrix as array-like.

    Returns
    -------
    eigenvalues, eigenvectors :
        Eigenvalues as a 1D complex array and eigenvectors as a 2D complex
        array whose columns are the eigenvectors.

    Raises
    ------
    ValueError
        If the matrix is not square.
    """
    arr = to_ndarray(matrix)
    if arr.shape[0] != arr.shape[1]:
        raise ValueError(f"Matrix must be square; got shape {arr.shape}.")
    eigenvalues, eigenvectors = np.linalg.eig(arr)
    return eigenvalues, eigenvectors


def format_eigendecomposition(
    eigenvalues: np.ndarray,
    eigenvectors: np.ndarray,
    precision: int = 3,
) -> str:
    """
    Format eigenvalues and eigenvectors as a human-readable string.

    Parameters
    ----------
    eigenvalues :
        1D array of eigenvalues.
    eigenvectors :
        2D array of eigenvectors (columns).
    precision :
        Number of decimal places.

    Returns
    -------
    str
        Multi-line formatted representation of the eigendecomposition.
    """
    if eigenvectors.ndim != 2:
        raise ValueError("Eigenvectors must be a 2D array.")

    n = eigenvalues.shape[0]
    if eigenvectors.shape[1] != n:
        raise ValueError("Eigenvectors must have one column per eigenvalue.")

    lines = []
    for i in range(n):
        val = eigenvalues[i]
        vec = eigenvectors[:, i]
        val_str = f"{val.real:.{precision}f}"
        if abs(val.imag) > 10 ** (-precision):
            val_str += f" + {val.imag:.{precision}f}i"
        vec_str = ", ".join(f"{c.real:.{precision}f}" for c in vec)
        lines.append(f"λ{i + 1} = {val_str}; v{i + 1} = [{vec_str}]")

    return "\n".join(lines)
