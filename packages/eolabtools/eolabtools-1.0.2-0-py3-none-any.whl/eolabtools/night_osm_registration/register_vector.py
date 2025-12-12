# -- coding: utf-8 --
"""Apply a displacement grid on a shapefile (geometry of type Point)

:authors: see AUTHORS file
:organization: CNES
:copyright: CNES. All rights reserved.
:license: see LICENSE file
:created: 23 October 2024
"""

import argparse
import warnings
import sys
from pathlib import Path

import rasterio
import shapely
import geopandas as gpd


def shift_vector(vector: str, grid: str) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(vector)
    grid_src = rasterio.open(grid)
    # Reproject vector to grid CRS
    if gdf.crs != grid_src.crs:
        gdf = gdf.to_crs(grid_src.crs)

    gdf = gdf[gdf.geometry.geom_type == "Point"]
    if not len(gdf):
        sys.exit("Only simple geometry of type Point is supported.")

    xgrid, ygrid = grid_src.read()

    def shift(shape: shapely.Point):
        # indexes of the point in the grid
        row, col = grid_src.index(shape.x, shape.y)

        # values of shift in pixels
        xshift_px = xgrid[row, col]
        yshift_px = ygrid[row, col]

        # shift of the indexes
        shifted_col = col - xshift_px
        shifted_row = row - yshift_px

        # coordinates of the shifted position
        shifted_x, shifted_y = grid_src.xy(shifted_row, shifted_col)
        shape = shapely.set_coordinates(shape, (shifted_x, shifted_y))

        return shape

    return gdf.set_geometry(gdf.geometry.apply(shift))


def night_osm_vector_registration(vector: str, grid: str, outdir: str, name: str):
    outdir = Path(outdir)
    gdf = shift_vector(vector, grid)
    out_file = str(outdir / (name + ".gpkg"))
    gdf.to_file(out_file)


def getarguments():
    """Main function with argument paser, for script entrypoint"""
    parser = argparse.ArgumentParser()
    parser.add_argument("vector", type=str, help="Path to the input vector file")
    parser.add_argument(
        "grid",
        type=str,
        help="Path to the displacement grid (band1 : shift along X in pixels, band 2 : shift along Y in pixels",
    )
    parser.add_argument("-o", "--outdir", type=str, help="Output directory")
    parser.add_argument("-n", "--name", type=str, help="Basename for the output file")
    # Read arguments as dict
    settings = vars(parser.parse_args())

    # Manage FutureWarnings from proj
    warnings.simplefilter(action="ignore", category=FutureWarning)
    return settings

def main():
    """
    Main function to run night vector registration.
    It parses the command line arguments and calls the night_osm_vector_registration function.
    """
    args = getarguments()
    night_osm_vector_registration(**args)

if __name__ == "__main__":
    main()