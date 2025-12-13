from ._picker import ColorPickerWidget
from ._crop import ManualCropWidget
from ._tracks import ToTracksWidget
from ._table import TableWidget
from ._remove import RemoveObjectsWidget

import imaging_server_kit as sk
from napari_mousetumorpy._widget import sk_lungs_seg, sk_tumor_seg, sk_tracking

from qtpy.QtWidgets import QWidget


class PluginWidget(QWidget):
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__()
        multi = sk.combine(
            [
                sk_lungs_seg,
                sk_tumor_seg,
                sk_tracking,
            ],
            name="Mousetumorpy",
        )
        widget = sk.to_qwidget(multi, viewer)
        self.setLayout(widget.layout())


from ._version import version as __version__

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
