import cv2
from typing import Optional
import numpy as np

def play_video(video_path, fps=30):
    """
    Plays an .mp4 video in a loop using OpenCV, until 'q', 'Esc', or window close (X) is pressed.

    Args:
        video_path (str): Path to the video file.
        fps (float): Target frames per second for display.
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video at {video_path}")
        return

    delay = 1 / fps  # Time per frame

    window_name = "Video"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()

        # Restart when video ends
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        cv2.imshow(window_name, frame)

        # Check for quit key or window close
        key = cv2.waitKey(int(delay * 1000)) & 0xFF
        if key in [ord('q'), 27]:  # 'q' or 'Esc'
            break

        # Detect if window is closed via 'X' button
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()


def show_image(
    img: np.ndarray,
    resolution: Optional[tuple[int, int]] = (1000, 1000),
    a = None,
    b = None,
    colormap_name = None,
    inverted = None
):
    """
    Zeigt ein NumPy-ndarray-Bild mit OpenCV an.
    Schließt, wenn 'q', 'Esc' gedrückt oder das Fenster geschlossen wird.
    Optional kann eine feste Ausgabeauflösung angegeben werden.

    Args:
        img (np.ndarray): Das anzuzeigende Bild.
        resolution (tuple[int, int], optional): Zielauflösung (Breite, Höhe) in Pixeln.
        rgb_to_bgr (bool): Falls True, wird das Bild von RGB nach BGR konvertiert.
    """
    if not isinstance(img, np.ndarray):
        raise TypeError("Input muss ein NumPy ndarray sein.")

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Bild auf gewünschte Auflösung skalieren
    if resolution is not None:
        if len(resolution) != 2:
            raise ValueError("resolution muss ein Tupel (width, height) sein.")
        width, height = resolution
        if width <= 0 or height <= 0:
            raise ValueError("resolution-Werte müssen > 0 sein.")
        img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    window_name = "window"
    if a is not None and b is not None:
        str_a = round(float(a), 2)
        str_b = round(float(b), 2)
        window_name = f"a: {str_a} b: {str_b}        Colormap: {colormap_name} ({inverted})"

    cv2.imshow(window_name, img)

    while True:
        key = cv2.waitKey(1) & 0xFF

        # Prüfen, ob Fenster geschlossen wurde
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break

        # 'q' oder 'Esc' beendet die Anzeige
        if key in (ord('q'), 27):
            break

    cv2.destroyAllWindows()
