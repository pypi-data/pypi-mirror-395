#!/usr/bin/env python

# stdlib imports
import argparse
import sys

# local imports
from strec.calc import select_regions
from strec.utils import render_row


class CustomFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    pass


def main():
    desc = """Determine various seismo-tectonic parameters for given input coordinates.

    The output will consist of the following data fields:

     - TectonicRegion : (Active, Stable, Volcanic, Subduction)
     - FocalMechanism : (RS [Reverse],SS [Strike-Slip], NM [Normal], ALL)
     - TensorType : composite
     - TensorSource : (composite, one of many moment tensor sources like GCMT)
     - KaganAngle : Angle between fault plane and slab orientation.
     - CompositeVariability :  A measure of the uncertainty in the composite
                               moment tensor.
     - NComposite : Number of events used to create composite moment tensor.
     - DistanceToStable : Distance in km from the nearest stable polygon.
     - DistanceToActive : Distance in km from the nearest active polygon.
     - DistanceToSubduction : Distance in km from the nearest subduction
                              polygon.
     - DistanceToVolcanic : Distance in km from the nearest volcanic polygon.
     - Oceanic : Boolean indicating whether we are in an oceanic region,
                 false indicates Continental.
     - DistanceToOceanic : Distance in km to nearest oceanic polygon.
     - DistanceToContinental : Distance in km to nearest continental polygon.
     - SlabModelRegion : Subduction region.
     - SlabModelDepth : Depth of slab2.0 grid at earthquake location.
     - SlabModelDepthUncertainty : Uncertainty of depth to slab.
     - SlabModelDip : Dip of slab at earthquake location.
     - SlabModelStrike : Strike of slab at earthquake location.
     - SlabModelMaximumDepth : Maximum depth of seismogenic zone.
     - ProbabilityActive: Probability that event occurred in an active region.
     - ProbabilityStable: Probability that event occurred in an stable region.
     - ProbabilityVolcanic: Probability that event occurred in a volcanic region.
     - ProbabilitySubduction: Probability that event occurred in a subduction region.
     - ProbabilityCrustal: Probability that event occurred in a subduction
                           crustal depth zone.
     - ProbabilityInterface: Probability that event occurred in a subduction
                             interface depth zone.
     - ProbabilityIntraslab: Probability that event occurred in a subduction
                             intraslab depth zone.
     - ProbabilityActiveShallow: When specified, the probability that event occurred
                                 in a configurable shallow zone in an active tectonic
                                 region.
     - ProbabilityActiveDeep: When specified, the probability that event occurred
                              in a configurable deep zone in an active tectonic
                              region.
     - ProbabilityStableShallow: When specified, the probability that event occurred
                                 in a configurable shallow zone in a stable tectonic
                                 region.
     - ProbabilityVolcanicShallow: When specified, the probability that event occurred
                                   in a configurable shallow zone in a volcanic tectonic
                                   region.

    where:
        - Active regions are boundaries between two plates that are colliding,
          sliding past each other, or pulling apart.
        - Stable regions are regions where those things are not happening.
        - Subduction regions are those that are above the Slab2.0 grids.
        - Volcanic regions are those that sit above mantle plumes
        - ALL FocalMechanisms that are some combination of the other types
        -


    Input files can be CSV or Excel format (regcalc will
    attempt to determine format automatically) and MUST include columns
    beginning with (case insensitive):

        Lat - Numeric latitude of input earthquake.
        Lon - Numeric longitude of input earthquake.
        Depth - Numeric depth of earthquake (km).

    Input files may optionally contain a column (also case insensitive) called:
    ComCatID - Valid ANSS ComCat ID
    Any other columns present in the input will be copied to the output.

    The output format must be one of the following:

        pretty - A human readable pretty-printed representation of the output.
        json - A JSON representation of the output
        csv - A CSV output, one earthquake per line.
        excel - Microsoft Excel format, one earthquake per line.

    Note that the -c/--columns option will override these defaults.
    """
    parser = argparse.ArgumentParser(
        description=desc,
        formatter_class=CustomFormatter,
    )
    parser.add_argument(
        "-e",
        "--eqinfo",
        nargs=4,
        metavar=("LAT", "LON", "DEPTH", "MAG"),
        type=float,
        help="Determine region based on lat, lon, depth, magnitude of earthquake",
    )
    parser.add_argument(
        "-d",
        "--event-id",
        help="Determine region based on ComCat event id (i.e., us6000iasi).",
    )
    parser.add_argument(
        "-i",
        "--input-file",
        help="Determine region for events specified in input file.",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["pretty", "csv", "excel", "json"],
        default="pretty",
        help="Specify output format for results.",
    )
    parser.add_argument(
        "-c",
        "--hypo-columns",
        help=(
            "When used with -i/--input-file, specify the columns "
            "that should be used for Latitude, Longitude, Depth and Magnitude."
        ),
        nargs=4,
    )
    parser.add_argument(
        "--id-column",
        help=(
            "When used with -i/--input-file, specify the column "
            "that should be used for ComCatID."
        ),
    )
    parser.add_argument(
        "-o",
        "--output-file",
        help="Specify output filename for results (see --format).",
    )
    parser.add_argument(
        "-n", "--moment-info", help="Specify strike, dip, rake for single earthquake."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Print out more verbose output.",
        default=False,
        action="store_true",
    )

    args = parser.parse_args()
    regcalc(args)


def regcalc(args):
    # error out on any invalid combinations of options
    if args.format in ["pretty", "json"] and args.output_file is not None:
        print(f"Output file is invalid when specified with format of {args.format}")
        sys.exit(1)

    if args.format in ["excel"] and args.output_file is None:
        print("Output format 'excel' is invalid unless an output file is specified")
        sys.exit(1)

    has_eq = int(args.eqinfo is not None)
    has_id = int(args.event_id is not None)
    has_file = int(args.input_file is not None)
    if sum([has_eq, has_id, has_file]) > 1:
        print(
            "Options --eqinfo, --event-id, --input-file are "
            "mutually exclusive. Please choose one."
        )
        sys.exit(1)

    if (
        args.hypo_columns is not None or args.id_column is not None
    ) and args.input_file is None:
        print(
            "Options --hypo-columns and --id-column only work "
            "when input_file is specified."
        )
        sys.exit(1)

    if args.moment_info is not None and args.input_file is not None:
        print("You can only specify moment information for a single earthquake.")
        sys.exit(1)

    regions_frame = select_regions(
        args.input_file,
        args.eqinfo,
        args.moment_info,
        args.event_id,
        args.hypo_columns,
        args.id_column,
        args.verbose,
    )
    if args.output_file is None:
        for idx, row in regions_frame.iterrows():
            render_row(row, args.format, args.hypo_columns)

    if args.output_file:
        if args.format == "csv":
            regions_frame.to_csv(args.output_file, index=False)
        else:
            regions_frame.to_excel(args.output_file, index=False)


if __name__ == "__main__":
    main()
