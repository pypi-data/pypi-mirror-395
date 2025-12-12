from numpy.typing import NDArray
import numpy as np
import os

from .colormap import ColorMap
from .render_class import Performance_Renderer
from .opts import Option
from dataclasses import dataclass
from enum import Enum, auto

class Waveform(Enum):
    Linear = auto()
    Sine = auto()
    Cosine = auto()
    Saw = auto()
    Sqaure = auto()
    Triangular = auto()

def linspace(lower: float, upper: float, n: int):
    """
    [equals np.linspace]
    Parameters: 
    - lower (float): The minimum value.
    - upper (float): The maximum value.
    - n (int): Number of points in the output array.

    Returns:
    - np.ndarray: An array of values from between lower and upper evenly spaced
    """
    return np.linspace(lower, upper, n)

def bpmspace(
        lower: float, 
        upper: float, 
        n: int, 
        bpm: int, 
        fps: int, 
        waveform: Waveform = Waveform.Sine,
        absolute=True):
    """
    Parameters:
    - lower (float): The minimum value.
    - upper (float): The maximum value.
    - n (int): Number of points in the output array.
    - p (float): Number of sine periods to span across the interval.

    Returns:
    - np.ndarray: An array of values shaped by a sine wave between lower and upper.
    """
    total_time = n / fps
    minutes = total_time / 60
    periods_needed = minutes * bpm
    match waveform:
        case Waveform.Sine:
            return sinspace(lower, upper, n, p=periods_needed, absolute=absolute)
        case Waveform.Cosine:
            return cosspace(lower, upper, n, p=periods_needed, absolute=absolute)
        case Waveform.Sqaure:
            return squarespace(lower, upper, n, p=periods_needed, absolute=absolute)
        case Waveform.Saw:
            return sawspace(lower, upper, n, p=periods_needed)
        case Waveform.Triangular:
            return trispace(lower, upper, n, p=periods_needed)
        case _:
            raise ValueError("No Valid Waveform!")


def sinspace(lower: float, upper: float, n: int, p: float = 1.0, absolute=False):
    """
    Parameters:
    - lower (float): The minimum value.
    - upper (float): The maximum value.
    - n (int): Number of points in the output array.
    - p (float): Number of sine periods to span across the interval.

    Returns:
    - np.ndarray: An array of values shaped by a sine wave between lower and upper.
    """
    phase = np.linspace(0, 2 * np.pi * p, n)
    sin_wave = np.sin(phase)
    if absolute:
        sin_wave = np.abs(sin_wave)
    sin_wave = (sin_wave + 1) / 2
    return lower + (upper - lower) * sin_wave


def trispace(lower: float, upper: float, n: int, p: float = 1.0):
    """
    Parameters:
    - lower (float): The minimum value.
    - upper (float): The maximum value.
    - n (int): Number of points in the output array.
    - p (float): Number of triangular periods to span across the interval.
    - absolute (bool): Whether to take the absolute value of the wave.

    Returns:
    - np.ndarray: An array of values shaped by a triangular wave between lower and upper.
    """
    x = np.linspace(0, p, n)  # Linear space over periods
    tri_wave = 2 * np.abs(x % 1 - 0.5)  # Triangle wave 0..1
    return lower + (upper - lower) * tri_wave


def cosspace(lower: float, upper: float, n: int, p: float = 1.0, absolute=False):
    """
    Parameters:
    - lower (float): The minimum value.
    - upper (float): The maximum value.
    - n (int): Number of points in the output array.
    - p (float): Number of sine periods to span across the interval.

    Returns:
    - np.ndarray: An array of values shaped by a cos wave between lower and upper.
    """
    phase = np.linspace(0, 2 * np.pi * p, n)
    cos_wave = (np.cos(phase) + 1) / 2
    cosine = lower + (upper - lower) * cos_wave
    return cosine if not absolute else np.abs(cosine)


def sawspace(lower: float, upper: float, n: int, p: float = 1.0, absolute: bool = False):
    """
    Generate a sawtooth-like sequence that behaves like a sine wave.

    Parameters:
    - lower (float): Minimum value.
    - upper (float): Maximum value.
    - n (int): Number of points in the output array.
    - p (float): Number of "periods" across the interval.
    - absolute (bool): If True, map output to [0, 1] using absolute value.

    Returns:
    - np.ndarray: A wave scaled between lower and upper.
    """
    # Create linear phase
    phase = np.linspace(0, 2 * np.pi * p, n)

    # Sine-shaped wave in [-1, 1]
    wave = np.sin(phase)

    # Optionally take absolute to map to [0, 1]
    if absolute:
        wave = np.abs(wave)

    # Scale to [lower, upper]
    wave_scaled = lower + (upper - lower) * (wave - wave.min()) / (wave.max() - wave.min())
    return wave_scaled


def squarespace(lower: float, upper: float, n: int, p: float = 1.0, absolute: bool = False):
    """
    Generate a square-wave-shaped sequence between `lower` and `upper`.

    Parameters:
    - lower (float): Minimum value.
    - upper (float): Maximum value.
    - n (int): Number of points in the output array.
    - p (float): Number of square wave periods across the interval.
    - absolute (bool): If True, use the absolute value of the square wave,
      effectively making it oscillate between 0 and 1 instead of -1 and 1.

    Returns:
    - np.ndarray: A square wave scaled between lower and upper.
    """
    phase = np.linspace(0, 1, n)
    square_wave = np.sign(np.sin(2 * np.pi * p * phase))

    if absolute:
        square_wave = np.abs(square_wave)  # transforms [-1, 1] → [0, 1]
    else:
        square_wave = (square_wave + 1) / 2  # normalize [-1, 1] → [0, 1]

    return lower + (upper - lower) * square_wave


def map_area(a: NDArray, b: NDArray, fname: str, colormap: ColorMap, skip_empty: bool = True, fps: int = 15, n=1_000_000, percentile=99, resolution=1000):
    """Generates a animation over a whole area. a, b are the axis (uses np.meshgrid)"""
    assert len(a) == len(b), "a & b dont match in length"
    A, B = np.meshgrid(a, b)

    for i in range(A.shape[0]):
        if i % 2 == 1:
            A[i] = A[i][::-1]
    A = A.flatten()

    # A = A.ravel()
    B = B.ravel()
    
    opts = Option(
        fps=fps, 
        frames=len(A), 
        resolution=resolution, 
        iterations=n,
        colormap=colormap
    )

    process = Performance_Renderer(
        opts=opts,
        a=A,
        b=B,
        percentile=percentile,
    )
    process.set_static("a", False)
    process.set_static("b", False)
    process.start_render_process(fname, verbose_image=True, threads=4, chunksize=8, skip_empty_frames=skip_empty)


def from_generic(path: str, colormap: ColorMap):
    # new filepath with colormap suffix
    suffix = "_inv" if colormap.inverted else ""
    fname = os.path.basename(path).replace(".mp4", "")
    fname = f"{fname}_{colormap.name}{suffix}.mp4"
    new_path = os.path.join(os.path.dirname(path), fname)
    print("export_path: ", new_path)


    # writer = VideoFileWriter()
    ...