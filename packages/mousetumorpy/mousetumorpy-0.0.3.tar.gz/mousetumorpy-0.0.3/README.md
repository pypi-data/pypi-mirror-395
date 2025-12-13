![EPFL Center for Imaging logo](https://imaging.epfl.ch/resources/logo-for-gitlab.svg)
# 🐭 Mousetumorpy

A toolbox to segment and track murine lung tumor nodules in mice CT scans.

## Hightlights

- **Lungs segmentation and cropping**: Run a pretrained [YoloV8](https://docs.ultralytics.com/) model to segment the lungs and crop the CT scans around them.
- **Tumor segmentation**: Run a pretrained [nnUNet](https://github.com/MIC-DKFZ/nnUNet) model to segment tumor nodules in 3D.
- **Tumor tracking**: Track tumor nodules longitudinally across CT scans.

## Installation

Install the `mousetumorpy` package with `pip`:

```sh
pip install git+https://github.com/EPFL-Center-for-Imaging/mousetumorpy.git
```

or clone the project and install the development version:

```
git clone https://github.com/EPFL-Center-for-Imaging/mousetumorpy.git
cd mousetumorpy
pip install -e .
```

## Usage from Napari

To use Mousetumorpy's functions interactively in Napari, install the [napari-mousetumorpy](https://github.com/EPFL-Center-for-Imaging/napari-mousetumorpy) package.

## Usage as a CLI

The command-line interface (CLI) provides several image processing functions.

### Crop

Run a [YoloV8](https://docs.ultralytics.com/) model to segment the lungs cavity and crop the image around the lungs.

```sh
mousetumorpy crop <image_file> <out_dir>
```
For more details, see `mousetumorpy crop --help`.

### Predict

Run a [nnUNet](https://github.com/MIC-DKFZ/nnUNet) model to segment tumor nodules.

```sh
mousetumorpy predict <image_file> <out_dir>
```

For more details, see `mousetumorpy predict --help`.

### Combine

Combine several 3D images (ZYX) into a single 4D image (TZYX).  

```sh
mousetumorpy combine <image_1> <image_2> <image_3> <out_dir>
```

For more details, see `mousetumorpy combine --help`.

### Track

Track tumor nodules across a 4D mask (TZYX) time series using [trackpy](https://soft-matter.github.io/trackpy/v0.6.4/) or [laptrack](https://github.com/yfukai/laptrack).

```sh
mousetumorpy track <labels_file> <image_file> <lungs_file> <out_dir>
```

For more details, see `mousetumorpy track --help`.

## License

This project is licensed under the [AGPL-3](LICENSE) license.

This project depends on the [ultralytics](https://github.com/ultralytics/ultralytics) package which is licensed under AGPL-3.
