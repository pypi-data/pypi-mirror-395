import argparse
import concurrent.futures
import csv
import glob
import math
import os
import statistics
import time
from datetime import datetime
from functools import partial
from multiprocessing import Manager
from typing import List, Tuple
from collections import Counter

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import rasterio.mask
import shapely
from shapely.ops import unary_union, polygonize
from rasterio.windows import Window
from shapely.geometry import (LineString, MultiLineString, Point, Polygon, box,
                              shape)
from sklearn.cluster import MeanShift, estimate_bandwidth

from .utils import (compute_angles, sec_to_hms,
                   filter_segments, fld_segment_detect,
                   get_mean_slope_aspect, normalize_img, save_centroids_orientations,
                   split_img_borders, split_img_dataset, split_windows, compute_centroids, set_str_to_all,
                   extend_line, transform, export_save_fld, clip_data_to_window)

import warnings
import logging
import ssl
import sys

ssl._create_default_https_context = ssl._create_unverified_context
warnings.filterwarnings("ignore")

_logger = logging.getLogger(__name__)


def get_splitting_lines(
        intersections: List[Polygon],
        parcel: Polygon,
        id_parcel: int
):
    """
        Get shapes of multi oriented parcels

        Parameters
        ----------
        intersections: List containing the Polygon shapes created from intersection
        parcel: Polygon of the initial crop

        Returns
        -------
        lines_list: List containing the LineString to keep to split the parcel later
    """

    lines_list = []
    for shape in intersections:
        try:
            points = list(shape)
        except TypeError as e:
            _logger.debug("ERROR comes from ", id_parcel)
            return []
        if len(points) > 2:
            return []
        try:
            line = LineString(points)
        except ValueError as e:
            _logger.debug("ValueError comes from ", id_parcel)
            return []

        where = 'both'
        extended_line = extend_line(line, 5, where)

        # extend line until its larger than the shape
        while parcel.contains(Point(extended_line.coords[0])) or parcel.contains(Point(extended_line.coords[1])):
            if not parcel.contains(Point(extended_line.coords[0])):
                where = 'end'
            if not parcel.contains(Point(extended_line.coords[1])):
                where = 'start'
            extended_line = extend_line(extended_line, 5, where)

        lines_list.append(extended_line)

    return lines_list


def get_pseudo_patches(
        polygon_list: List[Polygon],
        parcel: Polygon,
        id_parcel: int
):
    """
        Get shapes of multi oriented parcels

        Parameters
        ----------
        polygon_list: List containing the Polygon shapes (convex hull)

        Returns
        -------
        patches_list: List containing the shapes of the pseudo parcels
    """
    centroids = [poly.centroid for poly in polygon_list]

    intersection_shapes = []
    for i in range(len(centroids)):
        for j in range(i + 1, len(centroids)):
            inter = polygon_list[i].intersection(polygon_list[j])

            s1 = polygon_list[i]
            s2 = polygon_list[j]

            while inter.is_empty:
                s1 = s1.buffer(5)
                s2 = s2.buffer(5)
                inter = s1.intersection(s2)

            if s1.contains(s2) or s2.contains(s1):
                _logger.debug(f"parcel {id_parcel} is complex")
            else:
                inter = s1.boundary.intersection(s2.boundary)
                intersection_shapes.append(inter)

    splitting_lines = get_splitting_lines(intersection_shapes, parcel, id_parcel)

    if len(splitting_lines) == 0:
        return [parcel], []

    splitting_lines.append(parcel.boundary)  # append the boundary of the Polygon
    border_lines = unary_union(splitting_lines)
    splitted_shapes = polygonize(border_lines)
    splitted_shapes = list(splitted_shapes)

    # calcul des centroids de chaque polygone
    centroids_shapes = [poly.centroid for poly in splitted_shapes]
    areas_shapes = [poly.area for poly in splitted_shapes]

    clusters = []
    for c, a in zip(centroids_shapes, areas_shapes):
        distances = [p.distance(c) for p in centroids]
        clusters.append(distances.index(min(distances)))

    clusters = np.array(clusters)
    splitted_shapes = np.array(splitted_shapes)
    splitted_shapes = [unary_union(list(splitted_shapes[np.where(clusters == c)])) for c in range(len(centroids))]

    return splitted_shapes, intersection_shapes


def detect_multiple_orientations(
        fld_lines: List[LineString],
        vectx: List[float],
        vecty: List[float],
        len_lines: List[float],
        orientation: LineString,
        min_nb_line_per_parcelle: int,
        parcel_id: int
):
    """
        Detect if a parcel contains multiple orientations and compute these orientations

        Parameters
        ----------
        fld_lines: list of detected segments of one parcel
        vectx: the normalized x coordinates of the segments
        vecty: the normalized y coordinates of the segments
        len_lines: the lengths of the segments
        orientation: the orientation computed using the segments
        min_nb_line_per_parcelle: the minimum number of segments needed to compute a parcel's orientation

        Returns
        -------
        int
            the number of detected orientations
        dict
            a dictionnary containing:
            - the orientations
            - their centroids
            - the average length of the segments
            - the number of segments used
            - the std of the segments x coordinates
            - the std of the segments y coordinates
    """

    gdf_ = gpd.GeoDataFrame(geometry=[orientation])

    pd_lines = pd.DataFrame(fld_lines)

    v2 = orientation.coords
    v2 = np.array([v2[1][0] - v2[0][0], v2[1][1] - v2[0][1]])

    np.random.seed(2)
    r = np.random.randn(*v2.shape)
    angle_ortho = r - np.dot(r, v2) / np.dot(v2, v2) * v2
    angle_ortho = angle_ortho * 1000

    ortho_coords = list(orientation.coords)
    ortho_coords[1] = (angle_ortho[0] + ortho_coords[0][0], angle_ortho[1] + ortho_coords[0][1])
    ortho_coords = LineString(ortho_coords)

    centroids = pd_lines[pd_lines.columns[0]].apply(compute_centroids)
    centroids.columns = ['x', 'y']

    angles = pd_lines.applymap(partial(compute_angles, l_right=orientation, ortho=angle_ortho))
    # angles = angles.to_numpy().reshape(-1)

    # # We compute the angles histogram and count the peaks ie the clusters of segments
    hist, bins = np.histogram(pd.DataFrame([a if a < 160 else 180 - a for a in angles[0]]), bins=9,
                              range=(0, 180))

    # penalty = hist[0] > min_nb_line_per_parcelle and hist[-1] > min_nb_line_per_parcelle
    num_orient = len(hist[hist > min_nb_line_per_parcelle])  # - penalty

    if num_orient < 2:
        return num_orient, None

    _logger.info(f"[{parcel_id}] Multiple orientations found ({num_orient})")

    # if penalty:
    angles = angles.applymap(transform)

    data = pd.concat([angles, centroids], axis=1)
    data.columns = data.columns.astype('str')

    # normalize
    data = (data - data.min()) / (data.max() - data.min())

    # Mean shift
    b = estimate_bandwidth(data, random_state = 42)

    # grant more importance to angles than centroids
    data = data * [4, 1, 1]
    ms = MeanShift(bandwidth=b, bin_seeding=True).fit(data)
    clusters = ms.labels_

    counts = Counter(list(clusters))

    # identify the numbers that occur more than the threshold
    clusters_to_keep = [num for num, count in counts.items() if count > min_nb_line_per_parcelle]
    num_orient = len(clusters_to_keep)

    # We keep only the top 3 clusters of segments
    if num_orient > 4:
        clusters_to_keep = clusters_to_keep[:4]

    if len(clusters_to_keep) == 0:
        return 1, None

    orient_dict = compute_multiple_orientations(clusters, clusters_to_keep, fld_lines, len_lines, parcel_id, vectx,
                                  vecty)

    return len(clusters_to_keep), orient_dict


def compute_multiple_orientations(
        clusters,
        clusters_to_keep,
        fld_lines,
        len_lines,
        parcel_id,
        vectx,
        vecty
    ):
    """
    Compute orientation lines and statistics for plots with multiple orientations.

    Parameters:
    -----------
    clusters : array-like
        An array or list assigning each line segment to a cluster label.
    clusters_to_keep : iterable
        A list or set of cluster labels to process.
    fld_lines : list of shapely LineString
        The geometries corresponding to the input clusters.
    len_lines : array-like
        Lengths of each line segment.
    parcel_id : int or str
        Identifier for the parcel to which these clusters belong.
    vectx : array-like
        x-components of the orientation vectors of line segments.
    vecty : array-like
        y-components of the orientation vectors of line segments.

    Returns:
    --------
    orient_dict : dict
    """
    orient_dict = {"orientations": [], "centroids": [], "mean_len_lines": [
    ], "nb_lines_used": [], "std_orient_x": [], "std_orient_y": [], "min_bounding_box": []}

    for k in clusters_to_keep:

        ind_pseudo = list(clusters == k)
        vectx_pseudo = np.array(vectx)[ind_pseudo]
        vecty_pseudo = np.array(vecty)[ind_pseudo]
        len_lines_pseudo = np.array(len_lines)[ind_pseudo]

        fld_lines_pseudo = []
        for i in range(len(ind_pseudo)):
            if ind_pseudo[i]:
                fld_lines_pseudo.append(fld_lines[i])
        df = gpd.GeoDataFrame(geometry=fld_lines_pseudo)

        # Compute statistics
        mean_len_lines = statistics.mean(len_lines_pseudo)
        nb_lines_used = len(vectx_pseudo)
        std_orient_x = statistics.stdev(vectx_pseudo)
        std_orient_y = statistics.stdev(vecty_pseudo)

        xmed = statistics.median(vectx_pseudo)
        ymed = statistics.median(vecty_pseudo)

        # Get the "pseudo" parcel using the cluster of segments convex hull
        pseudo_parcel = MultiLineString(list(fld_lines_pseudo)).convex_hull
        centroid = pseudo_parcel.centroid

        # Coordinates of the pseudo parcels centroid
        xc = centroid.x
        yc = centroid.y

        # to get bigger lines, we can use the bounds of the pseudo parcel :
        av = (pseudo_parcel.bounds[2] - pseudo_parcel.bounds[0]) / \
             4 + (pseudo_parcel.bounds[3] - pseudo_parcel.bounds[1]) / 4

        # to have a minimum length of the line orientation :
        min_length_orientation = 40
        if av >= min_length_orientation:
            pseudo_orient = LineString(
                [((xc - xmed * av), (yc - ymed * av)), ((xc + xmed * av), (yc + ymed * av))])
        else:
            pseudo_orient = LineString([((xc - xmed * min_length_orientation), (yc - ymed * min_length_orientation)),
                                        ((xc + xmed * min_length_orientation), (yc + ymed * min_length_orientation))])

        orient_dict["orientations"].append(pseudo_orient)
        orient_dict["centroids"].append(centroid)
        orient_dict["mean_len_lines"].append(mean_len_lines)
        orient_dict["nb_lines_used"].append(nb_lines_used)
        orient_dict["std_orient_x"].append(std_orient_x)
        orient_dict["std_orient_y"].append(std_orient_y)
        orient_dict["min_bounding_box"].append(pseudo_parcel)
        orient_dict["id_parcel"] = parcel_id

    return orient_dict


def orientation_from_lines(
        vectx: List[float],
        vecty: List[float],
        pol: Polygon,
        value_mean_aspect: float
) -> Tuple[LineString, float, float]:
    """
    Extract global orientation from detected lines,
    calculate the azimuth angle associated,
    and the angle between the slope and the orientation.

    Parameters
    ----------
        vectx: x coordinates of the detected lines
        vecty: y coordinates of the detected lines
        pol: the RPG polygon
        value_mean_aspect

    Returns
    -------
        LineString
            the computed orientation
        float
            value_calc_aspect
        float
            indic_orient
    """

    # Calculating the median value of x and y  :
    # we have the median vector ie the median orientation of the parcel, Pmed=(xmed, ymed)
    xmed = statistics.median(vectx)
    ymed = statistics.median(vecty)
    # Coordinates of the centroid of the polygon
    xc = pol.centroid.x
    yc = pol.centroid.y

    # to get bigger lines, we can use the bounds of the polygon :
    av = (pol.bounds[2] - pol.bounds[0]) / 4 + \
         (pol.bounds[3] - pol.bounds[1]) / 4

    # to have a minimum length of the line orientation :
    min_length_orientation = 40
    if av >= min_length_orientation:
        final_linestrings_orientation = LineString(
            [((xc - xmed * av), (yc - ymed * av)), ((xc + xmed * av), (yc + ymed * av))])
    else:
        final_linestrings_orientation = LineString(
            [((xc - xmed * min_length_orientation), (yc - ymed * min_length_orientation)), ((
                                                                                                    xc + xmed * min_length_orientation),
                                                                                            (
                                                                                                        yc + ymed * min_length_orientation))])

    # convert the computed orientation vector into azimuth angle
    value_calc_aspect = 180 + math.degrees(math.atan2(xmed, ymed))

    # compute the indicator between the orientation of the plot and the slope orientation (both are in azimut angle)
    # 0 = plot orientation is in the same direction as the slope ; 90 = orientation is perpendicular to the direction of the slope.
    # 2nd version : is working as well, faster
    relativ_angle = (360 - value_mean_aspect +
                     value_calc_aspect) % 180  # modulo 180
    # the indicator is computed
    indic_orient = relativ_angle if relativ_angle <= 90 else 180 - relativ_angle

    return final_linestrings_orientation, value_calc_aspect, indic_orient


def compute_orientation(
        ind: int,
        RPG: gpd.GeoDataFrame,
        FLD: gpd.GeoDataFrame,
        slope: str,
        aspect: str,
        window_bb: shapely.geometry.box,
        area_min: float,
        parcel_ids_processed: list,
        min_nb_line_per_parcelle: int,
        min_len_line: float,
        time_slope_aspect: float,
        time_calculate_orientation: float,
        verbose: bool
):
    """
    Extract the orientation(s) of the parcel from detected lines,
    calculate the azimuth angle associated,
    and the angle between the slope and the orientation.

    Parameters
    ----------
        ind: the index of the parcel in the RPG
        RPG: the GeoDataFrame containing the parcels
        FLD: the GeoDataFrame containing the detected segments
        slope: the path to the slope file
        aspect: the path to the aspect file
        windows_bb: the window's bounding box
        area_min: a parameter used to calculate the minimum number of lines needed to compute the orientation of a parcel in relation to its area
        parcel_ids_processed: a list containing the ids of the parcel already handled
        min_nb_line_per_parcelle: the minimum number of lines needed to compute the orientation of a parcel
        min_len_line: the minimum length of a segment to be used in the orientation calculation
        time_slope_aspect: variable shared between processes to track process time
        time_slope_aspect: variable shared between processes to track process time
        verbose: boolean indicating whether or not to print all messages

    Returns
    -------
        list
            a list containing the computed orientation(s)
        list
            a list containing the computed centroid(s)
        str
            CODE_GROUP
        str
            CODE_CULTU
        list
            a list containing the number of lines used to compute each orientation
        int
            the number of orientations detected
        list
            a list containing the average lengths of the segments used to compute each orientation
        list
            a list containing the std of the segments x coordinates used to compute each orientation
        list
            a list containing the std of the segments y coordinates used to compute each orientation
        float
            value_mean_slope
        float
            value_mean_aspect
        float
            value_calc_aspect
        float
            indic_orient
        str
            the id of the parcel
        list
            a list of LineString that where used to compute the orientation(s)
        list
            a list of Polygon of the pseudo parcels
    """
    delta_calculate_orientation = time.process_time()

    # Get the parcel polygon
    pol = RPG.at[ind, "geometry"]
    centroid = [pol.centroid]

    # Get the id of the parcel
    ID_PARCEL = RPG.at[ind, "ID_PARCEL"]

    # Check if the parcel is not fully within the patch
    processed = ID_PARCEL in parcel_ids_processed

    # Check if the parcel has already been processed
    if processed:
        _logger.info(f"[{ID_PARCEL}] Skipping parcel: already processed")
        return

    # Erode the polygon edges to filter out the segments on the border
    # The erosion is proportional to the parcel's area
    erosion = - 5 * np.max([1, np.log((pol.area / area_min) ** 2)])
    within = FLD.within(pol.buffer(erosion))
    inter = FLD.loc[within]

    # Check if any segment where detected in the polygon
    if inter.shape[0] < 1:
        _logger.info(f"[{ID_PARCEL}] Skipping parcel: no segment to compute the parcel orientation")
        return

    parcel_ids_processed.append(ID_PARCEL)

    code_group = RPG.at[ind, "CODE_GROUP"]
    code_cultu = RPG.at[ind, "CODE_CULTU"]

    # compute mean value of slope and aspect with zonal_stats
    value_mean_slope, value_mean_aspect = get_mean_slope_aspect(
        pol, slope, aspect, time_slope_aspect)

    if value_mean_aspect is None or value_mean_slope is None:
        _logger.info(
            f"[{ID_PARCEL}] Skipping parcel: mean slope value={value_mean_slope}, mean aspect value={value_mean_aspect}")
        return

    # Filter the segments
    vectx, vecty, len_lines, kept_lines = filter_segments(inter, min_len_line)

    if len(vectx) <= (min_nb_line_per_parcelle * np.max([1, pol.area / area_min])):
        _logger.info(f"[{ID_PARCEL}] Skipping parcel: not enough segments kept to compute the parcel orientation")
        return

    # Compute orientation
    _logger.info("Computing orientations")
    orientation, value_calc_aspect, indic_orient = orientation_from_lines(
        vectx,
        vecty,
        pol,
        value_mean_aspect
    )

    # computes statistics for quality criteria
    mean_len_lines = [statistics.mean(len_lines)]
    nb_lines_used = [len(vectx)]
    std_orient_x = [statistics.stdev(vectx)]
    std_orient_y = [statistics.stdev(vecty)]

    nb_orientations, orient_dict = detect_multiple_orientations(
        kept_lines, vectx, vecty, len_lines, orientation, min_nb_line_per_parcelle, ID_PARCEL)

    _logger.info(
        f"[{ID_PARCEL}] {nb_orientations} orientation{'s' if nb_orientations > 1 else ''} orientations detected")

    if orient_dict is not None:
        pseudo_patches, intersection_shapes = get_pseudo_patches(orient_dict["min_bounding_box"], pol,
                                                                 orient_dict["id_parcel"])
        orientation = orient_dict["orientations"]
        centroid = orient_dict["centroids"]
        mean_len_lines = orient_dict["mean_len_lines"]
        nb_lines_used = orient_dict["nb_lines_used"]
        std_orient_x = orient_dict["std_orient_x"]
        std_orient_y = orient_dict["std_orient_y"]
        bb = orient_dict["min_bounding_box"]
    else:
        orientation = [orientation]
        intersection_shapes = []
        bb = []
        pseudo_patches = [pol]

    delta_calculate_orientation = time.process_time() - delta_calculate_orientation
    time_calculate_orientation.set(
        time_calculate_orientation.value + delta_calculate_orientation)
    return orientation, centroid, code_group, code_cultu, nb_lines_used, nb_orientations, mean_len_lines, std_orient_x, std_orient_y, value_mean_slope, value_mean_aspect, value_calc_aspect, indic_orient, ID_PARCEL, kept_lines, pseudo_patches, intersection_shapes, bb


def orientation_worker(
        data: Tuple[str, gpd.GeoDataFrame, Window],
        normalize: bool,
        parcel_ids_processed: list,
        slope: str,
        aspect: str,
        area_min: float,
        increment: int,
        min_nline: int,
        min_len_line: int,
        time_inter_mask_open: float,
        time_slope_aspect: float,
        time_fld: float,
        time_orientation_worker: float,
        time_calculate_orientation: float,
        save_fld: bool,
        verbose: bool
) -> Tuple[gpd.GeoDataFrame, gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """
    Apply the FLD algorithm to the input image and compute the crop orientations for the parcels in the RPG.

    Parameters
    ----------
        data: a tuple containing the input image path, the rpg parcels, and an optionnal rasterio.Window with which to read the image
        normalize: boolean indicating whether or not the image has to be normalized
        parcel_ids_processed: a list (shared between all the worker instances) containing the already processed parcels ids
        slope: the path to the raster containing the slope values
        aspect: the path to the raster containing the aspect values
        area_min: a parameter used to calculate the minimum number of lines needed to compute the orientation of a parcel in relation to its area
        increment: value to keep track of LineString not kept
        min_nline: minimum valid number of segments inside a parcel
        min_len_line : minimum length (meters) for a valid segment
        time_inter_mask_open: shared variable to track process time to open, intersect with RPG and mask the image
        time_slope_aspect: shared variable to track process time to compute slope and aspect
        time_fld: shared variable to track process time to detect segments with FLD
        time_orientation_worker: shared variable to track process time to compute the orientations
        time_calculate_orientation: shared variable to track process time to calculate each orientation
        save_fld: bool indicating whether or not the segments used to compute the orientations have to be saved in file
        verbose: boolean indicating whether or not to print all messages

    Returns
    -------
        gpd.GeoDataFrame
            a gpd.GeoDataFrame containing the orientations
        gpd.GeoDataFrame
            a gpd.GeoDataFrame containing the centroids
        gpd.GeoDataFrame
            a gpd.GeoDataFrame containing the segments used to compute the orientations
    """

    start = time.process_time()

    crs, img, mask_dataset, profile, rpg, rpg_expanded, win_transform, window, window_bb = clip_data_to_window(data)

    if normalize:
        img = normalize_img(img, mask_dataset)
        _logger.info("Image normalized")

    # Mask with RPG and dataset mask
    mask_rpg = rasterio.features.rasterize(list(rpg_expanded),
                                           out_shape=img.shape[1:],
                                           transform=win_transform,
                                           fill=0,
                                           all_touched=True,
                                           dtype=rasterio.uint8)
    img = np.uint8(img)
    img = np.where(mask_dataset * mask_rpg, img, 0)

    if window is not None:
        profile.data["width"] = window.width
        profile.data["height"] = window.height
        profile.data["transform"] = win_transform
        profile.data["dtype"] = "uint8"

    # image monobande
    img = np.mean(img[0:3], axis=0)
    end_time_inter_mask_open = time.process_time() - start

    time_inter_mask_open.set(
        time_inter_mask_open.value + end_time_inter_mask_open)

    # Detect segments with FLD
    FLD = fld_segment_detect(crs, img, profile, rpg, time_fld)

    orientations, centroids, list_code_group, list_code_cultu, nb_lines_used, nb_orientations, \
        mean_len_lines, std_orientation_x, std_orientation_y, mean_slope_list, mean_aspect_list, \
        calc_aspect, indic_orient, list_ID_PARCEL, kept_lines, ID_PARCEL_kept_lines, rpg_refined, \
        intersections, bbox = ([] for _ in range(19))

    # Compute orientations from the detected segments
    if not FLD.empty:
        for ind in list(rpg.index):
            r = compute_orientation(
                ind,
                rpg,
                FLD,
                slope,
                aspect,
                window_bb,
                area_min,
                parcel_ids_processed,
                min_nline,
                min_len_line,
                time_slope_aspect,
                time_calculate_orientation,
                verbose
            )

            if r is not None:
                orientations += r[0]
                centroids += r[1]
                list_code_group += [r[2]] * len(r[0])
                list_code_cultu += [r[3]] * len(r[0])
                nb_lines_used += r[4]
                nb_orientations += [r[5]] * len(r[0])
                mean_len_lines += r[6]
                std_orientation_x += r[7]
                std_orientation_y += r[8]
                mean_slope_list += [r[9]] * len(r[0])
                mean_aspect_list += [r[10]] * len(r[0])
                calc_aspect += [r[11]] * len(r[0])
                indic_orient += [r[12]] * len(r[0])
                list_ID_PARCEL += [r[13]] * len(r[0])
                kept_lines += r[14]
                ID_PARCEL_kept_lines += [r[13]] * len(r[14])
                rpg_refined += r[15]
                intersections += r[16]
                bbox += r[17]

    # Export and save the centroids and linestring orientations
    centroids, orientations = save_centroids_orientations(calc_aspect, centroids, indic_orient, list_ID_PARCEL,
                                                          list_code_cultu, list_code_group, mean_aspect_list,
                                                          mean_len_lines, mean_slope_list, nb_lines_used,
                                                          nb_orientations, orientations, rpg, std_orientation_x,
                                                          std_orientation_y)

    # Export and save the segments kept to compute the orientations
    return export_save_fld(ID_PARCEL_kept_lines, bbox, centroids, intersections, kept_lines, orientations, rpg,
                           rpg_refined, save_fld, start, time_orientation_worker)



def get_on_patch_border_lines(
        inputs,
        min_len_line,
        normalize,
        area_min,
        time_fld,
        time_inter_mask_open,
        verbose
):
    """
        Detect the segment in the parcels located on the borders of the image patches

        Parameters
        ----------
        inputs: tuple containing the image path, the rpg parcels within the window and the rasterio.windows.Window to use to read the input image
        min_len_line : minimum length (meters) for a valid segment
        normalize: boolean indicating weither or not to normalize the input image
        area_min: a parameter used to calculate the minimum number of lines needed to compute the orientation of a parcel in relation to its area
        time_fld: shared variable to track process time to detect segments with FLD algorithm
        time_inter_mask_open: shared variable to track process time to open, intersect with RPG and mask the image
        verbose: boolean indicating whether or not to print all messages

        Returns
        -------
            gpd.GeoDataFrame
                a gpd.GeoDataFrame containing segments located on the borders of the image patch

    """
    img_path, rpg, window = inputs

    start = time.process_time()

    rpg_expanded = rpg.buffer(1)
    with rasterio.open(img_path) as dataset:
        _logger.info(f"[PATCH] -> IMG : {os.path.basename(img_path)} | WINDOW : {window}")
        profile = dataset.profile

        # Get new window
        src_transform = dataset.transform
        win_transform = rasterio.windows.transform(window, src_transform)
        window_bb = box(*rasterio.windows.bounds(window, src_transform))

        rpg_expanded = rpg.buffer(1).intersection(window_bb)

        profile = dataset.profile
        mask_dataset = dataset.read_masks(1, window=window)
        crs = dataset.crs

        img = dataset.read(window=window)

    if normalize:
        img = normalize_img(img, mask_dataset)

    # Mask with RPG and dataset mask
    mask_rpg = rasterio.features.rasterize(list(rpg_expanded),
                                           out_shape=img.shape[1:],
                                           transform=win_transform,
                                           fill=0,
                                           all_touched=True,
                                           dtype=rasterio.uint8)
    img = np.uint8(img)
    img = np.where(mask_dataset * mask_rpg, img, 0)

    if window is not None:
        profile.data["width"] = window.width
        profile.data["height"] = window.height
        profile.data["transform"] = win_transform
        profile.data["dtype"] = "uint8"

    # image monobande
    img = np.mean(img[0:3], axis=0)

    time_inter_mask_open.set(
        time_inter_mask_open.value + time.process_time() - start)

    FLD = fld_segment_detect(crs, img, profile, rpg, time_fld, patch_border = True)

    gdf = []
    for ind in list(rpg.index):

        pol = rpg.at[ind, "geometry"]
        ID_PARCEL = rpg.at[ind, "ID_PARCEL"]

        # Erode the polygon edges to filter out the segments on the border
        erosion = - 5 * np.max([1, np.log((pol.area / area_min) ** 2)])
        within = FLD.within(pol.buffer(erosion))
        inter = FLD.loc[within]

        # The orientation calculation is applied only if the number of detected lines is over the threshold
        if inter.shape[0] < 1:
            _logger.info(f"[{ID_PARCEL}] Skipping parcel: no segment to compute the parcel orientation")
            continue

        vectx, vecty, len_lines, kept_lines = filter_segments(
            inter, min_len_line)

        df = pd.DataFrame({'geometry': kept_lines})
        kept_lines = gpd.GeoDataFrame(df, columns=['geometry'])
        kept_lines['ID_PARCEL'] = [ID_PARCEL] * len(kept_lines)
        kept_lines["vectx"] = vectx
        kept_lines["vecty"] = vecty
        kept_lines["len_lines"] = len_lines
        kept_lines.crs = rpg.crs

        gdf.append(kept_lines)

    if gdf:
        gdf = gpd.GeoDataFrame(pd.concat(gdf), crs=crs)
        gdf.crs = rpg.crs

        return gdf

    return gpd.GeoDataFrame(gdf)


def get_on_patch_border_orientation(
        inputs,
        min_nb_line_per_parcelle,
        area_min,
        slope,
        aspect,
        time_slope_aspect,
        time_calculate_orientation,
        verbose
):
    """
        Compute the orientation of the parcels located on the borders of the image patches

        Parameters
        ----------
        inputs: tuple containing the kept lines inside the parcel and the rpg parcels
        min_nb_line_per_parcelle: the minimum number of lines needed to compute the orientation of a parcel
        area_min: a parameter used to calculate the minimum number of lines needed to compute the orientation of a parcel in relation to its area
        slope: the path to the raster containing the slope values
        aspect: the path to the raster containing the aspect values
        time_slope_aspect: shared variable to track process time to compute slope and aspect
        time_calculate_orientation: shared variable to track process time to calculate each orientation
        verbose: boolean indicating whether or not to print all messages

        Returns
        -------
            List
                a list containing the orientations and many more statistical information about the parcel.

    """
    delta_calculate_orientation = time.process_time()

    kept_lines, rpg = inputs

    pol = rpg.geometry.iloc[0]
    centroid = [pol.centroid]
    ID_PARCEL = rpg["ID_PARCEL"].iloc[0]
    code_cultu = rpg["CODE_CULTU"].iloc[0]
    code_group = rpg["CODE_GROUP"].iloc[0]

    vectx = kept_lines["vectx"].to_list()
    vecty = kept_lines["vecty"].to_list()
    len_lines = kept_lines["len_lines"].to_list()
    kept_lines = kept_lines.geometry.to_list()

    if len(vectx) <= (min_nb_line_per_parcelle * np.max([1, pol.area / area_min])):
        _logger.info(f"[{ID_PARCEL}] Skipping parcel: not enough segments kept to compute the parcel orientation")
        return

    value_mean_slope, value_mean_aspect = get_mean_slope_aspect(
        pol, slope, aspect, time_slope_aspect)

    if value_mean_aspect is None or value_mean_slope is None:
        _logger.info(
            f"[{ID_PARCEL}] Skipping parcel: mean slope value={value_mean_slope}, mean aspect value={value_mean_aspect}")
        return

    # Compute orientation
    orientation, value_calc_aspect, indic_orient = orientation_from_lines(
        vectx,
        vecty,
        pol,
        value_mean_aspect
    )

    # computes statistics for quality criteria
    mean_len_lines = [statistics.mean(len_lines)]
    nb_lines_used = [len(vectx)]
    std_orient_x = [statistics.stdev(vectx)]
    std_orient_y = [statistics.stdev(vecty)]

    nb_orientations, orient_dict = detect_multiple_orientations(
        kept_lines, vectx, vecty, len_lines, orientation, min_nb_line_per_parcelle, ID_PARCEL)

    if orient_dict is not None:
        pseudo_patches, intersection_shapes = get_pseudo_patches(orient_dict["min_bounding_box"], pol,
                                                                 orient_dict["id_parcel"])
        orientation = orient_dict["orientations"]
        centroid = orient_dict["centroids"]
        mean_len_lines = orient_dict["mean_len_lines"]
        nb_lines_used = orient_dict["nb_lines_used"]
        std_orient_x = orient_dict["std_orient_x"]
        std_orient_y = orient_dict["std_orient_y"]
        bb = orient_dict["min_bounding_box"]
    else:
        orientation = [orientation]
        intersection_shapes = []
        bb = []
        pseudo_patches = [pol]

    delta_calculate_orientation = time.process_time() - delta_calculate_orientation
    time_calculate_orientation.set(
        time_calculate_orientation.value + delta_calculate_orientation)
    return orientation, centroid, code_group, code_cultu, nb_lines_used, nb_orientations, mean_len_lines, std_orient_x, std_orient_y, value_mean_slope, value_mean_aspect, value_calc_aspect, indic_orient, ID_PARCEL, kept_lines, pseudo_patches, intersection_shapes, bb


def handle_on_patch_border_crops(
        rpg,
        list_on_border,
        area_min,
        slope,
        aspect,
        save_fld,
        normalize,
        time_orientation_worker,
        time_calculate_orientation,
        time_fld,
        time_inter_mask_open,
        time_slope_aspect,
        nb_cores,
        verbose
):
    """
    Method that handles the crops that are on patch border.

    Parameters
    ----------
        rpg: a tuple containing the input image path, the rpg parcels, and an optionnal rasterio.Window with which to read the image
        list_on_border: the list of Tuples containing image path, RPG within the window and on the image border, and the Window
        slope: the path to the raster containing the slope values
        aspect: the path to the raster containing the aspect values
        save_fld: bool indicating whether or not the segments used to compute the orientations have to be saved in file
        area_min: a parameter used to calculate the minimum number of lines needed to compute the orientation of a parcel in relation to its area
        normalize: boolean indicating whether or not the image has to be normalized
        time_inter_mask_open: shared variable to track process time to open, intersect with RPG and mask the image
        time_slope_aspect: shared variable to track process time to compute slope and aspect
        time_fld: shared variable to track process time to detect segments with FLD algorithm
        time_orientation_worker: shared variable to track process time to compute the orientations
        time_calculate_orientation: shared variable to track process time to calculate each orientation
        verbose: boolean indicating whether or not to print all messages

    Returns
    -------
        List
            a list containing orientation, centroids, kept_lines, rpg_refined, intersections, bbox
    """

    start = time.process_time()

    with concurrent.futures.ProcessPoolExecutor(max_workers=nb_cores) as executor:
        kept_lines = list(executor.map(
            partial(get_on_patch_border_lines,
                    min_len_line=args.min_len_line,
                    normalize=normalize,
                    area_min=area_min,
                    time_fld=time_fld,
                    time_inter_mask_open=time_inter_mask_open,
                    verbose=verbose),
            list_on_border,
            chunksize=max([1, len(list_on_border) // nb_cores])
        ))
        kept_lines = gpd.geodataframe.GeoDataFrame(pd.concat(kept_lines))

        if not kept_lines.empty:
            kept_lines.crs = rpg.crs
            # gather the filtered segments with the same ID_PARCEL using pd.unique
            kept_lines = [(kept_lines.loc[kept_lines["ID_PARCEL"] == id_parcel], rpg.loc[rpg["ID_PARCEL"] == id_parcel])
                          for id_parcel in pd.unique(kept_lines["ID_PARCEL"])]

            res = list(executor.map(
                partial(get_on_patch_border_orientation,
                        min_nb_line_per_parcelle=args.min_nb_line_per_parcel,
                        area_min=area_min,
                        slope=slope,
                        aspect=aspect,
                        time_slope_aspect=time_slope_aspect,
                        time_calculate_orientation=time_calculate_orientation,
                        verbose=verbose),
                kept_lines,
                chunksize=max([1, len(kept_lines) // nb_cores])
            ))

            orientations, centroids, list_code_group, list_code_cultu, nb_lines_used, nb_orientations, \
                mean_len_lines, std_orientation_x, std_orientation_y, mean_slope_list, mean_aspect_list, \
                calc_aspect, indic_orient, list_ID_PARCEL, kept_lines, ID_PARCEL_kept_lines, rpg_refined, \
                intersections, bbox = ([] for _ in range(19))

            for r in res:
                if r is not None:
                    orientations += r[0]
                    centroids += r[1]
                    list_code_group += [r[2]] * len(r[0])
                    list_code_cultu += [r[3]] * len(r[0])
                    nb_lines_used += r[4]
                    nb_orientations += [r[5]] * len(r[0])
                    mean_len_lines += r[6]
                    std_orientation_x += r[7]
                    std_orientation_y += r[8]
                    mean_slope_list += [r[9]] * len(r[0])
                    mean_aspect_list += [r[10]] * len(r[0])
                    calc_aspect += [r[11]] * len(r[0])
                    indic_orient += [r[12]] * len(r[0])
                    list_ID_PARCEL += [r[13]] * len(r[0])
                    kept_lines += r[14]
                    ID_PARCEL_kept_lines += [r[13]] * len(r[14])
                    rpg_refined += r[15]
                    intersections += r[16]
                    bbox += r[17]

                # Export and save the centroids and linestring orientations
                conc_centroids, orientations = save_centroids_orientations(calc_aspect, centroids, indic_orient,
                                                                      list_ID_PARCEL,
                                                                      list_code_cultu, list_code_group,
                                                                      mean_aspect_list,
                                                                      mean_len_lines, mean_slope_list, nb_lines_used,
                                                                      nb_orientations, orientations, rpg,
                                                                      std_orientation_x,
                                                                      std_orientation_y)

            if save_fld:
                df = pd.DataFrame({'geometry': kept_lines})
                kept_lines = gpd.GeoDataFrame(df, columns=['geometry'])
                kept_lines['ID_PARCEL'] = ID_PARCEL_kept_lines
                kept_lines.crs = rpg.crs

                end_orientation = time.process_time() - start
                time_orientation_worker.set(
                    time_orientation_worker.value + end_orientation)
                _logger.info(f"Done ({len(orientations)} orientation(s) found)")

                rpg_refined = gpd.GeoDataFrame({'geometry': rpg_refined}, crs='EPSG:2154')
                intersections = gpd.GeoDataFrame({'geometry': intersections}, crs='EPSG:2154')
                bbox = gpd.GeoDataFrame({'geometry': bbox}, crs='EPSG:2154')
            else:
                kept_lines = None
                end_orientation = time.process_time() - start
                time_orientation_worker.set(
                    time_orientation_worker.value + end_orientation)
                _logger.info(f"Done ({len(orientations)} orientation(s) found)")

        else:
            _logger.info("No line detected on the image's borders.")
            return gpd.GeoDataFrame([]), gpd.GeoDataFrame([]), gpd.GeoDataFrame([]), gpd.GeoDataFrame(
                []), gpd.GeoDataFrame([]), gpd.GeoDataFrame([])

    return orientations, conc_centroids, kept_lines, rpg_refined, intersections, bbox


def get_rpg_patches(
        img_dataset,
        RPG,
        time_split,
        nb_cores,
        patch_size=None,
        mode=""
):
    """
        Construct the lists used for parallelization with multiprocessing.
        If the input image dataset is one image path:
            We construct a list of Tuples containing the image path, RPG within Window, and Window
            by doing the parallelization on the list of windows

        Parameters
        ----------
        img_dataset: list or str containing the image(s) path

        RPG: the input RPG
        time_split: variable shared between processes to track process time
        windows: the list of rasterio.windows.Window
        mode: str to choose to construct the list for the image(s) borders or not

        Returns
        -------
        list_rpg_patches: the list of Tuples containing image path, RPG within the window and fully within the image extent, and the Window
        list_on_border: the list of Tuples containing image path, RPG within the window and on the image border, and the Window



    """

    _logger.info("Splitting the RPG into patches...")

    with Manager() as manager:
        list_rpg_patches = manager.list()
        list_on_border = manager.list()
        with concurrent.futures.ProcessPoolExecutor(max_workers=nb_cores) as executor:
            if isinstance(img_dataset, list):
                if mode == "border":
                    res = list(executor.map(partial(split_img_borders,
                                                    RPG=RPG,
                                                    patch_size=patch_size,
                                                    list_on_border=list_on_border,
                                                    time_split=time_split),
                                            img_dataset,
                                            chunksize=max(
                                                [1, len(img_dataset) // nb_cores])
                                            ))
                    _logger.info("done: {:.3} seconds".format(time_split.value))
                    return list(list_on_border)
                else:
                    res = list(executor.map(partial(split_img_dataset,
                                                    RPG=RPG,
                                                    patch_size=patch_size,
                                                    list_rpg_patches=list_rpg_patches,
                                                    time_split=time_split),
                                            img_dataset,
                                            chunksize=max(
                                                [1, len(img_dataset) // nb_cores])
                                            ))
                    _logger.info("done: {:.3} seconds".format(time_split.value))
                    return list(list_rpg_patches)
            else:
                if mode != "border":
                    if patch_size:
                        with rasterio.open(img_dataset) as dataset:
                            num_rows, num_cols = dataset.shape

                        windows = [
                            rasterio.windows.Window(j, i, min(num_cols - j, patch_size), min(num_rows - i, patch_size))
                            for i in range(0, num_rows, patch_size) for j in range(0, num_cols, patch_size)]

                        res = list(executor.map(partial(split_windows,
                                                        img_path=img_dataset,
                                                        RPG=RPG,
                                                        list_rpg_patches=list_rpg_patches,
                                                        time_split=time_split),
                                                windows,
                                                chunksize=max([1, len(windows) // nb_cores])
                                                ))
                    else:
                        split_windows(window=None,
                                      img_path=img_dataset,
                                      RPG=RPG,
                                      list_rpg_patches=list_rpg_patches,
                                      time_split=time_split
                                      )

                _logger.info("done: {:.3} seconds".format(time_split.value))
                return list(list_rpg_patches)



def save_stats_csv(RPG, output_dir, data, data_norm, header, orientations):
    codes = []
    group_ = []
    rpg = []
    orients = []
    multiple = []
    for code in set(orientations.CODE_CULTU):
        codes.append(code)
        filtre = orientations.query("CODE_CULTU == @code")
        group_ += list(np.unique(filtre.CODE_GROUP))
        orients.append(len(set(filtre.ID_PARCEL)))
        rpg.append(len(RPG.query("CODE_CULTU == @code")))
        multiple.append(sum(filtre.ID_PARCEL.value_counts() > 1))
    dict = {'CULTURE': codes, 'GROUP': group_, 'len RPG': rpg, 'parcelles orientees': orients,
            'parcelles multiples': multiple}
    df = pd.DataFrame(dict)
    total = df.sum().apply(set_str_to_all)
    # df = df.append(total, ignore_index=True)
    df = pd.concat([df, pd.DataFrame([total])], ignore_index=True)
    df['% parcelles orientées'] = round(df['parcelles orientees'] / df['len RPG'] * 100, 2).astype(str) + ' %'
    df['% parcelles multiples'] = round(df['parcelles multiples'] / df['parcelles orientees'] * 100, 2).astype(
        str) + ' %'
    out_stats = os.path.join(output_dir, "statistics.csv")
    df.to_csv(out_stats, index=False)
    format_line = "{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {}"
    _logger.info("================================= PROCESSING TIME ==================================")
    _logger.info(format_line.format("", *header[:-4]))
    _logger.info(format_line.format("All processes", *data[:-4]))
    _logger.info(format_line.format("Per process", *data_norm))


def save_fld_process(crs, on_border_bbox, on_border_lines, on_border_rpg_patches, orientations, out_hulls, out_patches,
             out_segments):
    kept_lines = gpd.read_file(out_segments)
    kept_lines = kept_lines.set_crs('epsg:2154')
    _logger.info(f"Saving {len(kept_lines)} segments to {out_segments}")
    kept_lines = gpd.geodataframe.GeoDataFrame(
        pd.concat([kept_lines, on_border_lines]), crs=crs)
    kept_lines.to_crs(crs, inplace=True)
    kept_lines.to_file(out_segments)

    rpg_patches = gpd.read_file(out_patches)
    rpg_patches = rpg_patches.set_crs('epsg:2154')
    _logger.info(f"Saving {len(rpg_patches)} rpg patches to {out_patches}")
    rpg_patches = gpd.geodataframe.GeoDataFrame(
        pd.concat([rpg_patches, on_border_rpg_patches]), crs=crs)
    rpg_patches.to_crs(crs, inplace=True)
    rpg_patches.to_file(out_patches)

    bbox = gpd.read_file(out_hulls)
    bbox = bbox.set_crs('epsg:2154')
    _logger.info(f"Saving {len(orientations)} convex hulls to {out_hulls}")
    bbox = gpd.geodataframe.GeoDataFrame(
        pd.concat([bbox, on_border_bbox]), crs=crs)
    bbox.to_crs(crs, inplace=True)
    bbox.to_file(out_hulls)

    del kept_lines, rpg_patches, bbox

def orientation_compute_save_fld(output_dir, crs, list_gdf):
    kept_lines = gpd.geodataframe.GeoDataFrame(
        pd.concat([r[2] for r in list_gdf]), crs=crs)
    kept_lines.crs = crs
    out_segments = os.path.join(output_dir, "kept_lines.shp")
    kept_lines.to_file(out_segments)

    rpg_patches = gpd.geodataframe.GeoDataFrame(
        pd.concat([r[3] for r in list_gdf]), crs=crs)
    rpg_patches.crs = crs
    out_patches = os.path.join(output_dir, "rpg_patches.shp")
    rpg_patches.to_file(out_patches)

    bbox = gpd.geodataframe.GeoDataFrame(
        pd.concat([r[5] for r in list_gdf]), crs=crs)
    bbox.crs = crs
    out_hulls = os.path.join(output_dir, "convex_hulls.shp")
    bbox.to_file(out_hulls)

    del kept_lines, bbox
    return out_hulls, out_patches, out_segments


def border_patch_process(nb_cores, patch_size, RPG, img_dataset, time_split):
    list_on_border = get_rpg_patches(
        img_dataset,
        RPG,
        time_split,
        nb_cores,
        patch_size=patch_size,
        mode="border"
    )
    on_border_orient = gpd.geodataframe.GeoDataFrame([])
    on_border_centroids = gpd.geodataframe.GeoDataFrame([])
    on_border_lines = gpd.geodataframe.GeoDataFrame([])
    on_border_rpg_patches = gpd.geodataframe.GeoDataFrame([])
    on_border_bbox = gpd.geodataframe.GeoDataFrame([])
    return list_on_border, on_border_bbox, on_border_centroids, on_border_lines, on_border_orient, on_border_rpg_patches


def save_centroids(crs, on_border_centroids, on_border_orient, out_centroids, out_orient):
    start_concat = time.process_time()
    orientations = gpd.read_file(out_orient)
    orientations = orientations.set_crs('epsg:2154')
    _logger.info(f"Saving {len(orientations)} orientations to {out_orient}")
    orientations = gpd.geodataframe.GeoDataFrame(
        pd.concat([orientations, on_border_orient]), crs=crs)
    orientations.crs = crs
    orientations.to_crs(crs, inplace=True)
    orientations.to_file(out_orient)
    len_orientation = len(orientations)
    centroids = gpd.read_file(out_centroids)
    centroids = centroids.set_crs('epsg:2154')
    _logger.info(f"Saving {len(centroids)} centroids to {out_centroids}")
    centroids = gpd.geodataframe.GeoDataFrame(
        pd.concat([centroids, on_border_centroids]), crs=crs)
    centroids.to_crs(crs, inplace=True)
    return len_orientation, orientations


def orientation_compute_process(crs, list_gdf, output_dir):
    start_concat = time.process_time()
    orientations = gpd.geodataframe.GeoDataFrame(
        pd.concat([r[0] for r in list_gdf]), crs=crs)
    orientations.crs = crs
    orientations.to_crs(crs, inplace=True)
    out_orient = os.path.join(output_dir, "orientations.shp")
    orientations.to_file(out_orient)
    del orientations
    centroids = gpd.geodataframe.GeoDataFrame(
        pd.concat([r[1] for r in list_gdf]), crs=crs)
    centroids.crs = crs
    out_centroids = os.path.join(output_dir, "centroids.shp")
    centroids.to_file(out_centroids)
    del centroids
    return out_centroids, out_orient

def reading_input(img : str, rpg : str, nb_cores : int, patch_size : int):
    start_main = time.process_time()
    start = datetime.now()
    # Open rpg shapefile
    _logger.info("Reading RPG shapefile...")
    RPG = gpd.read_file(rpg)
    _logger.info("done in {:.3} seconds".format(time.process_time() - start_main))
    crs_rpg = RPG.crs
    _logger.info(f"CRS RPG : {crs_rpg}")
    crs = {"init": "epsg:2154"}
    img_dataset = sorted(glob.glob(img + "/*." + type)
                         ) if os.path.isdir(img) else img
    _logger.info(f"Image dataset size : {len(img_dataset)}")
    manager = Manager()
    time_split = manager.Value("time_split", 0.)
    time_slope_aspect = manager.Value("time_slope_aspect", 0.)
    time_fld = manager.Value("time_fld", 0.)
    time_orientation_worker = manager.Value("time_orientation_worker", 0.)
    time_calculate_orientation = manager.Value(
        "time_calculate_orientation", 0.)
    time_inter_mask_open = manager.Value("time_inter_mask_open", 0.)
    parcel_ids_processed = manager.list()
    increment = manager.Value('increment', 0)
    len_RPG = len(RPG)
    # Split RPG into patches
    list_rpg_patches = get_rpg_patches(
        img_dataset,
        RPG,
        time_split,
        nb_cores,
        patch_size=patch_size
    )
    return RPG, crs, img_dataset, increment, len_RPG, list_rpg_patches, parcel_ids_processed, start, start_main, time_calculate_orientation, time_fld, time_inter_mask_open, time_orientation_worker, time_slope_aspect, time_split


def getarguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Detection of crop orientation on BDORTHO and PHR images')
    parser.add_argument('-img', '--img', metavar='[IMAGE]', help='Image path or directory containing the images',
                        required=True)
    parser.add_argument('-rpg', '--rpg', metavar='[RPG]', help='Input RPG shapefile', required=True)
    parser.add_argument('-o', '--output_dir', default=None, help='Output directory where to store results')
    parser.add_argument('-slope', '--slope', help="Path to the slope file", required=True)
    parser.add_argument('-aspect', '--aspect', help="Path to the aspect file", required=True)
    parser.add_argument('-nb_cores', '--nb_cores', type=int, default=5)
    parser.add_argument('-type', '--type', metavar='[TYPE]', help='file extension of the images (tif or jp2)',
                        default="tif")
    parser.add_argument('-normalize', '--normalize', help="Normalize the image before line detection",
                        action="store_true")
    parser.add_argument('-save_fld', '--save_fld', help="save additional files", action="store_true")
    parser.add_argument('-verbose', '--verbose', help="print messages along process", action="store_true")
    parser.add_argument('-patch_size', '--patch_size', help="Size of image patches", type=int, default=10000)
    parser.add_argument('-area_min', '--area_min', help="Minimum area of plot to handle. Leave to default.", type=float,
                        default=20000.)
    parser.add_argument('-min_nline', '--min_nb_line_per_parcel',
                        help="minimum valid number of segments inside a parcel", type=int, default=10)
    parser.add_argument('-min_len_line', '--min_len_line', help="minimum length (meters) for a valid segment", type=int,
                        default=6)

    parser.print_help()
    args = parser.parse_args()
    return vars(args)


def detection_orientation_culture(img: str, rpg: str, output_dir: str, slope: str, aspect: str, nb_cores: int,
                                  type: str, normalize: bool, save_fld: bool, verbose: bool, patch_size: int,
                                  area_min: float, min_nb_line_per_parcel: int, min_len_line: int):
    # logging config
    logformat = "[%(asctime)s] %(levelname)s - %(name)s - %(message)s"
    logging.basicConfig(
        level=logging.INFO if verbose else logging.WARNING,  # Only show INFO if verbose=True
        stream=sys.stdout,
        format=logformat,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logging.getLogger("fiona").setLevel(logging.ERROR)


    _logger.info("==================================== PARAMETERS ====================================")
    for key, value in locals().items():
        _logger.info(f"{key}: {value}")
    _logger.info("================================== READING INPUTS ==================================")

    RPG, crs, img_dataset, increment, len_RPG, list_rpg_patches, parcel_ids_processed, start, start_main, time_calculate_orientation, time_fld, time_inter_mask_open, time_orientation_worker, time_slope_aspect, time_split = reading_input(
        img, rpg, nb_cores, patch_size)

    _logger.info(f"Patches list size : {len(list_rpg_patches)}")

    _logger.info("============================== ORIENTATION CALCULATION =============================")

    with concurrent.futures.ProcessPoolExecutor(max_workers=nb_cores) as executor:
        list_gdf = list(executor.map(
            partial(orientation_worker,
                    normalize=normalize,
                    parcel_ids_processed=parcel_ids_processed,
                    slope=slope,
                    aspect=aspect,
                    area_min=area_min,
                    increment=increment,
                    min_nline=min_nb_line_per_parcel,
                    min_len_line=min_len_line,
                    time_inter_mask_open=time_inter_mask_open,
                    time_slope_aspect=time_slope_aspect,
                    time_fld=time_fld,
                    time_orientation_worker=time_orientation_worker,
                    time_calculate_orientation=time_calculate_orientation,
                    save_fld=save_fld,
                    verbose=verbose),
            list_rpg_patches,
            chunksize=max([1, len(img_dataset) // nb_cores])
        ))
    del list_rpg_patches

    out_centroids, out_orient = orientation_compute_process(crs, list_gdf, output_dir)

    _logger.info("========================== HANDLING ON BORDER PATCH PLOTS ==========================")

    list_on_border, on_border_bbox, on_border_centroids, on_border_lines, on_border_orient, on_border_rpg_patches = border_patch_process(nb_cores, patch_size, RPG, img_dataset, time_split)

    if list_on_border:
        on_border_orient, on_border_centroids, on_border_lines, on_border_rpg_patches, on_border_intersections, on_border_bbox = handle_on_patch_border_crops(
            RPG,
            list_on_border,
            area_min,
            slope,
            aspect,
            save_fld,
            normalize,
            time_orientation_worker,
            time_calculate_orientation,
            time_fld,
            time_inter_mask_open,
            time_slope_aspect,
            nb_cores,
            verbose
        )

    del list_on_border

    _logger.info("================================== SAVING RESULTS ==================================")

    len_orientation, orientations = save_centroids(crs, on_border_centroids, on_border_orient, out_centroids,
                                                   out_orient)

    if save_fld:
        out_hulls, out_patches, out_segments = orientation_compute_save_fld(output_dir, crs, list_gdf)
        save_fld_process(crs, on_border_bbox, on_border_lines, on_border_rpg_patches, orientations, out_hulls, out_patches, out_segments)

    del list_gdf

    time_main = time.process_time() - start_main

    data = list(map(sec_to_hms,
                    [time_main + time_orientation_worker.value,
                     time_main,
                     time_orientation_worker.value,
                     time_slope_aspect.value,
                     time_fld.value,
                     time_inter_mask_open.value,
                     time_calculate_orientation.value]
                    )
                )
    data_norm = list(map(sec_to_hms,
                         [time_main + time_orientation_worker.value / nb_cores,
                          time_main,
                          time_orientation_worker.value / nb_cores,
                          time_slope_aspect.value / nb_cores,
                          time_fld.value / nb_cores,
                          time_inter_mask_open.value / nb_cores]
                         )
                     )
    data += [len_orientation, len_RPG,
             f"{int(100 * len_orientation / len_RPG)}%"]
    header = ["all", "main", "worker", "slope_aspect", "fld", "img_processing",
              "calculate_orientation", "num_orientations", "RPG_length", "ratio"]

    # Save time logs to csv
    out_csv = os.path.join(output_dir, "computation_time.csv")
    with open(out_csv, "w", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(header)
        csv_writer.writerow(data)

    # Save statistics to csv
    save_stats_csv(RPG, output_dir, data, data_norm, header, orientations)

    end = datetime.now() - start
    _logger.info(f'OVERALL TIME = {end}')


def main():
    """
    Main function to run the orientation detection computation.
    It parses the command line arguments and calls the detection_orientation_culture function.
    """
    args = getarguments()
    detection_orientation_culture(**args)

if __name__ == "__main__":
    sys.exit(main())