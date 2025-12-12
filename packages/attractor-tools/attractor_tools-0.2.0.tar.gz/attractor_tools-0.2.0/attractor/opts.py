from dataclasses import dataclass
from .colormap import ColorMap
from typing import Optional

@dataclass
class Option:
    fps: int
    frames: int
    resolution: int
    colormap: ColorMap = None # type: ignore

    def __post_init__(self):
        self.total_time: float = round(self.frames / self.fps, 1)
        self.colormap = ColorMap("viridis") if self.colormap is None else self.colormap
    
    @staticmethod
    def from_time(
          seconds: float, 
          fps: int,
          resolution: int = 1000,
          colormap: ColorMap = None, # type: ignore
        ) -> "Option":

        return Option(
            fps=fps, 
            frames=round(seconds * fps), 
            resolution=resolution,
            colormap=colormap,
        )
