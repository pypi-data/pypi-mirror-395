import numpy as np
from numpy.typing import NDArray
from PIL import Image
import cv2

def save_to_greyscale(img_array, filename) -> bool:
    """
    Save a high-bit-depth NumPy array as a 16-bit grayscale image.
    Always takes the first channel and scales values to 0-65535 if needed.
    """
    try:
        arr = np.asarray(img_array)

        # Always take the first channel if multi-channel
        if arr.ndim == 3:
            arr = arr[..., 0]

        # Convert to float for scaling safety
        arr = arr.astype(np.float64)

        # Normalize to 0–65535 range
        arr -= arr.min()
        if arr.max() > 0:
            arr = arr / arr.max() * 65535

        arr = arr.astype(np.uint16)

        # Save as 16-bit grayscale
        Image.fromarray(arr, mode='I;16').save(filename)
        return True
    
    except Exception as e:
        return False

def save(img_array, filename) -> bool:
    """
    Save a 3-channel (RGB) or 4-channel (RGBA) high-bit-depth NumPy array as an image using OpenCV.
    - Preserves 16-bit or higher precision.
    - Automatically scales float arrays to 0–65535.
    """
    try:
        arr = np.asarray(img_array)

        # Validate shape
        if arr.ndim != 3 or arr.shape[2] not in (3, 4):
            raise ValueError("Array must have 3 (RGB) or 4 (RGBA) channels.")

        # Convert float arrays to 16-bit
        if np.issubdtype(arr.dtype, np.floating):
            arr = np.clip(arr, 0, arr.max())
            if arr.max() > 0:
                arr = (arr / arr.max() * 65535)
            arr = arr.astype(np.uint16)

        # Convert 3-channel RGB to BGR for OpenCV
        if arr.shape[2] == 3:
            arr_bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        elif arr.shape[2] == 4:
            arr_bgr = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGRA)

        # Save using OpenCV (supports 16-bit PNG)
        return cv2.imwrite(filename, arr_bgr)

    except Exception as e:
        return False


def loadpng(filename):
    """
    Load a PNG (8-bit or 16-bit grayscale or RGB) into a NumPy array.
    Returns a NumPy array with the same bit depth as the source image.
    """
    try:
        img = Image.open(filename)
        arr = np.array(img)

        print(f"✅ Loaded '{filename}' → shape {arr.shape}, dtype {arr.dtype}")
        return arr

    except Exception as e:
        print(f"⚠️ Failed to load PNG: {e}")
        return None
    

def normalize_array(arr):
    """
    Normalize a NumPy array to the range [0, 1].
    
    Parameters
    ----------
    arr : np.ndarray
        Input array (any numeric dtype).

    Returns
    -------
    np.ndarray
        Normalized array with dtype float32, values in [0, 1].
    """
    arr = np.asarray(arr, dtype=np.float32)  # convert to float
    min_val = arr.min()
    max_val = arr.max()

    # Avoid division by zero if array is constant
    if max_val > min_val:
        arr = (arr - min_val) / (max_val - min_val)
    else:
        arr = np.zeros_like(arr, dtype=np.float32)

    return arr