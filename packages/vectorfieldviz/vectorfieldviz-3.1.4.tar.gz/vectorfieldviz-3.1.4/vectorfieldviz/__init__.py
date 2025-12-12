"""
vectorfieldviz
==============

A small library for visualizing 2D and 3D linear vector fields defined by
2×2 and 3×3 matrices, with eigenanalysis utilities.
"""

from .analysis import (
    compute_eigendecomposition,
    validate_matrix,
    format_eigendecomposition,
)
from .visualization2d import (
    plot_2d_vector_field,
    interactive_2d_matrix_explorer,
)
from .visualization3d import (
    plot_3d_vector_field,
)
from .utils import __version__

__all__ = [
    "compute_eigendecomposition",
    "validate_matrix",
    "format_eigendecomposition",
    "plot_2d_vector_field",
    "interactive_2d_matrix_explorer",
    "plot_3d_vector_field",
    "__version__",
]
