#!/usr/bin/env python
# coding: utf-8

import argparse
import logging
from os import environ
from pathlib import Path
from typing import List

from mcsas3.mc_hdf import storeKVPairs

import dachs.serialization
import dachs.structure


def outfileFromInput(infn, suffix="h5"):
    return Path(infn).resolve().with_suffix(f".{suffix}")


# perhaps, use environment vars for defaults later:
# https://stackoverflow.com/a/63828227
def configureParser() -> argparse.ArgumentParser:
    def validate_file(arg):
        if arg == '':
            return None  # nothing specified.
        filepath = Path(arg).absolute()
        if not filepath.is_file():
            raise ValueError
        return filepath

    # process input arguments
    parser = argparse.ArgumentParser(
        prog=__package__,
        description="""
            Creates an archival HDF5 structure containing synthesis details from a RoWaN AutoMOF synthesis.

            Released under a GPLv3+ license.
            """,
    )
    # TODO: add info about output files to be created ...
    parser.add_argument(
        "-l",
        "--logbook",
        type=validate_file,
        default=environ.get("DACHS_LOGBOOK", ""),
        help=(
            "Path to the filename containing the main AutoMOF logbook, "
            "read from environment variable DACHS_LOGBOOK if not specified on command line."
        ),
    )
    parser.add_argument(  # could perhaps be done with a multi-file input for multiple solutions...
        "-s0",
        "--s0file",
        type=validate_file,
        default=environ.get("DACHS_SOL0", ""),
        help=(
            "File containing the synthesis log of Solution 0, "
            "read from environment variable DACHS_SOL0 if not specified on command line."
        ),
    )
    parser.add_argument(
        "-s1",
        "--s1file",
        type=validate_file,
        default=environ.get("DACHS_SOL1", ""),
        help=(
            "File containing the synthesis log of Solution 1, "
            "read from environment variable DACHS_SOL1 if not specified on command line."
        ),
    )
    parser.add_argument(
        "-s2",
        "--s2file",
        type=validate_file,
        default=environ.get("DACHS_SOL2", ""),
        help=(
            "File containing the synthesis log of Solution 2, "
            "read from environment variable DACHS_SOL2 if not specified on command line."
        ),
    )
    parser.add_argument(
        "-s",
        "--synlog",
        type=validate_file,
        default=environ.get("DACHS_SYNLOG", ""),
        help=(
            "File containing the synthesis log of the MOF itself, "
            "read from environment variable DACHS_SYNLOG if not specified on command line."
        ),
    )
    parser.add_argument(
        "-o",
        "--outfile",
        help=(
            "Output file containing structured HDF5 data. "
            "If omitted, it is written to the same directory "
            "and with the same basename as *synlog* above, but with .h5 suffix."
        ),
    )
    parser.add_argument(
        "-a",
        "--amset",
        type=str,
        default=environ.get("DACHS_AMSET", ""),
        help=(
            "Equipment set AMSET identifier, "
            "read from environment variable DACHS_AMSET if not specified on command line."
        ),
    )
    return parser


def main(args: List[str] = None):
    """:param args: replaces sys.argv with a custom argument list."""
    args = configureParser().parse_args(args)
    if not args.outfile:
        args.outfile = outfileFromInput(args.synlog)

    solFiles = [args.s0file, args.s1file]
    if args.s2file is not None:
        solFiles += [args.s2file]

    exp = dachs.structure.create(args.logbook, solFiles, args.synlog, args.amset)
    paths = dachs.serialization.dumpKV(exp, dbg=False)
    logging.info(f"Writing structure to '{args.outfile}'.")
    # from pprint import pprint
    # pprint(paths)
    storeKVPairs(args.outfile, "", paths.items())
    dachs.serialization.graphKV(paths)
