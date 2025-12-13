import numpy as np
import scipy.ndimage as ndi
from skimage.measure import marching_cubes
from skimage.filters import gaussian
from vedo import Points
from mousetumorpy.lungs import LungsPredictor
from mousetumorpy.configuration import YOLO_MODELS


def _apply_transform(image, Phi, order: int = 3):
    """Applies an affine transformation to warp a 3D image."""
    warped = ndi.affine_transform(
        image, matrix=Phi[:3, :3], offset=Phi[:3, 3], order=order
    )

    return warped


def _fit_affine_from_lungs_masks(lungs0: np.ndarray, lungs1: np.ndarray):
    """Estimates the affine transformation that brings lung1 onto lung0."""
    verts0, *_ = marching_cubes(gaussian(lungs0.astype(float), sigma=1), level=0.5)
    verts1, *_ = marching_cubes(gaussian(lungs1.astype(float), sigma=1), level=0.5)

    aligned_pts1 = (
        Points(verts1).clone().align_to(Points(verts0), invert=True, use_centroids=True)
    )

    Phi = aligned_pts1.transform.matrix

    return Phi


def register_tumor_series(
    tumor_timeseries,
    lungs_timeseries=None,
    image_timeseries=None,
    order=3,
    skip_level=8,
):
    """
    Register a 4D array (TZYX) of tumor segmentation masks using the lungs segmentation masks.

    Parameters
    ----------
    tumor_timeseries : np.ndarray
        4D array (TZYX) of tumor segmentation masks.
    lungs_timeseries : np.ndarray, optional
        4D array of lung masks for registration.
    image_timeseries : np.ndarray, optional
        4D array of original images; used to compute lung masks if lungs_timeseries is not provided.
    order : int, default 3
        Interpolation order for warping the labeled images.
    skip_level : int, default 8
        Frame skipping interval when computing lung masks from images.

    Returns
    -------
    registered_timeseries : np.ndarray
        4D array (TZYX) of tumor segmentation masks registered to the first frame.
    lungs_timeseries : np.ndarray
        Provided or computed lungs segmentation mask (4D).
    registered_lungs_timeseries : np.ndarray
        Lungs segmentation mask (4D) registered to the first frame.
    """
    if lungs_timeseries is None:
        if image_timeseries is None:
            print("No images or lungs timeseries provided for the registration.")
            return

        # Compute the lungs timeseries
        default_model = list(YOLO_MODELS.keys())[
            0
        ]  # There is only one model (for now) - otherwise this would become a parameter
        predictor = LungsPredictor(model=default_model)
        lungs_timeseries = np.array(
            [
                predictor.fast_predict(frame, skip_level=skip_level)
                for frame in image_timeseries
            ]
        )

    image0 = tumor_timeseries[0]
    registered_timeseries = np.empty_like(tumor_timeseries)
    registered_timeseries[0] = image0

    lung0 = lungs_timeseries[0]
    registered_lungs_timeseries = np.empty_like(lungs_timeseries)
    registered_lungs_timeseries[0] = lung0

    for k, (image1, lung1) in enumerate(
        zip(tumor_timeseries[1:], lungs_timeseries[1:])
    ):
        Phi = _fit_affine_from_lungs_masks(lung0, lung1)

        warped_image1 = _apply_transform(image1, Phi, order=order)
        registered_timeseries[k + 1] = warped_image1

        warped_lung1 = _apply_transform(lung1, Phi, order=0)
        registered_lungs_timeseries[k + 1] = warped_lung1

    return registered_timeseries, lungs_timeseries, registered_lungs_timeseries
