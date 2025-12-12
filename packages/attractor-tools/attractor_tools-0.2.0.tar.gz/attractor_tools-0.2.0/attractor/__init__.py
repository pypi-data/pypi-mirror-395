from .space import (
    Performance_Renderer,
    ColorMap,
    sinspace,
    cosspace,
    bpmspace,
    map_area,
    linspace,
    sawspace,
    squarespace,
    Waveform
)
from .frame import Frame, SimonFrame
from .utils import apply_colormap
from .opts import Option
from .complex_path import KeyframeInterpolator, Point

__version__ = "0.1.0"

__all__ = [
    "Performance_Renderer",
    "KeyframeInterpolator",
    "apply_colormap",
    "squarespace",
    "SimonFrame",
    "ColorMap",
    "sawspace",
    "sinspace",
    "cosspace",
    "bpmspace",
    "linspace",
    "map_area",
    "Option",
    "Frame",
    "Point",
    "Waveform"
]
