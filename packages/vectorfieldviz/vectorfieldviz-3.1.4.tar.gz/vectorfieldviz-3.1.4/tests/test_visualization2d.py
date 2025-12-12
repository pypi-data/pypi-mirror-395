import numpy as np

from vectorfieldviz.visualization2d import plot_2d_vector_field


def test_plot_2d_vector_field_basic():
    A = np.array([[0.0, -1.0], [1.0, 0.0]])
    fig = plot_2d_vector_field(A, grid_density=5)
    # Smoke test: ensure we get a Figure with data
    assert fig.data is not None
    assert len(fig.data) >= 1
