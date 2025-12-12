#!/usr/bin/env python

# stdlib imports
import argparse
import inspect
import logging
import pathlib
import sys
from enum import Enum
from io import StringIO
from typing import Iterable, Union

# local imports
from strec.database import fetch_dataframe, read_datafile, stash_dataframe
from strec.gcmt import fetch_gcmt
from strec.slab import get_slab_grids
from strec.utils import create_config, get_config, get_config_file_name

HELPSTR = """
Initialize the system with the Slab 2.0 grids and GCMT moment tensor database.

# Usage

`strec_cfg update --datafolder <path/to/data/folder> --slab --gcmt</code>`

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


"""


# I hoped making an enum of string = loglevel would be clear, but typer prints the integer values
# of the log levels instead of CRITICAL, ERROR, etc. Making an enum and then a dict to make this
# clearer.
class LoggingLevel(str, Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


LOGDICT = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}


def config_exists():
    config_file = get_config_file_name()
    return config_file.exists()


def get_datafolder():
    try:
        config = get_config()
        datafolder = config["DATA"]["folder"]
        return datafolder
    except Exception:
        return None


def main():
    config_file = get_config_file_name()
    if config_file.exists():
        config = get_config()
        datafolder = config["DATA"]["folder"]
    else:
        datafolder = config_file.parent / "data"
    parser = argparse.ArgumentParser(
        description="Get information about an earthquake's tectonic regime."
    )
    subparsers = parser.add_subparsers(help="Two sub-commands are available:")

    parser_info = subparsers.add_parser(
        "info", help="Print out information regarding current configuration"
    )
    parser_info.set_defaults(func=info)

    parser_update = subparsers.add_parser(
        "update", help="Create/update STREC configuration."
    )

    parser_update.add_argument(
        "-d",
        "--datafolder",
        default=datafolder,
        help="Data folder where slab and GCMT data will be downloaded",
    )
    parser_update.add_argument(
        "-s", "--slab", default=False, action="store_true", help="Download slab data"
    )
    parser_update.add_argument(
        "-g", "--gcmt", default=False, action="store_true", help="Download GCMT data"
    )
    parser_update.add_argument(
        "-l",
        "--log",
        help="Set log level",
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
        default="INFO",
    )
    parser_update.set_defaults(func=update)

    moment_group = parser_update.add_argument_group(
        title="Moment data options",
        description="Supply neither OR both of these options",
    )
    moment_group.add_argument(
        "-m", "--moment-data", help="Supply moment data as CSV/Excel"
    )
    moment_group.add_argument(
        "-a",
        "--moment-data-source",
        help="Supply moment data source (US, CI, etc.)",
        default="unknown",
    )

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


def info(args):
    if not config_exists():
        print("No config file exists at. Run the update command.")
        sys.exit(1)
    config_file = get_config_file_name()
    print(f"Config file {config_file}:")
    print("------------------------")
    config = get_config()
    config_str = StringIO()
    config.write(config_str)
    config_str.seek(0)
    print(config_str.getvalue().rstrip())
    print("------------------------\n")
    dbfile = config["DATA"]["dbfile"]
    dataframe = fetch_dataframe(dbfile)
    nsources = len(dataframe["source"].unique())
    print(
        (
            f"Moment Tensor Database ({dbfile}) contains {len(dataframe)} "
            f"events from {nsources} sources.\n"
        )
    )
    slabfolder = config["DATA"]["slabfolder"]
    slab_files = list(pathlib.Path(slabfolder).glob("*.grd"))
    names = [slab_file.name for slab_file in slab_files]
    slabs = set([name.split("_")[0] for name in names])
    print(
        (
            f"There are {len(slab_files)} slab grids from {len(slabs)} "
            f"unique slab models located in {slabfolder}."
        )
    )
    sys.exit(0)


def update(args):
    if args.log:
        logging.basicConfig(level=LOGDICT[args.log])

    if args.gcmt and (
        args.moment_data is not None or args.moment_data_source != "unknown"
    ):
        print(
            (
                "You may either choose to download GCMT "
                "moment tensors or install your own source, not both."
            )
        )
        sys.exit(1)
    datafolder = pathlib.Path(args.datafolder)
    if not config_exists():
        config = create_config(datafolder)
    else:
        config = get_config()
        if str(datafolder) != config["DATA"]["folder"]:
            print("datafolder is already configured. Exiting.")
            sys.exit(1)

    messages = []
    if args.slab:
        slabfolder = pathlib.Path(config["DATA"]["slabfolder"])
        if not slabfolder.exists():
            slabfolder.mkdir(parents=True)
        slab_result, slab_msg = get_slab_grids(slabfolder)
        if not slab_result:
            messages.append(slab_msg)
    if args.gcmt:
        try:
            gcmt_dataframe = fetch_gcmt()
            dbfile = config["DATA"]["dbfile"]
            source = "GCMT"
            stash_dataframe(gcmt_dataframe, dbfile, source, create_db=True)
        except Exception as e:
            gcmt_msg = f"Failed to download GCMT data: {str(e)}"
            messages.append(gcmt_msg)

    if args.moment_data:
        dbfile = pathlib.Path(config["DATA"]["dbfile"])
        create_db = True
        if dbfile.exists():
            create_db = False
        try:
            moment_dataframe = read_datafile(args.moment_data)
            stash_dataframe(
                moment_dataframe, dbfile, args.moment_data_source, create_db=create_db
            )
        except Exception as e:
            moment_msg = f"Could not parse moment datafile {args.moment_data}: {str(e)}"
            messages.append(moment_msg)
    if len(messages):
        print("Errors were encountered during the course of downloading/loading data:")
        for message in messages:
            print(f"'{message}'")
    sys.exit(0)


if __name__ == "__main__":
    main()
