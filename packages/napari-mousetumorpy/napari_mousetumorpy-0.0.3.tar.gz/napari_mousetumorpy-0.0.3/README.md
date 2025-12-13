![EPFL Center for Imaging logo](https://imaging.epfl.ch/resources/logo-for-gitlab.svg)
# 🐭 napari-mousetumorpy

A Napari plugin for [mousetumorpy](https://github.com/EPFL-Center-for-Imaging/mousetumorpy.git): a toolbox to segment and track murine lung tumor nodules in mice CT scans.

## Installation

Install `napari-mousetumorpy` with `pip`:

```sh
pip install napari-mousetumorpy
```

or clone the project and install the development version:

```sh
git clone https://github.com/EPFL-Center-for-Imaging/napari-mousetumorpy.git
cd napari-mousetumorpy
pip install -e .
```

## Usage

Start napari from the terminal:

```sh
napari
```

You can find the plugin functions under `Plugins > Mousetumorpy`. Several tools are available:

- `Mousetumorpy`: The main image processing functions from the `mousetumorpy` package. Three workflows are available under *Algorithms*:
  - `Lungs segmentation`: Segments the lungs and crops a CT scan around them.
  - `Tumor segmentation`: Segments tumor nodules in a CT scan image (cropped around the lungs).
  - `Tumor tracking`: Tracks tumor nodules in a 4D (TZYX) tumor segmentation masks series.
- `Color picker`: Allows to display a segmentation in a chosen color.
- `Manual cropping`: Allows to crop CT scans manually by setting limits in the X, Y and Z directions.
- `Convert to tracks`: Displays tracks from a segmentation (Labels) layer, based on the label values.
- `Data table`: Displays tumor labels and corresponding volumes in a table. Allows to follow tumors across scans when the time slider is moved.
- `Remove objects`: Allows to remove individual tumors.

## Sample image

We provide a sample image under `File > Open Sample > Mouse lung CT scan` to test the package's functionality.