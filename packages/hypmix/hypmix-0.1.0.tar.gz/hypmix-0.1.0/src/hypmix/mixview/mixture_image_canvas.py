# Standard Libraries
from typing import Any
from dataclasses import dataclass

# Dependencies
import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
from matplotlib import colormaps
from matplotlib.colors import ListedColormap
from matplotlib.backend_bases import Event, MouseEvent, KeyEvent
from PyQt6.QtCore import pyqtSignal

# Relative Imports
from .pan_zoom_canvas import PanZoomCanvas
from .utils import square_image, set_image_axis

# Top-Level Imports
from hypmix.endmember import EndMemberGroup


gray_cmap = colormaps["gray"](np.linspace(0, 1, 100))
teal = np.asarray([0, 0.807843137254902, 0.819607843137255, 1])
red = np.asarray([0.698039215686274, 0.133333333333333, 0.133333333333333, 1])
cmap_array = np.concat([teal[None, :], gray_cmap, red[None, :]], axis=0)
minmax_cmap = ListedColormap(colors=cmap_array)


@dataclass
class HoverData:
    _img: npt.NDArray
    xexact: float = 0.0
    yexact: float = 0.0

    def __post_init__(self) -> None:
        self.xpixel: int = round(self.xexact)
        self.ypixel: int = round(self.yexact)
        if self.xpixel < 0:
            self.xpixel = 0
        if self.ypixel < 0:
            self.ypixel = 0
        self.value: float = self._img[self.ypixel, self.xpixel]


class MixtureImageCanvas(PanZoomCanvas):
    image_changed = pyqtSignal()

    def __init__(self, mixture_cube: npt.NDArray, endmembers: EndMemberGroup):
        fig, ax = plt.subplots()
        set_image_axis(ax)
        super().__init__(ax)

        self.selected_band: int = 0
        self.mixture_cube = mixture_cube
        self.endmembers = endmembers
        self.clipmin = -0.1
        self.clipmax = 1.1
        offsets, self.show_band = square_image(
            self.mixture_cube[:, :, self.selected_band]
        )
        self.img_obj = self.main_axis.imshow(
            self.show_band,
            cmap=minmax_cmap,
            vmin=self.clipmin,
            vmax=self.clipmax,
        )

        self.band_names = self.endmembers.endmember_name_list
        self.main_axis.set_title(self.band_names[self.selected_band])

        self.state.x_offset = offsets.x_offset
        self.state.y_offset = offsets.y_offset

        self.hover = HoverData(self.show_band)

    def change_image(self, new_band: int):
        self.img_obj.remove()
        self.selected_band = new_band
        _, self.show_band = square_image(
            self.mixture_cube[:, :, self.selected_band]
        )
        self.img_obj = self.main_axis.imshow(
            self.show_band,
            cmap=minmax_cmap,
            vmin=self.clipmin,
            vmax=self.clipmax,
        )
        self.main_axis.set_title(self.band_names[self.selected_band])
        self.image_changed.emit()
        self.draw_idle()

    def on_motion(self, event: Event, draw: bool = True) -> Any:
        super().on_motion(event, draw)
        if not isinstance(event, MouseEvent):
            return
        if event.xdata is None or event.ydata is None:
            return
        self.hover = HoverData(
            self.show_band,
            xexact=event.xdata,
            yexact=event.ydata,
        )

    def on_key_press(self, event: Event) -> Any:
        super().on_key_press(event)

        if not isinstance(event, KeyEvent):
            return

        if event.key == "right":
            if self.selected_band < self.mixture_cube.shape[-1] - 1:
                self.selected_band += 1
            self.change_image(self.selected_band)

        if event.key == "left":
            if self.selected_band > 0:
                self.selected_band -= 1
            self.change_image(self.selected_band)
