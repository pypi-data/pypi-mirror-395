import os

import numpy as np
import pandas as pd
import pooch
import scipy.ndimage as ndi
from scipy.interpolate import interp1d
from skimage.color import gray2rgb
from skimage.exposure import rescale_intensity
from skimage.measure import regionprops_table
from skimage.transform import resize
from skimage.util import img_as_ubyte
from tqdm import tqdm
from ultralytics import YOLO

from mousetumorpy.configuration import YOLO_MODELS


def extract_3d_roi(image: np.ndarray, lungs_mask: np.ndarray):
    """
    Extract a 3D region of interest (ROI) from an image using a lungs mask.

    Parameters
    ----------
    image : np.ndarray
        3D image array.
    lungs_mask : np.ndarray
        3D binary mask of the lungs region.

    Returns
    -------
    roi : np.ndarray
        Cropped image array corresponding to the bounding box of the lungs mask.
    roi_mask : np.ndarray
        Binary mask of the lungs region within the cropped image.
    """
    df = pd.DataFrame(
        regionprops_table(
            lungs_mask,
            intensity_image=image,
            properties=["bbox", "image"],
        )
    )

    # We assume a single object is present int he lungs mask
    x0 = int(df["bbox-0"].values[0])
    x1 = int(df["bbox-3"].values[0])
    y0 = int(df["bbox-1"].values[0])
    y1 = int(df["bbox-4"].values[0])
    z0 = int(df["bbox-2"].values[0])
    z1 = int(df["bbox-5"].values[0])

    roi = image[x0:x1, y0:y1, z0:z1]
    roi_mask = df["image"][0]
    roi_mask = img_as_ubyte(roi_mask)  # Convert bool to uint8

    return roi, roi_mask


def _keep_biggest_object(lab_int: np.ndarray) -> np.ndarray:
    """Selects only the biggest object of a labels image."""
    labels = ndi.label(lab_int)[0]
    counts = np.unique(labels, return_counts=1)
    biggestLabel = np.argmax(counts[1][1:]) + 1
    return (labels == biggestLabel).astype(int)


def _handle_2d_predict(image, model):
    image = rescale_intensity(image, out_range=(0, 255)).astype(np.uint8)
    image = gray2rgb(image)

    results = model.predict(
        source=image,
        conf=0.25,  # Confidence threshold for detections.
        iou=0.5,  # Intersection over union threshold.
        imgsz=640,  # Square resizing
        max_det=2,  # Two detections max
        augment=False,
        verbose=False,
    )

    mask = np.zeros_like(image, dtype=np.uint16)
    r = results[0]
    if r.masks is not None:
        mask = r.masks.cpu().numpy().data[0]  # First mask only
        mask = resize(mask, image.shape, order=0) == 1
        mask[mask] = 1

        # Keep one of the channels only
        if len(mask.shape) == 3:
            mask = mask[..., 0]

        # Fill-in the mask
        mask = ndi.binary_fill_holes(
            mask, structure=ndi.generate_binary_structure(2, 1)
        )

    if len(mask.shape) == 3:
        mask = mask[..., 0]

    return mask


def _handle_3d_predict(image, model):
    n_slices = len(image)

    mask_3d = []
    for slice_idx, z_slice in enumerate(tqdm(image, desc="Processing slices")):
        mask_2d = _handle_2d_predict(z_slice, model)
        mask_3d.append(mask_2d)
    mask_3d = np.stack(mask_3d)

    # Dilate in the Z direcion to suppress missing frames
    mask_3d = ndi.binary_dilation(
        mask_3d, structure=ndi.generate_binary_structure(3, 1), iterations=2
    )

    # Keep the biggest object (and convert the mask from bool => int64)
    mask_3d = _keep_biggest_object(mask_3d)

    return mask_3d


def _handle_predict(image, model):
    if len(image.shape) == 2:
        mask = _handle_2d_predict(image, model)
    elif len(image.shape) == 3:
        mask = _handle_3d_predict(image, model)

    mask = mask.astype(np.uint8)

    return mask


class LungsPredictor:
    """
    Predictor for lung segmentation using a pre-trained YOLO model.

    Parameters
    ----------
    model : str
        Identifier of the YOLO model to use. Must be a key in configuration.YOLO_MODELS.
    """

    def __init__(self, model: str):
        model_path = os.path.expanduser(
            os.path.join(os.getenv("XDG_DATA_HOME", "~"), ".mousetumornet")
        )

        model_url, model_known_hash = YOLO_MODELS.get(model)

        pooch.retrieve(
            url=model_url,
            known_hash=model_known_hash,
            path=model_path,
            progressbar=True,
            fname="yolo_seg_mouselungs.pt",
        )

        self.model = YOLO(os.path.join(model_path, "yolo_seg_mouselungs.pt"))

    def predict(self, image: np.ndarray) -> np.ndarray:
        """
        Segment lungs in a 3D image using the YOLO model.

        Parameters
        ----------
        image : np.ndarray
            3D image array.

        Returns
        -------
        np.ndarray
            Binary mask of the lung region with same shape as input image.
        """
        return _handle_predict(image, self.model)

    def fast_predict(self, image: np.ndarray, skip_level: int = 1) -> np.ndarray:
        """
        Quickly segment lungs by skipping slices in Z and interpolating predictions.

        Parameters
        ----------
        image : np.ndarray
            3D image array.
        skip_level : int, optional
            Frame skip interval for faster prediction (default is 1).

        Returns
        -------
        np.ndarray
            Binary mask of the lung region with same shape as input image.
        """
        rz, ry, rx = image.shape
        mask = np.zeros(image.shape, dtype=np.uint8)
        image_partial = image[::skip_level]
        mask_partial = self.predict(image_partial)
        mask[::skip_level] = mask_partial
        range_z = np.arange(rz)
        annotated_slices = range_z[::skip_level]
        for y in range(ry):
            for x in range(rx):
                values = mask_partial[:, y, x]
                interp_func = interp1d(
                    annotated_slices,
                    values,
                    kind="nearest",
                    bounds_error=False,
                    fill_value=0,
                )
                mask[:, y, x] = interp_func(range_z)

        return mask

    def compute_3d_roi(self, image: np.ndarray) -> np.ndarray:
        """
        Compute the 3D region of interest by segmenting the lungs and cropping.

        Parameters
        ----------
        image : np.ndarray
            3D image array.

        Returns
        -------
        roi : np.ndarray
            Cropped image array focused on the lungs.
        roi_mask : np.ndarray
            Binary mask of the lungs within the cropped image.
        """
        mask = self.predict(image)
        roi, roi_mask = extract_3d_roi(image, mask)
        return roi, roi_mask
