import cv2
import numpy as np
from .colormap import ColorMap
from .file_writer import VideoFileWriter
from .utils import apply_color
from .terminal import TerminalCounter
from typing import Generator
import os

def frames_from_video(path: str) -> Generator[np.typing.NDArray]:
    """
    Generator that yields grayscale frames (np.ndarray) from an mp4 video.
    """
    cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        raise IOError(f"Cannot open video file: {path}")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            yield gray  # gray is a 2D np.ndarray
    finally:
        cap.release()

def color_generic(path: str, colormap: ColorMap, fps: int = 10, frames=2800):
    folder = os.path.dirname(path)
    fname = os.path.basename(path)
    export_path = os.path.join(folder, f"{fname.split(".")[0]}-{colormap.name}.mp4")

    videowriter = VideoFileWriter(export_path, fps)

    def normalize(arr: np.ndarray) -> np.ndarray:
        return arr.astype(np.float32) / 255.0

    counter = TerminalCounter(999)
    cmap = colormap.get()
    for frameArray in frames_from_video(path):
        counter.count_up()
        colored = apply_color(normalize(frameArray), cmap)
        videowriter.add_frame(colored)
    videowriter.save()