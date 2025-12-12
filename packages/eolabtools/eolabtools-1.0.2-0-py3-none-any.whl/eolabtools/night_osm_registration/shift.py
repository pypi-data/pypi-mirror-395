"""Compute shift using Fourier Transform, then apply to image using OTB"""

from math import ceil
from pathlib import Path

import numpy as np
import rasterio
import cv2
from scipy import ndimage

KEEP_FILES = False


def apply_displacement_grid_opencv(otb_input, otb_displacementgrid, otb_output):
    with rasterio.open(otb_input) as src:
        image = src.read()  # shape: (bands, height, width)
        profile = src.profile
        bands, height, width = image.shape

    # Read displacement grid (dx, dy in pixels)
    with rasterio.open(otb_displacementgrid) as grid:
        dx = grid.read(1)  # X displacement (cols)
        dy = grid.read(2)  # Y displacement (rows)

    # Create meshgrid of original coordinates
    x, y = np.meshgrid(np.arange(width), np.arange(height))

    # Compute source (warped) coordinates
    map_x = (x + dx).astype(np.float32)
    map_y = (y + dy).astype(np.float32)

    # OpenCV interpolation map
    interp_map = {
        "nn": cv2.INTER_NEAREST,
        "linear": cv2.INTER_LINEAR,
        "bco": cv2.INTER_CUBIC  # Cubic approx to OTB bco
    }
    interpolation = interp_map.get("nn", cv2.INTER_LINEAR)

    # Prepare output array
    warped = np.empty_like(image, dtype=np.float32)

    # Apply remap per band
    for b in range(bands):
        warped[b] = cv2.remap(
            image[b].astype(np.float32), map_x, map_y,
            interpolation,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=0
        )

    # Update profile data type if needed
    profile.update(dtype=rasterio.float32)

    # Write warped raster
    with rasterio.open(otb_output, "w", **profile) as dst:
        dst.write(warped.astype(np.float32))


def get_shift_via_fft(raster_a: np.ndarray, raster_b: np.ndarray) -> tuple[np.ndarray]:
    # Get the spectral constituents for image 1 and its complex conjugate for image 2:
    image1_fft = np.fft.fft2(raster_a)
    image2_fft = np.conjugate(np.fft.fft2(raster_b))

    # Now we can directly correlate the two images (spectral cross correlation):
    cross_corr = np.real(np.fft.ifft2((image1_fft * image2_fft)))

    # The cross correlation matrix is mirrored so we need to do a fftshift :
    cross_corr_shift = np.fft.fftshift(cross_corr)

    # Now we can look for the correlation with the maximum amplitude :
    row, col = raster_a.shape

    row_shift, col_shift = np.unravel_index(np.argmax(cross_corr_shift), (row, col))

    row_shift -= int(row / 2)
    col_shift -= int(col / 2)

    return -row_shift, -col_shift


def compute_shift(
    raster_a: np.ndarray, raster_b: np.ndarray, tile_size: int, max_shift_thr: int
):
    shift_mask = np.zeros_like(raster_a, dtype=np.uint8)
    filtered_shift_mask = np.zeros_like(raster_a, dtype=np.uint8)

    n_row = ceil(raster_a.shape[0] / tile_size)
    n_col = ceil(raster_a.shape[1] / tile_size)

    shift_row_pos = np.zeros((n_row, n_col), dtype=np.int32)
    shift_col_pos = np.zeros((n_row, n_col), dtype=np.int32)
    shift_row_val = np.zeros((n_row, n_col), dtype=np.int32)
    shift_col_val = np.zeros((n_row, n_col), dtype=np.int32)
    dt = np.dtype((np.int64, (4,)))
    tiles = np.empty((n_row, n_col), dtype=dt)

    # print("Compute shift for %i tiles" % (n_row * n_col))

    for i in range(n_row):
        for j in range(n_col):
            k = j + n_col * i
            # print(i, j, "%i/%i" % (k, n_row * n_col))

            bounds = [
                i * tile_size,
                j * tile_size,
                min((i + 1) * tile_size, raster_a.shape[0]),
                min((j + 1) * tile_size, raster_a.shape[1]),
            ]
            tile_a = raster_a[bounds[0] : bounds[2], bounds[1] : bounds[3]]
            tile_b = raster_b[bounds[0] : bounds[2], bounds[1] : bounds[3]]

            if np.all(tile_a == 0) or np.all(tile_b == 0):
                continue

            dec_li, dec_co = get_shift_via_fft(tile_a, tile_b)

            # print(f"Values before filtering: {dec_li=}, {dec_co=}")

            # déplacement du filtrage par rapport max-shift plus loin pour interpoler
            # les valeurs selon les voisins plutôt que de supposer un déplacement nul
            # if abs(dec_co) > max_shift_thr or abs(dec_li) > max_shift_thr:
            #    continue

            shift_row_pos[i, j] = bounds[0] + int((bounds[2] - bounds[0]) / 2)
            shift_col_pos[i, j] = bounds[1] + int((bounds[3] - bounds[1]) / 2)
            shift_row_val[i, j] = dec_li
            shift_col_val[i, j] = dec_co
            tiles[i, j] = bounds
            # draw the shift in the mask
            startPoint = (shift_col_pos[i, j], shift_row_pos[i, j])
            endPoint = (shift_col_pos[i, j] + dec_co, shift_row_pos[i, j] + dec_li)

            if abs(dec_co) > max_shift_thr or abs(dec_li) > max_shift_thr:
                filtered_shift_mask = cv2.arrowedLine(
                    filtered_shift_mask, startPoint, endPoint, 1, 1
                )
            else:
                shift_mask = cv2.arrowedLine(shift_mask, startPoint, endPoint, 1, 1)

    return (
        (shift_row_val, shift_col_val),
        (shift_row_pos, shift_col_pos),
        tiles,
        shift_mask,
        filtered_shift_mask,
    )


def grid_hole_filling(src: np.ndarray) -> np.ndarray:
    nl = src.shape[0]
    nc = src.shape[1]
    # Replace filtered value by mean of 3*3 window
    for i in range(nl):
        for j in range(nc):
            if np.isnan(src[i, j]):
                imin = max(i - 1, 0)
                imax = min(i + 1, nl - 1)
                jmin = max(j - 1, 0)
                jmax = min(j + 1, nc - 1)
                window = src[imin : imax + 1, jmin : jmax + 1]
                mean = np.nanmean(window)
                if np.isnan(mean):
                    mean = 0
                src[i, j] = mean

    return src


def compute_displacement_grid(
    shape: tuple[int],
    shift_val: tuple[np.ndarray],
    window_size: int,
    max_shift: int,
    subsampling: int,
):
    # Outliers removal
    # Identify position where absolute values exceed a given threshold
    shift_row_val, shift_col_val = shift_val
    mask_row_shift = abs(shift_row_val) > max_shift
    mask_col_shift = abs(shift_col_val) > max_shift

    # Merge both masks to allow filtering to be applied to both shifts grids
    mask = mask_row_shift | mask_col_shift

    # Set Outliers to NaN in Displacements grids (remove shifts if line shift OR colum shift is higher than max_shift))
    shift_row_val = shift_row_val.astype(np.float32)
    shift_col_val = shift_col_val.astype(np.float32)
    shift_row_val[np.where(mask)] = np.nan
    shift_col_val[np.where(mask)] = np.nan

    # Mean to fill filtered values
    shift_row_val = grid_hole_filling(shift_row_val)
    shift_col_val = grid_hole_filling(shift_col_val)

    # Shifts values Replication according to intermediate resolution
    # Such a step allows keeping central shift values at the center of
    # the subtiles to force interpolation at the subtiles edges ONLY!
    # subsampling = 1 -> interpolation on all the subtile
    #          -------------------------------------
    #          | Shift Interpolation Only at EdgeS |
    #          | h ----------------------------- h |
    #          | i |                           | i |
    #          | f |                           | f |
    #          | t |                           | t |
    #          |   |                           |   |
    #          | I |                           | I |
    #          | n |                           | n |
    #          | t |      Keep Unchanged       | t |
    #          | e |       Shift Values        | e |
    #          | r |                           | r |
    #          | p |                           | p |
    #          |   |                           |   |
    #          | E |                           | E |
    #          | d |                           | d |
    #          | g |                           | g |
    #          | e ----------------------------- e |
    #          | Shift Interpolation Only at EdgeS |
    #          -------------------------------------
    shift_row_val = np.kron(shift_row_val, np.ones((subsampling, subsampling)))
    shift_col_val = np.kron(shift_col_val, np.ones((subsampling, subsampling)))

    # Resize to Radiance image dimension with spline interpolation
    zoom_factor = window_size / subsampling
    shift_row_val = ndimage.zoom(shift_row_val, (zoom_factor, zoom_factor), order=3)
    shift_col_val = ndimage.zoom(shift_col_val, (zoom_factor, zoom_factor), order=3)

    (ys, xs) = shape
    # Resize Interpolated Grids to fit cropped radiance image dimensions
    shift_row_val = shift_row_val[np.arange(ys), :][:, np.arange(xs)]
    shift_col_val = shift_col_val[np.arange(ys), :][:, np.arange(xs)]

    # plt.imshow(shift_row_val)
    # plt.show()
    # plt.imshow(shift_col_val)
    # plt.show()

    # Displacement Grid (opposite sign shift to be compliant with OTB GridBasedImageResampling
    disp_grid = np.stack((-shift_col_val, -shift_row_val), axis=0)
    # Round disp_grid to ensure relevant int type format
    disp_grid = np.round(disp_grid).astype(np.int16)

    return disp_grid


def apply_shift(infile: Path, disp_grid: np.ndarray, outdir: Path):
    """Apply Shift on the cropped image via OTB GridBasedImageResampling.
    Note: OTB GridBasedImageResampling needs input without transform information (for both input image and grid)
    """
    # Output filenames
    basename = infile.stem
    otb_input = outdir / f"{basename}_OTB_input_raster.tif"
    otb_displacementgrid = outdir / f"{basename}_OTB_displacement_grid.tif"
    otb_output = outdir / f"{basename}_OTB_shifted.tif"
    out_shifted = outdir / f"{basename}_shifted.tif"

    raster_src = rasterio.open(infile)
    raster = raster_src.read()
    tmp_profile = raster_src.profile.copy()

    # Write displacement grid without transform
    tmp_profile.update(
        {"count": 2, "dtype": "int16", "nodata": -9999.0, "transform": None}
    )
    with rasterio.open(otb_displacementgrid, "w", **tmp_profile) as new_dataset:
        new_dataset.write(disp_grid)

    # Write input image without transform
    tmp_profile = raster_src.profile.copy()
    tmp_profile.update({"transform": None})
    with rasterio.open(otb_input, "w", **tmp_profile) as new_dataset:
        new_dataset.write(raster)

    apply_displacement_grid_opencv(otb_input, otb_displacementgrid, otb_output)

    # Add transform to shifted raster
    otb_shifted_cropped_raster = rasterio.open(otb_output).read()
    tmp_profile = raster_src.profile.copy()
    if raster_src.count == 3:
        tmp_profile.update({"photometric": "RGB"})
    elif raster_src.count == 4:
        tmp_profile.update({"photometric": "RGB", "alpha": "YES"})
    with rasterio.open(out_shifted, "w", **tmp_profile) as new_dataset:
        new_dataset.write(otb_shifted_cropped_raster)

    if not KEEP_FILES:
        otb_input.unlink()
        otb_displacementgrid.unlink()
        otb_output.unlink()
