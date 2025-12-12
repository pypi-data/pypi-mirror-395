from dataclasses import dataclass
from .opts import Option
import numpy as np

@dataclass
class Point:
    frame: int
    value: float | int


@dataclass
class KeyframeInterpolator:
    opts: Option
    first_value: float
    last_value: float
    
    def __post_init__(self):
        self.points: dict[int, float] = {}
        self.points[0] = self.first_value
        self.points[self.opts.frames - 1] = self.last_value


    def add_keyframe(self, point: Point):
        assert 0 < point.frame <= self.opts.frames, "Points is out of bound [0 is already set]"
        self.points[point.frame] = point.value

    def to_array(self) -> np.typing.NDArray:
        spaces = []
        keys = sorted(self.points.keys())

        # interpolate using linsapce
        for i, (p1, p2) in enumerate(zip(keys, keys[1:])):
            v1, v2 = self.points[p1], self.points[p2]
            frame_diff = p2 - p1
            lin = np.linspace(v1, v2, frame_diff + 1)
            if i > 0:
                lin = lin[1:]  # remove overlap
            spaces.append(lin)

        # Merge arrays together
        length = sum([len(arr) for arr in spaces])
        empty_arr = np.zeros(shape=(length,), dtype=np.float32)
        i = 0
        for arr in spaces:
            for entry in arr:
                empty_arr[i] = entry
                i += 1

        return empty_arr