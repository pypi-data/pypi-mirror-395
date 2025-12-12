"""Simple example of using hough_jax to detect lines in an image."""

import jax
import jax.numpy as jnp
import numpy as np
from hough_jax import probabilistic_hough_line

# Create a simple image with a horizontal line
image = np.zeros((100, 100), dtype=np.float32)
image[50, 20:80] = 1.0

# Detect lines
lines, nlines = probabilistic_hough_line(
    jnp.array(image),
    threshold=10,
    line_length=30,
    line_gap=3,
    rng=jax.random.PRNGKey(0),
)

# lines: Array of shape (lines_max, 2, 2) with endpoints [[x0, y0], [x1, y1]]
# nlines: Number of valid lines detected
print(f"Detected {int(nlines)} line(s)")
for i in range(int(nlines)):
    x0, y0 = lines[i, 0]
    x1, y1 = lines[i, 1]
    print(f"  Line {i + 1}: ({int(x0)}, {int(y0)}) -> ({int(x1)}, {int(y1)})")


# To get the same output format as skimage.transform.probabilistic_hough_line:
def to_skimage_format(lines, nlines):
    """Convert JAX output to skimage format: list of ((x0, y0), (x1, y1)) tuples."""
    n = int(nlines)
    return [
        ((int(lines[i, 0, 0]), int(lines[i, 0, 1])), (int(lines[i, 1, 0]), int(lines[i, 1, 1])))
        for i in range(n)
    ]


print("\nIn skimage format:")
print(to_skimage_format(lines, nlines))
