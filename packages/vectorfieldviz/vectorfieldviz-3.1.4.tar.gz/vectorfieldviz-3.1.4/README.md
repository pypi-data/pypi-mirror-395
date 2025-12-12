# vectorfieldviz

Visualization toolkit for linear vector fields defined by 2×2 and 3×3 matrices,
with eigenanalysis utilities. Built on NumPy and Plotly.

## Installation

```bash
pip install vectorfieldviz

```

Source          =       https://gitlab.com/algebra-done-visually/vectorfieldviz


## 2D
```

import numpy as np
from vectorfieldviz import plot_2d_vector_field, compute_eigendecomposition, plot_3d_vector_field

A = np.array([[0.0, 1.0, 1.0],
              [1.0, 1.0, 1.0],
              [1.0, 0.0, 0.0]])

fig = plot_3d_vector_field(A)

fig.show()

```
![2D - Vector Field](https://gitlab.com/algebra-done-visually/vectorfieldviz/-/raw/master/images/img_1.png)


## 3D
```
import numpy as np
from vectorfieldviz import plot_2d_vector_field, compute_eigendecomposition, plot_3d_vector_field

A = np.array([[0.0, 1.0, 1.0],
              [1.0, 1.0, 1.0],
              [1.0, 0.0, 0.0]])

fig = plot_3d_vector_field(A)

fig.show()
```

![3D - Vector Field](https://gitlab.com/algebra-done-visually/vectorfieldviz/-/raw/master/images/img.png)