"""JAX implementation of the probabilistic Hough line transform."""

from typing import Optional

import jax
import jax.numpy as jnp
import numpy as np
from jaxtyping import Array, Float


def _probabilistic_hough_line_impl(
    image: Float[Array, "height width"],
    threshold: int,
    line_length: int,
    line_gap: int,
    theta: Float[Array, " num_theta"],
    rng: jax.Array,
    height: int,
    width: int,
):
    """JIT-compatible implementation of probabilistic Hough transform.

    Returns (lines, nlines) where lines is a (lines_max, 2, 2) array
    and nlines is the number of valid lines.
    """
    # Find nonzero pixels
    y_idxs, x_idxs = jnp.nonzero(image, size=height * width, fill_value=-1)
    valid_mask = y_idxs >= 0
    num_pixels = jnp.sum(valid_mask)

    # Compute sine and cosine of angles
    ctheta = jnp.cos(theta)
    stheta = jnp.sin(theta)

    # Compute accumulator dimensions
    max_distance = 2 * int(np.ceil(np.sqrt(height * height + width * width)))
    offset = max_distance // 2
    nthetas = theta.shape[0]

    # Initialize accumulator and mask
    accum = jnp.zeros((max_distance, nthetas), dtype=jnp.int32)
    mask = jnp.zeros((height, width), dtype=jnp.bool_)
    mask = mask.at[y_idxs, x_idxs].set(valid_mask)

    # Shuffle indices for all potential pixel positions
    max_pixels = height * width
    random_indices = jax.random.permutation(rng, max_pixels)

    # Clamp indices to valid range for x_idxs/y_idxs access
    # Use modulo to wrap indices - invalid pixels will be skipped by mask check
    clamped_indices = random_indices % jnp.maximum(num_pixels, 1)

    # Maximum number of lines
    lines_max = 2**15
    lines = jnp.zeros((lines_max, 2, 2), dtype=jnp.int32)

    shift = 16

    # State for the main loop
    initial_state = (
        num_pixels.astype(jnp.int32),
        mask,
        accum,
        lines,
        jnp.int32(0),
        x_idxs,
        y_idxs,
        clamped_indices,
    )

    def cond_fn(state):
        count, mask, accum, lines, nlines, x_idxs, y_idxs, indices = state
        return (count > 0) & (nlines < lines_max)

    def body_fn(state):
        count, mask, accum, lines, nlines, x_idxs, y_idxs, indices = state
        count = count - 1

        # Select random non-zero point (index is clamped to valid range)
        index = indices[count]
        x = x_idxs[index]
        y = y_idxs[index]

        # Check if previously eliminated
        is_valid = mask[y, x]

        # Apply Hough transform on point (always update accumulator for valid points)
        def apply_hough(carry, j):
            accum, max_value, max_theta = carry
            accum_idx = jnp.round(ctheta[j] * x + stheta[j] * y).astype(jnp.int32) + offset
            # Only increment if this point is valid
            new_accum = jnp.where(is_valid, accum.at[accum_idx, j].add(1), accum)
            value = new_accum[accum_idx, j]
            new_max_value = jnp.where(value > max_value, value, max_value)
            new_max_theta = jnp.where(value > max_value, j, max_theta)
            return (new_accum, new_max_value, new_max_theta), None

        (accum, max_value, max_theta), _ = jax.lax.scan(
            apply_hough,
            (accum, jnp.int32(threshold - 1), jnp.int32(-1)),
            jnp.arange(nthetas),
        )

        # Only proceed to line detection if valid and threshold met
        proceed = is_valid & (max_value >= threshold)

        # Calculate line direction
        a = -stheta[max_theta]
        b = ctheta[max_theta]

        xflag = jnp.abs(a) > jnp.abs(b)

        # Calculate gradient using fixed point math
        dx0 = jnp.where(
            xflag,
            jnp.where(a > 0, 1, -1),
            jnp.round(a * (1 << shift) / jnp.maximum(jnp.abs(b), 1e-10)).astype(jnp.int32),
        )
        dy0 = jnp.where(
            xflag,
            jnp.round(b * (1 << shift) / jnp.maximum(jnp.abs(a), 1e-10)).astype(jnp.int32),
            jnp.where(b > 0, 1, -1),
        )

        x0 = jnp.where(xflag, x, (x << shift) + (1 << (shift - 1)))
        y0 = jnp.where(xflag, (y << shift) + (1 << (shift - 1)), y)

        # Walk the line in both directions to find endpoints
        def walk_line(carry, _):
            px, py, gap, line_end_x, line_end_y, dx, dy, found_start = carry

            x1 = jnp.where(xflag, px, px >> shift)
            y1 = jnp.where(xflag, py >> shift, py)

            in_bounds = (x1 >= 0) & (x1 < width) & (y1 >= 0) & (y1 < height)
            pixel_set = jnp.where(in_bounds, mask[y1, x1], False)

            new_gap = jnp.where(pixel_set, 0, gap + 1)
            new_line_end_x = jnp.where(pixel_set & in_bounds, x1, line_end_x)
            new_line_end_y = jnp.where(pixel_set & in_bounds, y1, line_end_y)

            # Continue if in bounds and gap not too large
            continue_walk = in_bounds & (new_gap <= line_gap)

            new_px = jnp.where(continue_walk, px + dx, px)
            new_py = jnp.where(continue_walk, py + dy, py)

            return (
                new_px,
                new_py,
                new_gap,
                new_line_end_x,
                new_line_end_y,
                dx,
                dy,
                found_start | pixel_set,
            ), None

        # Maximum walk distance
        max_walk = height + width

        # Walk forward (k=0)
        init_forward = (x0, y0, jnp.int32(0), x, y, dx0, dy0, jnp.bool_(False))
        (_, _, _, end0_x, end0_y, _, _, _), _ = jax.lax.scan(
            walk_line, init_forward, None, length=max_walk
        )

        # Walk backward (k=1)
        init_backward = (x0, y0, jnp.int32(0), x, y, -dx0, -dy0, jnp.bool_(False))
        (_, _, _, end1_x, end1_y, _, _, _), _ = jax.lax.scan(
            walk_line, init_backward, None, length=max_walk
        )

        # Check line length
        line_len_x = jnp.abs(end1_x - end0_x)
        line_len_y = jnp.abs(end1_y - end0_y)
        good_line = proceed & ((line_len_x >= line_length) | (line_len_y >= line_length))

        # Update mask by walking the line again and clearing pixels
        def clear_line_pixel(mask_accum, _):
            curr_mask, px, py, dx, dy, reached_end, end_x, end_y = mask_accum

            x1 = jnp.where(xflag, px, px >> shift)
            y1 = jnp.where(xflag, py >> shift, py)

            in_bounds = (x1 >= 0) & (x1 < width) & (y1 >= 0) & (y1 < height)
            at_end = (x1 == end_x) & (y1 == end_y)
            should_clear = in_bounds & ~reached_end & good_line

            new_mask = jnp.where(should_clear, curr_mask.at[y1, x1].set(False), curr_mask)
            new_reached_end = reached_end | at_end

            new_px = jnp.where(~reached_end, px + dx, px)
            new_py = jnp.where(~reached_end, py + dy, py)

            return (
                new_mask,
                new_px,
                new_py,
                dx,
                dy,
                new_reached_end,
                end_x,
                end_y,
            ), None

        # Clear forward direction
        init_clear_forward = (mask, x0, y0, dx0, dy0, jnp.bool_(False), end0_x, end0_y)
        (mask_cleared, _, _, _, _, _, _, _), _ = jax.lax.scan(
            clear_line_pixel, init_clear_forward, None, length=max_walk
        )

        # Clear backward direction
        init_clear_backward = (
            mask_cleared,
            x0,
            y0,
            -dx0,
            -dy0,
            jnp.bool_(False),
            end1_x,
            end1_y,
        )
        (mask_cleared2, _, _, _, _, _, _, _), _ = jax.lax.scan(
            clear_line_pixel, init_clear_backward, None, length=max_walk
        )

        # Update mask only if we found a good line
        final_mask = jnp.where(good_line, mask_cleared2, mask)

        # Add line to results
        new_lines = (
            lines.at[nlines, 0, 0]
            .set(end0_x)
            .at[nlines, 0, 1]
            .set(end0_y)
            .at[nlines, 1, 0]
            .set(end1_x)
            .at[nlines, 1, 1]
            .set(end1_y)
        )
        final_lines = jnp.where(good_line, new_lines, lines)
        final_nlines = jnp.where(good_line, nlines + 1, nlines)

        return (
            count,
            final_mask,
            accum,
            final_lines,
            final_nlines,
            x_idxs,
            y_idxs,
            indices,
        )

    # Run the main loop
    final_state = jax.lax.while_loop(cond_fn, body_fn, initial_state)
    _, _, _, lines_result, nlines_result, _, _, _ = final_state

    return lines_result, nlines_result


def probabilistic_hough_line(
    image: Float[Array, "height width"],
    threshold: int = 10,
    line_length: int = 50,
    line_gap: int = 10,
    theta: Optional[Float[Array, " num_theta"]] = None,
    rng: Optional[jax.Array] = None,
) -> tuple[Float[Array, "lines_max 2 2"], Float[Array, ""]]:
    """Compute the probabilistic Hough transform for lines in an image.

    Args:
        image: The input image with nonzero values representing edges.
        threshold: Minimum accumulator value to consider a line.
        line_length: Minimum accepted length of detected lines.
        line_gap: Maximum gap between pixels to still form a line.
        theta: Angles at which to compute the transform, in radians.
        rng: JAX random key.

    Returns:
        A tuple (lines, nlines) where:
        - lines: Array of shape (lines_max, 2, 2) containing line endpoints
          in format [[x0, y0], [x1, y1]]. Only the first nlines entries are valid.
        - nlines: Scalar indicating the number of valid lines detected.
    """
    if image.ndim != 2:
        raise ValueError("The input image must be 2D.")

    if theta is None:
        theta = jnp.linspace(-jnp.pi / 2, jnp.pi / 2, 180, endpoint=False)

    if rng is None:
        rng = jax.random.PRNGKey(0)

    height, width = image.shape
    return _probabilistic_hough_line_impl(
        image, threshold, line_length, line_gap, theta, rng, height, width
    )
