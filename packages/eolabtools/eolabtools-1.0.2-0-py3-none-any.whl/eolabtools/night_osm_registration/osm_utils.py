"""OSM utilities: download, process and convert to binary raster"""

import getpass
import os
import ssl
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import pyrosm
import rasterio
from rasterio import features
from shapely import geometry


def get_osm_data(
    osm_dataset: str, raster_src: dict, download_dir: Path, proxy: str = ""
):
    """Download OSM data"""
    # Config Proxy if needed
    if proxy:
        u = getpass.getuser()
        p = getpass.getpass("Password: ")

        os.environ["HTTP_PROXY"] = f"http://{u}:{p}@{proxy}"
        os.environ["HTTPS_PROXY"] = f"http://{u}:{p}@{proxy}"
        ssl._create_default_https_context = ssl._create_unverified_context

    # Reproject raster bbox in WGS84
    bbox = geometry.box(*raster_src.bounds)
    bbox_gdf = gpd.GeoDataFrame({"geometry": [bbox]}, crs=raster_src.crs).to_crs(4326)
    bbox = bbox_gdf.geometry[0]

    if osm_dataset in pyrosm.data.sources.cities.available:
        fp = pyrosm.get_data(osm_dataset, directory=download_dir)
    elif Path(osm_dataset).exists():
        fp = osm_dataset
    else:
        raise ValueError(
            "Config 'osm_dataset' must point to an existing pbf file "
            "or an available city name in 'pyrosm.data.sources.cities.available'"
        )

    # Initialize the OSM parser object
    osm = pyrosm.OSM(fp, bounding_box=bbox)

    return osm, bbox


def rasterize_osm(
    gdf_positive: gpd.GeoDataFrame,
    raster_src: rasterio.io.DatasetReader,
    roi_list: gpd.GeoSeries,
    gdf_negative: gpd.GeoDataFrame = gpd.GeoDataFrame(),
):
    """Rasterize OSM vectors"""

    if gdf_positive.empty and gdf_negative.empty:
        raise ValueError(
            "Both positive and negative GeoDataframes are empty! Check OSM download step. "
        )

    options = {
        "out_shape": raster_src.shape,
        "transform": raster_src.transform,
        "all_touched": False,
        "dtype": "uint8",
    }
    # Default value is 1
    raster_osm = features.rasterize(gdf_positive.geometry, **options, fill=0)

    if not gdf_negative.empty:
        negative_raster_osm = features.rasterize(
            gdf_negative.geometry, **options, default_value=0, fill=1
        )
        raster_osm = np.logical_or(raster_osm, negative_raster_osm, out=raster_osm)

    if not roi_list.empty:
        raster_roi = features.rasterize(roi_list, **options, fill=0)
        raster_osm = np.multiply(raster_osm, raster_roi, out=raster_osm)

    return raster_osm


def get_osm_raster(
    osm_tags: dict,
    osm_dataset: str,
    raster_src: rasterio.io.DatasetReader,
    roi_list: gpd.GeoSeries,
    download_dir: Path,
    water_file: str = "",
    road_buffer_size: float = 0.0,
    proxy: str = "",
) -> np.ndarray:
    """
    Create binary raster from osm vectors
    """
    # Load OSM data
    osm, bbox = get_osm_data(osm_dataset, raster_src, download_dir, proxy)
    print("BBox:", bbox)
    print("OSM area bounds:", osm.bounding_box)

    # Rasterize OSM data depending on the chosen vectors
    # Positives vectors
    gdf_positive = osm.get_data_by_custom_criteria(
        osm_tags["positive"], keep_nodes=False
    )

    # Get geometries in raster crs
    if raster_src.crs != 4326:
        gdf_positive = gdf_positive.to_crs(raster_src.crs)

    # gdf_positive.to_file(download_dir / "osm_positive.gpkg")

    if road_buffer_size:
        if raster_src.crs == 4326 and road_buffer_size >= 1:
            print(
                f"Invalid buffer size ({road_buffer_size}) for this image CRS (EPSG:4326)"
            )
        else:
            # Buffered road vector with buffer size value
            is_highway = ~gdf_positive.highway.isna()
            geom_buffer = gdf_positive[is_highway].geometry.buffer(road_buffer_size)
            gdf_positive = pd.concat(
                (
                    gdf_positive[~is_highway],
                    gdf_positive[is_highway].set_geometry(geom_buffer),
                )
            )

    if not osm_tags["negative"]:
        return rasterize_osm(gdf_positive, raster_src, roi_list)

    # Negatives vectors
    gdf_negative = osm.get_data_by_custom_criteria(
        osm_tags["negative"], keep_nodes=False
    )
    # BUG: adding building with get_data_by_custom_criteria doesn't work, use osm.get_buildings instead
    if "building" in osm_tags["negative"]:
        gdf_building = osm.get_buildings()
        gdf_negative = pd.concat((gdf_negative, gdf_building))

    if raster_src.crs != 4326:
        gdf_negative = gdf_negative.to_crs(raster_src.crs)

    # Read water
    if water_file:
        gdf_water = gpd.read_file(water_file, bbox)
    else:
        #Raise pyrosm.py:767: UserWarning: Could not find any OSM data for given area. ERROR
        gdf_water = osm.get_data_by_custom_criteria(custom_filter={"water": ["river"]})
    if raster_src.crs != 4326 and gdf_water is not None :
        gdf_water = gdf_water.to_crs(raster_src.crs)

    gdf_negative = pd.concat((gdf_negative, gdf_water))
    # gdf_negative.to_file(download_dir / "osm_negative.gpkg")

    return rasterize_osm(gdf_positive, raster_src, roi_list, gdf_negative)
