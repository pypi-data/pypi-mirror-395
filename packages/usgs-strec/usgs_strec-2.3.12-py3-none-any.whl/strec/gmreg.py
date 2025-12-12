#!/usr/bin/env python

# stdlib imports
import pathlib
from collections import OrderedDict

# third party
import pandas as pd

# local imports
from strec.distance import calc_distances
from strec.utils import get_config


class Regionalizer(object):
    def __init__(self, datafolder):
        """Determine tectonic region information given epicenter and depth.

        Args:
            datafolder (str): Path to directory containing spatial data
            for tectonic regions.
        """
        self._datafolder = pathlib.Path(datafolder)
        config = get_config()
        grid_data_folder = pathlib.Path(config["DATA"]["folder"])
        self._tectonic_grid = grid_data_folder / "tectonic_global.tif"
        self._oceanic_grid = grid_data_folder / "oceanic_global.tif"

    @classmethod
    def load(cls):
        """Load regionalizer data from data in the repository.

        Returns:
            Regionalizer: Instance of Regionalizer class.
        """
        config = get_config()
        datadir = config["DATA"]["folder"]
        return cls(datadir)

    def getRegions(self, lat, lon):
        """Get information about the tectonic region of a given hypocenter.

        Args:
            lat (float): Earthquake hypocentral latitude.
            lon (float): Earthquake hypocentral longitude.
            depth (float): Earthquake hypocentral depth.
        Returns:
            Series: Pandas series object containing labels:
                - TectonicRegion: Subduction, Active, Stable, or Volcanic.
                - DistanceToStable: Distance in km to nearest stable region.
                - DistanceToActive: Distance in km to nearest active region.
                - DistanceToSubduction: Distance in km to nearest subduction
                                        region.
                - DistanceToVolcanic: Distance in km to nearest volcanic
                                      region.
                - Oceanic: Boolean indicating if epicenter is in the ocean.
                - DistanceToOceanic: Distance in km to nearest oceanic region.
                - DistanceToContinental: Distance in km to nearest continental
                                         region.
                - DistanceToBackarc: Distance in km to nearest backarc
                                         region.
        """
        regions = OrderedDict()

        region_dict = calc_distances(lat, lon)

        if region_dict["DistanceToActive"] == 0:
            region_dict["TectonicRegion"] = "Active"
        elif region_dict["DistanceToStable"] == 0:
            region_dict["TectonicRegion"] = "Stable"
        elif region_dict["DistanceToSubduction"] == 0:
            region_dict["TectonicRegion"] = "Subduction"
        else:
            region_dict["TectonicRegion"] = "Volcanic"

        region_dict["Oceanic"] = False
        if region_dict["DistanceToOceanic"] == 0:
            region_dict["Oceanic"] = True

        regions = pd.Series(
            region_dict,
            index=[
                "TectonicRegion",
                "DistanceToStable",
                "DistanceToActive",
                "DistanceToSubduction",
                "DistanceToVolcanic",
                "Oceanic",
                "DistanceToOceanic",
                "DistanceToContinental",
                "DistanceToBackarc",
            ],
        )

        return regions
