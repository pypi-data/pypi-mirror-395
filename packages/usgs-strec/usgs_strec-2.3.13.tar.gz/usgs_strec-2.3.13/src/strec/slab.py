# stdlib imports
import logging
import pathlib
import time
from io import BytesIO
from zipfile import ZipFile

# third party imports
import numpy as np
import pandas as pd
import rasterio
import requests
from rasterio.windows import Window

MAX_INTERFACE_DEPTH = 70  # depth beyond which any tectonic regime has to be intraslab

# Slab 1.0 does not have depth uncertainty, so we make this a constant
DEFAULT_DEPTH_ERROR = 10

ITEM_TEMPLATE = "https://www.sciencebase.gov/catalog/item/{itemid}?format=json"
# ITEM_TEMPLATE = "http://www.sciencebase.gov/catalog/file/get/[ITEMID]"
SEARCH_URL = "https://apps.usgs.gov/shakemap_geodata/slabs/slab2.zip"
KEYWORDS = ["subduction", "model", "slab2"]
SLABGRID_REGEX = "dep|str|dip|unc"
WAIT = 10
TIMEOUT = 60


def get_slab_grids2(path):
    print("Retrieving slab2 model")
    nfiles = 0
    response = requests.get(SEARCH_URL, timeout=TIMEOUT)
    data = response.content
    with BytesIO(data) as fobj:
        with ZipFile(fobj, mode="r") as myzip:
            for gridfile in myzip.namelist():
                logging.info(f"Writing {gridfile} to {path}...")
                myzip.extract(gridfile, path)
                nfiles += 1
    print("Done.")
    return (True, f"Downloaded {nfiles} grid files from {SEARCH_URL} to {path}")


def get_slab_grids(path):
    if not path.exists():
        path.mkdir(parents=True)
    logging.info(f"Downloading slab data from {SEARCH_URL}...")
    nfiles = 0
    try:
        response = requests.get(SEARCH_URL, timeout=TIMEOUT)
    except Exception as e:
        print(
            f"First download attempt failed. Sleeping for {WAIT} seconds, then trying again..."
        )
        time.sleep(WAIT)
        try:
            response = requests.get(SEARCH_URL)
        except Exception as e:
            print(
                f"First download attempt failed. Sleeping for {WAIT} seconds, then trying again..."
            )
            time.sleep(WAIT)
            try:
                response = requests.get(SEARCH_URL)
            except Exception:
                raise Exception(
                    f"Failed to download slab data from {SEARCH_URL} after three attempts."
                )
    with BytesIO(response.content) as fobj:
        with ZipFile(fobj, mode="r") as myzip:
            for gridfile in myzip.namelist():
                logging.info(f"Writing {gridfile} to {path}...")
                myzip.extract(gridfile, path)
                nfiles += 1

    return (True, f"Downloaded {nfiles} grid files from {SEARCH_URL} to {path}")


class GridSlab(object):
    """Represents USGS Slab model grids for a given subduction zone."""

    def __init__(self, depth_file, dip_file, strike_file, error_file):
        """Construct GridSlab object from input files.

        Args:
            depth_file (str): Path to Slab depth grid file.
            dip_file (str): Path to Slab dip grid file.
            strike_file (str): Path to Slab strike grid file.
            error_file (str): Path to Slab depth error grid file (can be None).
        """
        self._depth_file = pathlib.Path(depth_file)
        self._dip_file = pathlib.Path(dip_file)
        self._strike_file = pathlib.Path(strike_file)
        self._error_file = pathlib.Path(error_file)

        # there may be a table of maximum slab depths in the same directory
        # as all of the slab grids.  Read it into a local dictionary if found,
        # otherwise we'll use the MAX_INTERFACE_DEPTH constant found above.
        table_file_name = (
            pathlib.Path(__file__).parent / "data" / "maximum_interface_depths.csv"
        )
        if table_file_name.is_file():
            self._slab_table = pd.read_csv(table_file_name)
        else:
            self._slab_table = None

    def getGridValue(self, grid, lat, lon):
        # rasterio does geo-referencing on grid-line basis, we do it on pixel basis
        # (half pixel down and to the right)
        xmax, _ = grid.xy(grid.height, grid.width)
        if xmax > 180:
            lon += 360
        row, col = grid.index(lon, lat)
        nrows, ncols = grid.shape
        if row < 0 or row > nrows - 1 or col < 0 or col > ncols - 1:
            return np.nan

        value = grid.read(1, window=Window(col, row, 1, 1))[0][0]
        return value

    def contains(self, lat, lon):
        """Check to see if input coordinates are contained inside Slab model.

        Args:
            lat (float):  Hypocentral latitude in decimal degrees.
            lon (float):  Hypocentral longitude in decimal degrees.
        Returns:
            bool: True if point falls inside minimum bounding box of slab model.
        """
        with rasterio.open(self._depth_file, "r") as dataset:
            xmin, ymax = dataset.xy(0, 0)
            xmax, ymin = dataset.xy(dataset.height, dataset.width)
            if xmax > 180:
                lon += 360
        if lat >= ymin and lat <= ymax and lon >= xmin and lon <= xmax:
            return True
        return False

    def getSlabInfo(self, lat, lon):
        """Return a dictionary with depth,dip,strike, and depth uncertainty.

        Args:
            lat (float):  Hypocentral latitude in decimal degrees.
            lon (float):  Hypocentral longitude in decimal degrees.
        Returns:
            dict: Dictionary containing keys:
                - region Three letter Slab model region code.
                - strike Slab model strike angle.
                - dip Slab model dip angle.
                - depth Slab model depth (km).
                - depth_uncertainty Slab model depth uncertainty.
        """
        slabinfo = {}
        if not self.contains(lat, lon):
            return slabinfo
        fname = self._depth_file.with_suffix("").name
        parts = fname.split("_")
        region = parts[0]

        with rasterio.open(self._depth_file, "r") as depth_grid:
            # slab grids are negative depth
            depth = -1 * self.getGridValue(depth_grid, lat, lon)

        with rasterio.open(self._dip_file, "r") as dip_grid:
            dip = self.getGridValue(dip_grid, lat, lon)

        with rasterio.open(self._strike_file, "r") as strike_grid:
            strike = self.getGridValue(strike_grid, lat, lon)
            if strike < 0:
                strike += 360

        error = DEFAULT_DEPTH_ERROR
        with rasterio.open(self._error_file, "r") as error_grid:
            error = self.getGridValue(error_grid, lat, lon)
            if np.isnan(strike):
                error = np.nan

        # get the maximum interface depth from table (if present)
        if self._slab_table is not None:
            df = self._slab_table
            max_int_depth = df[df["zone"] == region].iloc[0]["interface_max_depth"]
        else:
            max_int_depth = MAX_INTERFACE_DEPTH

        slabinfo = {
            "region": region,
            "strike": strike,
            "dip": dip,
            "depth": depth,
            "maximum_interface_depth": max_int_depth,
            "depth_uncertainty": error,
        }
        return slabinfo


class SlabCollection(object):
    def __init__(self, datafolder):
        """Object representing a collection of SlabX.Y grids.

        This object can be queried with a latitude/longitude to see if that point is
        within a subduction slab - if so, the slab information is returned.

        Args:
            datafolder (str): String path where grid files and GeoJSON file reside.
        """
        datafolder = pathlib.Path(datafolder)
        self._depth_files = datafolder.glob("*_dep*.grd")

    def getSlabInfo(self, lat, lon, depth):
        """Query the entire set of slab models and return a SlabInfo object, or None.

        Args:
            lat (float):  Hypocentral latitude in decimal degrees.
            lon (float):  Hypocentral longitude in decimal degrees.
            depth (float): Hypocentral depth in km.

        Returns:
            dict: Dictionary containing keys:
                - region Three letter Slab model region code.
                - strike Slab model strike angle.
                - dip Slab model dip angle.
                - depth Slab model depth (km).
                - depth_uncertainty Slab model depth uncertainty.
        """

        deep_depth = 99999999999
        slabinfo = {}
        # loop over all slab regions, return keep all slabs found
        for depth_file in self._depth_files:
            dip_file = pathlib.Path(str(depth_file).replace("dep", "dip"))
            strike_file = pathlib.Path(str(depth_file).replace("dep", "str"))
            error_file = pathlib.Path(str(depth_file).replace("dep", "unc"))
            if not error_file.is_file():
                error_file = None
            gslab = GridSlab(depth_file, dip_file, strike_file, error_file)
            tslabinfo = gslab.getSlabInfo(lat, lon)
            if not len(tslabinfo):
                continue
            else:
                depth = tslabinfo["depth"]
                if depth < deep_depth:
                    slabinfo = tslabinfo.copy()
                    deep_depth = depth
                elif np.isnan(depth) and "depth" not in slabinfo:
                    slabinfo = tslabinfo.copy()

        return slabinfo
