import numpy as np
import imaging_server_kit as sk
from qtpy.QtWidgets import QWidget

@sk.algorithm(
    name="Manual cropping",
    description="Interactively7 crop a 3D image by setting min/max limits along the X, Y and Z axes.",
    parameters={
        "image": sk.Image(name="Image (3D)", dimensionality=[3]),
        "min_x": sk.Integer(name="Min X", description="Pixels to remove in X, from the start", min=0, step=5, auto_call=True),
        "max_x": sk.Integer(name="Max X", description="Pixels to remove in X, from the end", step=5, auto_call=True, min=1, default=1),
        "min_y": sk.Integer(name="Min Y", description="Pixels to remove in Y, from the start", min=0, step=5, auto_call=True),
        "max_y": sk.Integer(name="Max Y", description="Pixels to remove in Y, from the end", step=5, auto_call=True, min=1, default=1),
        "min_z": sk.Integer(name="Min Z", description="Pixels to remove in Z, from the start", min=0, step=5, auto_call=True),
        "max_z": sk.Integer(name="Max Z", description="Pixels to remove in Z, from the end", step=5, auto_call=True, min=1, default=1),
    },
    samples=[
        {"image": "https://zenodo.org/records/13268683/files/ct_example_image.tif"}
    ],
)
def sk_crop(
    image, min_x: int, max_x: int, min_y: int, max_y: int, min_z: int, max_z: int
):
    crop = image[min_z:-max_z, min_y:-max_y, min_x:-max_x]
    return sk.Image(crop, name="ROI", meta={"contrast_limits": [np.min(crop), np.max(crop)]}), f"ROI shape: {crop.shape}"

class ManualCropWidget(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        widget = sk.to_qwidget(sk_crop, napari_viewer)
        self.setLayout(widget.layout())