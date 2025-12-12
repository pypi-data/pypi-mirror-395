from numpy.typing import NDArray
from typing import Optional
import multiprocessing
from typing import Any
from time import time
import os
from json import dump, dumps
import numpy as np
from .file_writer import VideoFileWriter
from .terminal import TerminalCounter
from .utils import promt
from .view import play_video
from .utils import render_frame
from .frame import Frame, SimonFrame
from .colormap import ColorMap
from .opts import Option


class Performance_Renderer:
    """This is an api wrapper class for rendering simon attractors"""
    def __init__(
            self,
            opts: Option,
            a: float | NDArray,
            b: float | NDArray,
            percentile: float | NDArray = 99,
            iterations: float | NDArray = 1_000_000
    ) -> None:
        self.opts               = opts
        self.percentile         = percentile
        self.a                  = a
        self.b                  = b
        self.value = {
            'a': a,
            'b': b,
            'iterations': iterations,
            'resolution': opts.resolution,
            'percentile': percentile
        }
        self.static = {
            'a': True,
            'b': True,
            'iterations': True,
            'resolution': True,
            'percentile': True
        }
        self.fps = opts.fps
        self.writer = None
        self.color = None
        self.counter: TerminalCounter | None = None
        self.colormap: ColorMap = opts.colormap
        self.hook: None = None
        self._demo = False

    def set_static(self, argument: Any, is_static: bool):
        """
        argument: {'a', 'b', 'iterations', 'resolution', 'percentile'}
        """
        if argument not in self.static:
            raise ValueError(f"arg: {argument} is invalid, should be: ['a', 'b', 'iterations', 'resolution', 'percentile']")
        self.static[argument] = is_static

    def save_metadata(self, mp4path: str):

        def value_of(arg: str):
            value = None
            value = self.value[arg]

            if isinstance(value, np.ndarray):
                value = value.tolist()

            return value

        data = {
            "fps": self.fps,
            "frames": self.opts.frames,
            "cmap": {
                "name": self.opts.colormap.name,
                "inverted": self.opts.colormap.inverted
            },
            "resolution": self.opts.resolution,
            "seconds": round(self.opts.total_time, 1),
            "a": {
                "static": self.static["a"],
                "value": value_of("a")
            },
            "b": {
                "static": self.static["b"],
                "value": value_of("b")
            },
            "iterations": {
                "static": self.static["iterations"],
                "value": value_of("iterations")
            },
            "resolution": {
                "static": self.static["resolution"],
                "value": value_of("resolution")
            },
            "percentile": {
                "static": self.static["percentile"],
                "value": value_of("percentile")
            }
        }
        try:
            dumps(data)
        except Exception as e:
            print(e)
            raise e
            return


        with open(f"{mp4path.removesuffix(".mp4")}.json", "w") as f:
            dump(data, f, indent=4)

    def addHook(self, signal):
        self.hook = signal

    def get_iter_value(self, arg: str) -> list[Any]:
        if arg not in self.static:
            raise ValueError("arg not in static")
        is_static: bool = self.static[arg]

        if is_static:
            return [self.value[arg]] * self.opts.frames
        else:
            return self.value[arg]

    def get_unique_fname(self, fname: str) -> str:
        base_path = os.path.dirname(fname)
        full_name = os.path.basename(fname)
        name_only, ext = os.path.splitext(full_name)

        new_name = fname
        i_ = 0
        while os.path.exists(new_name):
            i_ += 1
            name_comp = f"{name_only}_{i_}_{ext}"
            new_name = os.path.join(base_path, name_comp)
        return new_name

    def show_frame(self, frame_index: int):
        frame: Frame = self.frames[frame_index]
        frame.render()
        frame.show()

    def get_frame(self, frame_index: int):
        return self.frames[frame_index]

    def show_first_frame(self):
        frame: Frame = self.frames[0]
        frame.render()
        frame.show()

    def show_last_frame(self):
        frame: Frame = self.frames[-1]
        frame.render()
        frame.show()

    def show_demo(
            self, 
            nth_frame: int = 10, 
            real_time: bool = False, 
            resolution: int = 750, 
            iterations: int = 500_000,
            fps: Optional[int] = None
        ):
        self._demo_var = nth_frame
        if os.path.exists("./tmp.mp4"):
            os.remove("./tmp.mp4")

        # cache class vars and change them
        fps_cache = self.fps
        self._demo = True
        self._demo_res = resolution
        self._demo_iterations = iterations
        self.fps = round(self.fps / self._demo_var)

        # render demo video
        self.start_render_process("./tmp.mp4", verbose_image=True, bypass_confirm=True, threads=8, chunksize=8)

        fps_ = fps if fps is not None else 10
        play_video("./tmp.mp4", self.fps if real_time else fps_)

        # rechange variables
        self.fps = fps_cache
        self._demo = False

    def get_frames(self, res, percentile, color, n, a, b) -> list[SimonFrame]:
        """Helper function"""
        assert all(len(lst) == len(res) for lst in [a, b, n, percentile, color]), "Mismatched lengths in input lists"
        frames = [
            SimonFrame(
                resolution=res[i],
                percentile=percentile[i],
                colors=color[i],
                n=n[i],
                a=a[i],
                b=b[i]
            )
            for i in range(len(res))
        ]
        return frames
    
    @property
    def frames(self) -> list[SimonFrame]:
        """Helper function"""
        res: list[int] = self.get_iter_value("resolution")
        a: list[int] = self.get_iter_value("a")
        b: list[int] = self.get_iter_value("b")
        n: list[int] = self.get_iter_value("iterations")
        percentile: list[int] = self.get_iter_value("percentile")

        assert all(len(lst) == len(res) for lst in [a, b, n, percentile]), "Mismatched lengths in input lists"
        return [
            SimonFrame(
                resolution=res[i],
                percentile=percentile[i],
                colors=self.colormap.get(), # type: ignore
                n=n[i],
                a=a[i],
                b=b[i]
            )
            for i in range(len(res))
        ]

    def start_render_process(
            self,
            fname: str,
            verbose_image: bool    = False,
            threads: Optional[int] = 4,
            chunksize: int         = 4,
            skip_empty_frames: bool= True,
            bypass_confirm: bool   = False,
            save_as_generic: bool  = False,
            use_counter: bool      = True,
            save_render_information= False
        ):
        """starts the render Process

        Args:
            fname (str): filename / filepath
            verbose_image (bool, optional): adds a small text with the parameter per frmae. Defaults to False.
            threads (Optional[int], optional): cpu cores to use. Defaults to 4.
            chunksize (int, optional): the higher the chunksize the more efficient but it needs more memory. Defaults to 4.
            skip_empty_frames (bool, optional): skips frames wheree the fractal collapses. Defaults to True.
            bypass_confirm (bool, optional): bypass the terminal confirmation. Defaults to False.
            save_as_generic (bool, optional): saves as grey space image so it can be loaded and colored again without the need to render it again. Defaults to False.
        """
        res: list[int] = self.get_iter_value("resolution")
        a: list[int] = self.get_iter_value("a")
        b: list[int] = self.get_iter_value("b")
        n: list[int] = self.get_iter_value("iterations")
        percentile: list[int] = self.get_iter_value("percentile")
        
        if save_as_generic:
            self.color = self.colormap.greyscale()
        else:
            self.color = self.colormap.get()

        col = [self.color] * len(a)

        # Create Frame dataclass for every frame
        if self._demo:
            frames = self.get_frames([self._demo_res] * len(n), percentile, col, [self._demo_iterations] * len(n), a, b)
            frames = frames[::self._demo_var]
        else:
            frames = self.get_frames(res, percentile, col, n, a, b)

        if not bypass_confirm:
            promt(len(frames), self.fps)
        

        if not fname.lower().endswith('.mp4'):
            fname += '.mp4'

        # File Writer
        fname_ = self.get_unique_fname(fname)
        self.writer = VideoFileWriter(
            filename=fname_,
            fps=self.fps
        )
        self.save_metadata(fname_)

        # Terminal Feedback
        tstart = time()

        if use_counter:
            self.counter = TerminalCounter(len(frames))
            if self.hook is None:
                self.counter.start()

        # Multiproccessing
        try:
            with multiprocessing.Pool(threads) as pool:
                frame: Frame
                for i, frame in enumerate(pool.imap(render_frame, frames, chunksize=chunksize)):

                    # Either emit a Signal (pyqt6 hook) or show the progress-bar in the Terminal
                    if self.hook is not None:
                        self.hook.emit(i)
                    else:
                        if self.counter is not None:
                            self.counter.count_up()

                    # filter if frame is collapsed
                    if frame.collapsed and skip_empty_frames:
                        continue

                    # write a, b
                    if verbose_image:
                        self.writer.add_frame(frame.img, a=a[i], b=b[i])
                    else:
                        self.writer.add_frame(frame.img)
        except Exception as e:
            raise e

        # Process Finished
        total = time() - tstart
        min_ = int(total // 60)
        sec_ = int(total % 60)
        print(f"Finished render process in {min_:02d}:{sec_:02d}")
        print(f"Average: {self.opts.frames / total:.2f} fps")
        self.writer.save()