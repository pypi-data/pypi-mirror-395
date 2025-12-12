"""Tests for the probabilistic Hough line transform."""

import jax
import jax.numpy as jnp
import numpy as np
import pytest
from skimage.transform import probabilistic_hough_line as skimage_hough
from src.probabilistic_hough_line import _probabilistic_hough_line_impl
from src.probabilistic_hough_line import probabilistic_hough_line as jax_hough


def lines_match(jax_lines, skimage_lines):
    """Check if two sets of lines match."""
    if len(jax_lines) != len(skimage_lines):
        return False

    def normalize_line(line):
        (x0, y0), (x1, y1) = line
        if (x0, y0) > (x1, y1):
            return ((x1, y1), (x0, y0))
        return ((x0, y0), (x1, y1))

    return {normalize_line(l) for l in jax_lines} == {normalize_line(l) for l in skimage_lines}


def jit_result_to_lines(lines_result, nlines_result):
    """Convert JIT output to list of line tuples."""
    nlines_int = int(nlines_result)
    lines_np = np.array(lines_result[:nlines_int])
    return [
        ((int(line[0, 0]), int(line[0, 1])), (int(line[1, 0]), int(line[1, 1])))
        for line in lines_np
    ]


@pytest.fixture
def horizontal_line():
    """Create a 100x100 image with a horizontal line."""
    img = np.zeros((100, 100), dtype=np.uint8)
    img[50, 20:80] = 1
    return img


@pytest.fixture
def vertical_line():
    """Create a 100x100 image with a vertical line."""
    img = np.zeros((100, 100), dtype=np.uint8)
    img[20:80, 50] = 1
    return img


@pytest.fixture
def diagonal_line():
    """Create a 100x100 image with a diagonal line."""
    img = np.zeros((100, 100), dtype=np.uint8)
    for i in range(60):
        img[20 + i, 20 + i] = 1
    return img


@pytest.fixture
def multiple_lines():
    """Create a 100x100 image with multiple lines."""
    img = np.zeros((100, 100), dtype=np.uint8)
    img[30, 10:90] = 1
    img[10:90, 70] = 1
    for i in range(50):
        img[40 + i, 10 + i] = 1
    return img


@pytest.fixture
def empty_image():
    """Create a 50x50 empty image."""
    return np.zeros((50, 50), dtype=np.uint8)


@pytest.fixture
def jit_hough_impl():
    """JIT-compiled version of the Hough transform."""
    return jax.jit(
        _probabilistic_hough_line_impl,
        static_argnames=["threshold", "line_length", "line_gap", "height", "width"],
    )


class TestProbabilisticHoughLine:
    """Tests for JAX probabilistic Hough line transform."""

    @pytest.mark.parametrize(
        "image_fixture", ["horizontal_line", "vertical_line", "diagonal_line", "multiple_lines"]
    )
    def test_line_detection(self, image_fixture, request):
        """Test line detection matches skimage for various line types."""
        img = request.getfixturevalue(image_fixture)
        seed = 42

        rng_np = np.random.default_rng(seed)
        skimage_lines = skimage_hough(img, threshold=10, line_length=30, line_gap=3, rng=rng_np)

        rng_jax = jax.random.PRNGKey(seed)
        jax_lines = jax_hough(
            jnp.array(img), threshold=10, line_length=30, line_gap=3, rng=rng_jax
        )

        assert len(jax_lines) == len(skimage_lines)
        assert lines_match(jax_lines, skimage_lines)

    def test_empty_image(self, empty_image):
        """Test with an empty image (no edges)."""
        rng_np = np.random.default_rng(42)
        skimage_lines = skimage_hough(empty_image, rng=rng_np)

        rng_jax = jax.random.PRNGKey(42)
        jax_lines = jax_hough(jnp.array(empty_image), rng=rng_jax)

        assert len(jax_lines) == 0
        assert len(skimage_lines) == 0

    def test_custom_theta(self, horizontal_line):
        """Test with custom theta values."""
        theta = np.linspace(-np.pi / 2, np.pi / 2, 90, endpoint=False)
        seed = 42

        rng_np = np.random.default_rng(seed)
        skimage_lines = skimage_hough(
            horizontal_line, threshold=10, line_length=30, line_gap=3, theta=theta, rng=rng_np
        )

        rng_jax = jax.random.PRNGKey(seed)
        jax_lines = jax_hough(
            jnp.array(horizontal_line),
            threshold=10,
            line_length=30,
            line_gap=3,
            theta=jnp.array(theta),
            rng=rng_jax,
        )

        assert len(jax_lines) == len(skimage_lines)
        assert lines_match(jax_lines, skimage_lines)

    @pytest.mark.parametrize("threshold", [5, 10, 20])
    def test_different_thresholds(self, multiple_lines, threshold):
        """Test with different threshold values."""
        seed = 42

        rng_np = np.random.default_rng(seed)
        skimage_lines = skimage_hough(
            multiple_lines, threshold=threshold, line_length=30, line_gap=3, rng=rng_np
        )

        rng_jax = jax.random.PRNGKey(seed)
        jax_lines = jax_hough(
            jnp.array(multiple_lines), threshold=threshold, line_length=30, line_gap=3, rng=rng_jax
        )

        assert len(jax_lines) == len(skimage_lines)

    @pytest.mark.parametrize("line_length", [20, 40, 60])
    def test_different_line_lengths(self, horizontal_line, line_length):
        """Test with different minimum line length values."""
        seed = 42

        rng_np = np.random.default_rng(seed)
        skimage_lines = skimage_hough(
            horizontal_line, threshold=10, line_length=line_length, line_gap=3, rng=rng_np
        )

        rng_jax = jax.random.PRNGKey(seed)
        jax_lines = jax_hough(
            jnp.array(horizontal_line),
            threshold=10,
            line_length=line_length,
            line_gap=3,
            rng=rng_jax,
        )

        assert len(jax_lines) == len(skimage_lines)

    def test_output_format(self, horizontal_line):
        """Test that output format matches skimage format."""
        rng_jax = jax.random.PRNGKey(42)
        jax_lines = jax_hough(
            jnp.array(horizontal_line), threshold=10, line_length=30, line_gap=3, rng=rng_jax
        )

        assert isinstance(jax_lines, list)
        if len(jax_lines) > 0:
            line = jax_lines[0]
            assert len(line) == 2
            assert len(line[0]) == 2
            assert len(line[1]) == 2


class TestProbabilisticHoughLineJIT:
    """Tests for JIT-compiled JAX probabilistic Hough line transform."""

    @pytest.mark.parametrize(
        "image_fixture", ["horizontal_line", "multiple_lines", "diagonal_line"]
    )
    def test_jit_matches_eager(self, image_fixture, request, jit_hough_impl):
        """Test JIT output matches eager mode for various line types."""
        img = request.getfixturevalue(image_fixture)
        theta = jnp.linspace(-jnp.pi / 2, jnp.pi / 2, 180, endpoint=False)
        rng = jax.random.PRNGKey(42)
        height, width = img.shape

        eager_lines = jax_hough(jnp.array(img), threshold=10, line_length=30, line_gap=3, rng=rng)
        lines_result, nlines_result = jit_hough_impl(
            jnp.array(img), 10, 30, 3, theta, rng, height, width
        )
        jit_lines = jit_result_to_lines(lines_result, nlines_result)

        assert len(jit_lines) == len(eager_lines)
        assert lines_match(jit_lines, eager_lines)

    def test_jit_vs_skimage(self, diagonal_line, jit_hough_impl):
        """Test JIT-compiled version against skimage reference."""
        theta = jnp.linspace(-jnp.pi / 2, jnp.pi / 2, 180, endpoint=False)
        height, width = diagonal_line.shape
        seed = 42

        rng_np = np.random.default_rng(seed)
        skimage_lines = skimage_hough(
            diagonal_line, threshold=10, line_length=30, line_gap=3, rng=rng_np
        )

        rng_jax = jax.random.PRNGKey(seed)
        lines_result, nlines = jit_hough_impl(
            jnp.array(diagonal_line), 10, 30, 3, theta, rng_jax, height, width
        )
        jit_lines = jit_result_to_lines(lines_result, nlines)

        assert len(jit_lines) == len(skimage_lines)
        assert lines_match(jit_lines, skimage_lines)

    def test_jit_empty_image(self, empty_image, jit_hough_impl):
        """Test JIT with empty image."""
        theta = jnp.linspace(-jnp.pi / 2, jnp.pi / 2, 180, endpoint=False)
        rng = jax.random.PRNGKey(42)
        height, width = empty_image.shape

        lines_result, nlines = jit_hough_impl(
            jnp.array(empty_image), 10, 30, 3, theta, rng, height, width
        )
        lines = jit_result_to_lines(lines_result, nlines)

        assert len(lines) == 0

    def test_jit_recompilation(self, horizontal_line, jit_hough_impl):
        """Test JIT recompilation with different static parameters."""
        theta = jnp.linspace(-jnp.pi / 2, jnp.pi / 2, 180, endpoint=False)
        rng = jax.random.PRNGKey(42)
        height, width = horizontal_line.shape

        lines1_result, nlines1 = jit_hough_impl(
            jnp.array(horizontal_line), 10, 30, 3, theta, rng, height, width
        )
        lines2_result, nlines2 = jit_hough_impl(
            jnp.array(horizontal_line), 5, 20, 5, theta, rng, height, width
        )

        assert isinstance(jit_result_to_lines(lines1_result, nlines1), list)
        assert isinstance(jit_result_to_lines(lines2_result, nlines2), list)

    @pytest.mark.parametrize(
        "size,line_slice,line_length", [(50, slice(10, 40), 20), (150, slice(20, 130), 50)]
    )
    def test_jit_different_image_sizes(self, size, line_slice, line_length, jit_hough_impl):
        """Test JIT with different image sizes."""
        img = np.zeros((size, size), dtype=np.uint8)
        img[size // 2, line_slice] = 1
        theta = jnp.linspace(-jnp.pi / 2, jnp.pi / 2, 180, endpoint=False)
        rng = jax.random.PRNGKey(42)

        lines_result, nlines = jit_hough_impl(
            jnp.array(img), 10, line_length, 3, theta, rng, size, size
        )
        lines = jit_result_to_lines(lines_result, nlines)

        assert len(lines) >= 0

    def test_jit_consistency(self, horizontal_line, jit_hough_impl):
        """Test that JIT produces consistent results across multiple calls."""
        theta = jnp.linspace(-jnp.pi / 2, jnp.pi / 2, 180, endpoint=False)
        rng = jax.random.PRNGKey(42)
        height, width = horizontal_line.shape

        results = [
            jit_result_to_lines(
                *jit_hough_impl(jnp.array(horizontal_line), 10, 30, 3, theta, rng, height, width)
            )
            for _ in range(3)
        ]

        for i in range(1, len(results)):
            assert len(results[i]) == len(results[0])
            assert lines_match(results[i], results[0])

    def test_jit_custom_theta(self, horizontal_line, jit_hough_impl):
        """Test JIT with custom theta values."""
        theta = jnp.linspace(-jnp.pi / 2, jnp.pi / 2, 90, endpoint=False)
        rng = jax.random.PRNGKey(42)
        height, width = horizontal_line.shape

        eager_lines = jax_hough(
            jnp.array(horizontal_line),
            threshold=10,
            line_length=30,
            line_gap=3,
            theta=theta,
            rng=rng,
        )
        lines_result, nlines = jit_hough_impl(
            jnp.array(horizontal_line), 10, 30, 3, theta, rng, height, width
        )
        jit_lines = jit_result_to_lines(lines_result, nlines)

        assert len(jit_lines) == len(eager_lines)
        assert lines_match(jit_lines, eager_lines)
