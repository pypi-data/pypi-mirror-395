import os
from pathlib import Path
import argparse
import skimage.io

from mousetumorpy.nnunet import TumorPredictor
from mousetumorpy.lungs import LungsPredictor
from mousetumorpy.track import (
    run_tracking,
    combine_images,
    to_formatted_df,
    generate_tracked_tumors,
)
from mousetumorpy.configuration import NNUNET_MODELS, YOLO_MODELS


def predict(image_file, out_dir, model):
    """CLI functionality for segmenting tumors"""
    if out_dir is None:
        out_dir = Path(image_file).parent
    else:
        out_dir = Path(out_dir)
        if not out_dir.exists():
            os.makedirs(out_dir)

    image_name = Path(image_file).stem
    out_file = out_dir / f"{image_name}_tumors.tif"

    image = skimage.io.imread(image_file)
    predictor = TumorPredictor(model)
    segmentation = predictor.predict(image)

    skimage.io.imsave(out_file, segmentation)
    print(f"Saved {out_file}")


def crop(image_file, out_dir, model, with_lungs):
    """CLI functionality for cropping the image and segmenting the lungs"""
    if out_dir is None:
        out_dir = Path(image_file).parent
    else:
        out_dir = Path(out_dir)
        if not out_dir.exists():
            os.makedirs(out_dir)

    image_name = Path(image_file).stem

    out_file_roi = out_dir / f"{image_name}_roi.tif"
    out_file_lungs = out_dir / f"{image_name}_lungs.tif"

    image = skimage.io.imread(image_file)
    predictor = LungsPredictor(model)
    image_roi, lungs_roi = predictor.compute_3d_roi(image)

    skimage.io.imsave(out_file_roi, image_roi)
    print(f"Saved {out_file_roi}")

    if with_lungs:
        skimage.io.imsave(out_file_lungs, lungs_roi)
        print(f"Saved {out_file_lungs}")


def combine(*files, out_dir):
    """CLI functionality for creating time series from several image files"""
    n_files = len(files)
    if n_files < 2:
        print(f"Please provide at least 2 files to combine (Got {n_files}).")
        return

    if out_dir is None:
        out_dir = Path(files[0]).parent
    else:
        out_dir = Path(out_dir)
        if not out_dir.exists():
            os.makedirs(out_dir)

    image_name = Path(files[0]).stem  # good choice?
    out_file = out_dir / f"{image_name}_{n_files:02d}-scans-series.tif"

    images = [skimage.io.imread(image_file) for image_file in files]
    image_series = combine_images(images)

    skimage.io.imsave(out_file, image_series)
    print(f"Saved {out_file}")


def track(
    labels_file,
    image_file,
    lungs_file,
    out_dir,
    with_lungs_registration,
    max_dist_px,
    memory,
    dist_weight_ratio,
    max_volume_diff_rel,
    method,
    skip_level,
    save_tracked_labels,
):
    """CLI functionality for tracking tumors"""
    labels_timeseries = skimage.io.imread(labels_file)
    if image_file is not None:
        image_timeseries = skimage.io.imread(image_file)
    else:
        image_timeseries = None
    if lungs_file is not None:
        lungs_timeseries = skimage.io.imread(lungs_file)
    else:
        lungs_timeseries = None

    if out_dir is None:
        out_dir = Path(labels_file).parent
    else:
        out_dir = Path(out_dir)
        if not out_dir.exists():
            os.makedirs(out_dir)

    image_name = Path(labels_file).stem
    out_file = out_dir / f"{image_name}_tracks.csv"

    linkage_df = run_tracking(
        tumor_timeseries=labels_timeseries,
        image_timeseries=image_timeseries,
        lungs_timeseries=lungs_timeseries,
        with_lungs_registration=with_lungs_registration,
        max_dist_px=max_dist_px,
        memory=memory,
        dist_weight_ratio=dist_weight_ratio,
        max_volume_diff_rel=max_volume_diff_rel,
        method=method,
        skip_level=skip_level,
    )

    formatted_df = to_formatted_df(linkage_df)
    formatted_df.to_csv(out_file)
    print(f"Saved {out_file}")

    if save_tracked_labels:
        tracked_labels_timeseries = generate_tracked_tumors(
            labels_timeseries, linkage_df
        )
        tracked_labels_file = out_dir / f"{image_name}_tracked.tif"
        skimage.io.imsave(tracked_labels_file, tracked_labels_timeseries)
        print(f"Saved {tracked_labels_file}")


def main():
    parser = argparse.ArgumentParser(description="Mousetumorpy CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Cropping and lungs segmentation
    crop_parser = subparsers.add_parser(
        "crop",
        help="Extract a region of interest (ROI) by detecting the lungs cavity",
    )
    crop_parser.add_argument(
        "image_file",
        help="Input image (.tif)",
    )
    crop_parser.add_argument(
        "-o",
        "--out-dir",
        help="Directory to save the model outputs",
    )
    crop_parser.add_argument(
        "-m",
        "--model",
        default="v1",
        choices=list(YOLO_MODELS.keys()),
        help="Model to use",
    )
    crop_parser.add_argument(
        "--image-only",
        action="store_false",
        help="Whether to save the image only or the image with the lungs mask",
    )

    # Tumor segmentation
    predict_parser = subparsers.add_parser("predict", help="Detect tumors in CT scans")
    predict_parser.add_argument(
        "image_file",
        help="Input image (.tif)",
    )
    predict_parser.add_argument(
        "-o",
        "--out-dir",
        help="Directory to save the model outputs",
    )
    predict_parser.add_argument(
        "-m",
        "--model",
        default="oct24",
        choices=list(NNUNET_MODELS.keys()),
        help="Model to use",
    )

    # Combining images into time series
    combine_parser = subparsers.add_parser(
        "combine",
        help="Combine images into a time series",
    )
    combine_parser.add_argument(
        "files",
        nargs="+",
        help="Files to process",
    )
    combine_parser.add_argument(
        "-o",
        "--out-dir",
        help="Directory to save the outputs",
    )

    # Tracking tumors
    track_parser = subparsers.add_parser(
        "track",
        help="Track tumors in time series",
    )
    track_parser.add_argument(
        "labels_file",
        help="Labels file (TIFF format)",
    )
    track_parser.add_argument(
        "--image-file",
        help="Input image (.tif)",
    )
    track_parser.add_argument(
        "--lungs-file",
        help="Lungs file (TIFF format)",
    )
    track_parser.add_argument(
        "-o",
        "--out-dir",
        help="Directory to save the outputs",
    )
    track_parser.add_argument(
        "--reg",
        action="store_true",
        help="Whether to use the lungs for registration",
    )
    track_parser.add_argument(
        "--max-dist",
        type=int,
        default=30,
        help="Max search distance in pixels",
    )
    track_parser.add_argument(
        "--memory",
        type=int,
        default=0,
        help="Maximum number of frames skipped before discontinuing tracks",
    )
    track_parser.add_argument(
        "--dist-ratio",
        type=float,
        default=0.9,
        help="Relative importance of the distance between objects and their similarity in size accounted for in the tracking",
    )
    track_parser.add_argument(
        "--vol-diff",
        type=float,
        default=1.0,
        help="Maximum relative volume change of an object between two consecutive frames",
    )
    track_parser.add_argument(
        "--method",
        default="trackpy",
        choices=["trackpy", "laptrack"],
    )
    track_parser.add_argument(
        "--reg-level",
        type=int,
        default=8,
        help="Number of Z slices to skip when computing the lungs for registration",
    )
    track_parser.add_argument(
        "--lab",
        action="store_false",
        help="Whether to save the tracked labels",
    )

    args = parser.parse_args()

    if args.command == "crop":
        crop(
            args.image_file,
            args.out_dir,
            args.model,
            args.image_only,
        )
    elif args.command == "predict":
        predict(args.image_file, args.out_dir, args.model)
    elif args.command == "combine":
        combine(*args.files, out_dir=args.out_dir)
    elif args.command == "track":
        track(
            args.labels_file,
            args.image_file,
            args.lungs_file,
            args.out_dir,
            args.reg,
            args.max_dist,
            args.memory,
            args.dist_ratio,
            args.vol_diff,
            args.method,
            args.reg_level,
            args.lab,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
