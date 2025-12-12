# Dependencies
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

# Relative Imports
from .pan_zoom_canvas import PanZoomCanvas
from .utils import square_image, set_image_axis


class ResidualImageCanvas(PanZoomCanvas):
    def __init__(self, residual_image: npt.NDArray):
        fig, ax = plt.subplots()
        fig.subplots_adjust(bottom=0.25)
        set_image_axis(ax)
        super().__init__(ax)

        self.residual_image = residual_image
        clean_res_img = residual_image[np.isfinite(residual_image)]
        self.image_extrema = (np.min(clean_res_img), np.max(clean_res_img))

        offsets, self.sqr_img = square_image(self.residual_image)

        self.img_obj = self.main_axis.imshow(self.sqr_img, cmap="gray")
        self.state.x_offset = offsets.x_offset
        self.state.y_offset = offsets.y_offset

    def _update(self, values: tuple[float, float]):
        vmin, vmax = values
        self.img_obj.norm.vmin = self.image_extrema[0] * vmin / 100
        self.img_obj.norm.vmax = self.image_extrema[1] * vmax / 100
        self.draw_idle()
