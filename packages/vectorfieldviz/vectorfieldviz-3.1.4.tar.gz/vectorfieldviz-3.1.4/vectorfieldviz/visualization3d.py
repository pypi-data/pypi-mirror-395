"""
3D vector field visualization for 3×3 matrices using Plotly.
"""

from __future__ import annotations

from typing import Iterable, Optional, Tuple, Dict

import numpy as np
import plotly.graph_objects as go

from .analysis import validate_matrix, compute_eigendecomposition
from .utils import default_3d_colors, real_eigen_pairs


def _generate_3d_grid(
    x_range: Tuple[float, float],
    y_range: Tuple[float, float],
    z_range: Tuple[float, float],
    density: int,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = np.linspace(x_range[0], x_range[1], density)
    y = np.linspace(y_range[0], y_range[1], density)
    z = np.linspace(z_range[0], z_range[1], density)
    X, Y, Z = np.meshgrid(x, y, z)
    return X, Y, Z


def plot_3d_vector_field(
    A: Iterable[Iterable[float]],
    x_range: Tuple[float, float] = (-3.0, 3.0),
    y_range: Tuple[float, float] = (-3.0, 3.0),
    z_range: Tuple[float, float] = (-3.0, 3.0),
    grid_density: int = 6,
    arrow_scale: float = 0.5,
    show_eigenvectors: bool = True,
    eigenvector_scale: float = 1.0,
    colors: Optional[Dict[str, object]] = None,
    width: int = 800,
    height: int = 700,
    title: Optional[str] = None,
) -> go.Figure:
    """
    Plot a 3D vector field defined by a 3×3 matrix A using Plotly.

    The field is given by F(x) = A x, where x ∈ ℝ³.

    Parameters
    ----------
    A :
        3×3 matrix (array-like).
    x_range, y_range, z_range :
        Axis ranges.
    grid_density :
        Number of grid points on each axis.
    arrow_scale :
        Scaling factor for cone sizes.
    show_eigenvectors :
        Whether to overlay eigenvectors.
    eigenvector_scale :
        Scaling of eigenvector lines relative to plot extents.
    colors :
        Optional color configuration dictionary. See `default_3d_colors`.
    width, height :
        Figure dimensions in pixels.
    title :
        Plot title. If None, a default title is used.

    Returns
    -------
    plotly.graph_objects.Figure
        Plotly figure object.
    """
    A_arr = validate_matrix(A, dim=3)
    colors = colors or default_3d_colors()

    # Grid
    X, Y, Z = _generate_3d_grid(x_range, y_range, z_range, grid_density)
    points = np.vstack([X.ravel(), Y.ravel(), Z.ravel()])
    vectors = A_arr @ points
    U = vectors[0, :].reshape(X.shape)
    V = vectors[1, :].reshape(Y.shape)
    W = vectors[2, :].reshape(Z.shape)

    # 3D cones for vector field
    fig = go.Figure(
        data=[
            go.Cone(
                x=X.ravel(),
                y=Y.ravel(),
                z=Z.ravel(),
                u=U.ravel(),
                v=V.ravel(),
                w=W.ravel(),
                sizemode="scaled",
                sizeref=arrow_scale,
                colorscale=colors["field"],
                showscale=False,
                name="Vector field",
            )
        ]
    )

    evals, evecs = compute_eigendecomposition(A_arr)
    evals_real, evecs_real = real_eigen_pairs(evals, evecs)

    # Overlay eigenvectors
    if show_eigenvectors and evecs_real.size > 0:
        max_extent = max(
            abs(x_range[0]),
            abs(x_range[1]),
            abs(y_range[0]),
            abs(y_range[1]),
            abs(z_range[0]),
            abs(z_range[1]),
        )
        length = eigenvector_scale * max_extent

        eigen_colors = colors.get("eigenvectors", [])
        if not eigen_colors:
            eigen_colors = ["red", "green", "orange"]

        for i in range(evecs_real.shape[1]):
            v = evecs_real[:, i]
            v = v / np.linalg.norm(v)
            c = eigen_colors[i % len(eigen_colors)]

            x_vals = [-length * v[0], length * v[0]]
            y_vals = [-length * v[1], length * v[1]]
            z_vals = [-length * v[2], length * v[2]]

            fig.add_trace(
                go.Scatter3d(
                    x=x_vals,
                    y=y_vals,
                    z=z_vals,
                    mode="lines",
                    line=dict(color=c, width=8),
                    name=f"Eigenvector {i + 1}",
                )
            )

    # Eigenvalue annotation
    if evals_real.size > 0:
        eval_text = "<br>".join(
            [f"λ{i + 1} = {lam:.3g}" for i, lam in enumerate(evals_real)]
        )
    else:
        eval_text = "No real eigenvalues"

    fig.update_layout(
        width=width,
        height=height,
        title=title or "3D Linear Vector Field",
        scene=dict(
            xaxis=dict(range=list(x_range), zeroline=True),
            yaxis=dict(range=list(y_range), zeroline=True),
            zaxis=dict(range=list(z_range), zeroline=True),
            bgcolor=colors.get("background", "white"),
        ),
        showlegend=True,
        annotations=[
            dict(
                x=0.01,
                y=0.99,
                xref="paper",
                yref="paper",
                text=eval_text,
                showarrow=False,
                align="left",
                bordercolor="black",
                borderwidth=1,
                bgcolor="rgba(255,255,255,0.7)",
                font=dict(size=10),
            )
        ],
    )

    return fig
