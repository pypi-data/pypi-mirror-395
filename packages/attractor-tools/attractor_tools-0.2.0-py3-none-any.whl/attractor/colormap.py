from numpy.typing import NDArray
import matplotlib.pyplot as plt
import numpy as np


class ColorMap:
    def __init__(self, name: str, inverted: bool = False) -> None:
        self.name = name
        self.color = self._get_colors_array(name)
        self.inverted = inverted

    def set_inverted(self, state: bool):
        self.inverted = state

    def _get_colors_array(self, cmap: str) -> NDArray:
        color_map = plt.get_cmap(cmap)
        linear = np.linspace(0, 1, 256)
        return color_map(linear)
    
    def change_color_entry(self, i_start: int, i_end: int, hexcolor: str) -> None:
        """
        Manipulate a specific part of a colormap.
        i_start, i_end in [0, 256)
        hexcolor: color in hex format, e.g., '#ff0000'
        """
        # Convert hex to RGB normalized [0,1]
        rgb = np.array([int(hexcolor[i:i+2], 16) for i in (1, 3, 5)]) / 255.0
        # Update the colormap entries
        for i in range(i_start, i_end):
            self.color[i, :3] = rgb  # keep alpha as is

    def fill_background(self, hexcolor: str):
        self.change_color_entry(0, 5, hexcolor)


    def greyscale(self, inverted: bool = False) -> NDArray:
        linear = np.linspace(1.0, 0.0, 256)
        rgb = np.stack([linear, linear, linear], axis=1)
        rgba = np.concatenate([rgb, np.ones((256, 1))], axis=1)
        return rgba if not inverted else rgba[::-1]

    def get(self) -> NDArray:
        return self.color[::-1] if self.inverted else self.color

    def __repr__(self) -> str:
        return f"Colormap['{self.name}', {self.inverted=}]"

    @staticmethod
    def colormaps():
        return list(plt.colormaps)