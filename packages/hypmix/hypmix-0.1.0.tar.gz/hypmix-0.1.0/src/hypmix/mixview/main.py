# Standard Libraries
import sys

# Dependencies
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QSlider,
)
from superqt import QRangeSlider

# Relative Imports
from .mixture_image_canvas import MixtureImageCanvas
from .residual_image_canvas import ResidualImageCanvas
import numpy.typing as npt

# Top-Level Imports
from hypmix.endmember import EndMemberGroup
from hypmix.run_model import ModelResult


class ResidualViewWindow(QMainWindow):
    def __init__(self, residual_image: npt.NDArray):
        super().__init__()

        self.res_canvas = ResidualImageCanvas(residual_image)
        self.res_canvas.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.res_canvas.setFocus()

        self.range_slider = QRangeSlider()
        self.range_slider.setValue((20, 80))
        self.range_slider.setRange(min=0, max_=100)
        self.range_slider.setOrientation(Qt.Orientation.Horizontal)
        self.range_slider.valueChanged.connect(self.res_canvas._update)

        layout = QVBoxLayout()
        layout.addWidget(self.res_canvas)
        layout.addWidget(self.range_slider)

        widget = QWidget()
        widget.setLayout(layout)

        self.setWindowTitle("ResidualView v0.0.1")
        # self.setFixedSize(QSize(1200, 6))
        self.setCentralWidget(widget)


class MixViewWindow(QMainWindow):
    def __init__(
        self,
        mixture_cube: npt.NDArray,
        endmembers: EndMemberGroup,
    ):
        super().__init__()

        self.im_canvas = MixtureImageCanvas(mixture_cube, endmembers)
        self.im_canvas.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.im_canvas.setFocus()

        self.band_slider = QSlider()
        self.band_slider.setRange(0, mixture_cube.shape[-1] - 1)
        self.band_slider.setOrientation(Qt.Orientation.Horizontal)

        self.band_slider.valueChanged.connect(self.im_canvas.change_image)

        layout = QVBoxLayout()
        layout.addWidget(self.im_canvas)
        layout.addWidget(self.band_slider)

        widget = QWidget()
        widget.setLayout(layout)

        self.setWindowTitle("MixView v0.0.1")
        # self.setFixedSize(QSize(1200, 900))
        self.setCentralWidget(widget)

        self.im_canvas.image_changed.connect(self._move_slider)

    def _move_slider(self):
        self.band_slider.setSliderPosition(self.im_canvas.selected_band)


def run_mixview(result: ModelResult) -> None:
    app = QApplication(sys.argv)

    window = MixViewWindow(result.unmixed_image.fracs, result.endmembers)
    window.show()

    app.exec()


def run_residualview(result: ModelResult) -> None:
    app = QApplication(sys.argv)

    window = ResidualViewWindow(result.rsquared)
    window.show()

    app.exec()
