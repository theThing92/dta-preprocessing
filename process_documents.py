"""
Module to preprocess DTA corpus files via multiprocessing.
"""
import argparse
import logging
import multiprocessing as mp
import os
import sys
from enum import Enum

from preprocessing import run_meta_data_extraction
from annotationen import get_annotations
from extract_epoch import extract_epochs

__author__ = "Maurice Vogel"


# basic logging
logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


class PreprocessingFunctions(Enum):
    annotations = "annotations"  # get_annotations
    epochs = "epochs"  # extract_epochs
    meta = "meta"  # run_meta_data_extraction


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Multiprocess DTA data",
        description="Process DTA related files in a given input directory and save the resulting"
        " output format into a given output directory.",
    )
    parser.add_argument(
        "input_directory",
        type=str,
        help="Directory path to the DTA related input files.",
    )
    parser.add_argument("output_directory", type=str, help="Output directory path.")
    parser.add_argument(
        "-n",
        "--num_processes",
        default=None,
        required=False,
        type=int,
        help="Number of processes to spawn for preprocessing functions."
        " Uses all available logical cpus per default, as returned from os.cpu_count().",
    )
    parser.add_argument(
        "function",
        type=str,
        help=f"Preprocessing functions to call, can be one of:"
        f" {', '.join([x.value for x in PreprocessingFunctions])}",
        default=PreprocessingFunctions.meta.value,
    )
    args = parser.parse_args()

    with mp.Pool(processes=args.num_processes) as pool:
        log_msg_start = "Start multiprocessing for DTA files in {} with {} processes and function '{}'."
        if args.num_processes:
            logging.info(log_msg_start.format(args.input_directory, args.num_processes, args.function))
        else:
            logging.info(log_msg_start.format(args.input_directory, os.cpu_count(), args.function))
        files = os.listdir(args.input_directory)
        file_paths = [
            os.path.abspath(os.path.join(args.input_directory, file_name))
            for file_name in files
        ]

        if args.function == PreprocessingFunctions.meta.value:
            pool.starmap(
                run_meta_data_extraction,
                zip(file_paths, [args.output_directory for i in range(len(files))]),
            )

        elif args.function == PreprocessingFunctions.annotations.value:
            pool.starmap(
                get_annotations,
                zip(
                    file_paths,
                    [
                        os.path.join(
                            args.output_directory, file.replace(".xml", ".csv")
                        )
                        for file in files
                    ],
                ),
            )

        elif args.function == PreprocessingFunctions.epochs.value:
            extract_epochs(args.input_directory+"*.pkl", os.path.join(args.output_directory, "epochs.txt"))
        else:
            raise ValueError(
                f"No valid function alias has been given, must be one of: {', '.join([x.value for x in PreprocessingFunctions])}"
            )

        logging.info(
            f"Preprocessing is finished. Files have been saved to {args.output_directory}."
        )
