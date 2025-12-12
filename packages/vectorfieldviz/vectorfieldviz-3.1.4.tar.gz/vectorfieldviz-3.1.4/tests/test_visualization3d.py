import numpy as np

from vectorfieldviz.visualization3d import plot_3d_vector_field


def test_plot_3d_vector_field_basic():
    A = np.eye(3)
    fig = plot_3d_vector_field(A, grid_density=3)
    assert fig.data is not None
    assert len(fig.data) >= 1
