from numpy.typing import NDArray
from numpy.typing import NDArray
from numba import njit
import numpy as np
import math


@njit
def simon(a: float, b: float, n: int) -> tuple[NDArray, NDArray]:
    """calculates the simon attractor

    Args:
        a (float): inital point of the system
        b (float): inital point of the system
        n (int): iterations

    Returns:
        tuple[ndarray, ndarray]: arr_x, arr_y
        # arr_x[i], arr_y[i] => x, y at iteration i
    """
    x, y = a, b

    arr_x = np.zeros(shape=(n,), dtype=np.float64)
    arr_y = np.zeros(shape=(n,), dtype=np.float64)
    for i in range(n):
        x_new = math.sin(x**2 - y**2 + a)
        y_new = math.cos(2 * x * y + b)

        x, y = x_new, y_new
        arr_x[i] = x
        arr_y[i] = y

    return arr_x, arr_y


@njit
def clifford(a: float, b: float, c: float, d: float, n: int) -> tuple[NDArray, NDArray]:
    x = 0.0
    y = 0.0

    arr_x = np.zeros(shape=(n,), dtype=np.float64)
    arr_y = np.zeros(shape=(n,), dtype=np.float64)

    for i in range(n):
        x_new = math.sin(a * y) + c * math.cos(a * x)
        y_new = math.sin(b * x) + d * math.cos(b * y)

        x, y = x_new, y_new
        arr_x[i] = x
        arr_y[i] = y
    return arr_x, arr_y


def render_simon(
    resolution: int,
    a: float,
    b: float,
    n: int,
    percentile: float,
) -> NDArray:
    """
    Computes the Simon Attractor and returns a normalized histogram

    Args:
        resolution (int): Resolution of the output grid (res x res).
        a (float): Parameter 'a' for the Simon Attractor.
        b (float): Parameter 'b' for the Simon Attractor.
        n (int): Number of iterations. Higher values yield smoother output; usually n > 1_000_000.
        percentile (float): Clipping percentile for histogram normalization (e.g., 95-99.9).

    Returns:
        NDArray[np.float32]
    """
    # calculate
    x_raw, y_raw = simon(a, b, n)
    points_per_pixel = np.histogram2d(x_raw, y_raw, bins=resolution)[0]

    # clip outliers
    max_value = np.percentile(points_per_pixel, percentile)
    max_value = max_value if np.isfinite(max_value) and max_value > 0 else 1.0
    points_per_pixel = np.clip(points_per_pixel, 0, max_value)

    # normalize to [0,1]
    normalized = (points_per_pixel / np.max(points_per_pixel)).astype(np.float32)
    return normalized