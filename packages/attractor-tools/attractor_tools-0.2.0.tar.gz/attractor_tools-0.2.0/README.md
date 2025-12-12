# Attractor Tools

**Attractor-tools** is a Python module for animating the **Simon fractal** using efficient rendering. It provides a clean API to generate frames, assinging colormaps, and export visualizations as videos.

---

## ✨ Features
- Animate the Simon fractal with customizable parameters
- NumPy, Numba and Multiprocessing for performance

---

## 📦 Installation
Clone the repo and install in editable mode for development:

```bash
git clone https://github.com/beasty79/attractor_api.git
cd attractor
pip install -e .
```

## Example usage
```python
from attractor import sinspace, Performance_Renderer, ColorMap

def main():
    # array with values from lower to upper using a sinewave (p=1)
    # a, b are the initial values of the system used in the attractor
    # To animate this effectively, at least one of these parameters should change each frame
    a = sinspace(0.32, 0.38, 100)

    # Main rendering class
    # Use this when rendering a video with multiple frames.
    # For single-frame rendering, this class is overkill — use 'render_frame(...)' instead.
    renderer = Performance_Renderer(
        a=a,
        b=1.5,
        colormap=ColorMap("viridis"),
        frames=len(a),
        fps=10
    )

    # Important: 'a' is an array of values, one per frame (a[i] used for frame i)
    # So we need to mark it as non-static to allow per-frame variation
    renderer.set_static("a", False)

    # Set how many processes/threads to use (via multiprocessing.Pool)
    # Use None for unlimited; here we use 4 threads with a chunk size of 4
    renderer.start_render_process("./your_filename.mp4", threads=4, chunksize=4)

if __name__ == "__main__":
    # see all colormaps available
    print(ColorMap.colormaps())
    main()
```

# Attractor Visualization API

## Overview

This package provides tools for generating and rendering dynamic attractor visualizations using customizable color maps and performance-optimized rendering techniques.


## API
- **render_frame**
  Core function to compute attractor frame data.

- **Performance_Renderer**
  High-performance renderer supporting multi-threaded frame generation and video output.

## Utility Functions

- **ColorMap**
  Utility class to create and manage color maps with optional inversion.

- **sinspace / cosspace**
  Generate smooth sine- or cosine-shaped value sequences over a specified range.

- **bpmspace**
  Create time-based sequences synced to beats per minute (BPM) for rhythmic animations.

- **map_area**
  Batch process and render attractor animations over a grid of parameters.

- **apply_colormap**
  Apply a color map to attractor data to produce a colored image.