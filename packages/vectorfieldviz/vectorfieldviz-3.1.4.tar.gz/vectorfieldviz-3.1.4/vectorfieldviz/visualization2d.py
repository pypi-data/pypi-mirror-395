"""
2D vector field visualization for 2×2 matrices using Plotly.
"""

from __future__ import annotations

from typing import Iterable, Optional, Tuple, Dict

import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go

from .analysis import validate_matrix, compute_eigendecomposition
from .utils import default_2d_colors, real_eigen_pairs


def _generate_2d_grid(
    x_range: Tuple[float, float],
    y_range: Tuple[float, float],
    density: int,
) -> Tuple[np.ndarray, np.ndarray]:
    x = np.linspace(x_range[0], x_range[1], density)
    y = np.linspace(y_range[0], y_range[1], density)
    X, Y = np.meshgrid(x, y)
    return X, Y


def plot_2d_vector_field(
    A: Iterable[Iterable[float]],
    x_range: Tuple[float, float] = (-5.0, 5.0),
    y_range: Tuple[float, float] = (-5.0, 5.0),
    grid_density: int = 20,
    arrow_scale: float = 0.15,
    show_eigenvectors: bool = True,
    eigenvector_scale: float = 1.0,
    colors: Optional[Dict[str, object]] = None,
    width: int = 700,
    height: int = 700,
    title: Optional[str] = None,
) -> go.Figure:
    """
    Plot a 2D vector field defined by a 2×2 matrix A using Plotly.

    The field is given by F(x) = A x, where x ∈ ℝ².

    Parameters
    ----------
    A :
        2×2 matrix (array-like).
    x_range :
        (min, max) range for x-axis.
    y_range :
        (min, max) range for y-axis.
    grid_density :
        Number of grid points per axis.
    arrow_scale :
        Scaling factor for arrow lengths.
    show_eigenvectors :
        Whether to overlay eigenvectors.
    eigenvector_scale :
        Scaling of eigenvector lines relative to plot extents.
    colors :
        Optional color configuration dictionary. See `default_2d_colors`.
    width, height :
        Figure dimensions in pixels.
    title :
        Plot title. If None, a default title is used.

    Returns
    -------
    plotly.graph_objects.Figure
        Plotly figure object.
    """
    A_arr = validate_matrix(A, dim=2)
    colors = colors or default_2d_colors()

    # Grid
    X, Y = _generate_2d_grid(x_range, y_range, grid_density)
    points = np.vstack([X.ravel(), Y.ravel()])
    vectors = A_arr @ points
    U = vectors[0, :].reshape(X.shape)
    V = vectors[1, :].reshape(Y.shape)

    # Quiver-like arrow field
    fig = ff.create_quiver(
        X,
        Y,
        U,
        V,
        scale=arrow_scale,
        arrow_scale=0.4,
        line_color=colors["field"],
    )

    # Eigen decomposition for annotations and optional overlay
    evals, evecs = compute_eigendecomposition(A_arr)
    evals_real, evecs_real = real_eigen_pairs(evals, evecs)

    # Overlay eigenvectors
    if show_eigenvectors and evecs_real.size > 0:
        max_extent = max(
            abs(x_range[0]),
            abs(x_range[1]),
            abs(y_range[0]),
            abs(y_range[1]),
        )
        length = eigenvector_scale * max_extent

        eigen_colors = colors.get("eigenvectors", [])
        if not eigen_colors:
            eigen_colors = ["red", "green", "orange", "purple"]

        for i in range(evecs_real.shape[1]):
            v = evecs_real[:, i]
            v = v / np.linalg.norm(v)
            c = eigen_colors[i % len(eigen_colors)]

            # Draw in both directions from origin
            x_vals = [-length * v[0], length * v[0]]
            y_vals = [-length * v[1], length * v[1]]

            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=y_vals,
                    mode="lines",
                    line=dict(color=c, width=3),
                    name=f"Eigenvector {i + 1}",
                )
            )

    # Eigenvalue annotations (compact)
    eval_text = ", ".join(f"{lam:.3g}" for lam in evals_real)
    annotation_text = f"Real eigenvalues: {eval_text}" if evals_real.size else "No real eigenvalues"

    fig.update_layout(
        width=width,
        height=height,
        title=title or "2D Linear Vector Field",
        xaxis=dict(
            range=list(x_range),
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="black",
        ),
        yaxis=dict(
            range=list(y_range),
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="black",
            scaleanchor="x",
            scaleratio=1,
        ),
        plot_bgcolor=colors.get("background", "white"),
        showlegend=True,
        annotations=[
            dict(
                x=0.01,
                y=0.99,
                xref="paper",
                yref="paper",
                text=annotation_text,
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


def interactive_2d_matrix_explorer(
    initial_matrix: Iterable[Iterable[float]] | None = None,
    x_range: Tuple[float, float] = (-5.0, 5.0),
    y_range: Tuple[float, float] = (-5.0, 5.0),
    grid_density: int = 20,
) -> None:
    """
    Create a simple Jupyter-based interactive explorer for 2×2 matrices.

    Requires `ipywidgets` and a Jupyter environment. Sliders control the
    2×2 matrix entries and update the vector field and eigenvectors in real time.

    Parameters
    ----------
    initial_matrix :
        Optional initial 2×2 matrix. Defaults to identity.
    x_range, y_range :
        Plot ranges.
    grid_density :
        Grid density for quiver plot.

    Notes
    -----
    This function uses `IPython.display.display` and `ipywidgets`.
    It has no effect outside a Jupyter-like environment.
    """
    try:
        import ipywidgets as widgets
        from IPython.display import display
    except ImportError as exc:
        raise ImportError(
            "interactive_2d_matrix_explorer requires `ipywidgets` and "
            "`IPython`. Install with `pip install ipywidgets`."
        ) from exc

    if initial_matrix is None:
        initial_matrix = [[1.0, 0.0], [0.0, 1.0]]
    A0 = validate_matrix(initial_matrix, dim=2)

    # Sliders for each entry
    slider_kwargs = dict(min=-5.0, max=5.0, step=0.1, continuous_update=False)
    a11 = widgets.FloatSlider(value=A0[0, 0], description="a11", **slider_kwargs)
    a12 = widgets.FloatSlider(value=A0[0, 1], description="a12", **slider_kwargs)
    a21 = widgets.FloatSlider(value=A0[1, 0], description="a21", **slider_kwargs)
    a22 = widgets.FloatSlider(value=A0[1, 1], description="a22", **slider_kwargs)

    out = widgets.Output()

    def update_plot(*_):
        with out:
            out.clear_output(wait=True)
            A = [[a11.value, a12.value], [a21.value, a22.value]]
            fig = plot_2d_vector_field(
                A,
                x_range=x_range,
                y_range=y_range,
                grid_density=grid_density,
                title=f"A = [[{a11.value:.1f}, {a12.value:.1f}], [{a21.value:.1f}, {a22.value:.1f}]]",
            )
            fig.show()

    for s in (a11, a12, a21, a22):
        s.observe(update_plot, names="value")

    # Initial draw
    update_plot()

    controls = widgets.VBox([a11, a12, a21, a22])
    display(widgets.HBox([controls, out]))
