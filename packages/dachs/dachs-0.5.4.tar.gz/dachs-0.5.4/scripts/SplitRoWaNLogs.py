import argparse
import os

# revamped log writer
from pathlib import Path

import pandas as pd


def configureParser() -> argparse.ArgumentParser:
    def validate_file(arg):
        if (file := Path(arg).absolute()).is_file():
            return file
        else:
            raise FileNotFoundError(arg)

    # process input arguments
    parser = argparse.ArgumentParser(
        prog=__package__,
        description="""
            Converts the raw RoWaN logs to split files, one file per sample.
            """,
    )
    # defaultPath = Path(__file__).resolve().parent.parent.parent / "tests" / "testData"
    # TODO: add info about output files to be created ...
    parser.add_argument(
        "-f",
        "--filename",
        type=validate_file,
        default=Path(os.getcwd()) / "AutoMOFs_6_2_20230224.log",
        help="Path to the filename containing the main AutoMOF logbook",
        # nargs="+",
        required=True,
    )
    return parser


if __name__ == "__main__":
    args = configureParser().parse_args()
    df_automofs = pd.read_csv(
        args.filename,
        skipinitialspace=True,
        skip_blank_lines=True,
        engine="python",
        sep=";",
        header=None,
        names=["Time", "Info", "ExperimentID", "SampleNumber", "Readout", "Value", "Unit", "Using"],
    )
    # for every AutoMOF experiment
    for expID in df_automofs["ExperimentID"].unique():
        # only need this to get unique samples:
        dsub = df_automofs.loc[df_automofs["ExperimentID"] == expID]
        uniqueSamples = dsub["SampleNumber"].unique()
        # some output to show we're doing something
        print(f"working on {expID=}, number of sampleNumbers: {len(uniqueSamples)}")
        for sampleID in uniqueSamples:  # for every unique sample
            # get a subset for only this automofs and samplenumbers
            df1 = df_automofs.loc[
                (df_automofs["SampleNumber"] == sampleID) & (df_automofs["ExperimentID"] == expID)
            ]
            # define an output filename and make it into a Path so we can do some checks and operations
            output_file_name = Path(args.filename.parent, f"log_{str(expID)}_{str(sampleID)}.xlsx")
            # get rid of the file if it already exists:
            if output_file_name.is_file():
                output_file_name.unlink()
            # output information to file:
            df1.to_excel(output_file_name, index=False)
