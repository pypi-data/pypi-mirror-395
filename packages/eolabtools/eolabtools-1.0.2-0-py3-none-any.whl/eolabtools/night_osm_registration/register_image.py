# -- coding: utf-8 --
"""Night visible data registration based on OSM reference

:authors: see AUTHORS file
:organization: CNES
:copyright: CNES. All rights reserved.
:license: see LICENSE file
:created: 2024
"""

import argparse
from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
import yaml
from osgeo import gdal
from rasterio import mask
from skimage.morphology import binary_closing

from .osm_utils import get_osm_raster
from .shift import apply_shift, compute_displacement_grid, compute_shift


def crop_raster(
    roi_file: str, raster_src: rasterio.io.DatasetReader, raster_crop: Path
):
    """Crop input raster from ROI"""

    profile = raster_src.profile.copy()

    # Reproj ROI in raster crs
    roi = gpd.read_file(roi_file).to_crs(raster_src.crs)
    roi_list = roi.geometry

    if not raster_crop.exists():
        print("Cropping the input raster")

        cropped_raster, cropped_transform = mask.mask(raster_src, roi_list, crop=True)
        _, height, width = cropped_raster.shape
        profile.update(
            {"transform": cropped_transform, "height": height, "width": width}
        )
        with rasterio.open(raster_crop, "w", **profile) as writer:
            writer.write(cropped_raster)
    else:
        print("Crop input raster already exists, skipping this step...")

    return rasterio.open(raster_crop), roi_list


def raster_to_bin(
    raster: rasterio.io.DatasetReader,
    rgb_weights: tuple[int] = (0.2989, 0.5870, 0.1140),
    S: float = 10,
) -> np.ndarray:
    """
    Build panchromatic raster from r, g, b bands and then apply binary closing
    :param raster: raster source
    :param rgb_weights: (red, green, blue) coefficients to compute brightness
    :param S: threshold to binarize a radiance raster
    :return: raster binarized and eventually cropped
    """

    if raster.count == 1:
        # one band with radiance information
        raster_pan = raster.read(1)
        raster_pan[raster_pan <= S] = 0
        raster_pan[raster_pan > S] = 1
    elif raster.count >= 3:
        # Combine R, G, B bands to produce brightness image
        r, g, b = rgb_weights
        raster_pan = r * raster.read(1) + g * raster.read(2) + b * raster.read(3)
        raster_pan[raster_pan <= S] = 0
        raster_pan[raster_pan > S] = 1
    else:
        raise ValueError(f"Invalid input image band count: {raster_pan.count}")

    raster_pan = raster_pan.astype(np.uint8)
    # Binary closing
    raster_bin = binary_closing(raster_pan, out=raster_pan)

    return raster_bin


def nparray_to_csv(array: np.ndarray, path: Path):
    """Helper function to write nparray to csv"""
    np.savetxt(path, array, fmt="%i", delimiter=",")


def getarguments():
    """Main function with argument paser, for script entrypoint"""
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="Path to input raster file to compute shift")
    parser.add_argument(
        "auxfiles",
        nargs="*",
        help="List of auxiliary image to apply shift",
    )
    parser.add_argument(
        "-o", "--outdir", required=True, help="Path to output directory"
    )
    parser.add_argument("--config", required=True, help="Path to configuration file")
    parser.add_argument(
        "--osm-config", required=True, help="Path to OSM tags configuration file"
    )
    # Read arguments as dict
    args = vars(parser.parse_args())

    # Load configuration files as dict
    with open(args["config"]) as f:
        config = yaml.safe_load(f)
    with open(args["osm_config"]) as f:
        osm_tags = yaml.safe_load(f)

    # Merge parsed args and config file in a new dict
    del args["config"], args["osm_config"]
    settings = args | config
    settings["osm_tags"] = osm_tags
    # Make sure to check that config keys matches run() arguments
    print(settings)
    return settings


def night_osm_image_registration(
    infile: str,
    outdir: str,
    osm_tags: dict,
    window_size: int = None,
    max_shift: int = None,
    subsampling: int = None,
    osm_dataset: str = None,
    road_buffer_size: float = None,
    water_vector: str = None,
    roi_file: str = None,
    radiance_threshold: float = 10,
    raster_bin_path: str = None,
    raster_osm_path: str = None,
    auxfiles: list[str] = None,
    proxy: str = None,
):
    """Core function, called in main() after parsing arguments"""
    # Create out directory if not exists
    outdir = Path(outdir)
    outdir.mkdir(exist_ok=True, parents=True)

    # Load raster
    infile = Path(infile)
    raster_src = rasterio.open(infile)
    profile = raster_src.profile.copy()

    """
    0. Crop night raster if needed
    """

    infile, profile, raster_src, roi_list = crop_night_raster(infile, outdir, profile, raster_src, roi_file)

    """
    1. Transform night raster into binary raster
    """
    bin_profile, raster_bin = night_raster_2_binary(infile, outdir, profile, radiance_threshold, raster_bin_path,
                                                    raster_src)

    """
    2. Get OSM building vector data and convert it to raster
    """
    raster_osm = osm_build_vector(bin_profile, infile, osm_dataset, osm_tags, outdir, profile, proxy, raster_osm_path,
                                  raster_src, road_buffer_size, roi_list, water_vector)

    """
    3. Compute colocalisation error between raster and osm locally for each tile
    """

    shift_dir, shift_val = compute_colocalisation_error(infile, max_shift, outdir, profile, raster_bin, raster_osm,
                                                        subsampling, window_size)

    """
    4. Compute displacement grid (size of raster_src)
    """
    print("Compute displacement grid")
    disp_grid = compute_displacement_grid(
        raster_src.shape, shift_val, window_size, max_shift, subsampling
    )

    disp_grid_path = shift_dir / "displacement_grid.tif"
    tmp_profile = profile.copy()
    tmp_profile.update({"count": 2, "dtype": disp_grid.dtype, "nodata": -9999.0})
    with rasterio.open(disp_grid_path, mode="w", **tmp_profile) as new_dataset:
        new_dataset.write(disp_grid)

    """
    5. Apply Shift on the cropped image via OTB GridBasedImageResampling. If the input image is RGB, the shifted output is in total radiance
    """
    apply_shift(infile, disp_grid, shift_dir)
    if not auxfiles:
        return

    """
    6. Apply shift on an auxiliary image if needed
    """

    for image_path in auxfiles:
        print(f"Processing auxiliary file: {image_path}")
        # Check & Create Shift result folder
        image_path = Path(image_path)
        aux_raster_src = rasterio.open(image_path)

        # Crop image_path like infile if necessary
        if roi_file is not None:
            aux_raster_crop = outdir / f"{image_path.stem}_cropped.tif"
            aux_raster_src, _ = crop_raster(roi_file, aux_raster_src, aux_raster_crop)
            image_path = aux_raster_crop

        if aux_raster_src.res == raster_src.res:
            aux_disp_grid = disp_grid
        else:
            # Resample displacement grid from infile res to aux res
            xres, yres = aux_raster_src.res
            aux_dispgrid_path = shift_dir / f"{image_path.stem}_displacement_grid.tif"
            gdal.Warp(
                str(aux_dispgrid_path),
                str(disp_grid_path),
                xRes=xres,
                yRes=yres,
                resampleAlg="average",
            )
            aux_disp_grid_src = rasterio.open(aux_dispgrid_path)
            aux_disp_grid = aux_disp_grid_src.read([1, 2])

            # Adapt displacement value to the new resolution
            ratio = aux_raster_src.res[0] / raster_src.res[0]
            aux_disp_grid = aux_disp_grid / ratio
            aux_disp_grid = (np.round(aux_disp_grid)).astype(disp_grid.dtype)
            with rasterio.open(
                aux_dispgrid_path, "w", **aux_disp_grid_src.profile
            ) as writer:
                writer.write(aux_disp_grid)

        # Apply new displacement grid
        apply_shift(image_path, aux_disp_grid, shift_dir)


def compute_colocalisation_error(infile, max_shift, outdir, profile, raster_bin, raster_osm, subsampling, window_size):
    shift_val, shift_pos, tiles, shift_mask, filtered_shift_mask = compute_shift(
        raster_bin, raster_osm, window_size, max_shift
    )
    del raster_bin
    del raster_osm
    # Check & Create Shift result folder
    shift_dir = outdir / f"{infile.stem}_MS{max_shift}_WS{window_size}_SS{subsampling}"
    shift_dir.mkdir(exist_ok=True, parents=True)
    tmp_profile = profile.copy()
    tmp_profile.update({"count": 1, "dtype": shift_mask.dtype, "nodata": None})
    with rasterio.open(
            shift_dir / "shift_mask.tif", mode="w", **tmp_profile
    ) as new_dataset:
        new_dataset.write(shift_mask, 1)
    out_filtered_shift = shift_dir / "filtered_shift_mask.tif"
    with rasterio.open(out_filtered_shift, mode="w", **tmp_profile) as new_dataset:
        new_dataset.write(filtered_shift_mask, 1)
    #  Save np array and Plot Quiver
    nparray_to_csv(shift_val[0], shift_dir / "row_offset_value.csv")
    nparray_to_csv(shift_val[1], shift_dir / "column_offset_value.csv")
    nparray_to_csv(shift_pos[0], shift_dir / "row_offset_position.csv")
    nparray_to_csv(shift_pos[1], shift_dir / "column_offset_position.csv")
    return shift_dir, shift_val


def osm_build_vector(bin_profile, infile, osm_dataset, osm_tags, outdir, profile, proxy, raster_osm_path, raster_src,
                     road_buffer_size, roi_list, water_vector):
    if raster_osm_path is None:
        raster_osm_path = outdir / f"{infile.stem}_osm.tif"
    if Path(raster_osm_path).exists():
        print("OSM binary raster already exists, skipping this step...")
        raster_osm = rasterio.open(raster_osm_path).read(1)
    else:
        print("Create OSM binary raster")
        raster_osm = get_osm_raster(
            osm_tags,
            osm_dataset,
            raster_src,
            roi_list,
            outdir,
            water_vector,
            road_buffer_size,
            proxy,
        )
        # Save file
        tmp_profile = profile.copy()
        tmp_profile.update(bin_profile)
        with rasterio.open(raster_osm_path, mode="w", **tmp_profile) as new_dataset:
            new_dataset.write(raster_osm, 1)
    return raster_osm


def night_raster_2_binary(infile, outdir, profile, radiance_threshold, raster_bin_path, raster_src):
    bin_profile = {
        "nodata": None,
        "dtype": np.uint8,
        "count": 1,
        # For compressed 1 bit outputs
        "nbits": 1,
        "compress": "CCITTFAX4",
    }
    if raster_bin_path is None:
        raster_bin_path = outdir / f"{infile.stem}_binary.tif"
    if Path(raster_bin_path).exists():
        print("Binary input raster already exists, skipping this step...")
        raster_bin = rasterio.open(raster_bin_path).read(1)
    else:
        print("Binarization of input raster")
        raster_bin = raster_to_bin(raster_src, S=radiance_threshold)
        # Save
        tmp_profile = profile.copy()
        tmp_profile.update(bin_profile)
        with rasterio.open(raster_bin_path, "w", **tmp_profile) as new_dataset:
            new_dataset.write(raster_bin, 1)
    return bin_profile, raster_bin


def crop_night_raster(infile, outdir, profile, raster_src, roi_file):
    if roi_file is not None:
        raster_crop = outdir / f"{infile.stem}_cropped.tif"
        raster_src, roi_list = crop_raster(roi_file, raster_src, raster_crop)
        profile = raster_src.profile.copy()
        infile = raster_crop
    else:
        roi_list = gpd.GeoSeries()
    return infile, profile, raster_src, roi_list


def main():
    """
    Main function to run night image registration.
    It parses the command line arguments and calls the night_osm_image_registration function.
    """
    args = getarguments()
    night_osm_image_registration(**args)

if __name__ == "__main__":
    main()
