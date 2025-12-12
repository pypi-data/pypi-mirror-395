# stdlib imports
import configparser
import json
import pathlib
import re

# third party imports
import numpy as np
import pandas as pd
import pyproj
from shapely.geometry import LineString, shape
from shapely.ops import transform

STRECINI = "config.ini"
MOMENT_DB = "moment_tensors.db"

CONSTANTS = {
    "minradial_disthist": 0.01,
    "maxradial_disthist": 1.0,
    "minradial_distcomp": 0.5,
    "maxradial_distcomp": 1.0,
    "step_distcomp": 0.1,
    "depth_rangecomp": 10,
    "minno_comp": 3,
    "default_szdip": 17,
    "dstrike_interf": 30,
    "ddip_interf": 30,
    "dlambda": 60,
    "ddepth_interf": 20,
    "ddepth_intra": 10,
}


def get_longest_axis():
    root = pathlib.Path(__file__).parent / "data"
    jsonfiles = root.glob("**/*.geojson")
    longest_axis = 0
    for jsonfile in jsonfiles:
        with open(jsonfile, "r") as input:
            jdict = json.load(input)
        for record in jdict["features"]:
            polygon = shape(record["geometry"])
            clon, clat = polygon.centroid.xy
            pstr = f"+proj=aeqd +lon_0={clon[0]:.6f} +lat_0={clat[0]:.6f} +ellps=WGS84"
            out_crs = pyproj.CRS(pstr)
            in_crs = pyproj.CRS("EPSG:4326")
            pfunction = pyproj.Transformer.from_crs(
                in_crs, out_crs, always_xy=True
            ).transform
            ppolygon = transform(pfunction, polygon)
            # get the minimum bounding rectangle and zip coordinates into a list
            # of point-tuples
            mbr_points = list(
                zip(*ppolygon.minimum_rotated_rectangle.exterior.coords.xy)
            )

            # calculate the length of each side of the minimum bounding rectangle
            mbr_lengths = [
                LineString((mbr_points[i], mbr_points[i + 1])).length
                for i in range(len(mbr_points) - 1)
            ]

            # get major/minor axis measurements
            major_axis = max(mbr_lengths) / 1000
            if major_axis > longest_axis:
                longest_axis = major_axis

    return longest_axis


def get_config_file_name():
    config_file = pathlib.Path().home() / ".strec" / STRECINI
    return config_file


def create_config(datafolder):
    datafolder = pathlib.Path(datafolder)
    # create or re-create config file
    config_file = get_config_file_name()
    config = configparser.ConfigParser()
    longest_axis = get_longest_axis()
    config["DATA"] = {
        "folder": datafolder,
        "slabfolder": datafolder / "slabs",
        "dbfile": datafolder / MOMENT_DB,
        "longest_axis": longest_axis,
    }
    config["CONSTANTS"] = CONSTANTS
    config_folder = config_file.parent
    if not config_folder.exists():
        config_folder.mkdir(parents=True)
    with open(config_file, "wt") as cfile:
        config.write(cfile)
    return config


def get_config():
    """Get configuration information as a dictionary.

    'folder' should always be set to point to library data path.
    'dbfile' should be set to point to library data path unless specified in
    ~/.strec/strec.ini
    'slabfolder' should be set to point to library data path unless specified in
    ~/.strec/strec.ini

    Returns:
        config (dict): Dictionary containing fields:
            - CONSTANTS Dictionary containing constants for the application.
            - DATA Dictionary containing 'folder', 'slabfolder', and 'dbfile'.
    """
    # first look in the default path for a config file
    config_file = get_config_file_name()
    if config_file.is_file():
        config = configparser.ConfigParser()
        config.read(config_file)
        if "DATA" not in config:
            raise KeyError("STREC config file is missing the [DATA] section.")
    else:
        raise FileNotFoundError(f"Config file not found at {config_file}.")
    return config


def read_input_file(input_file, hypo_columns, id_column):
    """Read a CSV/Excel input file, return a DataFrame

    This function will deal with any moment tensor component columns it finds,
    (mrr,mtt,etc) and convert any that are integers into floats.

    Args:
        input_file (str): Path to CSV/Excel file containing lat,lon,depth,mag columns
            and optionally moment tensor columns
            ('mrr','mtt','mpp','mrt','mrp','mtp').
    Returns:
        DataFrame: Pandas dataframe containing contents of input file.
    Raises:
        ValueError: When input file is neither a CSV nor an Excel file.
    """
    df = None
    try:
        df = pd.read_csv(input_file)
    except Exception:
        try:
            df = pd.read_excel(input_file)
        except Exception:
            raise ValueError("%s is neither a CSV nor Excel file." % input_file)

    idcol = None  # this is not required
    latcol = None
    loncol = None
    depcol = None
    magcol = None
    if hypo_columns is not None and all(hypo_columns):
        if not set(hypo_columns).issubset(set(df.columns)):
            raise KeyError(f"Missing input hypo columns: {str(hypo_columns)}")
        latcol, loncol, depcol, magcol = hypo_columns
    if id_column is not None:
        if id_column not in df.columns:
            raise KeyError(f"Missing input comcat ID column: {id_column}")
        idcol = id_column

    # if the column names were not set by the user, try to find columns
    # that indicate comcatid, latitude, longitude and depth.
    latidx = df.columns.to_series().str.contains("^lat", case=False)
    if latidx.any():
        latcol = df.columns[latidx].array[0]
    lonidx = df.columns.to_series().str.contains("^lon", case=False)
    if lonidx.any():
        loncol = df.columns[lonidx].array[0]
    depidx = df.columns.to_series().str.contains("^depth", case=False)
    if depidx.any():
        depcol = df.columns[depidx].array[0]
    magidx = df.columns.to_series().str.contains("^mag", case=False)
    if magidx.any():
        magcol = df.columns[magidx].array[0]

    # the id column is not mandatory
    ididx = df.columns.to_series().str.contains("^eventid", case=False)
    if ididx.any():
        idcol = df.columns[ididx].array[0]

    if latcol is None or loncol is None or depcol is None or magcol is None:
        raise KeyError(
            (
                "Input table is missing identifiable columns for latitude, "
                "longitude, depth, or magnitude."
            )
        )

    # convert any long integer moment component columns to floating point, because
    # otherwise pandas will complain later when re-writing row to a dataframe.  Doesn't
    # make sense, but seems necessary.
    for column in df:
        comps = ["mrr", "mtt", "mpp", "mrt", "mrp", "mtp"]
        for comp in comps:
            if column.lower().find(comp) > -1:
                col = df[column].apply(lambda x: convert_float(x))
                df[column] = col

    return (df, idcol, latcol, loncol, depcol, magcol)


def convert_float(val):
    try:
        return float(val)
    except ValueError:
        return np.nan


def render_row(row, format, hypo_columns):
    """Render a Series containing regselect output to the screen.

    Args:
        row (Series): Pandas series object.
        format (str): One of 'pretty','json','csv'.
        lat (float): Earthquake hypocentral latitude.
        lon (float): Earthquake hypocentral longitude.
        depth (float): Earthquake hypocentral depth.
    """
    if hypo_columns is not None and all(hypo_columns):
        lat, lon, depth = (
            row[hypo_columns[0]],
            row[hypo_columns[1]],
            row[hypo_columns[2]],
        )
    else:
        lat = row.filter(regex="^[l,L]at").values[0]
        lon = row.filter(regex="^[l,L]on").values[0]
        depth = row.filter(regex="^[d,D]epth").values[0]
    if format == "pretty":
        print("For event located at %.4f,%.4f,%.1f:" % (lat, lon, depth))
        for idx, value in row.items():
            if re.match("^lat|^lon|^depth", idx, re.IGNORECASE):
                continue
            print("\t%s : %s" % (idx, str(value)))
        print()
    elif format == "json":
        print(row.to_json())
    elif format == "csv":
        values = [str(v) for v in row.values]
        print(",".join(values))
