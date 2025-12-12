from dataclasses import dataclass
from typing import Any
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backend_bases import Event, MouseEvent


@dataclass
class PanZoomState:
    x_offset: int = 0
    y_offset: int = 0
    panning_active: bool = False
    panning_start_coord: tuple = (0, 0)


class PanZoomCanvas(FigureCanvasQTAgg):
    """
    Subclassing with this class adds zooming and panning with the middle
    mouse button to any matplotlib GUI figure.

    Parameters
    ----------
    axis: Axes
        Matplotlib Axes object for the zoom/panning to be applied to.
    zoom_speed: float, optional
        Adjusts the speed at which the mouse zooms in/out. Default is 1.5.
    pan_sensitivity: float, optional
        Adjusts the sensitivty of the panning motion. Default is 0.5.

    Attributes
    ----------
    main_axis: Axes
        Points to the `axis` argument.
    state: PanZoomState
        Canvas state variables: x_offset, y_offset, panning_active and
        panning_start_coord.

    Notes
    -----
    If modifying an image to make it square, be sure to adjust the
    `self.state.xoffset` and `self.state.yoffset` accordingly.
    """

    def __init__(
        self,
        axis: Axes,
        zoom_speed: float = 1.5,
        pan_sensitivity: float = 0.5,
    ):
        if isinstance(axis.figure, Figure):
            super().__init__(axis.figure)
        else:
            raise ValueError("Axis is part of a SubFigure.")
        self.main_axis = axis
        self._zoom_speed = zoom_speed
        self._pan_sensitivity = pan_sensitivity
        self.state = PanZoomState()
        self.mpl_connect("button_press_event", self.on_button_press)
        self.mpl_connect("button_release_event", self.on_button_release)
        self.mpl_connect("scroll_event", self.on_scroll)
        self.mpl_connect("motion_notify_event", self.on_motion)
        self.mpl_connect("key_press_event", self.on_key_press)

    def on_button_press(self, event: Event) -> Any:
        """When the middle mouse button is pressed, activate panning"""
        if not isinstance(event, MouseEvent):
            return
        if event.xdata is None or event.ydata is None:
            return

        if event.button == 2:
            self.state.panning_active = True
            self.state.panning_start_coord = (
                event.xdata + self.state.x_offset,
                event.ydata + self.state.y_offset,
            )

    def on_button_release(self, event: Event) -> Any:
        """On middle mouse button release, deactivate panning"""
        if not isinstance(event, MouseEvent):
            return

        if event.button == 2:
            self.state.panning_active = False

    def on_scroll(self, event: Event, draw: bool = True) -> Any:
        """Zoom in on a forward scroll and out on a backward scroll"""
        # Checking if the Event is the right type.
        if not isinstance(event, MouseEvent):
            return

        # Checking if the event is in the image axis.
        ax = event.inaxes
        if ax is None:
            return
        if ax != self.main_axis:
            return

        # Current cursor position in data coordinates
        fx = event.xdata
        fy = event.ydata
        if fx is None or fy is None:
            return

        x0, x1 = ax.get_xlim()
        y0, y1 = ax.get_ylim()

        xdata = event.xdata
        ydata = event.ydata

        if xdata is None:
            return
        if ydata is None:
            return

        if event.button == "down":
            scale = 1 / self._zoom_speed
        elif event.button == "up":
            scale = self._zoom_speed
        else:
            return

        # Distances from cursor to each side
        dx0 = fx - x0
        dx1 = x1 - fx
        dy0 = fy - y0
        dy1 = y1 - fy

        # Scale distances
        dx0 /= scale
        dx1 /= scale
        dy0 /= scale
        dy1 /= scale

        ax.set_xlim(fx - dx0, fx + dx1)
        ax.set_ylim(fy - dy0, fy + dy1)

        if draw:
            self.draw_idle()

    def on_motion(self, event: Event, draw: bool = True) -> Any:
        if not isinstance(event, MouseEvent):
            return
        if not self.state.panning_active:
            return
        if event.inaxes != self.main_axis:
            return
        if event.xdata is None or event.ydata is None:
            return

        start_pt = self.state.panning_start_coord
        end_pt = (
            event.xdata + self.state.x_offset,
            event.ydata + self.state.y_offset,
        )

        dx_data = (start_pt[0] - end_pt[0]) * self._pan_sensitivity
        dy_data = (start_pt[1] - end_pt[1]) * self._pan_sensitivity

        cur_xlim = self.main_axis.get_xlim()
        cur_ylim = self.main_axis.get_ylim()

        self.main_axis.set_xlim(cur_xlim[0] + dx_data, cur_xlim[1] + dx_data)
        self.main_axis.set_ylim(cur_ylim[0] + dy_data, cur_ylim[1] + dy_data)

        self.state.panning_start_coord = end_pt

        if draw:
            self.draw_idle()

    def on_key_press(self, event: Event) -> Any:
        return
