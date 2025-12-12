# stdlib imports
import logging

# third party imports
import numpy as np
import pandas as pd
from esi_utils_rupture.tensor import (
    fill_tensor_from_angles,
    fill_tensor_from_components,
)

# local imports
from strec.subtype import SubductionSelector, get_event_details
from strec.utils import read_input_file

LOGGER = "subselect"
MT_COMPS = ["mpp", "mrp", "mrr", "mrt", "mtp", "mtt"]
MT_ANGLES = ["dip", "rake", "strike"]


def get_input_dataframe(input_file, eqinfo, event_id, hypo_columns, id_column):
    """Create a dataframe of events (possibly only one).

    Args:
        input_file (str or None):  Name of input CSV/Excel file or None.
        eqinfo (tuple or None): Tuple of (lat, lon, depth, magnitude) or None.
        event_id (str or None): ComCat Event ID or None.
        hypo_columns (tuple or None): Tuple of hypocenter column names in input_file or
                                      None.
        id_column (str or None): Name of column in input_file containing ComCat Event
                                 ID or None.

    Returns:
        tuple of:
            - pandas DataFrame containing at least lat/lon/depth columns
            - Name of ComCat event ID column or None
            - Name of latitude column
            - Name of longitude column
            - Name of depth column
    """
    latcol = "lat"
    loncol = "lon"
    depcol = "depth"
    magcol = "mag"
    idcol = None
    if input_file is not None:
        df, idcol, latcol, loncol, depcol, magcol = read_input_file(
            input_file, hypo_columns, id_column
        )
    elif eqinfo is not None:
        lat, lon, depth, mag = eqinfo
        d = {"lat": [lat], "lon": [lon], "depth": [depth], "mag": [mag]}
        df = pd.DataFrame(d)
    if event_id is not None:
        detail = get_event_details(event_id)
        idcol = "ComCatID"
        lat, lon, depth, mag = (
            detail["latitude"],
            detail["longitude"],
            detail["depth"],
            detail["magnitude"],
        )
        d = {
            "ComCatID": event_id,
            "lat": [lat],
            "lon": [lon],
            "depth": [depth],
            "mag": [mag],
        }
        df = pd.DataFrame(d)
    return (df, idcol, latcol, loncol, depcol, magcol)


def get_moment_columns(row):
    """Return focal mechanism/moment tensor parameters from MT components or focal angles.

    Args:
        row (pandas Series): Contains moment tensor components (mtt, mpp, etc) OR
                             focal angles (strike, dip, rake)

    Returns:
        dict: Fully descriptive moment tensor dictionary, including fields:
            - mrr,mtt,mpp,mrt,mrp,mtp Moment tensor components.
            - T T-axis values:
              - azimuth (degrees)
              - plunge (degrees)
            - N N-axis values:
              - azimuth (degrees)
              - plunge (degrees)
            - P P-axis values:
              - azimuth (degrees)
              - plunge (degrees)
            - NP1 First nodal plane values:
              - strike (degrees)
              - dip (degrees)
              - rake (degrees)
            - NP2 Second nodal plane values:
              - strike (degrees)
              - dip (degrees)
              - rake (degrees)
    """
    # row is a pandas series object
    # is it a series containing moment tensor components or focal angles?
    indices = sorted([c.lower() for c in row.index.tolist()])
    if indices != MT_COMPS and indices != MT_ANGLES:
        return None
    # are all values finite (non NaN)?
    if row.notnull().sum() < len(row):
        return None
    rowdict = row.to_dict()
    rowdict = {k.lower(): v for k, v in rowdict.items()}
    if indices == MT_COMPS:
        tensor_params = fill_tensor_from_components(
            rowdict["mrr"],
            rowdict["mtt"],
            rowdict["mpp"],
            rowdict["mrt"],
            rowdict["mrp"],
            rowdict["mtp"],
        )
    else:
        tensor_params = fill_tensor_from_angles(
            rowdict["strike"], rowdict["dip"], rowdict["rake"]
        )

    return tensor_params


def check_moment_row(row):
    """Check row of dataframe for presence of moment tensor information.

    Args:
        row (pandas Series): Series possibly containing moment tensor data
    Returns:
        bool: True if input contains moment tensor or focal mechanism data.
    """
    # row is a pandas series object
    hasAngles = True
    hasComponents = True

    keys = set([key.lower() for key in (row.keys()).values.tolist()])
    cmp_components = set(["mrr", "mpp", "mtt", "mrt", "mrp", "mtp"])
    if not cmp_components.issubset(keys):
        hasComponents = False

    cmp_angles = set(["strike", "dip", "rake"])
    if not cmp_angles.issubset(keys):
        hasAngles = False

    return hasAngles or hasComponents


def select_regions(
    input_file,
    eqinfo,
    moment_info,
    event_id,
    hypo_columns,
    id_column,
    verbose,
):
    """Output full range of seismotectonic information.

    Args:
        input_file (str or None):  Name of input CSV/Excel file or None.
        eqinfo (tuple or None): Tuple of (lat, lon, depth, magnitude) or None.
        moment_info (tuple or None): Tuple of (strike, dip, rake) or None.
        event_id (str or None): ComCat Event ID or None.
        hypo_columns (tuple or None): Tuple of hypocenter column names in input_file
                                      or None.
        id_column (str or None): Name of column in input_file containing ComCat
                                 Event ID or None.
        verbose (bool): Turn verbose debugging on/off.
    Returns:
        Pandas Series object with indices:
            - TectonicRegion : (Subduction,Active,Stable,Volcanic)
            - FocalMechanism : (RS [Reverse],SS [Strike-Slip], NM [Normal], ALL
            [Unknown])
            - TensorType : (actual, composite)
            - TensorSource : String indicating the source of the moment tensor
            information.
            - KaganAngle : Angle between moment tensor and slab interface.
            - CompositeVariability : A measure of the uncertainty in the composite
            moment tensor.
            - NComposite : Number of events used to create composite moment tensor.
            - DistanceToStable : Distance in km from the nearest stable polygon.
            - DistanceToActive : Distance in km from the nearest active polygon.
            - DistanceToSubduction : Distance in km from the nearest subduction
            polygon.
            - DistanceToVolcanic : Distance in km from the nearest volcanic polygon.
            - Oceanic : Boolean indicating whether we are in an oceanic region.
            - DistanceToOceanic : Distance in km to nearest oceanic polygon.
            - DistanceToContinental : Distance in km to nearest continental polygon.
            - SlabModelRegion : Subduction region.
            - SlabModelType : (grid,trench)
            - SlabModelDepth : Depth to slab interface at epicenter.
            - SlabModelDepthUncertainty : Uncertainty of depth to slab interface.
            - SlabModelDip : Dip of slab at epicenter.
            - SlabModelStrike : Strike of slab at epicenter.
    """
    selector = SubductionSelector(verbose=verbose, prefix=LOGGER)
    dataframe, idcol, latcol, loncol, depcol, magcol = get_input_dataframe(
        input_file, eqinfo, event_id, hypo_columns, id_column
    )
    tensor_params = None
    if moment_info is not None and all(moment_info):
        strike, dip, rake = moment_info
        tensor_params = fill_tensor_from_angles(strike, dip, rake, dataframe[magcol])
    has_tensor = check_moment_row(dataframe.iloc[0]) or tensor_params is not None
    rows = []
    ic = 0
    inc = min(100, np.power(10, np.floor(np.log10(len(dataframe))) - 1))
    for _, row in dataframe.iterrows():
        if ic % inc == 0 and verbose:
            msg = "Getting detailed information for %i of %i events.\n"
            logging.info(msg % (ic, len(dataframe)))
        if idcol is not None:
            event_id = row[idcol]
        if not tensor_params and has_tensor:
            tensor_params = get_moment_columns(row)

        lat = row[latcol]
        lon = row[loncol]
        # for the cases where lon goes from 0-360
        if lon > 180:
            lon -= 360
        depth = row[depcol]
        mag = row[magcol]
        result = selector.getSubductionType(
            lat,
            lon,
            depth,
            mag,
            eventid=event_id,
            tensor_params=tensor_params,
        )

        tensor_params = None
        row = pd.concat([row, result])
        rows.append(row)
    output_dataframe = pd.DataFrame(rows)
    return output_dataframe
