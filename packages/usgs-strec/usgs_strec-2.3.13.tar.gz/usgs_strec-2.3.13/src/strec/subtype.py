#!/usr/bin/env python

# stdlib imports
import logging
import pathlib

# third party imports
import numpy as np
import requests
from esi_utils_rupture.tensor import (
    fill_tensor_from_angles,
    fill_tensor_from_components,
)

# local imports
from strec.cmt import getCompositeCMT
from strec.config import get_select_config
from strec.gmreg import Regionalizer
from strec.kagan import get_kagan_angle
from strec.slab import SlabCollection
from strec.sm_probs import get_probs
from strec.utils import get_config

EVENT_URL = (
    "https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=EVENTID&format=geojson"
)
SLAB_RAKE = 90  # presumed rake angle of slabs

SLAB_REGIONS = {
    "alu": "Alaska-Aleutians",
    "cal": "Calabria",
    "cam": "Central America",
    "car": "Caribbean",
    "cas": "Cascadia",
    "cot": "Cotabato",
    "hal": "Halmahera",
    "hel": "Helanic",
    "him": "Himalaya",
    "hin": "Hindu Kush",
    "izu": "Izu-Bonin",
    "ker": "Kermadec-Tonga",
    "kur": "Kamchatka/Kurils/Japan",
    "mak": "Makran",
    "man": "Manila",
    "mex": "Central America",
    "mue": "Muertos",
    "pam": "Pamir",
    "pan": "Panama",
    "phi": "Philippines",
    "png": "New Guinea",
    "puy": "Puysegur",
    "ryu": "Ryukyu",
    "sam": "South America",
    "sco": "Scotia",
    "sol": "Solomon Islands",
    "sul": "Sulawesi",
    "sum": "Sumatra-Java",
    "van": "Santa Cruz Islands/Vanuatu/Loyalty Islands",
}

CONSTANTS = {
    "tplunge_rs": 50,
    "bplunge_ds": 30,
    "bplunge_ss": 55,
    "pplunge_nm": 55,
    "delplunge_ss": 20,
}

COMCAT_TEMPLATE = (
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/[EVENTID].geojson"
)

PROB_TRANSLATOR = {
    "acr": "ProbabilityActive",
    "scr": "ProbabilityStable",
    "subduction": "ProbabilitySubduction",
    "volcanic": "ProbabilityVolcanic",
    "crustal": "ProbabilitySubductionCrustal",
    "interface": "ProbabilitySubductionInterface",
    "intraslab": "ProbabilitySubductionIntraslab",
}

TENSOR_COMPONENTS = {"T", "N", "P", "NP1", "NP2"}
TENSOR_PARAMETERS = {"mrr", "mtt", "mpp", "mtp", "mrt", "mrp"}


def fill_axis(axis, tensor_props):
    axis_dict = {}
    if f"{axis.lower()}-axis-plunge" in tensor_props:
        axis_dict[f"{axis.upper()}"] = {
            "azimuth": float(tensor_props[f"{axis.lower()}-axis-azimuth"]),
            "plunge": float(tensor_props[f"{axis.lower()}-axis-plunge"]),
        }
    return axis_dict


def fill_nodal_plane(nodal_plane, tensor_props):
    # nodal_plane = NP1/2
    planes = {
        "NP1": "nodal-plane-1",
        "NP2": "nodal-plane-2",
    }
    plane = planes[nodal_plane]
    nodal_dict = {}
    rake_str = f"{plane}-rake"
    slip_str = f"{plane}-slip"
    strike_str = f"{plane}-strike"
    dip_str = f"{plane}-dip"
    if rake_str in tensor_props:
        nodal_dict["rake"] = float(tensor_props[rake_str])
    else:
        nodal_dict["rake"] = float(tensor_props[slip_str])
    nodal_dict["strike"] = float(tensor_props[strike_str])
    nodal_dict["dip"] = float(tensor_props[dip_str])
    return nodal_dict


def get_event_details(eventid):
    event_dict = {}
    url = COMCAT_TEMPLATE.replace("[EVENTID]", eventid)
    response = requests.get(url)
    jdict = response.json()
    event_dict["latitude"] = jdict["geometry"]["coordinates"][1]
    event_dict["longitude"] = jdict["geometry"]["coordinates"][0]
    event_dict["depth"] = jdict["geometry"]["coordinates"][2]
    event_dict["magnitude"] = jdict["properties"]["mag"]
    mech_type = "moment-tensor"
    if "moment-tensor" not in jdict["properties"]["products"].keys():
        if "focal-mechanism" not in jdict["properties"]["products"].keys():
            return event_dict
        mech_type = "focal-mechanism"
    tensor_dict = jdict["properties"]["products"][mech_type][0]
    tensor_props = tensor_dict["properties"]
    tensor_type = tensor_props.get("derived-magnitude-type", "unknown")
    if tensor_type == "unknown":
        btype = tensor_props.get("beachball-type", "unknown")
        if btype != "unknown":
            if btype.find("/") > -1:
                btype = btype.split("/")[-1]
            tensor_type = btype
    tensor = {}
    tensor["type"] = tensor_type
    tensor["source"] = "unknown"
    tensor["source"] = tensor_props.get("eventsource", "unknown")
    if tensor["source"] == "unknown":
        tensor["source"] = tensor_props.get("beachball-source", "unknown")
    if mech_type == "moment-tensor":
        tensor["mrr"] = float(tensor_props["tensor-mrr"])
        tensor["mtt"] = float(tensor_props["tensor-mtt"])
        tensor["mpp"] = float(tensor_props["tensor-mpp"])
        tensor["mrt"] = float(tensor_props["tensor-mrt"])
        tensor["mrp"] = float(tensor_props["tensor-mrp"])
        tensor["mtp"] = float(tensor_props["tensor-mtp"])
    for axis in ["T", "N", "P"]:
        axis_dict = fill_axis(axis, tensor_props)
        tensor.update(axis_dict)
    for nodal_plane in ["NP1", "NP2"]:
        if "nodal-plane-1-dip" not in tensor_props:
            continue
        tensor[nodal_plane] = fill_nodal_plane(nodal_plane, tensor_props)
    event_dict["tensor"] = tensor
    return event_dict


class SubductionSelector(object):
    """For subduction events, determine subduction zone properties."""

    def __init__(self, prefix=None, verbose=False):
        """Construct a SubductionSelector object."""
        if prefix is not None:
            self.logger = logging.getLogger(prefix)
        else:
            self.logger = logging.getLogger()
        self.verbose = verbose
        self._regionalizer = Regionalizer.load()
        self._config = get_config()

    def getSubductionTypeByID(self, eventid):
        """Given an event ID, determine the subduction zone information.

        Args:
            eventid (str): ComCat EventID (Sumatra is official20041226005853450_30).
        Returns:
            Pandas Series object with indices:
                - TectonicRegion : (Subduction,Active,Stable,Volcanic)
                - TectonicDomain : SZ (generic)
                - FocalMechanism : (RS [Reverse],SS [Strike-Slip], NM [Normal], ALL
                [Unknown])
                - TensorType : (actual, composite)
                - KaganAngle : Angle between moment tensor and slab interface.
                - DistanceToStable : Distance in km from the nearest stable polygon.
                - DistanceToActive : Distance in km from the nearest active polygon.
                - DistanceToSubduction : Distance in km from the nearest subduction
                polygon.
                - DistanceToVolcanic : Distance in km from the nearest volcanic polygon.
                - Oceanic : Boolean indicating whether we are in an oceanic region.
                - DistanceToOceanic : Distance in km to nearest oceanic polygon.
                - DistanceToContinental : Distance in km to nearest continental polygon.
                - TectonicSubtype : (SZInter,ACR,SZIntra)
                - RegionContainsBackArc : Boolean indicating whether event is in a
                back-arc subduction region.
                - DomainDepthBand1 : Bottom of generic depth level for shallowest
                subduction type.
                - DomainDepthBand1Subtype : Shallowest subduction type.
                - DomainDepthBand2 : Bottom of generic depth level for middle
                subduction type.
                - DomainDepthBand2Subtype : Middle subduction type.
                - DomainDepthBand3 : Bottom of generic depth level for deepest
                subduction type.
                - DomainDepthBand3Subtype : Deepest subduction type
                - SlabModelRegion : Subduction region.
                - SlabModelType : (grid,trench)
                - SlabModelDepth : Depth to slab interface at epicenter.
                - SlabModelDip : Dip of slab at epicenter.
                - SlabModelStrike : Strike of slab at epicenter.
                - IsLikeInterface : Boolean indicating whether moment tensor strike is
                similar to interface.
                - IsNearInterface : Boolean indicating whether depth is close to
                interface.
                - IsInSlab : Boolean indicating whether depth is within the slab.
        Raises:
            AttributeError if the eventid is not found in ComCat.
        """
        if self.verbose:
            self.logger.info("Inside getSubductionTypeByID...")
        lat, lon, depth, magnitude, tensor_params = self.getOnlineTensor(eventid)
        if self.verbose:
            self.logger.info("Tensor Parameters: %s" % str(tensor_params))
        if lat is None:
            raise AttributeError("Event %s is not found in ComCat." % eventid)

        lat = float(lat)
        lon = float(lon)
        results = self.getSubductionType(
            lat, lon, depth, magnitude, tensor_params=tensor_params
        )
        return results

    def getOnlineTensor(self, eventid):
        """Get tensor parameters from preferred ComCat moment tensor.

        Args:
            eventid (str): ComCat EventID (Sumatra is official20041226005853450_30).
        Returns:
            Moment tensor parameters dictionary:
                - source Moment Tensor source
                - type usually mww,mwc,mwb,mwr,TMTS or "unknown".
                - mrr,mtt,mpp,mrt,mrp,mtp Moment tensor components.
                - T T-axis values:
                  - azimuth
                  - plunge
                - N N-axis values:
                  - azimuth
                  - plunge
                - P P-axis values:
                  - azimuth
                  - plunge
                - NP1 First nodal plane values:
                  - strike
                  - dip
                  - rake
                - NP2 Second nodal plane values:
                  - strike
                  - dip
                  - rake
        """
        if self.verbose:
            self.logger.info("Inside getOnlineTensor")
        try:
            detail = get_event_details(eventid)
        except Exception as e:
            msg = 'Failed to get event information for %s - error "%s"'
            tpl = (eventid, str(e))
            self.logger.warn(msg % tpl)
            return (None, None, None, None, None)
        lat = detail["latitude"]
        lon = detail["longitude"]
        depth = detail["depth"]
        magnitude = detail["magnitude"]
        if "tensor" not in detail:
            self.logger.info("No moment tensor available for %s" % eventid)
            return (lat, lon, depth, magnitude, None)

        if self.verbose:
            self.logger.info("Getting tensor components...")
        tensor_params = detail["tensor"]

        # if no tensor, bail out
        if tensor_params is None:
            return (lat, lon, depth, magnitude, tensor_params)

        if self.verbose:
            self.logger.info("Getting tensor axes...")
        # sometimes the online MT is missing properties

        tkeys = set(tensor_params.keys())
        if not TENSOR_COMPONENTS.issubset(tkeys):
            if TENSOR_PARAMETERS.issubset(tkeys):
                if self.verbose:
                    self.logger.info("Calling fill_tensor function...")
                tensor_dict = fill_tensor_from_components(
                    tensor_params["mrr"],
                    tensor_params["mtt"],
                    tensor_params["mpp"],
                    tensor_params["mrt"],
                    tensor_params["mrp"],
                    tensor_params["mtp"],
                )
            else:
                if "NP1" in tensor_params:
                    key = "NP1"
                elif "NP2" in tensor_params:
                    key = "NP2"
                else:
                    return (lat, lon, depth, magnitude, None)
                tensor_dict = fill_tensor_from_angles(
                    tensor_params[key]["strike"],
                    tensor_params[key]["dip"],
                    tensor_params[key]["rake"],
                    magnitude=magnitude,
                )

            tensor_params["T"] = tensor_dict["T"].copy()
            tensor_params["N"] = tensor_dict["T"].copy()
            tensor_params["P"] = tensor_dict["P"].copy()
            tensor_params["NP1"] = tensor_dict["NP1"].copy()
            tensor_params["NP2"] = tensor_dict["NP2"].copy()

        return (lat, lon, depth, magnitude, tensor_params)

    def getSubductionType(
        self, lat, lon, depth, magnitude, eventid=None, tensor_params=None
    ):
        """Given a event hypocenter, determine the subduction zone information.

        Args:
            lat (float): Epicentral latitude.
            lon (float): Epicentral longitude.
            depth (float): Epicentral depth.
            eventid (float): ComCat EventID (Sumatra is official20041226005853450_30).
            tensor_params (dict): Dictionary containing moment tensor parameters:
                - mrr,mtt,mpp,mrt,mrp,mtp Moment tensor components.
                - T T-axis values:
                  - azimuth
                  - plunge
                - N N-axis values:
                  - azimuth
                  - plunge
                - P P-axis values:
                  - azimuth
                  - plunge
                - NP1 First nodal plane values:
                  - strike
                  - dip
                  - rake
                - NP2 Second nodal plane values:
                  - strike
                  - dip
                  - rake
                (optional) - type Moment Tensor type.
                (optional) - source Moment Tensor source (regional network, name of
                study, etc.)
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
        if self.verbose:
            self.logger.info("Inside getSubductionType...")
        # sometimes events are specified with negative depths, which don't work with
        # our algorithms.  Pin those depths to 0.
        if depth < 0:
            depth = 0

        config = self._config
        slab_data_folder = pathlib.Path(config["DATA"]["slabfolder"])
        data_folder = pathlib.Path(config["DATA"]["folder"])
        tensor_type = None
        tensor_source = None
        similarity = np.nan
        nevents = 0
        if tensor_params is None:
            if eventid is not None:
                _, _, _, _, tensor_params = self.getOnlineTensor(eventid)
                if tensor_params is not None:
                    tensor_type = tensor_params["type"]
                    tensor_source = tensor_params["source"]

            if tensor_params is None:
                dbfile = data_folder / config["DATA"]["dbfile"]
                minboxcomp = float(config["CONSTANTS"]["minradial_distcomp"])
                maxboxcomp = float(config["CONSTANTS"]["maxradial_distcomp"])
                dboxcomp = float(config["CONSTANTS"]["step_distcomp"])

                # Minimum number of events required to get composite mechanism
                nmin = int(config["CONSTANTS"]["minno_comp"])
                tensor_params, similarity, nevents = getCompositeCMT(
                    lat,
                    lon,
                    dbfile,
                    box=minboxcomp,
                    maxbox=maxboxcomp,
                    dbox=dboxcomp,
                    nmin=nmin,
                )
                if tensor_params is not None:
                    tensor_type = "composite"
                    tensor_source = "composite"
        else:
            if "type" in tensor_params:
                tensor_type = tensor_params["type"]
            if "source" in tensor_params:
                tensor_source = tensor_params["source"]

        slab_collection = SlabCollection(slab_data_folder)
        slab_params = slab_collection.getSlabInfo(lat, lon, depth)

        results = self._regionalizer.getRegions(lat, lon)
        results["TensorType"] = tensor_type
        results["TensorSource"] = tensor_source
        results["CompositeVariability"] = similarity
        results["NComposite"] = nevents
        results["FocalMechanism"] = get_focal_mechanism(tensor_params)
        if len(slab_params):
            if np.isnan(slab_params["depth"]):
                results["SlabModelRegion"] = SLAB_REGIONS[slab_params["region"]]
                results["KaganAngle"] = np.nan
                results["SlabModelDepth"] = np.nan
                results["SlabModelDepthUncertainty"] = np.nan
                results["SlabModelDip"] = np.nan
                results["SlabModelStrike"] = np.nan
                results["SlabModelMaximumDepth"] = np.nan
            else:
                results["SlabModelRegion"] = SLAB_REGIONS[slab_params["region"]]
                results["SlabModelDepth"] = slab_params["depth"]
                results["SlabModelDepthUncertainty"] = slab_params["depth_uncertainty"]
                results["SlabModelDip"] = slab_params["dip"]
                results["SlabModelStrike"] = slab_params["strike"]
                results["SlabModelMaximumDepth"] = slab_params[
                    "maximum_interface_depth"
                ]
                if tensor_params is not None:
                    np1 = tensor_params["NP1"]
                    kagan = get_kagan_angle(
                        slab_params["strike"],
                        slab_params["dip"],
                        SLAB_RAKE,
                        np1["strike"],
                        np1["dip"],
                        np1["rake"],
                    )
                    results["KaganAngle"] = kagan
                else:
                    results["KaganAngle"] = np.nan
        else:
            results["SlabModelRegion"] = ""
            results["SlabModelDepth"] = np.nan
            results["SlabModelDepthUncertainty"] = np.nan
            results["SlabModelDip"] = np.nan
            results["SlabModelStrike"] = np.nan
            results["SlabModelMaximumDepth"] = np.nan
            results["KaganAngle"] = np.nan

        # Add in probability calculations for stable, active, volcanic, and
        # subduction
        # first, look for custom select.conf in data directory
        default_conf = pathlib.Path(__file__).parent / "data" / "select.conf"
        select_conf = pathlib.Path(config["DATA"]["folder"]) / "select.conf"
        if not select_conf.exists():
            select_conf = default_conf
        select_config, result = get_select_config(select_conf)
        probs = get_probs(magnitude, depth, results, select_config)

        for key, prob_value in probs.items():
            for shortkey, longkey in PROB_TRANSLATOR.items():
                if key.startswith(shortkey):
                    if "_" in key:
                        remainder = key.replace(f"{shortkey}_", "")
                        newkey = f"{longkey}{remainder.capitalize()}"
                        results[newkey] = prob_value
                    else:
                        results[longkey] = prob_value
                    break

        # TODO: Some of the probability keys may not be predictable. shove them to the end?
        predictable_index = [
            "TectonicRegion",
            "FocalMechanism",
            "TensorType",
            "TensorSource",
            "KaganAngle",
            "CompositeVariability",
            "NComposite",
            "DistanceToStable",
            "DistanceToActive",
            "DistanceToSubduction",
            "DistanceToVolcanic",
            "Oceanic",
            "DistanceToOceanic",
            "DistanceToContinental",
            "SlabModelRegion",
            "SlabModelDepth",
            "SlabModelDepthUncertainty",
            "SlabModelDip",
            "SlabModelStrike",
            "SlabModelMaximumDepth",
            "ProbabilityActive",
            "ProbabilityStable",
            "ProbabilitySubduction",
            "ProbabilityVolcanic",
            "ProbabilitySubductionCrustal",
            "ProbabilitySubductionInterface",
            "ProbabilitySubductionIntraslab",
        ]
        remainder_index = set(results.index) - set(predictable_index)
        index = predictable_index + list(remainder_index)
        results = results.reindex(index=index)

        return results


def get_focal_mechanism(tensor_params):
    """Return focal mechanism (strike-slip,normal, or reverse).

    Args:
        tensor_params (dict): Dictionary containing the following fields:
            - 'T' Dictionary of 'azimuth' and 'plunge' values for the T axis.
            - 'N' Dictionary of 'azimuth' and 'plunge' values for the N(B) axis.
            - 'P' Dictionary of 'azimuth' and 'plunge' values for the P axis.
            - 'NP1' Dictionary of angles for the first nodal plane ('strike','dip',
            'rake')
            - 'NP2' Dictionary of angles for the second nodal plane ('strike','dip',
            'rake')
        config (dict): dictionary containing:
            - constants:
            - tplunge_rs
            - bplunge_ds
            - bplunge_ss
            - pplunge_nm
            - delplunge_ss
    Returns:
        str: Focal mechanism string 'SS','RS','NM',or 'ALL'.
    """
    if tensor_params is None or "T" not in tensor_params:
        return "ALL"
    # implement eq 1 here
    Tp = tensor_params["T"]["plunge"]
    Np = tensor_params["N"]["plunge"]
    Pp = tensor_params["P"]["plunge"]
    tplunge_rs = CONSTANTS["tplunge_rs"]
    bplunge_ds = CONSTANTS["bplunge_ds"]
    bplunge_ss = CONSTANTS["bplunge_ss"]
    pplunge_nm = CONSTANTS["pplunge_nm"]
    delplunge_ss = CONSTANTS["delplunge_ss"]
    if Tp >= tplunge_rs and Np <= bplunge_ds:
        return "RS"
    if Np >= bplunge_ss and (Tp >= Pp - delplunge_ss and Tp <= Pp + delplunge_ss):
        return "SS"
    if Pp >= pplunge_nm and Np <= bplunge_ds:
        return "NM"
    return "ALL"
    return "ALL"
