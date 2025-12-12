import numpy as np
from numpy.typing import NDArray
if 0 != 0: from .space import ColorMap
if 0 != 0: from .frame import Frame


def promt(frames, fps):
    t = round(frames / fps, 1)
    print(f"{frames=} {fps=} video_length={t:.0f}s")
    accept = input("Enter y or yes to Continue: ")
    if accept not in ["y", "Y", "yes", "Yes", "YES"]:
        exit(0)


def render_frame(frame: "Frame", only_raw: bool = False) -> "Frame":
    """
    Helper function to render an existing frame
    """
    frame.render(only_raw=only_raw)
    assert frame.raw is not None
    return frame


def make_filename(a_1, a_2, b_1, b_2, extension="mp4"):
    parts = []
    if a_1 != a_2:
        parts.append(f"a_{a_1}-{a_2}")
    if b_1 != b_2:
        parts.append(f"b_{b_1}-{b_2}")

    fname = "_".join(parts) + f".{extension}"
    return fname


def apply_color(normalized: NDArray[np.floating], colors: NDArray[np.uint8]) -> NDArray[np.uint8]:
    assert np.max(normalized) <= 1, "normalize should be [0, 1]"
    values = (normalized * 255).astype(int)
    values = np.clip(values, 0, 255)
    img = (colors[values] * 255).astype(np.uint8)
    return img


def apply_colormap(raw_image: NDArray, colormap: "ColorMap"):
    return apply_color(raw_image, colormap.get())
