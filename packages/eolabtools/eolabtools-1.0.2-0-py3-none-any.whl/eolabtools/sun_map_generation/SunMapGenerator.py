# This is Python file that creates a sun map over a specified area
import argparse
import concurrent.futures
import sys
import pandas as pd
from functools import partial
import itertools

import pandas as pd
import geopandas as gpd
import ssl
import logging.config
import warnings
import subprocess
from datetime import datetime, timedelta
import ephem
import os
import math
import pytz
import re
import numpy as np
import rasterio
import rasterio.mask
import glob
from osgeo import gdal, ogr, osr
import time as t
from timezonefinder import TimezoneFinder
from multiprocessing import Manager
import csv

warnings.filterwarnings("ignore")
_logger = logging.getLogger(__name__)
ssl._create_default_https_context = ssl._create_unverified_context
logformat = "[%(asctime)s] %(levelname)s - %(name)s - %(message)s"
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S")

def find_timezone(in_file) -> str :
    """
    Find the timezone corresponding to the input image
    """
    # Extract longitude and latitude from input data
    _, latitude, longitude = get_resolution_and_geolocation(in_file)

    # object creation
    obj = TimezoneFinder()
    return obj.timezone_at(lng=longitude, lat=latitude)

def get_list_of_days(start, end, step):

    # transform inputs
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    step = timedelta(days=int(step))

    # Generate the range of dates
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += step

    return dates


def get_list_of_times(start, end, step):

    # transform inputs
    start_time = datetime.strptime(start, "%H:%M")
    end_time = datetime.strptime(end, "%H:%M")
    step = timedelta(minutes=int(step))

    # Generate the range of times
    times = []
    current_time = start_time
    while current_time <= end_time:
        times.append(current_time.strftime('%H:%M'))
        current_time += step

    return times


def merge_dates_and_times(dates_list, times_list):

    return_list = []
    for date in dates_list:
        datetime_list = []
        for time in times_list:
            time_obj = datetime.strptime(time, '%H:%M')
            datetime_obj = datetime(date.year, date.month, date.day, time_obj.hour, time_obj.minute)
            datetime_list.append(datetime_obj)
        return_list.append(datetime_list)
    return return_list


def to_utc_time(in_file, time, area):

    # Define the timezone for area
    tz = pytz.timezone(area)

    # Create a datetime object in the Paris timezone
    dt = tz.localize(time)

    # Convert the datetime to UTC
    utc_dt = dt.astimezone(pytz.utc)

    return utc_dt


def get_azimuth_and_elevation(in_file, datetimes, longitude, latitude, area):

    # Create an object to represent the sun
    sun = ephem.Sun()

    azimuths = []
    elevations = []
    _logger.info(f"Computing azimuth and elevation for day {datetimes[0].strftime('%Y/%m/%d')}")
    for date in datetimes:
        # transform to UTC
        date = to_utc_time(in_file, date, area)

        # Set the date and time for which you want to calculate the azimuth and elevation
        date = ephem.Date(date.strftime('%Y/%m/%d %H:%M:%S'))

        # Create an observer object from the geographical coordinates
        observer = ephem.Observer()
        observer.lat = str(latitude)
        observer.lon = str(longitude)

        # Set the date and time for the observer
        observer.date = date

        # Calculate the azimuth and elevation of the sun
        sun.compute(observer)

        # Get the calculated values in radians
        azimuth_rad = sun.az
        elevation_rad = sun.alt

        # Convert radians to degrees
        azimuth_deg = math.degrees(azimuth_rad)
        elevation_deg = math.degrees(elevation_rad)

        # Store results
        azimuths.append(azimuth_deg)
        elevations.append(elevation_deg)

        _logger.info(f"{date} UTC => Azimuth = {azimuth_deg} - Elevation = {elevation_deg}")

    return azimuths, elevations


def get_resolution_and_geolocation(file):

    # Open the TIFF file
    dataset = gdal.Open(file)

    # Get the geotransform information
    geotransform = dataset.GetGeoTransform()

    # Extract the pixel size in X and Y directions
    pixel_size_x = geotransform[1]
    pixel_size_y = geotransform[5]

    # Get the image dimensions
    width = dataset.RasterXSize
    height = dataset.RasterYSize

    # Calculate the center coordinates
    center_x = geotransform[0] + (width / 2) * pixel_size_x
    center_y = geotransform[3] + (height / 2) * pixel_size_y

    # Convert the center coordinates to latitude and longitude
    srs = osr.SpatialReference()
    srs.ImportFromWkt(dataset.GetProjection())
    srs_latlong = srs.CloneGeogCS()
    ct = osr.CoordinateTransformation(srs, srs_latlong)
    center_lat, center_lon, _ = ct.TransformPoint(center_x, center_y)

    return pixel_size_x, center_lat, center_lon


def compute_radius(inputfile, resolution, elevation):

    wmax = None
    wmin = None
    with rasterio.open(inputfile) as src:
        for ji, window in src.block_windows(1):
            data = src.read(1, masked=True, window=window)
            wmax = max(wmax, float(data.max())) if wmax is not None else float(data.max())
            wmin = min(wmin, float(data.min())) if wmin is not None else float(data.min())

    delta = int((wmax - wmin) / resolution)
    radius = int(delta / np.tan(np.radians(elevation)))

    return radius


def execute_command(dsm_file, elevation, azimuth, resolution, output_dir, wd_size=2048):

    # Define the command to execute
    radius = compute_radius(dsm_file, resolution, elevation)
    if radius > 500:
            radius = 500
    while radius >= (wd_size / 5):
            wd_size *= 2

    _logger.info(f"window size {wd_size} and radius {radius}")

    if radius is None:
        command = f"rio georastertools hs {dsm_file} --elevation {elevation} --azimuth {azimuth} --resolution {resolution} " \
              f"-o {output_dir} -ws {wd_size}"
    else:
        command = f"rio georastertools hs {dsm_file} --elevation {elevation} --azimuth {azimuth} --resolution {resolution} " \
              f"-o {output_dir} -ws {wd_size} --radius {radius}"

    _logger.info(command)

    subprocess.run(command.split(' '))

    """
    # Execute the command
    try:
        subprocess.run(command, shell=True, capture_output=True, text=True, check=True, timeout=1000)

    except subprocess.CalledProcessError as e:
        # Error on radius value. Set window_size to larger value
        print(compute_radius(dsm_file, resolution, elevation))
        radius = get_radius_value(e.stdout)
        print(radius)
        # pas plus de 1000 pixels (500m) prise en compte pour l'ombre
        if radius > 1000:
            radius = 1000
        window_size = wd_size # default
        while radius >= (window_size / 5):
            window_size *= 2
        _logger.info(f"window size {window_size} and radius {radius}")
        # retry command
        # command = f"rio georastertools hs {dsm_file} --elevation {elevation} --azimuth {azimuth} --resolution {resolution} " \
                  # f"-o {output_dir} -ws {window_size}"
        # subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        execute_command(dsm_file, elevation, azimuth, resolution, output_dir, window_size, radius)

    except subprocess.TimeoutExpired:
        _logger.info("TIMEOUT")
        wd_size = wd_size*2
        os.remove(output_dir + dsm_file.split('/')[-1][:-4] + '-' + 'hillshade.tif')
        execute_command(dsm_file, elevation, azimuth, resolution, output_dir, wd_size, radius)
    """


def execute_merge_command(dsm_file, neighbors, output_dir):
    # define command to execute
    merged_file = output_dir + dsm_file.split('/')[-1]
    assert os.path.exists(dsm_file), f"Missing input: {dsm_file}"
    command = ["gdal_merge.py",  "-o" , merged_file, dsm_file] + neighbors
    command = " ".join(command)
    # _logger.info(command)
    try:
        subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("STDOUT:\n", e.stdout)
        print("STDERR:\n", e.stderr)
        raise

    return merged_file


def get_neighbors(tiles, tile_name):

    tile_name = os.path.basename(tile_name)
    gdf = gpd.read_file(tiles)

    # Trouver la dalle cible
    target_tile = gdf[gdf['TILE_NAME'] == tile_name]
    
    if target_tile.empty:
        raise ValueError(f"No tile found with name {tile_name}")
    
    # Calculer le bounding box de la dalle cible
    target_bounds = target_tile.geometry.bounds.values[0]

    # Filtrer les dalles dans le bounding box étendu
    minx, miny, maxx, maxy = target_bounds
    buffered_bounds = gdf.cx[minx-1:maxx+1, miny-1:maxy+1]

    # Filtrer les dalles adjacentes
    neighbors = buffered_bounds[buffered_bounds.touches(target_tile.geometry.squeeze())]

    dir_path = os.path.dirname(tiles)

    return [dir_path + '/' + name for name in neighbors['TILE_NAME'].tolist()]


def generate_sun_map(dsm_file, dsm_tiles, start_date, end_date, step_date, start_time, end_time, step_time, output_dir,
                     area, time_az_el, time_mask_exec):

    # get resolution in meters of dsm file
    _logger.info("----------------------------------------------------------------------------------------------------")
    _logger.info(f"Treating file {dsm_file}")
    neighbors = get_neighbors(dsm_tiles, dsm_file)
    _logger.info(f"There are {len(neighbors)} neighbors, which are {neighbors}")
    resolution, latitude, longitude = get_resolution_and_geolocation(dsm_file)
    _logger.info(f"Resolution of GeoTIFF image is {resolution} meters")
    _logger.info(f"Center of tile coordinates are : Longitude = {longitude} and Latitude = {latitude}")
    
    # get range of dates
    list_of_days = get_list_of_days(start_date, end_date, step_date)

    # get range of times
    list_of_times = get_list_of_times(start_time, end_time, step_time)

    # get full list of datetimes
    list_of_datetimes = merge_dates_and_times(list_of_days, list_of_times)

    # compute azimuth, elevation for each datetime
    start_az_el_time = t.time()
    list_of_azimuths, list_of_elevations = zip(*(get_azimuth_and_elevation(dsm_file, dt, longitude, latitude, area)
                                                 for dt in list_of_datetimes))
    end_az_el_time = t.time() - start_az_el_time
    time_az_el.set(time_az_el.value + end_az_el_time)

    _logger.info("All azimuths and elevations computed.")

    tile_name = os.path.basename(dsm_file)
    gdf = gpd.read_file(dsm_tiles)

    # Trouver la dalle cible
    target_tile = gdf[gdf['TILE_NAME'] == tile_name]

    files_created = []
    for l1, l2, l3 in zip(list_of_datetimes, list_of_azimuths, list_of_elevations):
        daily_files = []
        for d, a, e in zip(l1, l2, l3):

            current_path = output_dir + os.path.splitext(os.path.basename(dsm_file))[0] + '-hillshade.tif'
            # check if it's dark night
            if e < 1.5:
                _logger.info("It's totally dark at that time of the day")
                mask_data, profile = create_dark_image(dsm_file)
            else:
                # execute merge command
                merged_dsm_file = execute_merge_command(dsm_file, neighbors, output_dir)

                # execute hillshade command
                start_exec_command_time = t.time()

                execute_command(merged_dsm_file, e, a, resolution, output_dir, wd_size=2048)

                end_exec_command_time = t.time() - start_exec_command_time
                time_mask_exec.set(time_mask_exec.value + end_exec_command_time)

                os.remove(merged_dsm_file)
                
                # to change data type to uint8
                with rasterio.open(current_path) as src:
                    # Read the image data
                    out_image, out_transform = rasterio.mask.mask(src, target_tile['geometry'], crop=True)
                    mask_data = out_image[0,:,:]
                    #profile = src.profile
                    
                os.remove(current_path)

            # rename file to keep track of datetime
            new_path = current_path[:-4] + '-' + d.strftime("%Y%m%d-%H%M") + '.tif'

            with rasterio.open(dsm_file) as src:
                profile = src.profile
                
            # Save the new image as a TIF file
            profile['dtype']= 'uint8'
            profile['nodata'] = 2
            #profile['width'] = mask_data.shape[1]
            #profile['height'] = mask_data.shape[0]
            with rasterio.open(new_path, 'w', **profile) as dst:
                dst.write(mask_data, 1)

            daily_files.append(new_path)
        files_created.append(daily_files)

    _logger.info("File saved successfully")
    return files_created
    

def get_quadruplet(code, dict):
    return pd.Series(dict.get(code, [None, None, None, None]), index=['first_sun_appearance',
                                                                             'first_shadow_appearance',
                                                                             'second_sun_appearance',
                                                                             'second_shadow_appearance'])


def create_dark_image(file):

    with rasterio.open(file) as src:
        # Read the image data
        image = src.read()

        # Create a new array with all pixels set to 1
        modified_image = image.copy()
        modified_image[:] = 1
        modified_image = modified_image.astype(np.uint8)

        # Update the metadata
        profile = src.profile

    return modified_image[0,:,:], profile


def get_radius_value(error_message):
    match = re.search(r"value=(\d+)", error_message)
    if match:
        return int(match.group(1))
    else:
        return None


def code_raster(stacked_array):
    # reshape array
    data_2d = stacked_array.reshape(-1, 4)

    # get quadruples
    unique_quadruplets, _ = np.unique(data_2d, axis=0, return_inverse=True)

    # create dict
    quadruplet_dict = {tuple(q): i + 1 for i, q in enumerate(unique_quadruplets)}

    # create coded raster
    new_array = np.array(
        [[quadruplet_dict[tuple(stacked_array[i, j, :])] for j in range(stacked_array.shape[1])] for i in
         range(stacked_array.shape[0])])

    return new_array, quadruplet_dict


def generate_sun_time_vector(files, time_polygonize, time_dissolve, area, occ_changes=4):

    files = files[0] # first day for now
    prefix = files[0][:-9]

    with rasterio.open(files[0]) as src:
        height = src.height
        width = src.width
        profile = src.profile

    tz = pytz.timezone(area)
    times = [tz.localize(datetime.strptime(date_string[-17:-4], "%Y%m%d-%H%M")) for date_string in files]
    timestamps = [int(time.timestamp()) for time in times]

    # occurrence des changements
    raster_arrays = []
    for path in files:
        with rasterio.open(path) as src:
            raster_arrays.append(src.read(1))

    # Initialize counters for changes from 1 to 0 and 0 to 1
    changes_1_to_0 = np.zeros_like(raster_arrays[0])
    changes_0_to_1 = np.zeros_like(raster_arrays[0])

    # Compare corresponding pixels across the arrays to identify changes
    for i in range(len(raster_arrays) - 1):
        changes_1_to_0 += np.logical_and(raster_arrays[i] == 1, raster_arrays[i + 1] == 0)
        changes_0_to_1 += np.logical_and(raster_arrays[i] == 0, raster_arrays[i + 1] == 1)

    coded_raster, dictionnary = raster_stack(changes_0_to_1, changes_1_to_0, files, height, occ_changes, timestamps,
                                             width)
    # save raster
    profile['dtype'] = 'int32'
    profile['nodata'] = -999
    out_file = prefix.replace('hillshade', 'coded_raster') + '.tif'
    with rasterio.open(out_file, 'w', **profile) as dst:
        dst.write(coded_raster, 1)

    # polygonize coded raster
    _logger.info("Starting polygonization")
    in_file = out_file
    out_file = prefix.replace('hillshade', 'coded_geoms') + '.gpkg'
    start_polygonize_time = t.time()
    command = f"gdal_polygonize.py {in_file} -b 1 -f GPKG {out_file} coded_geoms code"
    subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
    end_polygonize_time = t.time() - start_polygonize_time
    time_polygonize.set(time_polygonize.value + end_polygonize_time)
    _logger.info("End polygonization")

    # dissolve vector
    in_file, out_file = dissolve_vector(out_file, time_dissolve)

    # remove unnecessary files
    [os.remove(filename) for filename in glob.glob(f"{in_file}*")]
    os.remove(prefix.replace('hillshade', 'coded_raster') + '.tif')

    # revert dictionnary
    dictionnary = {v: k for k, v in dictionnary.items()}

    # read vector
    sun_time_vector = gpd.read_file(out_file)

    # Appliquer la fonction à la colonne 'code'
    if occ_changes == 2:
        cols = ['first_sun_appearance', 'first_shadow_appearance']
    else:
        cols = ['first_sun_appearance', 'first_shadow_appearance', 'second_sun_appearance', 'second_shadow_appearance']

    sun_time_vector[cols] = sun_time_vector['code'].apply(get_quadruplet, dict=dictionnary)

    sun_time_vector = sun_time_vector.drop(columns='code')

    def safe_convert(x):
        if x > 0:
            return pd.to_datetime(x, unit='s', utc=True).tz_convert(area).tz_localize(None).strftime("%Y-%m-%d %H:%M:%S")
        elif x == -1:
            return pd.NaT
        else:
            return times[0].replace(hour=23, minute=59, second=59).strftime("%Y-%m-%d %H:%M:%S")

    sun_time_vector[cols] = sun_time_vector[cols].applymap(safe_convert)
    final_name = out_file.replace('_dissolved', '')
    sun_time_vector.to_file(final_name, driver="GPKG")
    os.remove(out_file)

    return final_name


def dissolve_vector(out_file, time_dissolve):
    _logger.info("Starting dissolving")
    in_file = out_file
    out_file = in_file.replace('coded_geoms', 'sun_times_dissolved')
    start_dissolve_time = t.time()
    command = f'ogr2ogr {out_file} {in_file} -dialect sqlite -sql "SELECT ST_Union(geom), code FROM coded_geoms GROUP BY code" -f "GPKG"'
    subprocess.run(command, shell=True)
    end_dissolve_time = t.time() - start_dissolve_time
    time_dissolve.set(time_dissolve.value + end_dissolve_time)
    _logger.info("End dissolving")
    return in_file, out_file


def raster_stack(changes_0_to_1, changes_1_to_0, files, height, occ_changes, timestamps, width):
    # create 4 rasters
    first_sun = np.full((height, width), 0.)  # Initialize with infinity
    first_shadow = np.full((height, width), 0.)  # Initialize with infinity
    second_sun = np.full((height, width), 0.)
    second_shadow = np.full((height, width), 0.)
    # Iterate through the input rasters
    for path, timestamp in zip(files, timestamps):
        with rasterio.open(path) as src:
            data = src.read(1)  # Read the raster data
            mask_first_sun = (first_sun == 0.) & (data == 0.)  # Identify pixels changing from 1 to 0
            mask_first_shadow = (first_shadow == 0.) & (first_sun != 0.) & (
                    data == 1.)  # Identify pixels changing from 0 to 1
            mask_second_sun = (second_sun == 0.) & (first_shadow != 0.) & (
                    data == 0.)  # Identify pixels changing from 0 to 1
            mask_second_shadow = (second_shadow == 0.) & (second_sun != 0.) & (
                    data == 1.)  # Identify pixels changing from 0 to 1

            first_sun[mask_first_sun] = timestamp  # Update time for pixels changing from 1 to 0
            first_shadow[mask_first_shadow] = timestamp  # Update time for pixels changing from 0 to 1
            second_sun[mask_second_sun] = timestamp  # Update time for pixels changing from 1 to 0
            second_shadow[mask_second_shadow] = timestamp  # Update time for pixels changing from 0 to 1
    mask = changes_0_to_1 + changes_1_to_0 > occ_changes
    # set pixels with too much changes to -1
    first_sun[mask] = -1
    first_shadow[mask] = -1
    second_sun[mask] = -1
    second_shadow[mask] = -1
    # stack rasters for poligonization
    stacked_rasters = np.stack([first_sun, first_shadow, second_sun, second_shadow], axis=2)
    coded_raster, dictionnary = code_raster(stacked_rasters)
    return coded_raster, dictionnary


def generate_daily_shadow_maps(files, time_process):

    prefix = files[0][:-9]

    # create a shadow map for each day
    n_masks = len(files)
    _logger.info(f"{n_masks} for each day")
    _logger.info(files)

    # SHADOW_MAP
    start_sun_map_time = t.time()
    # Read the raster data as arrays
    raster_datasets = [rasterio.open(path) for path in files]
    raster_arrays = [raster.read(1) for raster in raster_datasets]

    # Perform pixel-wise addition
    result = np.zeros(raster_arrays[0].shape, dtype=raster_arrays[0].dtype)
    for arr in raster_arrays:
        result += arr

    result = 1 - (result / float(n_masks))
    result = np.round(result*100).astype(np.uint8)

    # write the result to a new raster file
    out_file = prefix.replace("hillshade", "sun_map") + ".tif"
    p = raster_datasets[0].profile
    p['nodata'] = 255
    p['dtype'] = 'uint8'
    with rasterio.open(out_file, 'w', **p) as dst:
        dst.write(result, 1)

    # Don't forget to close the raster datasets
    for raster in raster_datasets:
        raster.close()
    
    end_sun_map_time = t.time() - start_sun_map_time
    time_process.set(time_process.value + end_sun_map_time)

    return out_file


def seconds_to_hhmmss(seconds):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return '{:02d}:{:02d}:{:02d}.{:02d}'.format(int(hours), int(minutes), int(seconds), int((seconds - int(seconds)) * 100))

def check_date(date):
    # Check if date argument is correct
    if date:
        date_input = date
        # One date
        if len(date_input) == 1:
            start_date = date_input[0]
            end_date = date_input[0]
            step_date = 1
        # date range
        elif len(date_input) == 2:
            start_date = date_input[0]
            end_date = date_input[1]
            step_date = 1
        # date range and step
        elif len(date_input) == 3:
            start_date = date_input[0]
            end_date = date_input[1]
            step_date = date_input[2]
        else:
            _logger.info("Date format incorrect")
            sys.exit(1)
    return end_date, start_date, step_date


def check_time(time):
    # Check if time argument is correct
    if time:
        time_input = time
        # one time
        if len(time_input) == 1:
            start_time = time_input[0]
            end_time = time_input[0]
            step_time = 30
        # time range
        elif len(time_input) == 2:
            start_time = time_input[0]
            end_time = time_input[1]
            step_time = 30
        # time range and step
        elif len(time_input) == 3:
            start_time = time_input[0]
            end_time = time_input[1]
            step_time = time_input[2]
        else:
            _logger.info("Time format incorrect")
            sys.exit(1)
    return end_time, start_time, step_time


def save_temp_run(output_dir, start_main, time_azimuth_elevation_computation, time_daily_sun_percentage,
                  time_dissolve_geometries, time_polygonize_coded_raster, time_shadow_mask_execution):
    _logger.info("Saving processing times to csv file")

    time_main = t.time() - start_main
    _logger.info(f"end main {time_main}")
    _logger.info(f"test{time_azimuth_elevation_computation}")

    times = list(map(seconds_to_hhmmss,
                     [time_main,
                      time_azimuth_elevation_computation.value,
                      time_shadow_mask_execution.value,
                      time_daily_sun_percentage.value,
                      time_polygonize_coded_raster.value,
                      time_dissolve_geometries.value]
                     )
                 )

    header = ["all", "compute azimuth & elevation", "execute shadow mask", "generate daily sun percentage",
              "polygonize coded raster", "dissolve geometries"]

    with open(output_dir + "processing_time.csv", "w", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(header)
        csv_writer.writerow(times)


# Press the green button in the gutter to run the script.
def getarguments():
    parser = argparse.ArgumentParser(description="Generate a Sun Map based day, time and place")
    parser.add_argument("-dsm", "--digital_surface_model", type=str,
                        help="Path to the Digital Surface Model (DSM) or path to"
                             " .lst files that contains one input file (.tif) per line",
                        required=True)
    parser.add_argument("-tiles", "--tiles_file", type=str,
                        help="Path to the Digital Surface Model (DSM) shapes (.shp)", required=True)
    parser.add_argument("-d", "--date", nargs='+', help="Date or date range (YYYT-MM-DD format) and step (in days). "
                                                        "Default step value set to 1.", required=True)
    parser.add_argument("-t", "--time", nargs='+', help="Time or time range (HH:MM format) and step (in minutes). "
                                                        "Default step value set to 30 min", required=True)
    parser.add_argument("-n_occ", "--occ_changes", type=int, default=4, help="Number of sun/shadow changes limit a day")
    parser.add_argument("-nbc", "--nb_cores", type=int, default=1, help="Number of cores to use")
    parser.add_argument('-o', '--output_dir', default=os.getcwd(), help='Output directory path')
    parser.add_argument('-st', '--save_temp', action='store_true', help='Store processing times in CSV file')
    parser.add_argument('-sm', '--save_masks', action='store_true', help='Store hourly shadow masks')

    args = parser.parse_args()
    return vars(args)


def sun_map_generation(digital_surface_model : str, tiles_file : str, date : list, time : list, occ_changes : int,
                       nb_cores : int, output_dir : str, save_temp : bool, save_masks : bool):
    # Time management
    manager = Manager()
    time_azimuth_elevation_computation = manager.Value("time_azimuth_elevation_computation", 0.)
    time_shadow_mask_execution = manager.Value("time_shadow_mask_execution", 0.)
    time_daily_sun_percentage = manager.Value("time_daily_sun_percentage", 0.)
    time_polygonize_coded_raster = manager.Value("time_polygonize_coded_raster", 0.)
    time_dissolve_geometries = manager.Value("time_dissolve_geometries", 0.)
    start_main = t.time()
    _logger.info(f"start_main {start_main}")

    end_date, start_date, step_date = check_date(date)

    end_time, start_time, step_time = check_time(time)
    # check dsm argument
    if digital_surface_model[-3:] == 'lst':
        # Open file
        paths = []
        with open(digital_surface_model, "r") as file:
            for line in file:
                # delete /n
                line = line.strip()
                # add to list
                paths.append(line)

    elif digital_surface_model[-3:] == 'tif':
        paths = [digital_surface_model]

    else:
        _logger.info("DSM file has incorrect extension")
        parser.print_help()
        sys.exit(1)
    # Find automatically the timezone of file's location
    area = find_timezone(paths[0])
    with concurrent.futures.ProcessPoolExecutor(max_workers=nb_cores) as executor:

        all_files_created = list(executor.map(partial(generate_sun_map,
                                                      dsm_tiles=tiles_file,
                                                      start_date=start_date,
                                                      end_date=end_date,
                                                      step_date=step_date,
                                                      start_time=start_time,
                                                      end_time=end_time,
                                                      step_time=step_time,
                                                      output_dir=output_dir,
                                                      area=area,
                                                      time_az_el=time_azimuth_elevation_computation,
                                                      time_mask_exec=time_shadow_mask_execution),
                                              paths))
    if True:
        _logger.info("Creating daily shadow maps")
        path_list_by_days = list(itertools.chain.from_iterable(all_files_created))
        with concurrent.futures.ProcessPoolExecutor(max_workers=nb_cores) as executor:
            daily_sun_map_paths = list(executor.map(partial(generate_daily_shadow_maps,
                                                            time_process=time_daily_sun_percentage),
                                                    path_list_by_days))
        # generate_daily_shadow_maps(all_files_created, True, output_dir)
    # create vector with sun times (first tile and first day for now)
    if True:
        _logger.info("Creating sun time vector")
        with concurrent.futures.ProcessPoolExecutor(max_workers=nb_cores) as executor:
            sun_time_vector_paths = list(executor.map(partial(generate_sun_time_vector,
                                                              area=area,
                                                              occ_changes=occ_changes,
                                                              time_polygonize=time_polygonize_coded_raster,
                                                              time_dissolve=time_dissolve_geometries),
                                                      all_files_created))
    _logger.info("Done.")
    # remove mask files
    if not save_masks:
        files_to_remove = glob.glob(output_dir + '*hillshade*.tif')
        for f in files_to_remove:
            os.remove(f)

    # saving processing times to csv file
    if save_temp:
        save_temp_run(output_dir, start_main, time_azimuth_elevation_computation, time_daily_sun_percentage,
                  time_dissolve_geometries, time_polygonize_coded_raster, time_shadow_mask_execution)


def main():
    """
    Main function to generate sun maps.
    It parses the command line arguments and calls the sun_map_generation function.
    """
    args = getarguments()
    sun_map_generation(**args)


if __name__ == "__main__":
    main()