# Table of Contents
- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Installation](#installation)
- [Upgrade](#upgrade)
- [Configuration](#configuration)
- [Usage](#usage)
- [Probabilities] (#probabilities)
- [Glossary](#glossary)

# Introduction

This library and set of tools was created to provide functionality to
automatically determine the tectonic region of an earthquake
(Subduction, Active, Volcanic, Stable), and the distance to the tectonic
regions to which it does *not* belong.

In addition, SeismoTectonic Regime Earthquake Calculator (STREC) provides a tool that, 
in subduction zones, returns information about the subduction zone, using the 
USGS Slab2 models.

(https://www.sciencebase.gov/catalog/item/5aa1b00ee4b0b1c392e86467/).


This code was based on the [paper](https://doi.org/10.1785/0120110124):

```
A Global Earthquake Discrimination Scheme to Optimize Ground‐Motion Prediction Equation Selection
D. García; D. J. Wald; M. G. Hearne
Bulletin of the Seismological Society of America (2012) 102 (1): 185–203.
```


# Installation

`pip install usgs-strec`

# Upgrade

`pip install --upgrade usgs-strec`

# Configuration

In order to use STREC you will need to:

 - download USGS Slab 2.0 models, described at the Science Base 
   link above. 
 - create a database of moment tensors, either manually from a 
   spreadsheet/CSV file (described below), or by downloading 
   a default database of moment tensors from the 
   [Global Centroid Moment Tensor (GCMT) catalog](https://www.globalcmt.org/)
 - Create a configuration file describing the locations of these files.

To make this easier, a configuration progran called `strec_cfg` is provided which automates 
all of these processes. This program comes with two *sub-commands* called `info` and `update`. 
To initialize the system with the Slab 2.0 grids and GCMT moment tensor database:

`strec_cfg update --datafolder <path/to/data/folder> --slab --gcmt`

For example, if you set the STREC data folder to be */data/strec*:

`strec_cfg update --datafolder /data/strec --slab --gcmt`

and then use the following command to see the resulting configuration:

`strec_cfg info`

The output should look something like the following:

```
Config file /home/user/.strec/config.ini:
------------------------
[DATA]
folder = /data/strec
slabfolder = /data/strec/slabs
dbfile = /data/strec/moment_tensors.db

[CONSTANTS]
minradial_disthist = 0.01
maxradial_disthist = 1.0
minradial_distcomp = 0.5
maxradial_distcomp = 1.0
step_distcomp = 0.1
depth_rangecomp = 10
minno_comp = 3
default_szdip = 17
dstrike_interf = 30
ddip_interf = 30
dlambda = 60
ddepth_interf = 20
ddepth_intra = 10
------------------------

Moment Tensor Database (/data/strec/moment_tensors.db) contains 60535 events from 1 sources.

There are 135 slab grids from 27 unique slab models located in /data/strec/slabs.
```

# Usage

`regcalc` is the program used to calculate region parameters.

The details of the options are visible by running `regcalc --help`.

The three most basic use cases are:

 - Getting information about an event by ComCat ID: `regcalc -d us6000id0t`
 - Getting information about a (possibly theoretical) event by providing hypocenter information: `regcalc -e -5.0735 103.0826 50.5`
 - Getting information about more than one event, with input like below as Excel or CSV:

<table>
<tr> 
  <th>Latitude</th>
  <th>Longitude</th>
  <th>Depth</th>
</tr>
<tr>
  <td>-5.074</td>
  <td>103.083</td>
  <td>50.5</td>
</tr>
<tr>
  <td>-1.008</td>
  <td>98.642</td>
  <td>17.6</td>
</tr>
</table>

`regcalc -i input_file.xlsx`

You can add a ComCat ID column to this - the name which will be automatically detected is *EventID* (case does not matter). If the file has another name for the same column you can supply that with the --id-column command line option:

`regcalc -i input_file.xlsx --id-column id`

If the file contains column names for latitude, longitude and depth that do not match the regular expression patterns "^lat", "^lon", "^dep" (ignoring case) then you can supply those column names as well using the --hypo-columns command line option:

`regcalc -i input_file.xlsx --hypo-columns EventLatitude EventLongitude EventDepth`

If an input spreadsheet has moment tensor columns named Mrr, Mtt, Mpp, etc. (case does not matter) then those values will be used to calculate the Kagan angle and determine the focal mechanism.

You can also optionally specify moment tensor information for a single event in the form of strike/dip/rake angles and a magnitude, using the --moment-info command line option:

`regcalc -e -0.950 -21.725 10.0 -m 260 84 169 6.9`

*Note: Users may notice that distances to tectonic regions the earthquake is NOT in may be unreasonably large values. The reason 
for returning the distances to other regions is to help inform the user when the earthquake is close to another region.
When STREC outputs these large numbers it indicates that the distance to that other region is not close enough to affect
the properties of the earthquake.*

# Probabilities

STREC now calculates the probabilities of an earthquake being in any of the tectonic regions, and also in
any of the various defined depth categories. For subduction regions these are hardcoded as 
crustal, interface, and intraslab. For other regions, the *default* configuration includes the following:

 - acr_shallow : active earthquakes occurring above 30 km
 - acr_deep - active earthquakes occurring below 30 km
 - scr_shallow - stable earthquakes at any depth
 - volcanic_shallow - volcanic earthquakes at any depth

## Probability configuration

Users can configure the probability settings to include more finely grained depth zones for active, 
stable, and volcanic regions. The default config file is located in the [repository] 
(https://code.usgs.gov/ghsc/esi/strec/-/blob/main/src/strec/data/select.conf) and 
installed with the software. To customize the probability depth zones, download a copy of the file from 
the repository and save it in the [DATA]->folder in the config.ini file described above.

```
[DATA]
folder = /data/strec
```

The relevant section of the select.conf file to modify looks like the following:

```
[tectonic_regions]
    [[acr]]
        horizontal_buffer = 100
        vertical_buffer = 5
        depth_labels = shallow, deep
        min_depth = -Inf, 30
        max_depth = 30, Inf
    [[scr]]
        horizontal_buffer = 100
        vertical_buffer = 5
        depth_labels = shallow
        min_depth = -Inf
        max_depth = Inf
    [[subduction]]
        horizontal_buffer = 100
        vertical_buffer = 5
        depth_labels = crustal, interface, intraslab
        min_depth = -Inf, 15, 70
        max_depth = 15, 70, Inf
        use_slab = True
    [[volcanic]]
        horizontal_buffer = 10
        vertical_buffer = 5
        depth_labels = shallow
        min_depth = -Inf
        max_depth = Inf
```

To add a "deep" (10 km or deeper) category to the scr section, you would modify that 
section to look like the following:

```
    [[scr]]
        horizontal_buffer = 100
        vertical_buffer = 5
        depth_labels = shallow, deep
        min_depth = -Inf, 10
        max_depth = 10, Inf
```


# Glossary

STREC defines a number of terms that may not be commonly
understood, so they are explained here.  These terms may be different
from the Garcia paper upon which this software is originally based.

 - *Tectonic Region*: One of Subduction, Active, Volcanic, or Stable.
   We have split up the globe into these four regions, such that any
   point on the globe should fall into one and only one of these
   regions.
   
     * *Subduction*: A tectonic region defined by one plate descending below
     another (e.g., the western portion of the United States), more specifically
     by those locations above the Slab2.0 grids.

     * *Active*: A tectonic region which experiences crustal deformation due
     to plate tectonics.

     * *Volcanic*: A tectonic region which is sitting above mantle plumes, 
                  where magma pushes through cracks in the crust.

     * *Stable*: Tectonic regions which unlike Active regions, do not
     experience crustal deformation (e.g., the interior of the
     Australian continent.)

![Map showing tectonic regions](select_regions.png "Map Showing Tectonic Regions")
*Fig 1 - Map showing tectonic regions. ACR=Active Crustal Region, SUB=Subduction Zone, VOL=Volcanic Region, SCR=Stable Continental Region* 

 - *Oceanic*: Another region, not exclusive with the four Tectonic
   Regions, that indicates whether the point supplied is in the ocean
   (i.e., not continental).

 - *Continental*: The opposite of Oceanic.

 - *Backarc*: The area of a subduction region that is behind the volcanic arc.

 - *Focal Mechanism*: A set of parameters that define the deformation in
   the source region that generates the seismic waves of an earthquake.

 - *Tensor Type*: The short name for the algorithm used to generate
   the moment tensor used to determine focal mechanism, Kagan angle,
   etc.  This is usually a short code like *Mww* (W-phase), *Mwr*
   (regional), *Mwb* (body wave), or *composite*, which indicates that
   there is no computed moment tensor, so a composite of historical
   moment tensors around the input coordinates is used instead.

 - *Tensor Source*: When available, this is usually the network that
   contributed the moment tensor, followed by the ID used by that
   network (e.g., us_2000bmcg).

 - *Kagan Angle*: An single angle between any two moment tensors or in
    our case, between a moment tensor and a subducting slab.

 - *Composite Moment Tensor*: When moment tensors are not available 
    for a given event, a composite moment tensor is calculated by 
    essentially taking the mean of at least three moment tensors in a 0.1 
    degree box surrounding the earthquake hypocenter.

 - *Composite Variability*: When the moment tensor solution is of type
 *composite*, a scalar value describing the variability of the moment
 tensors used to determine the composite.

 - *Distance to [Region]*: The great circle distance from the input
   coordinates to the nearest vertex of [Region] polygon.

 - *Slab Model Region*: We currently use Slab 2.0 subduction models
   (Hayes 2012), which are currently provided for 27 regions around
   the globe.  These regions are described in detail here:
   https://www.sciencebase.gov/catalog/item/5aa1b00ee4b0b1c392e86467/

 - *Slab Model Depth*: The best estimate of depth to subduction
   interface.

 - *Slab Model Depth Uncertainty*: The best estimate of the uncertainty
   of the depth to subduction interface.

 - *Slab Model Dip*: The best estimate of the dip angle of the
   subducting plate.

 - *Slab Model Strike*: The best estimate of the strike angle of the
   subducting plate.

